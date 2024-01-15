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
    c_size_t,
    c_float,
    c_double,
    c_void_p,
    POINTER,
    _Pointer,  # type: ignore
    Structure,
    Array,
)
import pathlib
from typing import List, Union

import cLLM.cllm_cpp as cllm_cpp


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

    if "LLAVA_CPP_LIB" in os.environ:
        lib_base_name = os.environ["LLAVA_CPP_LIB"]
        _lib = pathlib.Path(lib_base_name)
        _base_path = _lib.parent.resolve()
        _lib_paths = [_lib.resolve()]

    cdll_args = dict()
    if sys.platform == "win32" and sys.version_info >= (3, 8):
        os.add_dll_directory(str(_base_path))
        if "CUDA_PATH" in os.environ:
            os.add_dll_directory(os.path.join(os.environ["CUDA_PATH"], "bin"))
            os.add_dll_directory(os.path.join(os.environ["CUDA_PATH"], "lib"))
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


_libllava_base_name = "llava"

# Load the library
_libllava = _load_shared_library(_libllava_base_name)

clip_ctx_p = c_void_p


class llava_image_embed(Structure):
    _fields_ = [
        ("embed", POINTER(c_float)),
        ("n_image_pos", c_int),
    ]


def llava_validate_embed_size(ctx_cllm: cllm_cpp.cllm_context_p, ctx_clip: clip_ctx_p) -> bool:
    return _libllava.llava_validate_embed_size(ctx_cllm, ctx_clip)


_libllava.llava_validate_embed_size.argtypes = [cllm_cpp.cllm_context_p, clip_ctx_p]
_libllava.llava_validate_embed_size.restype = c_bool


def llava_image_embed_make_with_bytes(ctx_clip: clip_ctx_p, n_threads: Union[c_int, int], image_bytes: bytes,
                                      image_bytes_length: Union[c_int, int]) -> "_Pointer[llava_image_embed]":
    return _libllava.llava_image_embed_make_with_bytes(ctx_clip, n_threads, image_bytes, image_bytes_length)


_libllava.llava_image_embed_make_with_bytes.argtypes = [clip_ctx_p, c_int, POINTER(c_uint8), c_int]
_libllava.llava_image_embed_make_with_bytes.restype = POINTER(llava_image_embed)


def llava_image_embed_make_with_filename(ctx_clip: clip_ctx_p, n_threads: Union[c_int, int],
                                         image_path: bytes) -> "_Pointer[llava_image_embed]":
    return _libllava.llava_image_embed_make_with_filename(ctx_clip, n_threads, image_path)


_libllava.llava_image_embed_make_with_filename.argtypes = [clip_ctx_p, c_int, c_char_p]
_libllava.llava_image_embed_make_with_filename.restype = POINTER(llava_image_embed)


def llava_image_embed_free(embed: "_Pointer[llava_image_embed]"):
    return _libllava.llava_image_embed_free(embed)


_libllava.llava_image_embed_free.argtypes = [POINTER(llava_image_embed)]
_libllava.llava_image_embed_free.restype = None


def llava_eval_image_embed(
        ctx_cllm: cllm_cpp.cllm_context_p,
        embed: "_Pointer[llava_image_embed]",
        n_batch: Union[c_int, int],
        n_past: "_Pointer[c_int]"
) -> bool:
    return _libllava.llava_eval_image_embed(ctx_cllm, embed, n_batch, n_past)


_libllava.llava_eval_image_embed.argtypes = [
    cllm_cpp.cllm_context_p,
    POINTER(llava_image_embed),
    c_int,
    POINTER(c_int)
]

_libllava.llava_eval_image_embed.restype = c_bool


class ClipVisionHparams(Structure):
    _fields_ = [
        ("image_size", c_int32),
        ("patch_size", c_int32),
        ("hidden_size", c_int32),
        ("n_intermediate", c_int32),
        ("projection_dim", c_int32),
        ("n_head", c_int32),
        ("n_layer", c_int32),
        ("eps", c_float),
    ]


def clip_model_load(fname: bytes, verbosity: Union[c_int, int]) -> clip_ctx_p:
    return _libllava.clip_model_load(fname, verbosity)


_libllava.clip_model_load.argtypes = [c_char_p, c_int]
_libllava.clip_model_load.restype = clip_ctx_p


def clip_free(ctx: clip_ctx_p):
    return _libllava.clip_free(ctx)


_libllava.clip_free.argtypes = [clip_ctx_p]
_libllava.clip_free.restype = None
