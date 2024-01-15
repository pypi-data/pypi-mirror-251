from ..cllm import cLLM
from dataclasses import dataclass
from typing import Optional, Literal, List, Iterable


@dataclass
class InferencePredictions:
    text: str
    index: int
    logprobs: Optional[float]
    finish_reason: Optional[bool]


@dataclass
class InferenceOutput:
    id: str
    object: str
    created: str
    model: str
    predictions: InferencePredictions


class InferenceSession:
    def __init__(
            self,
            model: cLLM,
            max_tokens: int = 2048
    ):
        """
        The __init__ function is the constructor for a class. it's called when an object of that class is created.

        :param self: Represent the instance of the class
        :param model: cLLM: Pass the model object to the class
        :param max_tokens: int: Set the maximum number of tokens that can be used in a single query
        """
        self.model = model
        self.max_tokens = max_tokens

    def __call__(
            self,
            string: str,
            suffix: Optional[str] = None,
            max_tokens: Optional[int] = None,
            temperature: float = 0.8,
            top_p: float = 0.95,
            min_p: float = 0.05,
            typical_p: float = 1.0,
            logprobs: Optional[int] = None,
            echo: bool = False,
            stop=None,
            frequency_penalty: float = 0.0,
            presence_penalty: float = 0.0,
            repeat_penalty: float = 1.1,
            top_k: int = 40,
            seed: Optional[int] = None,
            tfs_z: float = 1.0,
            mirostat_mode: int = 0,
            mirostat_tau: float = 5.0,
            mirostat_eta: float = 0.1,
    ) -> Iterable[InferenceOutput]:
        """
       The __call__ function is the main function of this class.
       It takes in a string, and returns an iterable of InferenceOutput objects.
       The InferenceOutput object contains the following attributes:

       :param self: Bind the method to an object
       :param string: str: Pass the text to be completed by the model
       :param suffix: Optional[str]: Add a suffix to the end of the string
       :param max_tokens: Optional[int]: Limit the number of tokens that can be generated
       :param temperature: float: Control the randomness of the output
       :param top_p: float: Filter out the top p% of tokens
       :param min_p: float: Filter out tokens that have a probability less than min_p
       :param typical_p: float: Set the probability of a token being generated
       :param logprobs: Optional[int]: Control the number of log probabilities that are returned
       :param echo: bool: Determine whether to echo the string back as a prediction
       :param stop: Stop the inference at a certain token
       :param frequency_penalty: float: Penalize the frequency of words in the text
       :param presence_penalty: float: Penalize the presence of certain words in the output
       :param repeat_penalty: float: Penalize the model for repeating words
       :param top_k: int: Control the number of tokens that are considered for each step
       :param seed: Optional[int]: Set the seed for the random number generator
       :param tfs_z: float: Control the amount of text that is generated
       :param mirostat_mode: int: Determine which type of mirostat to use
       :param mirostat_tau: float: Control the rate of change in the probability distribution
       :param mirostat_eta: float: Control the amount of randomness in the model
       :param : Set the maximum number of tokens to generate
       :return: An iterable of inferenceoutput objects
       """

        if stop is None:
            stop = []
        for model_response in self.model(
                string,
                stream=True,
                seed=seed,
                max_tokens=max_tokens or self.max_tokens,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                repeat_penalty=repeat_penalty,
                mirostat_mode=mirostat_mode,
                mirostat_tau=mirostat_tau,
                mirostat_eta=mirostat_eta,
                top_k=top_k,
                top_p=top_p,
                suffix=suffix,
                min_p=min_p,
                temperature=temperature,
                echo=echo,
                stop=stop,
                typical_p=typical_p,
                logprobs=logprobs
        ):
            predictions = InferencePredictions(
                **model_response["choices"][0]
            )
            predictions.text = predictions.text.replace("<0x0A>", "\n")
            response = InferenceOutput(
                predictions=predictions,
                created=model_response["created"],
                model=model_response["model"],
                object=model_response["object"],
                id=model_response["id"]
            )
            yield response

    @staticmethod
    def llama_chat_template(
            message: str,
            chat_history: Optional[List[str] | List[List[str]]] = None,
            system_prompt: str = None
    ):
        """
        The chat_template function takes in a message, chat_history and system prompt.
        It then formats the message into a template that can be used to train the model.
        The function returns a string of text formatted as follows:

        :param message: str: Pass in the user's message to be added to the chat history
        :param chat_history: Optional[List[str] | List[List[str]]]: Pass in a list of strings or a list of lists
        :param system_prompt: str: Set the prompt for the system
        :return: prompt string
        """
        if system_prompt == "":
            system_prompt = None
        if chat_history is None:
            chat_history = []
        do_strip = False
        texts = [
            f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n"
        ] if system_prompt is not None else [f"<s>[INST] "]
        for user_input, response in chat_history:
            user_input = user_input.strip() if do_strip else user_input
            do_strip = True
            texts.append(
                f"{user_input} [/INST] {response.strip()} </s><s>[INST] ")
        message = message.strip() if do_strip else message
        texts.append(f"{message} [/INST]")
        return "".join(texts)

    @staticmethod
    def os_chat_template(
            message: str,
            chat_history: Optional[List[str] | List[List[str]]] = None,
            system_prompt: Optional[str] = None
    ):
        """
        The os_chat_template function takes in a message, chat history, and system prompt.
        It returns a string that is formatted to be used as the input for the OpenSubtitles dataset.
        The format of this string is:

        :param message: str: Pass in the user"s message to the assistant
        :param chat_history: Optional[List[str] | List[List[str]]]: Specify the history of the conversation
        :param system_prompt: Optional[str]: Add a system prompt to the chat history
        :return: prompt string
        """
        if chat_history is None:
            chat_history = []
        system = f"<|system|>\n{system_prompt}</s>\n" if system_prompt is not None else ""
        ua = ""
        for user_input, response in chat_history:
            ua += f"<|user|>\n{user_input}</s>\n<|assistant|>\n{response}</s>\n"
        return system + ua + f"<|user|>\n{message}</s>\n<|assistant|>\n"

    def get_chat_template(self, template_name: Literal["Llama2", "OpenChat"] = "Llama2"):
        if template_name == "Llama2":
            return self.llama_chat_template
        elif template_name == "OpenChat":
            return self.os_chat_template
        else:
            raise ValueError("UnKnown Chat Template requested")

    @classmethod
    def load_from_checkpoint(
            cls,
            checkpoint_path: str,
            n_gpu_layers: int = 0,
            main_gpu: int = 0,
            tensor_split: Optional[List[float]] = None,
            vocab_only: bool = False,
            use_mmap: bool = True,
            use_mlock: bool = False,
            n_ctx: int = 512,
            n_batch: int = 512,
            n_threads: Optional[int] = None,
            n_threads_batch: Optional[int] = None,
            rope_freq_base: float = 0.0,
            rope_freq_scale: float = 0.0,
            yarn_ext_factor: float = -1.0,
            yarn_attn_factor: float = 1.0,
            yarn_beta_fast: float = 32.0,
            yarn_beta_slow: float = 1.0,
            yarn_orig_ctx: int = 0,
            mul_mat_q: bool = True,
            logits_all: bool = False,
            embedding: bool = False,
            offload_kqv: bool = False,
            last_n_tokens_size: int = 64,
            lora_base: Optional[str] = None,
            lora_scale: float = 1.0,
            lora_path: Optional[str] = None,
            numa: bool = False,
            verbose: bool = True,
            max_length: int = 2048
    ):
        return cls(
            model=cLLM(
                checkpoint_path,
                n_gpu_layers=n_gpu_layers,
                main_gpu=main_gpu,
                tensor_split=tensor_split,
                vocab_only=vocab_only,
                use_mmap=use_mmap,
                use_mlock=use_mlock,
                n_ctx=n_ctx,
                n_batch=n_batch,
                n_threads=n_threads,
                n_threads_batch=n_threads_batch,
                rope_freq_base=rope_freq_base,
                rope_freq_scale=rope_freq_scale,
                yarn_ext_factor=yarn_ext_factor,
                yarn_attn_factor=yarn_attn_factor,
                yarn_beta_fast=yarn_beta_fast,
                yarn_beta_slow=yarn_beta_slow,
                yarn_orig_ctx=yarn_orig_ctx,
                mul_mat_q=mul_mat_q,
                logits_all=logits_all,
                embedding=embedding,
                offload_kqv=offload_kqv,
                last_n_tokens_size=last_n_tokens_size,
                lora_base=lora_base,
                lora_scale=lora_scale,
                lora_path=lora_path,
                numa=numa,
                verbose=verbose,

            ),
            max_tokens=max_length
        )
