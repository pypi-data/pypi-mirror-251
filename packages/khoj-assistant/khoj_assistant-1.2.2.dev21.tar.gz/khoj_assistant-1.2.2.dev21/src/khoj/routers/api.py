import concurrent.futures
import json
import logging
import math
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Union
from urllib.parse import unquote

from asgiref.sync import sync_to_async
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.requests import Request
from fastapi.responses import Response, StreamingResponse
from starlette.authentication import requires

from khoj.configure import configure_server
from khoj.database import adapters
from khoj.database.adapters import (
    ConversationAdapters,
    EntryAdapters,
    get_user_search_model_or_default,
)
from khoj.database.models import ChatModelOptions
from khoj.database.models import Entry as DbEntry
from khoj.database.models import (
    GithubConfig,
    KhojUser,
    LocalMarkdownConfig,
    LocalOrgConfig,
    LocalPdfConfig,
    LocalPlaintextConfig,
    NotionConfig,
    SpeechToTextModelOptions,
)
from khoj.processor.conversation.offline.chat_model import extract_questions_offline
from khoj.processor.conversation.offline.whisper import transcribe_audio_offline
from khoj.processor.conversation.openai.gpt import extract_questions
from khoj.processor.conversation.openai.whisper import transcribe_audio
from khoj.processor.conversation.prompts import help_message, no_entries_found
from khoj.processor.conversation.utils import save_to_conversation_log
from khoj.processor.tools.online_search import search_with_google
from khoj.routers.helpers import (
    ApiUserRateLimiter,
    CommonQueryParams,
    ConversationCommandRateLimiter,
    agenerate_chat_response,
    get_conversation_command,
    is_ready_to_chat,
    text_to_image,
    update_telemetry_state,
    validate_conversation_config,
)
from khoj.search_filter.date_filter import DateFilter
from khoj.search_filter.file_filter import FileFilter
from khoj.search_filter.word_filter import WordFilter
from khoj.search_type import image_search, text_search
from khoj.utils import constants, state
from khoj.utils.config import GPT4AllProcessorModel, TextSearchModel
from khoj.utils.helpers import (
    AsyncIteratorWrapper,
    ConversationCommand,
    command_descriptions,
    get_device,
    is_none_or_empty,
    timer,
)
from khoj.utils.rawconfig import (
    FullConfig,
    GithubContentConfig,
    NotionContentConfig,
    SearchConfig,
    SearchResponse,
)
from khoj.utils.state import SearchType

# Initialize Router
api = APIRouter()
logger = logging.getLogger(__name__)
conversation_command_rate_limiter = ConversationCommandRateLimiter(trial_rate_limit=5, subscribed_rate_limit=100)


def map_config_to_object(content_source: str):
    if content_source == DbEntry.EntrySource.GITHUB:
        return GithubConfig
    if content_source == DbEntry.EntrySource.GITHUB:
        return NotionConfig
    if content_source == DbEntry.EntrySource.COMPUTER:
        return "Computer"


async def map_config_to_db(config: FullConfig, user: KhojUser):
    if config.content_type:
        if config.content_type.org:
            await LocalOrgConfig.objects.filter(user=user).adelete()
            await LocalOrgConfig.objects.acreate(
                input_files=config.content_type.org.input_files,
                input_filter=config.content_type.org.input_filter,
                index_heading_entries=config.content_type.org.index_heading_entries,
                user=user,
            )
        if config.content_type.markdown:
            await LocalMarkdownConfig.objects.filter(user=user).adelete()
            await LocalMarkdownConfig.objects.acreate(
                input_files=config.content_type.markdown.input_files,
                input_filter=config.content_type.markdown.input_filter,
                index_heading_entries=config.content_type.markdown.index_heading_entries,
                user=user,
            )
        if config.content_type.pdf:
            await LocalPdfConfig.objects.filter(user=user).adelete()
            await LocalPdfConfig.objects.acreate(
                input_files=config.content_type.pdf.input_files,
                input_filter=config.content_type.pdf.input_filter,
                index_heading_entries=config.content_type.pdf.index_heading_entries,
                user=user,
            )
        if config.content_type.plaintext:
            await LocalPlaintextConfig.objects.filter(user=user).adelete()
            await LocalPlaintextConfig.objects.acreate(
                input_files=config.content_type.plaintext.input_files,
                input_filter=config.content_type.plaintext.input_filter,
                index_heading_entries=config.content_type.plaintext.index_heading_entries,
                user=user,
            )
        if config.content_type.github:
            await adapters.set_user_github_config(
                user=user,
                pat_token=config.content_type.github.pat_token,
                repos=config.content_type.github.repos,
            )
        if config.content_type.notion:
            await adapters.set_notion_config(
                user=user,
                token=config.content_type.notion.token,
            )


