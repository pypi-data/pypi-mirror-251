from typing import Literal

from huggingface_hub import hf_hub_download

AVAILABLE_FORMATS = [
    "Q2_K",
    "Q3_K_S",
    "Q3_K_M",
    "Q3_K_L",
    "Q4_K_S",
    "Q4_K_M",
    "Q5_K_S",
    "Q5_K_M",
    "Q6_K"
]

PROMPTING_STYLES = [
    "Llama2",
    "OpenChat"
]

CHAT_MODE = [
    "Instruction",
    "Chat"
]


def prepare_model_to_load(
        model_name: str,
        provider: str,
        quantize_format: str,
):
    """
    The prepare_model_to_load function is used to prepare the model name and format for loading.

    :param model_name: str: Specify the model name
    :param quantize_format: str: Specify the format of the model
    :param provider: str: Specify the provider of the model
    :return: name and the file path of the quantized model
    """

    file_path = f"{model_name}.{quantize_format}.gguf"
    repo_id = f"{provider}/{model_name}"
    return repo_id, file_path


def download_model_gguf(
        pretrained_model_name_or_path: str | None = None,
        quantize_type: str | Literal[
            "Q2_K",
            "Q3_K_S",
            "Q3_K_M",
            "Q3_K_L",
            "Q4_K_S",
            "Q4_K_M",
            "Q5_K_S",
            "Q5_K_M",
            "Q6_K"
        ] = "Q4_K_S",
        model_name: str | None = None,
        provider: str | Literal["erfanzar"] | None = None,
        hf_token: str | None = None,
        file_name: str | None = None
):
    if pretrained_model_name_or_path is not None and (model_name is None or provider is None):
        provider, model_name = pretrained_model_name_or_path.split("/")
    repo_id, file_path = prepare_model_to_load(
        model_name=model_name,
        quantize_format=quantize_type,
        provider=provider
    )

    if file_name is None:
        file_name = file_path
    tkn = {}
    if hf_token is not None or hf_token != "":
        tkn = dict(token=hf_token)
    ref = hf_hub_download(
        repo_id=repo_id,
        filename=file_name,
        **tkn
    )
    return ref
