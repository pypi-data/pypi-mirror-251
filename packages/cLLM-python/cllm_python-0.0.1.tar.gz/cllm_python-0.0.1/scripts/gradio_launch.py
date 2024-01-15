from absl.app import run, flags
from cLLM.user_interface import GradioUserInference

FLAGS = flags.FLAGS

flags.DEFINE_integer(
    "context_length",
    2048,
    "Maximum Context Length or model Context length "
)


def main(argv):
    user_inference = GradioUserInference(
        inference_session=None,
        max_tokens=FLAGS.context_length,
        max_length=FLAGS.context_length,
    )
    user_inference.build_inference().launch(share=True)


if __name__ == "__main__":
    run(main)
