""""
File for defining the event data classes: https://www.gradio.app/docs/eventdata.
In general, the value will be the payload passed from the frontend AIConfig as 
a json string
"""
import asyncio
import copy
import ctypes
import json
import threading
import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from aiconfig import AIConfigRuntime, InferenceOptions
from aiconfig.schema import ExecuteResult, Output, Prompt
from gradio.events import EventData

from .aiconfig_manager import AIConfigManager
from .utils import EXCLUDE_OPTIONS, QueueIterator, show_debug, STOP_STREAMING_SIGNAL

if TYPE_CHECKING:
    from gradio.blocks import Block


class AddPromptEventData(EventData):
    """
    Add a prompt to the component's AIConfig.

        Default position is at the end for now
        TODO (rossdanlm): Add index to specify what position we should add
        prompt to AIConfig
    """

    def __init__(self, target: Union["Block", None], data: Any):
        super().__init__(target, data)

        self.prompt_name: str = data["prompt_name"]

        # Data of the Prompt to be added
        self.prompt: Prompt = data["prompt"]

        # Index to add the prompt to
        self.index: int = data["index"]


class CancelRunEventData(EventData):
    """
    Cancel the prompt run operation identified by the cancellation_token field
    """

    def __init__(self, target: Union["Block", None], data: Any):
        super().__init__(target, data)

        # Token generated and stored by prompt client whenever the run prompt
        # button is clicked to start running the prompt
        self.cancellation_token_id: str = data["cancellation_token_id"]

class DeletePromptEventData(EventData):
    """
    Delete the identified by the prompt_name field
    """

    def __init__(self, target: Union["Block", None], data: Any):
        super().__init__(target, data)

        # Name of the prompt to be deleted
        self.prompt_name: str = data["prompt_name"]


class RunPromptEventData(EventData):
    """
    Run the prompt identified by the prompt_name field
    """

    def __init__(self, target: Union["Block", None], data: Any):
        super().__init__(target, data)

        # Name of the prompt to be run
        self.prompt_name: str = data["prompt_name"]

        # Token to use for cancelling this particular run
        self.cancellation_token: Optional[str] = data.get("cancellation_token", None)

        # Whether we should run the other prompts that this depends on
        # TODO(rossdanlm): Make this generic kwargs
        self.run_with_dependencies: bool = data.get("run_with_dependencies", True)

        # TODO(rossdanlm): Add inference options (streaming) here?


class SetConfigDescriptionEventData(EventData):
    """
    Set the description for the AIConfig
    """

    def __init__(self, target: Union["Block", None], data: Any):
        super().__init__(target, data)

        # Description to set for the AIConfig
        self.description: str = data["description"]


class SetConfigNameEventData(EventData):
    """
    Set the name for the AIConfig
    """

    def __init__(self, target: Union["Block", None], data: Any):
        super().__init__(target, data)

        # Name to set for the AIConfig
        self.name: str = data["name"]


class SetParametersEventData(EventData):
    """
    Set parameter values either for the overall config or a specific prompt
    identified by the prompt_name field
    """

    def __init__(self, target: Union["Block", None], data: Any):
        super().__init__(target, data)

        # Parameter name key to be set
        self.parameters: Dict[str, Any] = data["parameters"]

        # Name of the prompt to be updated. If None, update the overall config
        self.prompt_name: str = data.get("prompt_name", None)


class UpdateModelEventData(EventData):
    """
    Update the model either for the overall config or a specific prompt
    identified by the prompt_name field
    """

    def __init__(self, target: Union["Block", None], data: Any):
        super().__init__(target, data)

        # Model name to update the prompt (if not None) or AIConfig with
        self.model_name: Optional[str] = data.get("model_name", None)

        # Model settings to update the prompt (if not None) or AIConfig with
        self.model_settings: Optional[Dict[str, Any]] = data.get("model_settings", None)

        # Name of the prompt to be updated. If None, update the overall config
        self.prompt_name: Optional[str] = data.get("prompt_name", None)


class UpdatePromptEventData(EventData):
    """
    Update the prompt identified by the prompt_name field
    """

    def __init__(self, target: Union["Block", None], data: Any):
        super().__init__(target, data)

        # Name of the prompt to be updated
        self.prompt_name: str = data["prompt_name"]

        # Data to update the prompt with
        self.prompt: Prompt = data["prompt"]


