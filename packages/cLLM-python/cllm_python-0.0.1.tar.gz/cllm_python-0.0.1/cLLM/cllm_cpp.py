import sys
import os
import ctypes
from ctypes import (
    c_bool,
    c_char_p,
    c_int,
    c_int8,
    c_int32,
    c_uint8,
    c_uint32,
    c_int64,
    c_size_t,
    c_float,
    c_double,
    c_void_p,
    POINTER,
    _Pointer,  # type: ignore
    Structure,
    Union as CtypesUnion,
    Array,
)
import pathlib
from typing import List, Union


# Load the library
def _load_shared_library(lib_base_name: str):
    _base_path = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
    _lib_paths: List[pathlib.Path] = []
    if sys.platform.startswith("linux"):
        _lib_paths += [
            _base_path / f"lib{lib_base_name}.so",
        ]
    elif sys.platform == "darwin":
        _lib_paths += [
            _base_path / f"lib{lib_base_name}.so",
            _base_path / f"lib{lib_base_name}.dylib",
        ]
    elif sys.platform == "win32":
        _lib_paths += [
            _base_path / f"{lib_base_name}.dll",
            _base_path / f"lib{lib_base_name}.dll",
        ]
    else:
        raise RuntimeError("Unsupported platform")

    if "LLAMA_CPP_LIB" in os.environ:
        lib_base_name = os.environ["LLAMA_CPP_LIB"]
        _lib = pathlib.Path(lib_base_name)
        _base_path = _lib.parent.resolve()
        _lib_paths = [_lib.resolve()]

    cdll_args = dict()  # type: ignore
    if sys.platform == "win32" and sys.version_info >= (3, 8):
        os.add_dll_directory(str(_base_path))
        if "CUDA_PATH" in os.environ:
            os.add_dll_directory(os.path.join(os.environ["CUDA_PATH"], "bin"))
            os.add_dll_directory(os.path.join(os.environ["CUDA_PATH"], "lib"))
        if "HIP_PATH" in os.environ:
            os.add_dll_directory(os.path.join(os.environ["HIP_PATH"], "bin"))
            os.add_dll_directory(os.path.join(os.environ["HIP_PATH"], "lib"))
        cdll_args["winmode"] = ctypes.RTLD_GLOBAL

    for _lib_path in _lib_paths:
        if _lib_path.exists():
            try:
                return ctypes.CDLL(str(_lib_path), **cdll_args)
            except Exception as e:
                raise RuntimeError(f"Failed to load shared library '{_lib_path}': {e}")

    raise FileNotFoundError(
        f"Shared library with base name '{lib_base_name}' not found"
    )


_lib_base_name = "llama"

_lib = _load_shared_library(_lib_base_name)

c_float_p = POINTER(c_float)
c_uint8_p = POINTER(c_uint8)
c_size_t_p = POINTER(c_size_t)

_lib.llama_max_devices.argtypes = []
_lib.llama_max_devices.restype = ctypes.c_int32

LLAMA_MAX_DEVICES = _lib.llama_max_devices()

LLAMA_DEFAULT_SEED = 0xFFFFFFFF

LLAMA_MAX_RNG_STATE = 64 * 1024

LLAMA_FILE_MAGIC_GGLA = 0x67676C61

LLAMA_FILE_MAGIC_GGSN = 0x6767736E

LLAMA_SESSION_MAGIC = LLAMA_FILE_MAGIC_GGSN
LLAMA_SESSION_VERSION = 4

cllm_model_p = c_void_p

cllm_context_p = c_void_p

cllm_pos = c_int32
cllm_token = c_int32
cllm_token_p = POINTER(cllm_token)
cllm_seq_id = c_int32

LLAMA_VOCAB_TYPE_SPM = 0
LLAMA_VOCAB_TYPE_BPE = 1

LLAMA_TOKEN_TYPE_UNDEFINED = 0
LLAMA_TOKEN_TYPE_NORMAL = 1
LLAMA_TOKEN_TYPE_UNKNOWN = 2
LLAMA_TOKEN_TYPE_CONTROL = 3
LLAMA_TOKEN_TYPE_USER_DEFINED = 4
LLAMA_TOKEN_TYPE_UNUSED = 5
LLAMA_TOKEN_TYPE_BYTE = 6

LLAMA_FTYPE_ALL_F32 = 0
LLAMA_FTYPE_MOSTLY_F16 = 1
LLAMA_FTYPE_MOSTLY_Q4_0 = 2
LLAMA_FTYPE_MOSTLY_Q4_1 = 3
LLAMA_FTYPE_MOSTLY_Q4_1_SOME_F16 = 4
LLAMA_FTYPE_MOSTLY_Q8_0 = 7
LLAMA_FTYPE_MOSTLY_Q5_0 = 8
LLAMA_FTYPE_MOSTLY_Q5_1 = 9
LLAMA_FTYPE_MOSTLY_Q2_K = 10
LLAMA_FTYPE_MOSTLY_Q3_K_S = 11
LLAMA_FTYPE_MOSTLY_Q3_K_M = 12
LLAMA_FTYPE_MOSTLY_Q3_K_L = 13
LLAMA_FTYPE_MOSTLY_Q4_K_S = 14
LLAMA_FTYPE_MOSTLY_Q4_K_M = 15
LLAMA_FTYPE_MOSTLY_Q5_K_S = 16
LLAMA_FTYPE_MOSTLY_Q5_K_M = 17
LLAMA_FTYPE_MOSTLY_Q6_K = 18
LLAMA_FTYPE_MOSTLY_IQ2_XXS = 19
LLAMA_FTYPE_MOSTLY_IQ2_XS = 20
LLAMA_FTYPE_MOSTLY_Q2_K_S = 21
LLAMA_FTYPE_GUESSED = 1024

LLAMA_ROPE_SCALING_UNSPECIFIED = -1
LLAMA_ROPE_SCALING_NONE = 0
LLAMA_ROPE_SCALING_LINEAR = 1
LLAMA_ROPE_SCALING_YARN = 2
LLAMA_ROPE_SCALING_MAX_VALUE = LLAMA_ROPE_SCALING_YARN

LLAMA_SPLIT_NONE = 0
LLAMA_SPLIT_LAYER = 1
LLAMA_SPLIT_ROW = 2


class CLLMTokenData(Structure):
    _fields_ = [
        ("id", cllm_token),
        ("logit", c_float),
        ("p", c_float),
    ]


CLLMTokenData_p = POINTER(CLLMTokenData)


class CLLMTokenDataArray(Structure):
    _fields_ = [
        ("data", CLLMTokenData_p),
        ("size", c_size_t),
        ("sorted", c_bool),
    ]


CLLMTokenDataArray_p = POINTER(CLLMTokenDataArray)

cllm_progress_callback = ctypes.CFUNCTYPE(c_bool, c_float, c_void_p)


