import os
import llm
from llm.default_plugins.openai_models import Chat


MODELS = (
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "meta-llama/Llama-2-7b-chat-hf",
    "meta-llama/Llama-2-13b-chat-hf",
    "meta-llama/Llama-2-70b-chat-hf",
    "HuggingFaceH4/zephyr-7b-beta",
    "HuggingFaceH4/tiny-random-LlamaForCausalLM",
    "NousResearch/Yarn-Mistral-7b-128k",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "TheBloke/TinyLlama-1.1B-Chat-v1.0-AWQ",
    "TheBloke/Mixtral-8x7B-Instruct-v0.1-AWQ",
    "mlabonne/phixtral-2x2_8",
    "mlabonne/phixtral-4x2_8",
)


class NOSRunChat(Chat):
    needs_key = "nosrun"

    def __str__(self):
        return "NOSRun: {}".format(self.model_id)


@llm.hookimpl
def register_models(register):
    # Only do this if the key is set
    key = llm.get_key("", "nosrun", "LLM_NOSRUN_KEY")
    if not key:
        return
    for model_id in MODELS:
        register(
            NOSRunChat(
                model_id=model_id,
                model_name=model_id,
                api_base=os.getenv("NOSRUN_API_BASE", "https://llama2.nos.run/v1"),
            )
        )