def _initialize_config():
    if state.config is None:
        state.config = FullConfig()
        state.config.search_type = SearchConfig.model_validate(constants.default_config["search-type"])


@api.get("/config/data", response_model=FullConfig)
@requires(["authenticated"])
def get_config_data(request: Request):
    user = request.user.object
    EntryAdapters.get_unique_file_types(user)

    return state.config


@api.post("/config/data")
@requires(["authenticated"])
async def set_config_data(
    request: Request,
    updated_config: FullConfig,
    client: Optional[str] = None,
):
    user = request.user.object
    await map_config_to_db(updated_config, user)

    configuration_update_metadata = {}

    enabled_content = await sync_to_async(EntryAdapters.get_unique_file_types)(user)

    if state.config.content_type is not None:
        configuration_update_metadata["github"] = "github" in enabled_content
        configuration_update_metadata["notion"] = "notion" in enabled_content
        configuration_update_metadata["org"] = "org" in enabled_content
        configuration_update_metadata["pdf"] = "pdf" in enabled_content
        configuration_update_metadata["markdown"] = "markdown" in enabled_content

    if state.config.processor is not None:
        configuration_update_metadata["conversation_processor"] = state.config.processor.conversation is not None

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="set_config",
        client=client,
        metadata=configuration_update_metadata,
    )
    return state.config


@api.post("/config/data/content-source/github", status_code=200)
@requires(["authenticated"])
async def set_content_config_github_data(
    request: Request,
    updated_config: Union[GithubContentConfig, None],
    client: Optional[str] = None,
):
    _initialize_config()

    user = request.user.object

    try:
        await adapters.set_user_github_config(
            user=user,
            pat_token=updated_config.pat_token,
            repos=updated_config.repos,
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to set Github config")

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="set_content_config",
        client=client,
        metadata={"content_type": "github"},
    )

    return {"status": "ok"}


@api.post("/config/data/content-source/notion", status_code=200)
@requires(["authenticated"])
async def set_content_config_notion_data(
    request: Request,
    updated_config: Union[NotionContentConfig, None],
    client: Optional[str] = None,
):
    _initialize_config()

    user = request.user.object

    try:
        await adapters.set_notion_config(
            user=user,
            token=updated_config.token,
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to set Github config")

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="set_content_config",
        client=client,
        metadata={"content_type": "notion"},
    )

    return {"status": "ok"}


@api.delete("/config/data/content-source/{content_source}", status_code=200)
@requires(["authenticated"])
async def remove_content_source_data(
    request: Request,
    content_source: str,
    client: Optional[str] = None,
):
    user = request.user.object

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="delete_content_config",
        client=client,
        metadata={"content_source": content_source},
    )

    content_object = map_config_to_object(content_source)
    if content_object is None:
        raise ValueError(f"Invalid content source: {content_source}")
    elif content_object != "Computer":
        await content_object.objects.filter(user=user).adelete()
    await sync_to_async(EntryAdapters.delete_all_entries)(user, content_source)

    enabled_content = await sync_to_async(EntryAdapters.get_unique_file_types)(user)
    return {"status": "ok"}


@api.delete("/config/data/file", status_code=200)
@requires(["authenticated"])
async def remove_file_data(
    request: Request,
    filename: str,
    client: Optional[str] = None,
):
    user = request.user.object

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="delete_file",
        client=client,
    )

    await EntryAdapters.adelete_entry_by_file(user, filename)

    return {"status": "ok"}


@api.get("/config/data/{content_source}", response_model=List[str])
@requires(["authenticated"])
async def get_all_filenames(
    request: Request,
    content_source: str,
    client: Optional[str] = None,
):
    user = request.user.object

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="get_all_filenames",
        client=client,
    )

    return await sync_to_async(list)(EntryAdapters.aget_all_filenames_by_source(user, content_source))  # type: ignore[call-arg]