class CLLMBatch(Structure):
    """
    Input data for cllm_decode

    A CLLMBatch object can contain input about one or many sequences

    The provided arrays (i.e. token, embd, pos, etc.) must have size of n_tokens

    :param token :ctypes.Array[cllm_token]: the token ids of the input (used when embd is NULL)
    :param embd :ctypes.Array[ctypes.c_float]: token embeddings (i.e. float vector of size n_embd) (used when token is NULL)
    :param pos :ctypes.Array[ctypes.Array[cllm_pos]]: the positions of the respective token in the sequence
    :param seq_id :ctypes.Array[ctypes.Array[cllm_seq_id]]: the sequence to which the respective token belongs
    """

    _fields_ = [
        ("n_tokens", c_int32),
        ("token", POINTER(cllm_token)),
        ("embd", c_float_p),
        ("pos", POINTER(cllm_pos)),
        ("n_seq_id", POINTER(c_int32)),
        ("seq_id", POINTER(POINTER(cllm_seq_id))),
        ("logits", POINTER(c_int8)),
        ("all_pos_0", cllm_pos),
        ("all_pos_1", cllm_pos),
        ("all_seq_id", cllm_seq_id),
    ]


LLAMA_KV_OVERRIDE_INT = 0
LLAMA_KV_OVERRIDE_FLOAT = 1
LLAMA_KV_OVERRIDE_BOOL = 2


class CLLMModelKVOverrideValue(CtypesUnion):
    _fields_ = [
        ("int_value", c_int64),
        ("float_value", c_double),
        ("bool_value", c_bool),
    ]


class CLLMModelKVOverride(Structure):
    _fields_ = [
        ("key", ctypes.c_char * 128),
        ("tag", c_int),
        ("value", CLLMModelKVOverrideValue),
    ]


class CLLMModelParams(Structure):
    """
    Parameters for llama_model
    :param n_gpu_layers: int : Number of layers to store in VRAM

    :param split_mode: int : How to split the model across multiple GPUs

    :param main_gpu: int : The GPU that is used for the entire model. The interpretation of main_gpu depends on split_mode: : - LLAMA_SPLIT_NONE: the GPU that is used for the entire model : - LLAMA_SPLIT_ROW: the GPU that is used for small tensors and intermediate results : - LLAMA_SPLIT_LAYER: ignored

    :param tensor_split: ctypes.Array[ctypes.c_float] : Proportion of the model (layers or rows) to offload to each GPU, size: LLAMA_MAX_DEVICES

    :param progress_callback: cllm_progress_callback : Called with a progress value between 0.0 and 1.0. Pass NULL to disable. If the provided progress_callback returns true, model loading continues. If it returns false, model loading is immediately aborted.

    :param progress_callback_user_data: ctypes.c_void_p : Context pointer passed to the progress callback

    :param kv_overrides: ctypes.Array[CLLMModelKVOverride] : Override key-value pairs of the model meta data

    :param vocab_only: bool : Only load the vocabulary, no weights

    :param use_mmap: bool : Use mmap if possible

    :param use_mlock: bool : Force system to keep model in RAM
    """

    _fields_ = [
        ("n_gpu_layers", c_int32),
        ("split_mode", c_int),
        ("main_gpu", c_int32),
        ("tensor_split", c_float_p),
        ("progress_callback", cllm_progress_callback),
        ("progress_callback_user_data", c_void_p),
        ("kv_overrides", POINTER(CLLMModelKVOverride)),
        ("vocab_only", c_bool),
        ("use_mmap", c_bool),
        ("use_mlock", c_bool),
    ]


class CLLMContextParams(Structure):
    """Parameters for llama_context

    Attributes:
        seed (int): RNG seed, -1 for random
        n_ctx (int): text context, 0 = from model
        n_batch (int): prompt processing maximum batch size
        n_threads (int): number of threads to use for generation
        n_threads_batch (int): number of threads to use for batch processing
        rope_scaling_type (int): RoPE scaling type, from `enum llama_rope_scaling_type`
        rope_freq_base (float): RoPE base frequency, 0 = from model
        rope_freq_scale (float): RoPE frequency scaling factor, 0 = from model
        yarn_ext_factor (float): YaRN extrapolation mix factor, negative = from model
        yarn_attn_factor (float): YaRN magnitude scaling factor
        yarn_beta_fast (float): YaRN low correction dim
        yarn_beta_slow (float): YaRN high correction dim
        yarn_orig_ctx (int): YaRN original context size
        type_k (int): data type for K cache
        type_v (int): data type for V cache
        mul_mat_q (bool): if true, use experimental mul_mat_q kernels (DEPRECATED - always true)
        logits_all (bool): the llama_eval() call computes all logits, not just the last one (DEPRECATED - set CLLMBatch.logits instead)
        embedding (bool): embedding mode only
        offload_kqv (bool): whether to offload the KQV ops (including the KV cache) to GPU
    """

    _fields_ = [
        ("seed", c_uint32),
        ("n_ctx", c_uint32),
        ("n_batch", c_uint32),
        ("n_threads", c_uint32),
        ("n_threads_batch", c_uint32),
        ("rope_scaling_type", c_int8),
        ("rope_freq_base", c_float),
        ("rope_freq_scale", c_float),
        ("yarn_ext_factor", c_float),
        ("yarn_attn_factor", c_float),
        ("yarn_beta_fast", c_float),
        ("yarn_beta_slow", c_float),
        ("yarn_orig_ctx", c_uint32),
        ("type_k", c_int),
        ("type_v", c_int),
        ("mul_mat_q", c_bool),
        ("logits_all", c_bool),
        ("embedding", c_bool),
        ("offload_kqv", c_bool),
    ]


llama_log_callback = ctypes.CFUNCTYPE(None, c_int, c_char_p, c_void_p)


# Signature for logging events
# Note that text includes the new line character at the end for most events.
# If your logging mechanism cannot handle that, check if the last character is '\n' and strip it
# if it exists.
# It might not exist for progress report where '.' is output repeatedly.


class llama_model_quantize_params(Structure):
    _fields_ = [
        ("nthread", c_int32),
        ("ftype", c_int),
        ("allow_requantize", c_bool),
        ("quantize_output_tensor", c_bool),
        ("only_copy", c_bool),
    ]


llama_grammar_p = c_void_p

LLAMA_GRETYPE_END = 0
LLAMA_GRETYPE_ALT = 1
LLAMA_GRETYPE_RULE_REF = 2
LLAMA_GRETYPE_CHAR = 3
LLAMA_GRETYPE_CHAR_NOT = 4
LLAMA_GRETYPE_CHAR_RNG_UPPER = 5
LLAMA_GRETYPE_CHAR_ALT = 6


class llama_grammar_element(Structure):
    _fields_ = [
        ("type", c_int),
        ("value", c_uint32),
    ]


llama_grammar_element_p = POINTER(llama_grammar_element)


class llama_timings(Structure):
    _fields_ = [
        ("t_start_ms", c_double),
        ("t_end_ms", c_double),
        ("t_load_ms", c_double),
        ("t_sample_ms", c_double),
        ("t_p_eval_ms", c_double),
        ("t_eval_ms", c_double),
        ("n_sample", c_int32),
        ("n_p_eval", c_int32),
        ("n_eval", c_int32),
    ]


def llama_model_default_params() -> CLLMModelParams:
    """Get default parameters for llama_model"""
    return _lib.llama_model_default_params()


_lib.llama_model_default_params.argtypes = []
_lib.llama_model_default_params.restype = CLLMModelParams


def llama_context_default_params() -> CLLMContextParams:
    """Get default parameters for llama_context"""
    return _lib.llama_context_default_params()


