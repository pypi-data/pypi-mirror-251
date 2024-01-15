# cLLM 🛸

cLLM is an Open-Source Simple Python bindings for [`llama.cpp`](https://github.com/ggerganov/llama.cpp)

> cLLM is a branch of llama.cpp in python like `llama-cpp-python` and a lot of parts of code is from `llama-cpp-python`
> but a lot of things will be customized soon

## Features 🔮

- **C++ Llama.cpp GGML Framework**: The program is built using the C++ language and utilizes the Llama.cpp framework for
  efficient performance.


- **EasyDeL Platform**: if you use provided open-source models The models have been trained using the EasyDeL platform,
  ensuring high-quality and accurate
  assistance.


- **Customized Models**: Users can access models customized for their specific needs, such as coding assistance, grammar
  correction, and more.

## Using cLLM

using cLLM is same as Llama from cLLM

```python
from cLLM import cLLM

model = cLLM(
    checkpoint_path="PATH_TO_CHECKPOINT"
)
for result in model(
        "Llama, Mistral, Mixtral, Falcon, MPT are 5 friends ",
        stream=True
):
    print(result["choices"][0]["text"], end="")
```

### Using InferenceSession

`InferenceSession` is another easy option to use LLMs and makes is compatible with server

```python
from cLLM.inference import InferenceSession

session = InferenceSession.load_from_checkpoint(
    "PATH_TO_CHECKPOINT",
    n_threads=16,
)

for res in session(
        "Llama, Mistral, Mixtral, Falcon, MPT are 5 friends ",
):
    print(res.predictions.text, end="")

```

## Getting Started

### Github

To use cLLM, follow these steps:

1. Clone the cLLM repository from GitHub.

  ```shell
  git clone https://github.com/erfanzar/cLLM.git
  ```

2. Compile and build the library

  ```shell
  python -m pip install -e .
  ```

3. Run the program and start utilizing the available models for your personal computer needs.

```shell
python scripts/gradio_launch.py
```

### PYPI

you can install cLLM right from pypi indexes

```shell
pip install cLLM
```

### Installation with Specific Hardware Acceleration (BLAS, CUDA, Metal, etc)

The default behavior for `llama.cpp` installation is to build for CPU only on Linux and Windows, and to use Metal on
MacOS. However, `llama.cpp` supports various hardware acceleration backends such as OpenBLAS, cuBLAS, CLBlast, HIPBLAS,
and Metal.

To install with a specific hardware acceleration backend, you can set the `CMAKE_ARGS` environment variable before
installing. Here are the instructions for different backends:

**OpenBLAS**

```bash
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install cLLM
```

**cuBLAS**

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install cLLM
```

**Metal**

```bash
CMAKE_ARGS="-DLLAMA_METAL=on" pip install cLLM
```

**CLBlast**

```bash
CMAKE_ARGS="-DLLAMA_CLBLAST=on" pip install cLLM
```

**hipBLAS**

```bash
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" pip install cLLM
```

You can set the `CMAKE_ARGS` environment variable accordingly based on your specific hardware acceleration requirements
before installing `llama.cpp`.

## Contributing

If you would like to contribute to cLLM, please follow the guidelines outlined in the CONTRIBUTING.md file in the
repository.

## License

cLLM is licensed under the [Apache v2.0](https://github.com/erfanzar/cLLM/blob/main/LICENSE). See the LICENSE.md file for more details.

## Support

For any questions or issues, please contact me [erfanzare810@gmail.com](erfanzare810@gmail.com).

Thank you for using cLLM! We hope it enhances your personal computer experience.