@api.post("/config/data/conversation/model", status_code=200)
@requires(["authenticated"])
async def update_chat_model(
    request: Request,
    id: str,
    client: Optional[str] = None,
):
    user = request.user.object

    new_config = await ConversationAdapters.aset_user_conversation_processor(user, int(id))

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="set_conversation_chat_model",
        client=client,
        metadata={"processor_conversation_type": "conversation"},
    )

    if new_config is None:
        return {"status": "error", "message": "Model not found"}

    return {"status": "ok"}


@api.post("/config/data/search/model", status_code=200)
@requires(["authenticated"])
async def update_search_model(
    request: Request,
    id: str,
    client: Optional[str] = None,
):
    user = request.user.object

    new_config = await adapters.aset_user_search_model(user, int(id))

    if new_config is None:
        return {"status": "error", "message": "Model not found"}
    else:
        update_telemetry_state(
            request=request,
            telemetry_type="api",
            api="set_search_model",
            client=client,
            metadata={"search_model": new_config.setting.name},
        )

    return {"status": "ok"}


# Create Routes
@api.get("/config/data/default")
def get_default_config_data():
    return constants.empty_config


@api.get("/config/index/size", response_model=Dict[str, int])
@requires(["authenticated"])
async def get_indexed_data_size(request: Request, common: CommonQueryParams):
    user = request.user.object
    indexed_data_size_in_mb = await sync_to_async(EntryAdapters.get_size_of_indexed_data_in_mb)(user)
    return Response(
        content=json.dumps({"indexed_data_size_in_mb": math.ceil(indexed_data_size_in_mb)}),
        media_type="application/json",
        status_code=200,
    )


@api.get("/config/types", response_model=List[str])
@requires(["authenticated"])
def get_config_types(
    request: Request,
):
    user = request.user.object
    enabled_file_types = EntryAdapters.get_unique_file_types(user)
    configured_content_types = list(enabled_file_types)

    if state.config and state.config.content_type:
        for ctype in state.config.content_type.dict(exclude_none=True):
            configured_content_types.append(ctype)

    return [
        search_type.value
        for search_type in SearchType
        if (search_type.value in configured_content_types) or search_type == SearchType.All
    ]


@api.get("/search", response_model=List[SearchResponse])
@requires(["authenticated"])
async def search(
    q: str,
    request: Request,
    common: CommonQueryParams,
    n: Optional[int] = 5,
    t: Optional[SearchType] = SearchType.All,
    r: Optional[bool] = False,
    max_distance: Optional[Union[float, None]] = None,
    dedupe: Optional[bool] = True,
):
    user = request.user.object
    start_time = time.time()

    # Run validation checks
    results: List[SearchResponse] = []
    if q is None or q == "":
        logger.warning(f"No query param (q) passed in API call to initiate search")
        return results

    # initialize variables
    user_query = q.strip()
    results_count = n or 5
    max_distance = max_distance or math.inf
    search_futures: List[concurrent.futures.Future] = []

    # return cached results, if available
    if user:
        query_cache_key = f"{user_query}-{n}-{t}-{r}-{max_distance}-{dedupe}"
        if query_cache_key in state.query_cache[user.uuid]:
            logger.debug(f"Return response from query cache")
            return state.query_cache[user.uuid][query_cache_key]

    # Encode query with filter terms removed
    defiltered_query = user_query
    for filter in [DateFilter(), WordFilter(), FileFilter()]:
        defiltered_query = filter.defilter(defiltered_query)

    encoded_asymmetric_query = None
    if t != SearchType.Image:
        with timer("Encoding query took", logger=logger):
            search_model = await sync_to_async(get_user_search_model_or_default)(user)
            encoded_asymmetric_query = state.embeddings_model[search_model.name].embed_query(defiltered_query)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        if t in [
            SearchType.All,
            SearchType.Org,
            SearchType.Markdown,
            SearchType.Github,
            SearchType.Notion,
            SearchType.Plaintext,
            SearchType.Pdf,
        ]:
            # query markdown notes
            search_futures += [
                executor.submit(
                    text_search.query,
                    user,
                    user_query,
                    t,
                    question_embedding=encoded_asymmetric_query,
                    max_distance=max_distance,
                )
            ]

        elif (t == SearchType.Image) and state.content_index.image and state.search_models.image_search:
            # query images
            search_futures += [
                executor.submit(
                    image_search.query,
                    user_query,
                    results_count,
                    state.search_models.image_search,
                    state.content_index.image,
                )
            ]

        # Query across each requested content types in parallel
        with timer("Query took", logger):
            for search_future in concurrent.futures.as_completed(search_futures):
                if t == SearchType.Image and state.content_index.image:
                    hits = await search_future.result()
                    output_directory = constants.web_directory / "images"
                    # Collate results
                    results += image_search.collate_results(
                        hits,
                        image_names=state.content_index.image.image_names,
                        output_directory=output_directory,
                        image_files_url="/static/images",
                        count=results_count,
                    )
                else:
                    hits = await search_future.result()
                    # Collate results
                    results += text_search.collate_results(hits, dedupe=dedupe)

                    # Sort results across all content types and take top results
                    results = text_search.rerank_and_sort_results(
                        results, query=defiltered_query, rank_results=r, search_model_name=search_model.name
                    )[:results_count]

    # Cache results
    if user:
        state.query_cache[user.uuid][query_cache_key] = results

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="search",
        **common.__dict__,
    )

    end_time = time.time()
    logger.debug(f"🔍 Search took: {end_time - start_time:.3f} seconds")

    return results