_lib.llama_context_default_params.argtypes = []
_lib.llama_context_default_params.restype = CLLMContextParams


def llama_model_quantize_default_params() -> llama_model_quantize_params:
    """Get default parameters for llama_model_quantize"""
    return _lib.llama_model_quantize_default_params()


_lib.llama_model_quantize_default_params.argtypes = []
_lib.llama_model_quantize_default_params.restype = llama_model_quantize_params


def llama_backend_init(numa: Union[c_bool, bool]):
    """Initialize the llama + ggml backend
    If numa is true, use NUMA optimizations
    Call once at the start of the program"""
    return _lib.llama_backend_init(numa)


_lib.llama_backend_init.argtypes = [c_bool]
_lib.llama_backend_init.restype = None


def llama_backend_free():
    """Call once at the end of the program - currently only used for MPI"""
    return _lib.llama_backend_free()


_lib.llama_backend_free.argtypes = []
_lib.llama_backend_free.restype = None


def llama_load_model_from_file(
        path_model: bytes, params: CLLMModelParams
) -> cllm_model_p:
    return _lib.llama_load_model_from_file(path_model, params)


_lib.llama_load_model_from_file.argtypes = [c_char_p, CLLMModelParams]
_lib.llama_load_model_from_file.restype = cllm_model_p


def llama_free_model(model: cllm_model_p):
    return _lib.llama_free_model(model)


_lib.llama_free_model.argtypes = [cllm_model_p]
_lib.llama_free_model.restype = None


def llama_new_context_with_model(
        model: cllm_model_p, params: CLLMContextParams
) -> cllm_context_p:
    return _lib.llama_new_context_with_model(model, params)


_lib.llama_new_context_with_model.argtypes = [cllm_model_p, CLLMContextParams]
_lib.llama_new_context_with_model.restype = cllm_context_p


def llama_free(ctx: cllm_context_p):
    """Frees all allocated memory"""
    return _lib.llama_free(ctx)


_lib.llama_free.argtypes = [cllm_context_p]
_lib.llama_free.restype = None


def llama_time_us() -> int:
    return _lib.llama_time_us()


_lib.llama_time_us.argtypes = []
_lib.llama_time_us.restype = ctypes.c_int64


def llama_max_devices() -> int:
    return _lib.llama_max_devices()


_lib.llama_max_devices.argtypes = []
_lib.llama_max_devices.restype = ctypes.c_int32


def llama_mmap_supported() -> bool:
    return _lib.llama_mmap_supported()


_lib.llama_mmap_supported.argtypes = []
_lib.llama_mmap_supported.restype = c_bool


def llama_mlock_supported() -> bool:
    return _lib.llama_mlock_supported()


_lib.llama_mlock_supported.argtypes = []
_lib.llama_mlock_supported.restype = c_bool


def llama_get_model(ctx: cllm_context_p) -> cllm_model_p:
    return _lib.llama_get_model(ctx)


_lib.llama_get_model.argtypes = [cllm_context_p]
_lib.llama_get_model.restype = cllm_model_p


# LLAMA_API uint32_t llama_n_ctx      (const struct llama_context * ctx);
def llama_n_ctx(ctx: cllm_context_p) -> int:
    return _lib.llama_n_ctx(ctx)


_lib.llama_n_ctx.argtypes = [cllm_context_p]
_lib.llama_n_ctx.restype = c_uint32


# LLAMA_API uint32_t llama_n_batch    (const struct llama_context * ctx);
def llama_n_batch(ctx: cllm_context_p) -> int:
    return _lib.llama_n_batch(ctx)


_lib.llama_n_batch.argtypes = [cllm_context_p]
_lib.llama_n_batch.restype = c_uint32


# LLAMA_API enum llama_vocab_type llama_vocab_type(const struct llama_model * model);
def llama_vocab_type(model: cllm_model_p) -> int:
    return _lib.llama_vocab_type(model)


_lib.llama_vocab_type.argtypes = [cllm_model_p]
_lib.llama_vocab_type.restype = c_int


# LLAMA_API int32_t llama_n_vocab    (const struct llama_model * model);
def llama_n_vocab(model: cllm_model_p) -> int:
    return _lib.llama_n_vocab(model)


_lib.llama_n_vocab.argtypes = [cllm_model_p]
_lib.llama_n_vocab.restype = c_int32


def llama_n_ctx_train(model: cllm_model_p) -> int:
    return _lib.llama_n_ctx_train(model)


_lib.llama_n_ctx_train.argtypes = [cllm_model_p]
_lib.llama_n_ctx_train.restype = c_int32


def llama_n_embd(model: cllm_model_p) -> int:
    return _lib.llama_n_embd(model)


_lib.llama_n_embd.argtypes = [cllm_model_p]
_lib.llama_n_embd.restype = c_int32


def llama_rope_freq_scale_train(model: cllm_model_p) -> float:
    """Get the model's RoPE frequency scaling factor"""
    return _lib.llama_rope_freq_scale_train(model)


_lib.llama_rope_freq_scale_train.argtypes = [cllm_model_p]
_lib.llama_rope_freq_scale_train.restype = c_float


def llama_model_meta_val_str(
        model: cllm_model_p, key: Union[c_char_p, bytes], buf: bytes, buf_size: int
) -> int:
    """Get metadata value as a string by key name"""
    return _lib.llama_model_meta_val_str(model, key, buf, buf_size)


_lib.llama_model_meta_val_str.argtypes = [cllm_model_p, c_char_p, c_char_p, c_size_t]
_lib.llama_model_meta_val_str.restype = c_int32


def llama_model_meta_count(model: cllm_model_p) -> int:
    """Get the number of metadata key/value pairs"""
    return _lib.llama_model_meta_count(model)


_lib.llama_model_meta_count.argtypes = [cllm_model_p]
_lib.llama_model_meta_count.restype = c_int32


def llama_model_meta_key_by_index(
        model: cllm_model_p, i: Union[c_int, int], buf: bytes, buf_size: int
) -> int:
    """Get metadata key name by index"""
    return _lib.llama_model_meta_key_by_index(model, i, buf, buf_size)


_lib.llama_model_meta_key_by_index.argtypes = [
    cllm_model_p,
    c_int32,
    c_char_p,
    c_size_t,
]
_lib.llama_model_meta_key_by_index.restype = c_int32


def llama_model_meta_val_str_by_index(
        model: cllm_model_p, i: Union[c_int, int], buf: bytes, buf_size: int
) -> int:
    """Get metadata value as a string by index"""
    return _lib.llama_model_meta_val_str_by_index(model, i, buf, buf_size)


_lib.llama_model_meta_val_str_by_index.argtypes = [
    cllm_model_p,
    c_int32,
    c_char_p,
    c_size_t,
]
_lib.llama_model_meta_val_str_by_index.restype = c_int32


def llama_model_desc(
        model: cllm_model_p, buf: bytes, buf_size: Union[c_size_t, int]
) -> int:
    """Get a string describing the model type"""
    return _lib.llama_model_desc(model, buf, buf_size)


_lib.llama_model_desc.argtypes = [cllm_model_p, c_char_p, c_size_t]
_lib.llama_model_desc.restype = c_int32


def llama_model_size(model: cllm_model_p) -> int:
    """Returns the total size of all the tensors in the model in bytes"""
    return _lib.llama_model_size(model)


