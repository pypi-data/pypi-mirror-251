import logging
import warnings
from typing import Any, Callable, Optional, Union

import torch

import torch_geometric.typing

JIT_WARNING = ("Could not convert the 'model' into a jittable version. "
               "As such, 'torch.compile' may currently fail to correctly "
               "optimize your model. 'MessagePassing.jittable()' reported "
               "the following error: {error}")


def is_compiling() -> bool:
    r"""Returns :obj:`True` in case :pytorch:`PyTorch` is compiling via
    :meth:`torch.compile`.
    """
    if torch_geometric.typing.WITH_PT21:
        return torch._dynamo.is_compiling()
    return False  # pragma: no cover


def to_jittable(model: torch.nn.Module) -> torch.nn.Module:
    if isinstance(model, torch_geometric.nn.MessagePassing):
        try:
            model = model.jittable()
        except Exception as e:
            warnings.warn(JIT_WARNING.format(error=e))

    elif isinstance(model, torch.nn.Module):
        for name, child in model.named_children():
            if isinstance(child, torch_geometric.nn.MessagePassing):
                try:
                    setattr(model, name, child.jittable())
                except Exception as e:
                    warnings.warn(JIT_WARNING.format(error=e))
            else:
                to_jittable(child)

    return model


def compile(
    model: Optional[torch.nn.Module] = None,
    *args: Any,
    **kwargs: Any,
) -> Union[torch.nn.Module, Callable[[torch.nn.Module], torch.nn.Module]]:
    r"""Optimizes the given :pyg:`PyG` model/function via
    :meth:`torch.compile`.

    This function has the same signature as :meth:`torch.compile` (see
    `here <https://pytorch.org/docs/stable/generated/torch.compile.html>`__),
    but it applies further optimization to make :pyg:`PyG` models/functions
    more compiler-friendly.

    Specifically, it

    1. converts all instances of
       :class:`~torch_geometric.nn.conv.MessagePassing` modules into their
       jittable instances
       (see :meth:`torch_geometric.nn.conv.MessagePassing.jittable`)

    2. disables generation of device asserts during fused gather/scatter calls
       to avoid performance impacts

    .. note::
        Without these adjustments, :meth:`torch.compile` may currently fail to
        correctly optimize your :pyg:`PyG` model.
        We are working on fully relying on :meth:`torch.compile` for future
        releases.
    """
    if model is None:

        def fn(model: torch.nn.Module) -> torch.nn.Module:
            if model is None:
                raise RuntimeError("'model' cannot be 'None'")
            out = compile(model, *args, **kwargs)
            assert not callable(out)
            return out

        return fn

    # Adjust the logging level of `torch.compile`:
    # TODO (matthias) Disable only temporarily
    prev_log_level = {
        'torch._dynamo': logging.getLogger('torch._dynamo').level,
        'torch._inductor': logging.getLogger('torch._inductor').level,
    }
    log_level = kwargs.pop('log_level', logging.WARNING)
    for key in prev_log_level.keys():
        logging.getLogger(key).setLevel(log_level)

    # Replace instances of `MessagePassing` by their jittable version:
    model = to_jittable(model)

    # Do not generate device asserts which may slow down model execution:
    config = torch._inductor.config
    if torch_geometric.typing.WITH_PT22:
        config.assert_indirect_indexing = False  # type: ignore
    elif torch_geometric.typing.WITH_PT21:
        config.triton.assert_indirect_indexing = False

    # Finally, run `torch.compile` to create an optimized version:
    out = torch.compile(model, *args, **kwargs)

    return out