@api.get("/update")
@requires(["authenticated"])
def update(
    request: Request,
    common: CommonQueryParams,
    t: Optional[SearchType] = None,
    force: Optional[bool] = False,
):
    user = request.user.object
    if not state.config:
        error_msg = f"🚨 Khoj is not configured.\nConfigure it via http://localhost:42110/config, plugins or by editing {state.config_file}."
        logger.warning(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    try:
        configure_server(state.config, regenerate=force, search_type=t, user=user)
    except Exception as e:
        error_msg = f"🚨 Failed to update server via API: {e}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)
    else:
        components = []
        if state.search_models:
            components.append("Search models")
        if state.content_index:
            components.append("Content index")
        components_msg = ", ".join(components)
        logger.info(f"📪 {components_msg} updated via API")

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="update",
        **common.__dict__,
    )

    return {"status": "ok", "message": "khoj reloaded"}


@api.get("/chat/starters", response_class=Response)
@requires(["authenticated"])
async def chat_starters(
    request: Request,
    common: CommonQueryParams,
) -> Response:
    user: KhojUser = request.user.object
    starter_questions = await ConversationAdapters.aget_conversation_starters(user)
    return Response(content=json.dumps(starter_questions), media_type="application/json", status_code=200)


@api.get("/chat/history")
@requires(["authenticated"])
def chat_history(
    request: Request,
    common: CommonQueryParams,
):
    user = request.user.object
    validate_conversation_config()

    # Load Conversation History
    meta_log = ConversationAdapters.get_conversation_by_user(user=user).conversation_log

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="chat",
        **common.__dict__,
    )

    return {"status": "ok", "response": meta_log.get("chat", [])}


@api.delete("/chat/history")
@requires(["authenticated"])
async def clear_chat_history(
    request: Request,
    common: CommonQueryParams,
):
    user = request.user.object

    # Clear Conversation History
    await ConversationAdapters.adelete_conversation_by_user(user)

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="clear_chat_history",
        **common.__dict__,
    )

    return {"status": "ok", "message": "Conversation history cleared"}


@api.get("/chat/options", response_class=Response)
@requires(["authenticated"])
async def chat_options(
    request: Request,
    common: CommonQueryParams,
) -> Response:
    cmd_options = {}
    for cmd in ConversationCommand:
        cmd_options[cmd.value] = command_descriptions[cmd]

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="chat_options",
        **common.__dict__,
    )
    return Response(content=json.dumps(cmd_options), media_type="application/json", status_code=200)