_lib.llama_model_size.argtypes = [cllm_model_p]
_lib.llama_model_size.restype = ctypes.c_uint64


def llama_model_n_params(model: cllm_model_p) -> int:
    """Returns the total number of parameters in the model"""
    return _lib.llama_model_n_params(model)


_lib.llama_model_n_params.argtypes = [cllm_model_p]
_lib.llama_model_n_params.restype = ctypes.c_uint64


def llama_get_model_tensor(
        model: cllm_model_p, name: Union[c_char_p, bytes]
) -> c_void_p:
    """Get a llama model tensor"""
    return _lib.llama_get_model_tensor(model, name)


_lib.llama_get_model_tensor.argtypes = [cllm_model_p, c_char_p]
_lib.llama_get_model_tensor.restype = c_void_p


def llama_model_quantize(
        fname_inp: bytes,
        fname_out: bytes,
        params,  # type: POINTER(llama_model_quantize_params) # type: ignore
) -> int:
    """Returns 0 on success"""
    return _lib.llama_model_quantize(fname_inp, fname_out, params)


_lib.llama_model_quantize.argtypes = [
    c_char_p,
    c_char_p,
    POINTER(llama_model_quantize_params),
]
_lib.llama_model_quantize.restype = c_uint32


def llama_apply_lora_from_file(
        ctx: cllm_context_p,
        path_lora: Union[c_char_p, bytes],
        scale: Union[c_float, float],
        path_base_model: Union[c_char_p, bytes],
        n_threads: Union[c_int, int],
) -> int:
    """
    Apply a LoRA adapter to a loaded model
    path_base_model is the path to a higher quality model to use as a base for
    the layers modified by the adapter. Can be NULL to use the current loaded model.
    The model needs to be reloaded before applying a new adapter, otherwise the adapter
    will be applied on top of the previous one
    Returns 0 on success
    """
    return _lib.llama_apply_lora_from_file(
        ctx, path_lora, scale, path_base_model, n_threads
    )


_lib.llama_apply_lora_from_file.argtypes = [
    cllm_context_p,
    c_char_p,
    c_float,
    c_char_p,
    c_int32,
]
_lib.llama_apply_lora_from_file.restype = c_int32


def llama_model_apply_lora_from_file(
        model: cllm_model_p,
        path_lora: Union[c_char_p, bytes],
        scale: Union[c_float, float],
        path_base_model: Union[c_char_p, bytes],
        n_threads: Union[c_int, int],
) -> int:
    return _lib.llama_model_apply_lora_from_file(
        model, path_lora, scale, path_base_model, n_threads
    )


_lib.llama_model_apply_lora_from_file.argtypes = [
    cllm_model_p,
    c_char_p,
    c_float,
    c_char_p,
    c_int32,
]
_lib.llama_model_apply_lora_from_file.restype = c_int32


class llama_kv_cache_view_cell(Structure):
    _fields_ = [("pos", cllm_pos)]


class llama_kv_cache_view(Structure):
    _fields_ = [
        ("n_cells", c_int32),
        ("n_max_seq", c_int32),
        ("token_count", c_int32),
        ("used_cells", c_int32),
        ("max_contiguous", c_int32),
        ("max_contiguous_idx", c_int32),
        ("cells", POINTER(llama_kv_cache_view_cell)),
        ("cells_sequences", POINTER(cllm_seq_id)),
    ]


llama_kv_cache_view_p = POINTER(llama_kv_cache_view)


def llama_kv_cache_view_init(
        ctx: cllm_context_p, n_max_seq: Union[c_int32, int]
) -> llama_kv_cache_view:
    """Create an empty KV cache view. (use only for debugging purposes)"""
    return _lib.llama_kv_cache_view_init(ctx, n_max_seq)


_lib.llama_kv_cache_view_init.argtypes = [cllm_context_p, c_int32]
_lib.llama_kv_cache_view_init.restype = llama_kv_cache_view


def llama_kv_cache_view_free(view: "ctypes.pointer[llama_kv_cache_view]"):  # type: ignore
    """Free a KV cache view. (use only for debugging purposes)"""
    return _lib.llama_kv_cache_view_free(view)


_lib.llama_kv_cache_view_free.argtypes = [llama_kv_cache_view_p]
_lib.llama_kv_cache_view_free.restype = None


def llama_kv_cache_view_update(ctx: cllm_context_p, view: "ctypes.pointer[llama_kv_cache_view]"):  # type: ignore
    """Update the KV cache view structure with the current state of the KV cache. (use only for debugging purposes)"""
    return _lib.llama_kv_cache_view_update(ctx, view)


_lib.llama_kv_cache_view_update.argtypes = [cllm_context_p, llama_kv_cache_view_p]
_lib.llama_kv_cache_view_update.restype = None


def llama_get_kv_cache_token_count(ctx: cllm_context_p) -> int:
    """Returns the number of tokens in the KV cache (slow, use only for debug)
    If a KV cell has multiple sequences assigned to it, it will be counted multiple times
    """
    return _lib.llama_get_kv_cache_token_count(ctx)


_lib.llama_get_kv_cache_token_count.argtypes = [cllm_context_p]
_lib.llama_get_kv_cache_token_count.restype = c_int32


def llama_get_kv_cache_used_cells(ctx: cllm_context_p) -> int:
    """Returns the number of used KV cells (i.e. have at least one sequence assigned to them)"""
    return _lib.llama_get_kv_cache_used_cells(ctx)


_lib.llama_get_kv_cache_used_cells.argtypes = [cllm_context_p]
_lib.llama_get_kv_cache_used_cells.restype = c_int32


def llama_kv_cache_clear(ctx: cllm_context_p):
    """Clear the KV cache"""
    return _lib.llama_kv_cache_clear(ctx)


_lib.llama_kv_cache_clear.argtypes = [cllm_context_p]
_lib.llama_kv_cache_clear.restype = None


# // Removes all tokens that belong to the specified sequence and have positions in [p0, p1)
# // seq_id < 0 : match any sequence
# // p0 < 0     : [0,  p1]
# // p1 < 0     : [p0, inf)
# LLAMA_API void llama_kv_cache_seq_rm(
#         struct llama_context * ctx,
#                 cllm_seq_id   seq_id,
#                    cllm_pos   p0,
#                    cllm_pos   p1);
def llama_kv_cache_seq_rm(
        ctx: cllm_context_p,
        seq_id: Union[cllm_seq_id, int],
        p0: Union[cllm_pos, int],
        p1: Union[cllm_pos, int],
):
    """Removes all tokens that belong to the specified sequence and have positions in [p0, p1)
    seq_id < 0 : match any sequence
    p0 < 0     : [0,  p1]
    p1 < 0     : [p0, inf)"""
    return _lib.llama_kv_cache_seq_rm(ctx, seq_id, p0, p1)


_lib.llama_kv_cache_seq_rm.argtypes = [
    cllm_context_p,
    cllm_seq_id,
    cllm_pos,
    cllm_pos,
]
_lib.llama_kv_cache_seq_rm.restype = None


