"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import numpy as np
from onnx import AttributeProto, NodeProto, numpy_helper
from onnx.helper import make_node


def make_constant(name: str, value: np.ndarray) -> "NodeProto":
    """Make a Constant node according to given value."""
    node = make_node(
        op_type="Constant",
        name=name,
        inputs=[],
        outputs=[f"{name}_output_0"],
        value=numpy_helper.from_array(value),
    )
    return node


def attribute_value(attr: AttributeProto):
    """Get the value of an onnx attribute."""
    match attr.type:
        case AttributeProto.FLOAT:
            return float(attr.f)
        case AttributeProto.INT:
            return int(attr.i)
        case AttributeProto.STRING:
            return attr.s.decode("utf-8")
        case AttributeProto.TENSOR:
            return numpy_helper.to_array(attr.t)
        case AttributeProto.GRAPH:
            return attr.g
        case AttributeProto.TYPE_PROTO:
            return attr.tp
        case AttributeProto.FLOATS:
            return [float(f) for f in attr.floats]
        case AttributeProto.INTS:
            return [int(i) for i in attr.ints]
        case AttributeProto.STRINGS:
            return [s.decode("utf-8") for s in attr.strings]
        case AttributeProto.TENSORS:
            return [numpy_helper.to_array(t) for t in attr.tensors]
        case AttributeProto.GRAPHS:
            return [g for g in attr.graphs]
        case AttributeProto.TYPE_PROTOS:
            return [tp for tp in attr.type_protos]
    raise ValueError(f"Unsupported attribute type {attr.type}")
