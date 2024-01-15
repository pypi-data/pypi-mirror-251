from absl.app import run, flags
from cLLM import cLLM
from cLLM.inference import download_model_gguf, InferenceSession

FLAGS = flags.FLAGS

flags.DEFINE_string(
    "repo_id",
    "erfanzar/LinguaMatic-2.7B-GGUF",
    "Model Repo ID from provider be used to load model",
    required=True
)

flags.DEFINE_string(
    "filename",
    "LinguaMatic-2.7B-GGUF.Q4_K_M.gguf",
    "Model checkpoint name in the repo",
    required=True
)
flags.DEFINE_integer(
    "ctx",
    2048,
    "Maximum Context Length or model Context length "
)

flags.DEFINE_enum(
    "chat_format",
    "Llama2",
    ["Llama2", "OpenChat"],
    "Chat Format To be used For LLM"
)


def main(argv):
    checkpoint_path = download_model_gguf(
        pretrained_model_name_or_path=FLAGS.repo_id,
        file_name=FLAGS.filename
    )
    model = cLLM(
        checkpoint_path=checkpoint_path,
        n_ctx=FLAGS.ctx,
        verbose=False
    )
    inference_session = InferenceSession(
        model=model,
        max_tokens=FLAGS.ctx
    )
    history = []
    try:
        while True:
            total_response = ""
            user = input("USER : ")
            prompt = inference_session.llama_chat_template(
                user,
                history
            )
            print("ASSISTANCE : ", end="")
            history.append([user, ""])
            for response in inference_session(
                    prompt,
            ):
                total_response += response.predictions.text
                print(response.predictions.text, end="")
            history[-1][-1] = total_response
            print()

    except KeyboardInterrupt as e:
        ...


if __name__ == "__main__":
    run(main)