def llama_kv_cache_seq_cp(
        ctx: cllm_context_p,
        seq_id_src: Union[cllm_seq_id, int],
        seq_id_dst: Union[cllm_seq_id, int],
        p0: Union[cllm_pos, int],
        p1: Union[cllm_pos, int],
):
    """Copy all tokens that belong to the specified sequence to another sequence
    Note that this does not allocate extra KV cache memory - it simply assigns the tokens to the new sequence
    p0 < 0 : [0,  p1]
    p1 < 0 : [p0, inf)"""
    return _lib.llama_kv_cache_seq_cp(ctx, seq_id_src, seq_id_dst, p0, p1)


_lib.llama_kv_cache_seq_cp.argtypes = [
    cllm_context_p,
    cllm_seq_id,
    cllm_seq_id,
    cllm_pos,
    cllm_pos,
]
_lib.llama_kv_cache_seq_cp.restype = None


def llama_kv_cache_seq_keep(
        ctx: cllm_context_p,
        seq_id: Union[cllm_seq_id, int],
):
    """Removes all tokens that do not belong to the specified sequence"""
    return _lib.llama_kv_cache_seq_keep(ctx, seq_id)


_lib.llama_kv_cache_seq_keep.argtypes = [cllm_context_p, cllm_seq_id]
_lib.llama_kv_cache_seq_keep.restype = None


def llama_kv_cache_seq_shift(
        ctx: cllm_context_p,
        seq_id: Union[cllm_seq_id, int],
        p0: Union[cllm_pos, int],
        p1: Union[cllm_pos, int],
        delta: Union[cllm_pos, int],
):
    """
    Adds relative position "delta" to all tokens that belong to the specified sequence and have positions in [p0, p1)
    If the KV cache is RoPEd, the KV data is updated accordingly
    p0 < 0 : [0,  p1]
    p1 < 0 : [p0, inf]
    """
    return _lib.llama_kv_cache_seq_shift(ctx, seq_id, p0, p1, delta)


_lib.llama_kv_cache_seq_shift.argtypes = [
    cllm_context_p,
    cllm_seq_id,
    cllm_pos,
    cllm_pos,
    cllm_pos,
]
_lib.llama_kv_cache_seq_shift.restype = None


def llama_kv_cache_seq_div(
        ctx: cllm_context_p,
        seq_id: Union[cllm_seq_id, int],
        p0: Union[cllm_pos, int],
        p1: Union[cllm_pos, int],
        d: Union[c_int, int],
):
    """
    Integer division of the positions by factor of `d > 1`
    If the KV cache is RoPEd, the KV data is updated accordingly
    p0 < 0 : [0,  p1]
    p1 < 0 : [p0, inf]
    """
    return _lib.llama_kv_cache_seq_div(ctx, seq_id, p0, p1, d)


_lib.llama_kv_cache_seq_div.argtypes = [
    cllm_context_p,
    cllm_seq_id,
    cllm_pos,
    cllm_pos,
    c_int,
]
_lib.llama_kv_cache_seq_div.restype = None


def llama_get_state_size(ctx: cllm_context_p) -> int:
    """Returns the maximum size in bytes of the state (rng, logits, embedding
    and kv_cache) - will often be smaller after compacting tokens"""
    return _lib.llama_get_state_size(ctx)


_lib.llama_get_state_size.argtypes = [cllm_context_p]
_lib.llama_get_state_size.restype = c_size_t


def llama_copy_state_data(
        ctx: cllm_context_p, dst  # type: Array[c_uint8]
) -> int:
    """
    Copies the state to the specified destination address.
    Destination needs to have allocated enough memory.
    Returns the number of bytes copied
    """
    return _lib.llama_copy_state_data(ctx, dst)


_lib.llama_copy_state_data.argtypes = [cllm_context_p, c_uint8_p]
_lib.llama_copy_state_data.restype = c_size_t


def llama_set_state_data(
        ctx: cllm_context_p, src  # type: Array[c_uint8]
) -> int:
    """Set the state reading from the specified address"""
    return _lib.llama_set_state_data(ctx, src)


_lib.llama_set_state_data.argtypes = [cllm_context_p, c_uint8_p]
_lib.llama_set_state_data.restype = c_size_t


def llama_load_session_file(
        ctx: cllm_context_p,
        path_session: bytes,
        tokens_out,  # type: Array[cllm_token]
        n_token_capacity: Union[c_size_t, int],
        n_token_count_out,  # type: _Pointer[c_size_t]
) -> int:
    return _lib.llama_load_session_file(
        ctx, path_session, tokens_out, n_token_capacity, n_token_count_out
    )


_lib.llama_load_session_file.argtypes = [
    cllm_context_p,
    c_char_p,
    cllm_token_p,
    c_size_t,
    c_size_t_p,
]
_lib.llama_load_session_file.restype = c_size_t


def llama_save_session_file(
        ctx: cllm_context_p,
        path_session: bytes,
        tokens,  # type: Array[cllm_token]
        n_token_count: Union[c_size_t, int],
) -> int:
    return _lib.llama_save_session_file(ctx, path_session, tokens, n_token_count)


_lib.llama_save_session_file.argtypes = [
    cllm_context_p,
    c_char_p,
    cllm_token_p,
    c_size_t,
]
_lib.llama_save_session_file.restype = c_size_t


def llama_eval(
        ctx: cllm_context_p,
        tokens,  # type: Array[cllm_token]
        n_tokens: Union[c_int, int],
        n_past: Union[c_int, int],
) -> int:
    """
    Run the llama inference to obtain the logits and probabilities for the next token(s).
    tokens + n_tokens is the provided batch of new tokens to process
    n_past is the number of tokens to use from previous eval calls
    Returns 0 on success
    DEPRECATED: use cllm_decode() instead
    """
    return _lib.llama_eval(ctx, tokens, n_tokens, n_past)


_lib.llama_eval.argtypes = [cllm_context_p, cllm_token_p, c_int32, c_int32]
_lib.llama_eval.restype = c_int


def llama_eval_embd(
        ctx: cllm_context_p,
        embd,  # type: Array[c_float]
        n_tokens: Union[c_int, int],
        n_past: Union[c_int, int],
) -> int:
    """
    Same as llama_eval, but use float matrix input directly.
    DEPRECATED: use cllm_decode() instead
    """
    return _lib.llama_eval_embd(ctx, embd, n_tokens, n_past)


_lib.llama_eval_embd.argtypes = [cllm_context_p, c_float_p, c_int32, c_int32]
_lib.llama_eval_embd.restype = c_int


def cllm_batch_get_one(
        tokens,  # type: Array[cllm_token]
        n_tokens: Union[c_int, int],
        pos_0: Union[cllm_pos, int],
        seq_id: cllm_seq_id,
) -> CLLMBatch:
    """
    Return batch for single sequence of tokens starting at pos_0

    NOTE: this is a helper function to facilitate transition to the new batch API - avoid using it
    """
    return _lib.llama_batch_get_one(tokens, n_tokens, pos_0, seq_id)


_lib.llama_batch_get_one.argtypes = [
    cllm_token_p,
    c_int,
    cllm_pos,
    cllm_seq_id,
]
_lib.llama_batch_get_one.restype = CLLMBatch