@api.post("/transcribe")
@requires(["authenticated"])
async def transcribe(
    request: Request,
    common: CommonQueryParams,
    file: UploadFile = File(...),
    rate_limiter_per_minute=Depends(ApiUserRateLimiter(requests=1, subscribed_requests=10, window=60)),
    rate_limiter_per_day=Depends(ApiUserRateLimiter(requests=10, subscribed_requests=600, window=60 * 60 * 24)),
):
    user: KhojUser = request.user.object
    audio_filename = f"{user.uuid}-{str(uuid.uuid4())}.webm"
    user_message: str = None

    # If the file is too large, return an unprocessable entity error
    if file.size > 10 * 1024 * 1024:
        logger.warning(f"Audio file too large to transcribe. Audio file size: {file.size}. Exceeds 10Mb limit.")
        return Response(content="Audio size larger than 10Mb limit", status_code=422)

    # Transcribe the audio from the request
    try:
        # Store the audio from the request in a temporary file
        audio_data = await file.read()
        with open(audio_filename, "wb") as audio_file_writer:
            audio_file_writer.write(audio_data)
        audio_file = open(audio_filename, "rb")

        # Send the audio data to the Whisper API
        speech_to_text_config = await ConversationAdapters.get_speech_to_text_config()
        if not speech_to_text_config:
            # If the user has not configured a speech to text model, return an unsupported on server error
            status_code = 501
        elif state.openai_client and speech_to_text_config.model_type == SpeechToTextModelOptions.ModelType.OPENAI:
            speech2text_model = speech_to_text_config.model_name
            user_message = await transcribe_audio(audio_file, speech2text_model, client=state.openai_client)
        elif speech_to_text_config.model_type == SpeechToTextModelOptions.ModelType.OFFLINE:
            speech2text_model = speech_to_text_config.model_name
            user_message = await transcribe_audio_offline(audio_filename, speech2text_model)
    finally:
        # Close and Delete the temporary audio file
        audio_file.close()
        os.remove(audio_filename)

    if user_message is None:
        return Response(status_code=status_code or 500)

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="transcribe",
        **common.__dict__,
    )

    # Return the spoken text
    content = json.dumps({"text": user_message})
    return Response(content=content, media_type="application/json", status_code=200)


@api.get("/chat", response_class=Response)
@requires(["authenticated"])
async def chat(
    request: Request,
    common: CommonQueryParams,
    q: str,
    n: Optional[int] = 5,
    d: Optional[float] = 0.18,
    stream: Optional[bool] = False,
    rate_limiter_per_minute=Depends(ApiUserRateLimiter(requests=10, subscribed_requests=60, window=60)),
    rate_limiter_per_day=Depends(ApiUserRateLimiter(requests=10, subscribed_requests=600, window=60 * 60 * 24)),
) -> Response:
    user: KhojUser = request.user.object
    q = unquote(q)

    await is_ready_to_chat(user)
    conversation_command = get_conversation_command(query=q, any_references=True)

    conversation_command_rate_limiter.update_and_check_if_valid(request, conversation_command)

    q = q.replace(f"/{conversation_command.value}", "").strip()

    meta_log = (await ConversationAdapters.aget_conversation_by_user(user)).conversation_log

    compiled_references, inferred_queries, defiltered_query = await extract_references_and_questions(
        request, common, meta_log, q, (n or 5), (d or math.inf), conversation_command
    )
    online_results: Dict = dict()

    if conversation_command == ConversationCommand.Default and is_none_or_empty(compiled_references):
        conversation_command = ConversationCommand.General

    elif conversation_command == ConversationCommand.Help:
        conversation_config = await ConversationAdapters.aget_user_conversation_config(user)
        if conversation_config == None:
            conversation_config = await ConversationAdapters.aget_default_conversation_config()
        model_type = conversation_config.model_type
        formatted_help = help_message.format(model=model_type, version=state.khoj_version, device=get_device())
        return StreamingResponse(iter([formatted_help]), media_type="text/event-stream", status_code=200)

    elif conversation_command == ConversationCommand.Notes and not await EntryAdapters.auser_has_entries(user):
        no_entries_found_format = no_entries_found.format()
        return StreamingResponse(iter([no_entries_found_format]), media_type="text/event-stream", status_code=200)

    elif conversation_command == ConversationCommand.Online:
        try:
            online_results = await search_with_google(defiltered_query)
        except ValueError as e:
            return StreamingResponse(
                iter(["Please set your SERPER_DEV_API_KEY to get started with online searches 🌐"]),
                media_type="text/event-stream",
                status_code=200,
            )
    elif conversation_command == ConversationCommand.Image:
        update_telemetry_state(
            request=request,
            telemetry_type="api",
            api="chat",
            metadata={"conversation_command": conversation_command.value},
            **common.__dict__,
        )
        image, status_code, improved_image_prompt = await text_to_image(q)
        if image is None:
            content_obj = {
                "image": image,
                "intentType": "text-to-image",
                "detail": "Failed to generate image. Make sure your image generation configuration is set.",
            }
            return Response(content=json.dumps(content_obj), media_type="application/json", status_code=status_code)
        await sync_to_async(save_to_conversation_log)(
            q, image, user, meta_log, intent_type="text-to-image", inferred_queries=[improved_image_prompt]
        )
        content_obj = {"image": image, "intentType": "text-to-image", "inferredQueries": [improved_image_prompt]}  # type: ignore
        return Response(content=json.dumps(content_obj), media_type="application/json", status_code=status_code)

    # Get the (streamed) chat response from the LLM of choice.
    llm_response, chat_metadata = await agenerate_chat_response(
        defiltered_query,
        meta_log,
        compiled_references,
        online_results,
        inferred_queries,
        conversation_command,
        user,
    )

    chat_metadata.update({"conversation_command": conversation_command.value})

    update_telemetry_state(
        request=request,
        telemetry_type="api",
        api="chat",
        metadata=chat_metadata,
        **common.__dict__,
    )

    if llm_response is None:
        return Response(content=llm_response, media_type="text/plain", status_code=500)

    if stream:
        return StreamingResponse(llm_response, media_type="text/event-stream", status_code=200)

    iterator = AsyncIteratorWrapper(llm_response)

    # Get the full response from the generator if the stream is not requested.
    aggregated_gpt_response = ""
    async for item in iterator:
        if item is None:
            break
        aggregated_gpt_response += item

    actual_response = aggregated_gpt_response.split("### compiled references:")[0]

    response_obj = {"response": actual_response, "context": compiled_references}

    return Response(content=json.dumps(response_obj), media_type="application/json", status_code=200)