class EventHandler:
    """
    A class to store the event implementation for a specific event type
    """

    config_manager: AIConfigManager

    def __init__(self, config_manager: AIConfigManager):
        self.config_manager = config_manager

    def add_prompt_impl(self, event: AddPromptEventData) -> str:
        """
        Run this for the add_prompt event
        """
        prompt_name = event.prompt_name
        prompt_json_str = json.dumps(event.prompt)
        index = event.index

        prompt = Prompt.model_validate_json(prompt_json_str)

        config: AIConfigRuntime = self.config_manager.get_config()
        config.add_prompt(prompt_name=prompt_name, prompt_data=prompt, index=index)
        return json.dumps({"aiconfig": self.config_manager.get_config_json()})

    def cancel_run_impl(self, event: CancelRunEventData) -> str:
        """
        Run this for the cancel_run event
        """
        cancellation_token_id: str = event.cancellation_token_id
        if cancellation_token_id is not None:
            thread_event = self.config_manager.thread_events.get(cancellation_token_id)
            if thread_event is not None:
                thread_event.set()
                self.config_manager.thread_events.pop(cancellation_token_id)
                return json.dumps({"aiconfig": self.config_manager.get_config_json()})
            # TODO: Implement 422 Unprocessable Entity error

        # TODO implement 400 bad request error
        return json.dumps({"aiconfig": self.config_manager.get_config_json()})

    def clear_outputs_impl(self) -> str:
        """
        Run this for the clear_outputs event
        """
        config: AIConfigRuntime = self.config_manager.get_config()
        for prompt in config.prompts:
            prompt_name = prompt.name
            config.delete_output(prompt_name)
        return json.dumps({"aiconfig": self.config_manager.get_config_json()})

    def delete_prompt_impl(self, event: DeletePromptEventData) -> str:
        """
        Run this for the delete_prompt event
        """
        config: AIConfigRuntime = self.config_manager.get_config()
        config.delete_prompt(event.prompt_name)
        return json.dumps({"aiconfig": self.config_manager.get_config_json()})

    def run_prompt_impl(
        self, event: RunPromptEventData
    ) -> str:
        """
        Run this for the run_prompt event
        """
        executing_config: AIConfigRuntime = self.config_manager.get_config()

        prompt_name = event.prompt_name
        params = executing_config.get_parameters(prompt_name)

        # Define stream callback and queue object for streaming results
        output_text_queue = QueueIterator()
        def update_output_queue(data, _accumulated_data, _index) -> None:
            should_end_stream = data == STOP_STREAMING_SIGNAL
            output_text_queue.put(data, should_end_stream)

        inference_options = InferenceOptions(
            stream=True,  # Stream is always true for Gradio server implementation
            stream_callback=update_output_queue,
        )

        # Deepcopy the aiconfig prior to run so we can restore it in the case the run operation is cancelled or encounters some error
        pre_run_config = copy.deepcopy(executing_config)

        cancellation_token_id = event.cancellation_token
        if not cancellation_token_id:
            cancellation_token_id = str(uuid.uuid4())
        self.config_manager.thread_events[cancellation_token_id] = threading.Event()

        def generate(cancellation_token_id: str):  # type: ignore
            # Use multi-threading so that we don't block run command from
            # displaying the streamed output (if streaming is supported)
            def run_async_config_in_thread():
                try:
                    asyncio.run(executing_config.run(prompt_name=prompt_name, params=params, run_with_dependencies=False, options=inference_options))  # type: ignore
                except Exception as e:
                    output_text_queue.put(e)
                output_text_queue.put(STOP_STREAMING_SIGNAL)  # type: ignore

            def create_error_payload(message: str, code: int):
                error_info = {"error": {"message": message, "code": code}}
                aiconfig_json = pre_run_config.model_dump(exclude=EXCLUDE_OPTIONS) if pre_run_config is not None else None
                # Gradio needs to be updated with full aiconfig value so no point
                # in passing it in twice again inside of the error info JSON
                error_info["aiconfig"] = aiconfig_json
                return json.dumps(error_info)

            def create_cancellation_payload():
                return create_error_payload(message="The task was cancelled.", code=499)

            def handle_cancellation():
                yield create_cancellation_payload()
                # Reset the aiconfig state to the state prior to the run, 
                # and kill the running thread
                kill_thread(t.ident)
                self.config_manager.set_config(pre_run_config)

            def kill_thread(thread_id: int | None):
                """
                Kill the thread with the given thread_id.

                PyThreadState_SetAsyncExc: This is a C API function in Python
                which is used to raise an exception in the context of the 
                specified thread.

                SystemExit: This is the exception we'd like to raise in the 
                target thread.
                """
                if thread_id is None:
                    # Nothing to do
                    return
                response = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))

                if response == 0:
                    print(f"Invalid thread id {thread_id}")
                elif response != 1:
                    # If the response is not 1, the function didn't work correctly, and you should call it again with exc=NULL to reset it.
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, None)

            displaying_config = copy.deepcopy(executing_config)
            cancellation_event = self.config_manager.thread_events[cancellation_token_id]
            t = threading.Thread(target=run_async_config_in_thread)
            t.start()

            # If model supports streaming, need to wait until streamer has at
            # least 1 item to display. If model does not support streaming,
            # need to wait until the aiconfig.run() thread is complete
            while output_text_queue.isEmpty() and t.is_alive():
                if cancellation_event.is_set():
                    yield from handle_cancellation()
                    return

            if not output_text_queue.isEmpty():
                accumulated_output_text = ""
                for text in output_text_queue:
                    if cancellation_event.is_set():
                        yield from handle_cancellation()
                        return

                    if isinstance(text, Exception):
                        yield from create_error_payload(message=f"Exception: {text}", code=500)
                        return
                    elif isinstance(text, str):
                        accumulated_output_text += text
                    elif isinstance(text, dict) and "content" in text:
                        # TODO: Fix streaming output format so that it returns text
                        accumulated_output_text += text["content"]
                    elif isinstance(text, dict) and "generated_text" in text:
                        # TODO: Fix streaming output format so that it returns text
                        accumulated_output_text += text["generated_text"]

                    accumulated_output: Output = ExecuteResult(
                        **{
                            "output_type": "execute_result",
                            "data": accumulated_output_text,
                            # Assume streaming only supports single output
                            # I think this actually may be wrong for PaLM or OpenAI
                            # TODO: Need to sync with Ankush but can fix forward
                            "execution_count": 0,
                            "metadata": {},
                        }  # type: ignore
                    )
                    displaying_config.add_output(
                        prompt_name, accumulated_output, overwrite=True
                    )
                    if show_debug():
                        print(f"{accumulated_output_text=}")
                    yield json.dumps({"aiconfig_chunk": displaying_config.model_dump(exclude=EXCLUDE_OPTIONS)})

            # Ensure that the run process is complete to yield final output
            t.join()

            if cancellation_event.is_set():
                yield from handle_cancellation()
                return

            self.config_manager.thread_events.pop(cancellation_token_id, None)
            aiconfig_json = self.config_manager.get_config_json()
            stop_streaming_json = json.dumps({"stop_streaming": True, "aiconfig_chunk": aiconfig_json})
            if show_debug():
                print(f"{stop_streaming_json=}")
            yield stop_streaming_json

        if show_debug():
            print(f"Running `aiconfig.run()` command with request: {event}")
        # TODO: Add try-catch for error handling
        yield from generate(cancellation_token_id)

    def set_config_description_impl(self, event: SetConfigDescriptionEventData) -> str:
        """
        Run this for the set_config_description event
        """
        config: AIConfigRuntime = self.config_manager.get_config()
        config.set_description(event.description)
        return json.dumps({"aiconfig": self.config_manager.get_config_json()})

    def set_config_name_impl(self, event: SetConfigNameEventData) -> str:
        """
        Run this for the set_config_name event
        """
        config: AIConfigRuntime = self.config_manager.get_config()
        config.set_name(event.name)
        return json.dumps({"aiconfig": self.config_manager.get_config_json()})

    def set_parameters_impl(self, event: SetParametersEventData) -> str:
        """
        Run this for the set_parameters event
        """
        config: AIConfigRuntime = self.config_manager.get_config()
        config.set_parameters(event.parameters, event.prompt_name)
        return json.dumps({"aiconfig": self.config_manager.get_config_json()})

    def update_model_impl(self, event: UpdateModelEventData) -> str:
        """
        Run this for the update_model event
        """
        config: AIConfigRuntime = self.config_manager.get_config()
        config.update_model(event.model_name, event.model_settings, event.prompt_name)
        return json.dumps({"aiconfig": self.config_manager.get_config_json()})

    def update_prompt_impl(self, event: UpdatePromptEventData) -> str:
        """
        Run this for the update_prompt event
        """
        prompt_json_str = json.dumps(event.prompt)
        prompt = Prompt.model_validate_json(prompt_json_str)

        config: AIConfigRuntime = self.config_manager.get_config()
        config.update_prompt(event.prompt_name, prompt)
        return json.dumps({"aiconfig": self.config_manager.get_config_json()})