def cllm_batch_init(
        n_tokens: Union[c_int32, int],
        embd: Union[c_int32, int],
        n_seq_max: Union[c_int32, int],
) -> CLLMBatch:
    """
    Allocates a batch of tokens on the heap that can hold a maximum of n_tokens
    Each token can be assigned up to n_seq_max sequence ids
    The batch has to be freed with cllm_batch_free()
    If embd != 0, CLLMBatch.embd will be allocated with size of n_tokens * embd * sizeof(float)
    Otherwise, CLLMBatch. Token will be allocated to store n_tokens cllm_token
    The rest of the CLLMBatch members are allocated with size n_tokens
    All members are left uninitialized
    """
    return _lib.llama_batch_init(n_tokens, embd, n_seq_max)


_lib.llama_batch_init.argtypes = [c_int32, c_int32, c_int32]
_lib.llama_batch_init.restype = CLLMBatch


def cllm_batch_free(batch: CLLMBatch):
    """Frees a batch of tokens allocated with cllm_batch_init()"""
    return _lib.llama_batch_free(batch)


_lib.llama_batch_free.argtypes = [CLLMBatch]
_lib.llama_batch_free.restype = None


def cllm_decode(ctx: cllm_context_p, batch: CLLMBatch) -> int:
    """Positive return values does not mean a fatal error, but rather a warning.
    0 - success
    1 - could not find a KV slot for the batch (try reducing the size of the batch or increase the context)
    < 0 - error"""
    return _lib.llama_decode(ctx, batch)


_lib.llama_decode.argtypes = [cllm_context_p, CLLMBatch]
_lib.llama_decode.restype = c_int32


def llama_set_n_threads(
        ctx: cllm_context_p,
        n_threads: Union[c_uint32, int],
        n_threads_batch: Union[c_uint32, int],
):
    """
    Set the number of threads used for decoding
    n_threads is the number of threads used for generation (single token)
    n_threads_batch is the number of threads used for prompt and batch processing (multiple tokens)
    """
    return _lib.llama_set_n_threads(ctx, n_threads, n_threads_batch)


_lib.llama_set_n_threads.argtypes = [cllm_context_p, c_uint32, c_uint32]
_lib.llama_set_n_threads.restype = None


def llama_get_logits(
        ctx: cllm_context_p,
):
    """
    Token logits obtained from the last call to llama_eval()
    The logits for the last token are stored in the last row
    Logits for which CLLMBatch.logits[i] == 0 are undefined
    Rows: n_tokens provided with CLLMBatch
    Cols: n_vocab
    """
    return _lib.llama_get_logits(ctx)


_lib.llama_get_logits.argtypes = [cllm_context_p]
_lib.llama_get_logits.restype = c_float_p


def llama_get_logits_ith(
        ctx: cllm_context_p, i: Union[c_int32, int]
):
    """
    Logits for the ith token. Equivalent to:
    llama_get_logits(ctx) + i*n_vocab
    """
    return _lib.llama_get_logits_ith(ctx, i)


_lib.llama_get_logits_ith.argtypes = [cllm_context_p, c_int32]
_lib.llama_get_logits_ith.restype = c_float_p


def llama_get_embeddings(
        ctx: cllm_context_p,
):
    """
    Get the embeddings for the input
    shape: [n_embd] (1-dimensional)
    """
    return _lib.llama_get_embeddings(ctx)


_lib.llama_get_embeddings.argtypes = [cllm_context_p]
_lib.llama_get_embeddings.restype = c_float_p


def llama_token_get_text(model: cllm_model_p, token: Union[cllm_token, int]) -> bytes:
    return _lib.llama_token_get_text(model, token)


_lib.llama_token_get_text.argtypes = [cllm_model_p, cllm_token]
_lib.llama_token_get_text.restype = c_char_p


def llama_token_get_score(
        model: cllm_model_p, token: Union[cllm_token, int]
) -> float:
    return _lib.llama_token_get_score(model, token)


_lib.llama_token_get_score.argtypes = [cllm_model_p, cllm_token]
_lib.llama_token_get_score.restype = c_float


def llama_token_get_type(model: cllm_model_p, token: Union[cllm_token, int]) -> int:
    return _lib.llama_token_get_type(model, token)


_lib.llama_token_get_type.argtypes = [cllm_model_p, cllm_token]
_lib.llama_token_get_type.restype = ctypes.c_int


def llama_token_bos(model: cllm_model_p) -> int:
    """beginning-of-sentence"""
    return _lib.llama_token_bos(model)


_lib.llama_token_bos.argtypes = [cllm_model_p]
_lib.llama_token_bos.restype = cllm_token


def llama_token_eos(model: cllm_model_p) -> int:
    """end-of-sentence"""
    return _lib.llama_token_eos(model)


_lib.llama_token_eos.argtypes = [cllm_model_p]
_lib.llama_token_eos.restype = cllm_token


# LLAMA_API cllm_token llama_token_nl (const struct llama_model * model); // next-line
def llama_token_nl(model: cllm_model_p) -> int:
    """next-line"""
    return _lib.llama_token_nl(model)


_lib.llama_token_nl.argtypes = [cllm_model_p]
_lib.llama_token_nl.restype = cllm_token


def llama_add_bos_token(model: cllm_model_p) -> int:
    """Returns -1 if unknown, 1 for true or 0 for false."""
    return _lib.llama_add_bos_token(model)


_lib.llama_add_bos_token.argtypes = [cllm_model_p]
_lib.llama_add_bos_token.restype = c_int32


def llama_add_eos_token(model: cllm_model_p) -> int:
    """Returns -1 if unknown, 1 for true or 0 for false."""
    return _lib.llama_add_eos_token(model)


_lib.llama_add_eos_token.argtypes = [cllm_model_p]
_lib.llama_add_eos_token.restype = c_int32


def llama_token_prefix(model: cllm_model_p) -> int:
    """codellama infill tokens"""
    return _lib.llama_token_prefix(model)


_lib.llama_token_prefix.argtypes = [cllm_model_p]
_lib.llama_token_prefix.restype = cllm_token


def llama_token_middle(model: cllm_model_p) -> int:
    return _lib.llama_token_middle(model)


_lib.llama_token_middle.argtypes = [cllm_model_p]
_lib.llama_token_middle.restype = cllm_token


def llama_token_suffix(model: cllm_model_p) -> int:
    return _lib.llama_token_suffix(model)


_lib.llama_token_suffix.argtypes = [cllm_model_p]
_lib.llama_token_suffix.restype = cllm_token


def llama_token_eot(model: cllm_model_p) -> int:
    return _lib.llama_token_eot(model)


_lib.llama_token_eot.argtypes = [cllm_model_p]
_lib.llama_token_eot.restype = cllm_token


def llama_tokenize(
        model: cllm_model_p,
        text: bytes,
        text_len: Union[c_int, int],
        tokens,  # type: Array[cllm_token]
        n_max_tokens: Union[c_int, int],
        add_bos: Union[c_bool, bool],
        special: Union[c_bool, bool],
) -> int:
    """Convert the provided text into tokens."""
    return _lib.llama_tokenize(
        model, text, text_len, tokens, n_max_tokens, add_bos, special
    )


_lib.llama_tokenize.argtypes = [
    cllm_model_p,
    c_char_p,
    c_int32,
    cllm_token_p,
    c_int32,
    c_bool,
    c_bool,
]
_lib.llama_tokenize.restype = c_int32


