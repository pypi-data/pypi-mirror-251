"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import itertools
from collections import defaultdict

import networkx as nx
import numpy as np
from onnx import TensorProto, numpy_helper
from onnx.helper import (
    make_attribute,
    make_node,
    make_tensor_type_proto,
    make_value_info,
)
from onnx.numpy_helper import from_array, to_array

from onnx2onnx.graph import OnnxGraph

from . import PASSES
from .utils import make_constant


@PASSES.register()
def half_to_float(graph: OnnxGraph) -> OnnxGraph:
    """Convert half consts and values to float32."""

    for node in graph:
        node_pb = graph.nodes[node]["pb"]
        if node_pb.op_type == "Constant":
            tensor = node_pb.attribute[0].t
            if tensor.data_type == TensorProto.FLOAT16:
                array = to_array(tensor).astype("float32")
                attr = make_attribute(key="value", value=from_array(array))
                node_pb.attribute.pop()
                node_pb.attribute.append(attr)
        elif node_pb.op_type == "Cast":
            # if cast target is fp16, change it to fp32
            for attr in node_pb.attribute:
                if attr.name == "to" and attr.i == TensorProto.FLOAT16:
                    attr.i = TensorProto.FLOAT
    for init in graph.initializer:
        if init.data_type == TensorProto.FLOAT16:
            array = to_array(init).astype("float32")
            init.data_type = TensorProto.FLOAT
            init.raw_data = from_array(array).raw_data
    for io in itertools.chain(graph.input, graph.output):
        if io.type.tensor_type.elem_type == TensorProto.FLOAT16:
            io.type.tensor_type.elem_type = TensorProto.FLOAT
    return graph


@PASSES.register()
def float_to_half(graph: OnnxGraph) -> OnnxGraph:
    """Convert float32 consts and values to half."""

    for node in graph:
        node_pb = graph.nodes[node]["pb"]
        if node_pb.op_type == "Constant":
            tensor = node_pb.attribute[0].t
            if tensor.data_type == TensorProto.FLOAT:
                array = to_array(tensor).astype("float16")
                attr = make_attribute(key="value", value=from_array(array))
                node_pb.attribute.pop()
                node_pb.attribute.append(attr)
    for init in graph.initializer:
        if init.data_type == TensorProto.FLOAT:
            array = to_array(init).astype("float16")
            init.data_type = TensorProto.FLOAT16
            init.raw_data = from_array(array).raw_data
    for io in itertools.chain(graph.input, graph.output):
        if io.type.tensor_type.elem_type == TensorProto.FLOAT:
            io.type.tensor_type.elem_type = TensorProto.FLOAT16
    return graph


@PASSES.register()
def initializer_to_constant(graph: OnnxGraph) -> OnnxGraph:
    """Convert initializer value to node Constant."""
    node_to_add = []
    init_names = []
    for init in graph.initializer:
        init_names.append(init.name)
        node_to_add.append(make_constant(init.name, to_array(init)))
        graph._value_info.append(  # pylint: disable=W0212
            make_value_info(
                node_to_add[-1].output[0],
                make_tensor_type_proto(init.data_type, init.dims),
            )
        )
    while graph.initializer:
        graph.initializer.pop()
    for node in graph:
        node_pb = graph.nodes[node]["pb"]
        for i, name in enumerate(node_pb.input):
            if name in init_names:
                node_pb.input[i] = name + "_output_0"
    for node in node_to_add:
        graph.add_onnx_node(node)
    return graph


@PASSES.register()
def yolov5_5d_to_4d(graph: OnnxGraph) -> OnnxGraph:
    """Convert YOLOv5 5D subgraph to equivalent 4D subgraph."""
    node_to_add = []
    node_to_remove = []
    nodes_5d = defaultdict(list)
    for node_id in nx.topological_sort(graph):
        node_pb = graph.nodes[node_id]["pb"]
        if node_pb.op_type == "Constant":
            continue
        input_5d = []
        output_5d = []
        preds = graph.onnx_predecessors(node_pb)
        preds = [i for i in preds if i.op_type != "Constant"]
        for i in node_pb.input:
            if not i:
                continue
            ndim = len(graph.tensor_shape(i))
            if ndim == 5 and any(i in p.output for p in preds):
                input_5d.append(i)
        for i in node_pb.output:
            if len(graph.tensor_shape(i)) == 5:
                output_5d.append(i)
        if input_5d and output_5d:
            # both input and output is 5D
            if not nodes_5d:
                nodes_5d[node_id].append(node_id)
            else:
                new_head = True
                for head in nodes_5d:
                    if nx.has_path(graph, head, node_id):
                        nodes_5d[head].append(node_id)
                        new_head = False
                        break
                if new_head:
                    nodes_5d[node_id].append(node_id)
    # yolo v5 check
    assert len(nodes_5d) == 3  # 3 branches
    for head in nodes_5d:
        head_node = graph.nodes[head]["pb"]
        # insert 4d reshape
        for i, input_name in enumerate(head_node.input):
            shape = graph.tensor_shape(input_name)
            shape[3] *= shape.pop(-1)  # [N, C, D, H, W] -> [N, C, D, H*W]
            shape = make_constant(
                f"{head}/Reshape/Const", np.array(shape, dtype="int64")
            )
            reshape_node = make_node(
                "Reshape",
                [input_name, shape.output[0]],
                [f"{head}/Reshape_Output"],
                name=f"{head}/Reshape",
            )
            head_node.input[i] = f"{head}/Reshape_Output"
            node_to_add.extend([reshape_node, shape])
        for node in nodes_5d[head]:
            node_pb = graph.nodes[node]["pb"]
            if node_pb.op_type == "Transpose":
                for attr in node_pb.attribute:
                    if attr.name == "perm":
                        attr.ints.remove(4)
            elif node_pb.op_type in ("Split", "Concat"):
                for attr in node_pb.attribute:
                    if attr.name == "axis":
                        attr.i = 3
            else:
                for pred in graph.onnx_predecessors(node_pb):
                    # replace 5d constant with 4d
                    if pred.op_type == "Constant":
                        data = numpy_helper.to_array(pred.attribute[0].t)
                        shape = data.shape
                        if data.ndim != 5:
                            continue
                        # [N, C, H, W, D] -> [N, C, -1, D]
                        shape = [*shape[:2], shape[2] * shape[3], shape[4]]
                        new_node = make_constant(f"{pred.name}/4D", data.reshape(shape))
                        for i, j in enumerate(node_pb.input):
                            if j == pred.output[0]:
                                node_pb.input[i] = new_node.output[0]
                        node_to_remove.append(pred)
                        node_to_add.append(new_node)

    for node in node_to_remove:
        graph.remove_onnx_node(node)
    for node in node_to_add:
        graph.add_onnx_node(node)
    return graph


@PASSES.register()
def trans_input_to_constant(graph: OnnxGraph, input_name: str, value: np.ndarray):
    """Consolidate a input to a fixed value as a constant node.

    Args:
        graph (OnnxGraph): _description_
        input_name (str): _description_
        value (np.ndarray):
    """

    if input_name not in graph.inputs:
        raise ValueError(f"{input_name} is not an input of the model")

    node = make_constant(input_name + "/Const", value)
    node.output[0] = input_name
    graph.add_onnx_node(node)
    return graph