async def extract_references_and_questions(
    request: Request,
    common: CommonQueryParams,
    meta_log: dict,
    q: str,
    n: int,
    d: float,
    conversation_type: ConversationCommand = ConversationCommand.Default,
):
    user = request.user.object if request.user.is_authenticated else None

    # Initialize Variables
    compiled_references: List[Any] = []
    inferred_queries: List[str] = []

    if conversation_type == ConversationCommand.General or conversation_type == ConversationCommand.Online:
        return compiled_references, inferred_queries, q

    if not await sync_to_async(EntryAdapters.user_has_entries)(user=user):
        logger.warning(
            "No content index loaded, so cannot extract references from knowledge base. Please configure your data sources and update the index to chat with your notes."
        )
        return compiled_references, inferred_queries, q

    # Extract filter terms from user message
    defiltered_query = q
    for filter in [DateFilter(), WordFilter(), FileFilter()]:
        defiltered_query = filter.defilter(defiltered_query)
    filters_in_query = q.replace(defiltered_query, "").strip()

    using_offline_chat = False

    # Infer search queries from user message
    with timer("Extracting search queries took", logger):
        # If we've reached here, either the user has enabled offline chat or the openai model is enabled.
        offline_chat_config = await ConversationAdapters.aget_offline_chat_conversation_config()
        conversation_config = await ConversationAdapters.aget_conversation_config(user)
        if conversation_config is None:
            conversation_config = await ConversationAdapters.aget_default_conversation_config()
        if (
            offline_chat_config
            and offline_chat_config.enabled
            and conversation_config.model_type == ChatModelOptions.ModelType.OFFLINE
        ):
            using_offline_chat = True
            default_offline_llm = await ConversationAdapters.get_default_offline_llm()
            chat_model = default_offline_llm.chat_model
            if state.gpt4all_processor_config is None:
                state.gpt4all_processor_config = GPT4AllProcessorModel(chat_model=chat_model)

            loaded_model = state.gpt4all_processor_config.loaded_model

            inferred_queries = extract_questions_offline(
                defiltered_query, loaded_model=loaded_model, conversation_log=meta_log, should_extract_questions=False
            )
        elif conversation_config and conversation_config.model_type == ChatModelOptions.ModelType.OPENAI:
            openai_chat_config = await ConversationAdapters.get_openai_chat_config()
            default_openai_llm = await ConversationAdapters.get_default_openai_llm()
            api_key = openai_chat_config.api_key
            chat_model = default_openai_llm.chat_model
            inferred_queries = extract_questions(
                defiltered_query, model=chat_model, api_key=api_key, conversation_log=meta_log
            )

    # Collate search results as context for GPT
    with timer("Searching knowledge base took", logger):
        result_list = []
        for query in inferred_queries:
            n_items = min(n, 3) if using_offline_chat else n
            result_list.extend(
                await search(
                    f"{query} {filters_in_query}",
                    request=request,
                    n=n_items,
                    r=True,
                    max_distance=d,
                    dedupe=False,
                    common=common,
                )
            )
        result_list = text_search.deduplicated_search_responses(result_list)
        compiled_references = [item.additional["compiled"] for item in result_list]

    return compiled_references, inferred_queries, defiltered_query


@api.get("/health")
async def health_check():
    return Response(status_code=200)
