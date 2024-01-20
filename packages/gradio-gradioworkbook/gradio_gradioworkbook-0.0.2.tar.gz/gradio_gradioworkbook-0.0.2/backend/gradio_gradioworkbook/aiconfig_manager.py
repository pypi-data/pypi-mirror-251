"""Helper class to reference the AIConfigRuntime state
"""
from threading import Event
from typing import Any, Dict, Literal

from aiconfig import AIConfigRuntime, ModelParserRegistry
from aiconfig.registry import update_model_parser_registry_with_config_runtime
from gradio.data_classes import FileData

from .utils import EXCLUDE_OPTIONS, show_debug

# TODO (rossdanlm): Use os.path to get better relative path to file
DEFAULT_FILE_PATH: Literal = "./my_config.aiconfig.json"
DEFAULT_AICONFIG_SETTINGS: Dict[str, Any] = {
    "name": "Gradio Workbook AIConfig",
    "description": "This is the AIConfig that is used for the current Gradio workbook",
}


class AIConfigManager:
    """
    Manages the AIConfigRuntime state so that we can
    reference it from other classes without worrying about it being stale
    This also ensures that there are no circular dependencies for classes
    that need to reference the AIConfigRuntime

    Also will contain utility methods if needed
    """

    config: AIConfigRuntime
    thread_events: dict[str, Event]

    def __init__(self, filepath: str):
        self.config = self.create_or_load_aiconfig(filepath)
        self.thread_events = {}

    def get_config(self) -> AIConfigRuntime:
        """Self-explanatory"""
        return self.config

    def get_config_json(self) -> str:
        """Helper function to return the config in json str format"""
        return self.get_config().model_dump(exclude=EXCLUDE_OPTIONS)

    def set_config(self, config: AIConfigRuntime):
        """Self-explanatory"""
        self.config = config

    def create_or_load_aiconfig(self, filepath: str) -> AIConfigRuntime:
        """Create or load an AIConfigRuntime from a filepath"""
        already_tried_default_filepath = False
        if not filepath:
            print(
                f"Warning, no filepath was provided so using default path '{DEFAULT_FILE_PATH}' instead"
            )
            filepath = DEFAULT_FILE_PATH
            already_tried_default_filepath = True

        try:
            config = AIConfigRuntime.load(filepath)
        # TODO (rossdanlm): Test this also with malformed json format to see which error it produces and catch for that
        except FileNotFoundError:
            try:
                if not already_tried_default_filepath:
                    print(
                        f"Warning, filepath '{filepath}' not found, trying default filepath '{DEFAULT_FILE_PATH}' instead..."
                    )
                    filepath = DEFAULT_FILE_PATH
                    config = AIConfigRuntime.load(filepath)
                else:
                    raise FileNotFoundError()
            except FileNotFoundError:
                print(
                    f"Warning, filepath '{filepath}' not found, creating new AIConfig. If needed, this AIConfig will be saved to '{DEFAULT_FILE_PATH}'"
                )
                filepath = DEFAULT_FILE_PATH
                config = AIConfigRuntime.create(**DEFAULT_AICONFIG_SETTINGS)
        config.file_path = filepath
        update_model_parser_registry_with_config_runtime(config)
        return config

    def get_aiconfig_from_filedata(self, filedata: FileData) -> AIConfigRuntime:
        """Get an AIConfigRuntime from a FileData object. Used in the
        "Upload AIConfig" button. This also attaches the returned AIConfig
        to the AIConfigManager object

        Args:
            filedata (FileData): The FileData object that is the result of the upload
                button input component

        Returns:
            AIConfigRuntime: We need to retun an AIConfigRuntime which is the value of
            the GradioWorkbookComponent. Here we return self.config
        """
        file_path = filedata.name
        config: AIConfigRuntime = self.create_or_load_aiconfig(file_path)
        if show_debug():
            print(f"inside {self.get_aiconfig_from_filedata.__name__}")
            print(f"{config=}")
        self.set_config(config)
        return self.config

    def get_models(self) -> list[str]:
        """Helper function to get the models from the ModelParserRegistry"""
        return ModelParserRegistry.parser_ids()