def llama_token_to_piece(
        model: cllm_model_p,
        token: Union[cllm_token, int],
        buf: Union[c_char_p, bytes],
        length: Union[c_int, int],
) -> int:
    """
    Token ID -> Piece.
    Uses the vocabulary in the provided context.
    Does not write null terminator to the buffer.
    User code is responsible to remove the leading whitespace of the first non-BOS token when decoding multiple tokens.
    """
    return _lib.llama_token_to_piece(model, token, buf, length)


_lib.llama_token_to_piece.argtypes = [cllm_model_p, cllm_token, c_char_p, c_int32]
_lib.llama_token_to_piece.restype = c_int32


def llama_grammar_init(
        rules,  # type: Array[llama_grammar_element_p] # type: ignore
        n_rules: Union[c_size_t, int],
        start_rule_index: Union[c_size_t, int],
) -> llama_grammar_p:
    """Initialize a grammar from a set of rules."""
    return _lib.llama_grammar_init(rules, n_rules, start_rule_index)


_lib.llama_grammar_init.argtypes = [
    POINTER(llama_grammar_element_p),
    c_size_t,
    c_size_t,
]
_lib.llama_grammar_init.restype = llama_grammar_p


# LLAMA_API void llama_grammar_free(struct llama_grammar * grammar);
def llama_grammar_free(grammar: llama_grammar_p):
    """Free a grammar."""
    return _lib.llama_grammar_free(grammar)


_lib.llama_grammar_free.argtypes = [llama_grammar_p]
_lib.llama_grammar_free.restype = None


# LLAMA_API struct llama_grammar * llama_grammar_copy(const struct llama_grammar * grammar);
def llama_grammar_copy(grammar: llama_grammar_p) -> llama_grammar_p:
    """Copy a grammar."""
    return _lib.llama_grammar_copy(grammar)


_lib.llama_grammar_copy.argtypes = [llama_grammar_p]
_lib.llama_grammar_copy.restype = llama_grammar_p


def llama_set_rng_seed(ctx: cllm_context_p, seed: Union[c_uint32, int]):
    """Sets the current rng seed."""
    return _lib.llama_set_rng_seed(ctx, seed)


_lib.llama_set_rng_seed.argtypes = [cllm_context_p, c_uint32]
_lib.llama_set_rng_seed.restype = None


def llama_sample_repetition_penalties(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        last_tokens_data,  # type: Array[cllm_token]
        penalty_last_n: Union[c_size_t, int],
        penalty_repeat: Union[c_float, float],
        penalty_freq: Union[c_float, float],
        penalty_present: Union[c_float, float],
):
    """
    Repetition penalty described in CTRL academic paper https://arxiv.org/abs/1909.05858, with negative logit fix.
    Frequency and presence penalties described in OpenAI API https://platform.openai.com/docs/api-reference/parameter-details.
    """
    return _lib.llama_sample_repetition_penalties(
        ctx,
        candidates,
        last_tokens_data,
        penalty_last_n,
        penalty_repeat,
        penalty_freq,
        penalty_present,
    )


_lib.llama_sample_repetition_penalties.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    cllm_token_p,
    c_size_t,
    c_float,
    c_float,
    c_float,
]
_lib.llama_sample_repetition_penalties.restype = None


def llama_sample_classifier_free_guidance(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        guidance_ctx: cllm_context_p,
        scale: Union[c_float, float],
):
    """
    Apply classifier-free guidance to the logits as described in academic paper "Stay on topic
     with Classifier-Free Guidance" https://arxiv.org/abs/2306.17806
     """
    return _lib.llama_sample_classifier_free_guidance(
        ctx, candidates, guidance_ctx, scale
    )


_lib.llama_sample_classifier_free_guidance.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    cllm_context_p,
    c_float,
]
_lib.llama_sample_classifier_free_guidance.restype = None


def llama_sample_softmax(
        ctx: cllm_context_p, candidates  # type: _Pointer[CLLMTokenData]
):
    """Sorts candidate tokens by their logits in descending order and calculate probabilities based on logits."""
    return _lib.llama_sample_softmax(ctx, candidates)


_lib.llama_sample_softmax.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
]
_lib.llama_sample_softmax.restype = None


def llama_sample_top_k(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        k: Union[c_int, int],
        min_keep: Union[c_size_t, int],
):
    """
    Top-K sampling described in academic paper "The Curious Case of Neural
    Text Degeneration" https://arxiv.org/abs/1904.09751
    """
    return _lib.llama_sample_top_k(ctx, candidates, k, min_keep)


_lib.llama_sample_top_k.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    c_int32,
    c_size_t,
]
_lib.llama_sample_top_k.restype = None


def llama_sample_top_p(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        p: Union[c_float, float],
        min_keep: Union[c_size_t, int],
):
    """
    Nucleus sampling described in academic paper "The Curious Case of
    Neural Text Degeneration" https://arxiv.org/abs/1904.09751
    """
    return _lib.llama_sample_top_p(ctx, candidates, p, min_keep)


_lib.llama_sample_top_p.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    c_float,
    c_size_t,
]
_lib.llama_sample_top_p.restype = None


def llama_sample_min_p(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        p: Union[c_float, float],
        min_keep: Union[c_size_t, int],
):
    """Minimum P sampling as described in https://github.com/ggerganov/llama.cpp/pull/3841"""
    return _lib.llama_sample_min_p(ctx, candidates, p, min_keep)


_lib.llama_sample_min_p.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    c_float,
    c_size_t,
]
_lib.llama_sample_min_p.restype = None


def llama_sample_tail_free(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        z: Union[c_float, float],
        min_keep: Union[c_size_t, int],
):
    """Tail Free Sampling described in https://www.trentonbricken.com/Tail-Free-Sampling/."""
    return _lib.llama_sample_tail_free(ctx, candidates, z, min_keep)


_lib.llama_sample_tail_free.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    c_float,
    c_size_t,
]
_lib.llama_sample_tail_free.restype = None


def llama_sample_typical(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        p: Union[c_float, float],
        min_keep: Union[c_size_t, int],
):
    """Locally Typical Sampling implementation described in the paper https://arxiv.org/abs/2202.00666."""
    return _lib.llama_sample_typical(ctx, candidates, p, min_keep)


_lib.llama_sample_typical.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    c_float,
    c_size_t,
]
_lib.llama_sample_typical.restype = None


def llama_sample_temp(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        temp: Union[c_float, float],
):
    return _lib.llama_sample_temp(ctx, candidates, temp)


_lib.llama_sample_temp.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    c_float,
]
_lib.llama_sample_temp.restype = None


def llama_sample_temperature(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        temp: Union[c_float, float],
):
    """use llama_sample_temp instead"""
    return _lib.llama_sample_temperature(ctx, candidates, temp)


_lib.llama_sample_temperature.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    c_float,
]
_lib.llama_sample_temperature.restype = None


def llama_sample_grammar(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        grammar,  # type: llama_grammar_p
):
    """
    Apply constraints from grammar

    :param candidates: A vector of `CLLMTokenData` containing the candidate tokens, their probabilities (p), and log-odds (logit) for the current position in the generated text.
    :param grammar: A grammar object containing the rules and constraints to apply to the generated text.
    """
    return _lib.llama_sample_grammar(ctx, candidates, grammar)


