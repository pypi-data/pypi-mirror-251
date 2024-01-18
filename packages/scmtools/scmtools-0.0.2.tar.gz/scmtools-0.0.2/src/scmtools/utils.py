from copy import deepcopy
from itertools import cycle
from typing import Any, Callable, Dict, List, Optional, Union, AnyStr, Tuple

import numpy as np
import pandas as pd
from dowhy import gcm
import networkx as nx
from scipy import stats
import graphviz as gviz
from sklearn import base
from tqdm.auto import tqdm
import matplotlib.pyplot as plt


def make_graph(adjacency_matrix, labels=None):
    '''Function adapted from https://github.com/py-why/dowhy/blob/main/docs/source/example_notebooks/dowhy_causal_discovery_example.ipynb'''
    idx = np.abs(adjacency_matrix) > 0.01
    dirs = np.where(idx)
    d = gviz.Digraph(engine='dot')
    names = labels if labels else [f'x{i}' for i in range(len(adjacency_matrix))]
    for name in names:
        d.node(name)
    for to, from_, coef in zip(dirs[0], dirs[1], adjacency_matrix[idx]):
        d.edge(names[from_], names[to])
    return d


def str_to_dot(string):
    '''
    Converts input string from graphviz library to valid DOT graph format.
    Function from https://github.com/py-why/dowhy/blob/main/docs/source/example_notebooks/dowhy_causal_discovery_example.ipynb
    '''
    graph = string.strip().replace('\n', ';').replace('\t','')
    # remove unnecessary characters from string
    graph = graph[:9] + graph[10:-2] + graph[-1]
    return graph


def get_dot_graph(graph: nx.DiGraph):
    """Convert an nx.DiGraph to a DOT graph with easy-to-read nodes."""
    labels = [f'{col}' for i, col in enumerate(graph.nodes)]
    adj_matrix = nx.to_numpy_matrix(graph)
    adj_matrix = np.asarray(adj_matrix).T
    graph_dot = make_graph(adj_matrix, labels)
    return graph_dot


def clone_causal_models_deepcopy(source, destination):
    '''Create a deepcopy of causal mechanisms while cloning.
    TODO: add detailed docstring.
    '''
    for node in destination.nodes:
        if gcm.graph.CAUSAL_MECHANISM in source.nodes[node]:
            destination.nodes[node][gcm.graph.CAUSAL_MECHANISM] = deepcopy(source.nodes[node][gcm.graph.CAUSAL_MECHANISM])


def copy_causal_model_with_frozen_mechanisms(
        causal_model: gcm.InvertibleStructuralCausalModel,
        freeze_mechanisms_of: List[AnyStr]
    ) -> gcm.InvertibleStructuralCausalModel:
    """Make a copy of causal_model where the mechanisms for every node in freeze_mechanisms_of are
    frozen, i.e., each node in freeze_mechanisms_of becomes a root node with no parents and a
    gcm.EmpiricalDistribution() mechanism.

    NOTE: it is assumed that the output of each node in freeze_mechanisms_of does not matter,
    and the node will be under intervention {node: lambda x: x}, passing through observed data
    as-is while ignoring the values of all parents

    Args:
        causal_model (gcm.InvertibleStructuralCausalModel): the causal model to modify
        freeze_mechanisms_of (List[AnyStr]): list of nodes whose mechanisms should be frozen

    Returns:
        gcm.InvertibleStructuralCausalModel: a replica of causal_model with requested nodes frozen
    """
    # function adapted from: https://github.com/py-why/dowhy/issues/548
    # create copy of original causal graph
    causal_graph_with_frozen_nodes = nx.DiGraph(causal_model.graph)
    # gcm.graph.clone_causal_models(source=causal_model.graph, destination=causal_graph_with_frozen_nodes)
    clone_causal_models_deepcopy(source=causal_model.graph, destination=causal_graph_with_frozen_nodes)

    # freeze the mechanisms for every node in freeze_mechanisms_of
    for node in freeze_mechanisms_of:
        # remove incoming edges from all parents
        parents = causal_model.graph.predecessors(node)
        edges_to_remove = [(parent, node) for parent in parents]
        causal_graph_with_frozen_nodes.remove_edges_from(edges_to_remove)

        # node is now a root node which requires a root mechanism like gcm.EmpiricalDistribution()
        # NOTE: the output of this node will not matter -- assuming that this node will be under the
        # intervention {node: lambda x: x} and pass through observed data as-is
        causal_graph_with_frozen_nodes.nodes[node][gcm.graph.CAUSAL_MECHANISM] = gcm.EmpiricalDistribution()

    # initialize causal model with frozen mechanisms
    causal_model_frozen = gcm.InvertibleStructuralCausalModel(causal_graph_with_frozen_nodes)

    # tell dowhy.gcm that model is already fit by setting each node's PARENTS_DURING_FIT attribute
    for node in causal_model_frozen.graph.nodes:
        causal_model_frozen.graph.nodes[node][gcm.graph.PARENTS_DURING_FIT] = gcm.graph.get_ordered_predecessors(causal_graph=causal_model_frozen.graph, node=node)

    return causal_model_frozen
