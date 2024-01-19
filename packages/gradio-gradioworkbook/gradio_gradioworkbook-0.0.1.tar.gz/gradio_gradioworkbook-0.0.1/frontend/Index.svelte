<script lang="ts">
  //@ts-ignore Import IS used by react:GradioWorkbook below
  import GradioWorkbook from "./GradioWorkbook";

  import "./styles.css";

  import type { Gradio } from "@gradio/utils";
  import { Block } from "@gradio/atoms";
  import { StatusTracker } from "@gradio/statustracker";
  import type { LoadingStatus } from "@gradio/statustracker";
  import type { SelectData } from "@gradio/utils";
  import {
    // AIConfigEditor,
    type RunPromptStreamCallback,
    type RunPromptStreamErrorCallback,
    type RunPromptStreamErrorEvent,
  } from "@lastmileai/aiconfig-editor";
  import type {
    AIConfig,
    InferenceSettings,
    JSONObject,
    Prompt,
  } from "aiconfig";

  type AddPromptEventData = {
    prompt_name: string;
    prompt: Prompt;
    index: number;
  };

  type CancelRunEventData = {
    cancellation_token_id: string;
  };

  type DeletePromptEventData = {
    prompt_name: string;
  };

  type RunPromptEventData = {
    prompt_name: string;
    cancellation_token?: string;
  };

  type SetConfigDescriptionEventData = {
    description: string;
  };

  type SetConfigNameEventData = {
    name: string;
  };

  type SetParametersEventData = {
    parameters: JSONObject;
    prompt_name?: string;
  };

  type UpdateModelEventData = {
    model_name?: string;
    model_settings?: InferenceSettings;
    prompt_name?: string;
  };

  type UpdatePromptEventData = {
    prompt_name: string;
    prompt: Prompt;
  };

  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = true;

  // We obtain a serialized JSON string from the backend, containing
  // the aiconfig and model_ids
  export let value: string;
  let parsedValue: any;
  let aiconfig: AIConfig | undefined;
  let model_ids: string[] = [];
  // TODO: Remove any from onStreamHandler after package has been updated
  let onStreamHandler: RunPromptStreamCallback | any | undefined;
  let onStreamErrorHandler: RunPromptStreamErrorCallback | undefined;

  $: {
    try {
      if (value != null) {
        parsedValue = JSON.parse(value);
        aiconfig = parsedValue.aiconfig ?? parsedValue.aiconfig_chunk!;

        if (parsedValue.model_ids) {
          model_ids = parsedValue.model_ids;
        }
      }
    } catch (e) {
      console.error("Invalid JSON value passed to GradioWorkbook", e);
    }

    // We are setting up streaming functionality outside of the
    // `handleRunPrompt` because Gradio probably isn't capable of awaiting
    // for server response and we just directly check the value each time
    if (onStreamHandler && parsedValue.stop_streaming) {
      onStreamHandler({ type: "stop_streaming", data: null });
      onStreamHandler = undefined;
    } else if (onStreamHandler && parsedValue.aiconfig_chunk) {
      onStreamHandler({
        type: "aiconfig_chunk",
        data: parsedValue.aiconfig_chunk,
      });
    } else if (parsedValue.error && onStreamErrorHandler) {
      onStreamErrorHandler({
        type: "error",
        data: {
          message: parsedValue.error.message,
          code: parsedValue.error.code,
          // Gradio needs to be updated with full aiconfig value so no point
          // in passing it in twice again inside of the error info JSON
          data: aiconfig,
        } as RunPromptStreamErrorEvent["data"],
      });
      onStreamErrorHandler = undefined;
    }
  }

  export let container = true;
  export let scale: number | null = null;
  export let min_width: number | undefined = undefined;
  export let loading_status: LoadingStatus;
  export let gradio: Gradio<{
    change: never;
    select: SelectData;
    input: never;
    add_prompt: AddPromptEventData;
    cancel_run: CancelRunEventData;
    clear_outputs: void;
    delete_prompt: DeletePromptEventData;
    run_prompt: RunPromptEventData;
    set_config_description: SetConfigDescriptionEventData;
    set_config_name: SetConfigNameEventData;
    set_parameters: SetParametersEventData;
    update_model: UpdateModelEventData;
    update_prompt: UpdatePromptEventData;
  }>;

  function handleAddPrompt(prompt_name: string, prompt: Prompt, index: number) {
    gradio.dispatch("add_prompt", {
      prompt_name,
      prompt,
      index,
    });
  }

  function handleCancel(cancellation_token_id: string) {
    gradio.dispatch("cancel_run", {
      cancellation_token_id,
    });
  }

  function handleClearOutputs() {
    gradio.dispatch("clear_outputs");
  }

  function handleDeletePrompt(prompt_name: string) {
    gradio.dispatch("delete_prompt", {
      prompt_name,
    });
  }

  function handleGetModels(search: string) {
    return model_ids.filter((model_id) =>
      model_id.toLowerCase().includes(search.toLowerCase())
    );
  }

  function handleSetConfigDescription(description: string) {
    gradio.dispatch("set_config_description", {
      description,
    });
  }

  function handleSetConfigName(name: string) {
    gradio.dispatch("set_config_name", {
      name,
    });
  }

  function handleSetParameters(parameters: JSONObject, prompt_name?: string) {
    gradio.dispatch("set_parameters", {
      parameters,
      prompt_name,
    });
  }

  // TODO: Refactor runPrompt callback to make stream/error callbacks optional
  function handleRunPrompt(
    prompt_name: string,
    // TODO: Remove any from onStream after package has been updated
    onStream: RunPromptStreamCallback | any,
    onError: RunPromptStreamErrorCallback,
    _enable_streaming?: boolean,
    cancellation_token?: string
  ) {
    gradio.dispatch("run_prompt", {
      prompt_name,
      cancellation_token,
    });
    // Instead of implementing run functionality directly in the
    // handleRunPrompt command, Gradio simply registers the callbacks
    // so that this can be handled outside of this function.
    if (!onStreamHandler) {
      onStreamHandler = onStream;
    }
    if (!onStreamErrorHandler) {
      onStreamErrorHandler = onError;
    }
  }

  function handleUpdateModel(updateRequest: {
    modelName?: string;
    settings?: InferenceSettings;
    promptName?: string;
  }) {
    gradio.dispatch("update_model", {
      prompt_name: updateRequest.promptName,
      model_name: updateRequest.modelName,
      model_settings: updateRequest.settings,
    });
  }

  function handleUpdatePrompt(prompt_name: string, prompt: Prompt) {
    gradio.dispatch("update_prompt", {
      prompt_name,
      prompt,
    });
  }
</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
  {#if loading_status}
    <StatusTracker
      autoscroll={gradio.autoscroll}
      i18n={gradio.i18n}
      {...loading_status}
    />
  {/if}
  <react:GradioWorkbook
    {aiconfig}
    callbacks={{
      addPrompt: handleAddPrompt,
      cancel: handleCancel,
      clearOutputs: handleClearOutputs,
      deletePrompt: handleDeletePrompt,
      getModels: handleGetModels,
      runPrompt: handleRunPrompt,
      setConfigDescription: handleSetConfigDescription,
      setConfigName: handleSetConfigName,
      setParameters: handleSetParameters,
      updateModel: handleUpdateModel,
      updatePrompt: handleUpdatePrompt,
    }}
  />
</Block>