_lib.llama_sample_grammar.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    llama_grammar_p,
]
_lib.llama_sample_grammar.restype = None


def llama_sample_token_mirostat(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        tau: Union[c_float, float],
        eta: Union[c_float, float],
        m: Union[c_int, int],
        mu,  # type: _Pointer[c_float]
) -> int:
    """
    Mirostat 1.0 algorithm described in the paper https://arxiv.org/abs/2007.14966. Uses tokens instead of words.


    :param candidates: A vector of `CLLMTokenData` containing the candidate tokens, their probabilities (p), and log-odds
         (logit) for the current position in the generated text.
    :param tau: The target cross-entropy (or surprise) value you want to achieve for the generated text. A higher value
        corresponds to more surprising or less predictable text, while a lower value corresponds to less surprising
        or more predictable text.
    :param eta: The learning rate used to update `mu` based on the error between the target and observed surprisal of the
         sampled word. A larger learning rate will cause `mu` to be updated more quickly, while a smaller learning rate
         will result in slower updates.
    :param m: The number of tokens considered in the estimation of `s_hat`. This is an arbitrary value that is used to
        calculate `s_hat`, which in turn helps to calculate the value of `k`. In the paper, they use `m = 100`, but
         you can experiment with different values to see how it affects the performance of the algorithm.
    :param mu: Maximum cross-entropy. This value is initialized to be twice the target cross-entropy (`2 * tau`) and
         is updated in the algorithm based on the error between the target and observed surprisal.
    """
    return _lib.llama_sample_token_mirostat(ctx, candidates, tau, eta, m, mu)


_lib.llama_sample_token_mirostat.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    c_float,
    c_float,
    c_int32,
    c_float_p,
]
_lib.llama_sample_token_mirostat.restype = cllm_token


def llama_sample_token_mirostat_v2(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
        tau: Union[c_float, float],
        eta: Union[c_float, float],
        mu,  # type: _Pointer[c_float]
) -> int:
    """
    Mirostat 2.0 algorithm described in the paper https://arxiv.org/abs/2007.14966. Uses tokens instead of words.


    :param candidates: A vector of `CLLMTokenData` containing the candidate tokens, their probabilities (p), and
    log-odds (logit) for the current position in the generated text.
    :param tau: The target cross-entropy (or surprise) value you want to achieve for the generated text. A higher
     value corresponds to more surprising or less predictable text, while a lower value corresponds to less
      surprising or more predictable text.
    :param eta: The learning rate used to update `mu` based on the error between the target and observed surprisal
    of the sampled word. A larger learning rate will cause `mu` to be updated more quickly, while a smaller learning
    rate will result in slower updates.
    :param mu: Maximum cross-entropy. This value is initialized to be twice the target cross-entropy (`2 * tau`) and
    is updated in the algorithm based on the error between the target and observed surprisal.
    """
    return _lib.llama_sample_token_mirostat_v2(ctx, candidates, tau, eta, mu)


_lib.llama_sample_token_mirostat_v2.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
    c_float,
    c_float,
    c_float_p,
]
_lib.llama_sample_token_mirostat_v2.restype = cllm_token


def llama_sample_token_greedy(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
) -> int:
    """Selects the token with the highest probability."""
    return _lib.llama_sample_token_greedy(ctx, candidates)


_lib.llama_sample_token_greedy.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
]
_lib.llama_sample_token_greedy.restype = cllm_token


def llama_sample_token(
        ctx: cllm_context_p,
        candidates,  # type: _Pointer[CLLMTokenDataArray]
) -> int:
    """Randomly selects a token from the candidates based on their probabilities."""
    return _lib.llama_sample_token(ctx, candidates)


_lib.llama_sample_token.argtypes = [
    cllm_context_p,
    CLLMTokenDataArray_p,
]
_lib.llama_sample_token.restype = cllm_token


def llama_grammar_accept_token(
        ctx: cllm_context_p,
        grammar: llama_grammar_p,
        token: Union[cllm_token, int],
) -> None:
    """Accepts the sampled token into the grammar"""
    _lib.llama_grammar_accept_token(ctx, grammar, token)


_lib.llama_grammar_accept_token.argtypes = [
    cllm_context_p,
    llama_grammar_p,
    cllm_token,
]
_lib.llama_grammar_accept_token.restype = None


class llama_beam_view(ctypes.Structure):
    _fields_ = [
        ("tokens", cllm_token_p),
        ("n_tokens", c_size_t),
        ("p", c_float),
        ("eob", c_bool),
    ]


class llama_beams_state(ctypes.Structure):
    _fields_ = [
        ("beam_views", POINTER(llama_beam_view)),
        ("n_beams", c_size_t),
        ("common_prefix_length", c_size_t),
        ("last_call", c_bool),
    ]


llama_beam_search_callback_fn_t = ctypes.CFUNCTYPE(None, c_void_p, llama_beams_state)


def llama_beam_search(
        ctx: cllm_context_p,
        callback: "ctypes._CFuncPtr[None, c_void_p, llama_beams_state]",  # type: ignore
        callback_data: c_void_p,
        n_beams: Union[c_size_t, int],
        n_past: Union[c_int, int],
        n_predict: Union[c_int, int],
):
    return _lib.llama_beam_search(
        ctx, callback, callback_data, n_beams, n_past, n_predict
    )


_lib.llama_beam_search.argtypes = [
    cllm_context_p,
    llama_beam_search_callback_fn_t,
    c_void_p,
    c_size_t,
    c_int32,
    c_int32,
]
_lib.llama_beam_search.restype = None


def llama_get_timings(ctx: cllm_context_p) -> llama_timings:
    """Get performance information"""
    return _lib.llama_get_timings(ctx)


_lib.llama_get_timings.argtypes = [cllm_context_p]
_lib.llama_get_timings.restype = llama_timings


def llama_print_timings(ctx: cllm_context_p):
    """Print performance information"""
    _lib.llama_print_timings(ctx)


_lib.llama_print_timings.argtypes = [cllm_context_p]
_lib.llama_print_timings.restype = None


def llama_reset_timings(ctx: cllm_context_p):
    """Reset performance information"""
    _lib.llama_reset_timings(ctx)


_lib.llama_reset_timings.argtypes = [cllm_context_p]
_lib.llama_reset_timings.restype = None


def llama_print_system_info() -> bytes:
    """
    Print system information
    """
    return _lib.llama_print_system_info()


_lib.llama_print_system_info.argtypes = []
_lib.llama_print_system_info.restype = c_char_p


def llama_log_set(
        log_callback: "ctypes._FuncPointer", user_data: c_void_p  # type: ignore
):
    """
    Set callback for all future logging events.

    If this is not called, or NULL is supplied, everything is output on stderr."""
    return _lib.llama_log_set(log_callback, user_data)


_lib.llama_log_set.argtypes = [llama_log_callback, c_void_p]
_lib.llama_log_set.restype = None


def llama_dump_timing_info_yaml(stream: ctypes.c_void_p, ctx: cllm_context_p):
    return _lib.llama_dump_timing_info_yaml(stream, ctx)


_lib.llama_dump_timing_info_yaml.argtypes = [ctypes.c_void_p, cllm_context_p]
_lib.llama_dump_timing_info_yaml.restype = None
