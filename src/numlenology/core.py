from collections import defaultdict

import graphviz as gv
import numpy as np
from num2words import CONVERTER_CLASSES, num2words
from scipy.sparse import csgraph

from numlenology.utils import float_range, rank_keys
from numlenology.utils.color import fade_color


LANGS = sorted(set(lang[:2] for lang in CONVERTER_CLASSES.keys()))

NODE_COLOR_LEAF = "#009000bb"
NODE_COLOR_ROOT = "#000000bb"
NODE_SIZE_MIN = 0.4
NODE_SIZE_MAX = 0.9

"""
# connected components.
cc_num, cc_labels = csgraph.connected_components(m)
if cc_num > 1:
    for label in range(cc_num):
        cc_nodes = np.where(cc_labels == label)[0]
        # cc_nodes.mean()
        # cc_nodes.std()
        # cc_nodes.sum()
        # len(cc_nodes)


node = 10

# with axis=0 we calculate for each node X how many times we jumped from any node to X
# when we built the matrix. then we get the value for this `node`.
degree = m.sum(axis=0)[node]

# get chain until loop.
dfo = csgraph.depth_first_order(m, node, return_predecessors=False)
# node that "closes" the loop, the only child node of `dfo[-1]`.
ncl = m[dfo[-1]].argmax()
# depth is equal to the number of nodes in `dfo` until we reach the end loop.
depth = np.where(dfo == ncl)[0][0]
"""

def recursive_build_chain(lang, matrix, i, visited):
    visited.append(i)
    j = len(num2words(i, lang=lang))
    if j in visited:
        # add the last edge to "close" the loop.
        matrix[i][j] += 1
        return
    else:
        matrix[i][j] += 1
        return recursive_build_chain(lang, matrix, j, visited)


def build_graph_matrix_rec(bound=10, lang="es"):
    bound += 1  # from 0 to `bund` included.
    matrix = np.zeros([bound, bound], dtype=np.int16)
    for i in range(bound):
        recursive_build_chain(lang, matrix, i, [])
    return matrix


def build_graph_matrix(bound=10, lang="es"):
    bound += 1  # from 0 to `bund` included.
    matrix = np.zeros([bound, bound], dtype=np.int16)
    for i in range(bound):
        visited = [i]
        while (j := len(num2words(i, lang=lang))) not in visited:
            matrix[i][j] += 1
            visited.append(j)
            i = j
        # add the last edge to "close" the loop.
        matrix[i][j] += 1
    return matrix


# old methods.

def build_single_chain(n, lang="en"):
    """
    Build a chain with the following relationship:
        `n` in the language `lang` is `x` letters long.
        then `n = x`, and repeat.
        this will eventually go into a loop.

    For example:
        "ten" is 3 letters long.
        "three" is 5 letters long.
        "five" is 4 letters long.
        "four" is 4 letters long.

    The result is a tuple (visited, end_loop) where:
        - `visited` contains all visited numbers (initial `n` included).
        - `end_loop` is the sublist with the last numbers of `visited` that
            are in the final loop.

    So for the example above the result will be:
        build_single_chain(10) == ([10, 3, 5, 4], [4])

    Note that in english the only `end_loop` is [4].
    But in french for example there is a loop of 4 elements:
        "trois" is 5 letters long.
        "cinq" is 4 letters long.
        "quatre" is 6 letters long.
        "six" is 3 letters long.
    """
    visited = []
    while n not in visited:
        visited.append(n)
        w = num2words(n, lang=lang)
        n = len(w)
    end_loop = visited[visited.index(n) :]
    return visited, end_loop


def build_graph(bound=100, lang="en"):
    """
    Call `build_single_chain` for each number from 0 to `bound` included
    and return the following tuple:
        - connected_comp: dict {end_loop: nodes}. `nodes` is the set of nodes
            in each connected component, characterized by `end_loop`.
        - edges: each tuple (A, B) in this set is an edge A->B.
        - degree_by_node: dict {node: degree}. only NOT leaf nodes are here.
        - depth_by_node: dict {node: depth}. all nodes are here.
    """
    connected_comp = defaultdict(set)
    graph_edges = set()
    degree_by_node = defaultdict(int)
    depth_by_node = defaultdict(int)

    for n in range(bound + 1):
        visited, end_loop = build_single_chain(n, lang)
        depth_by_node[n] = len(visited) - len(end_loop)

        # # use a set of tuples to find unique end loops.
        # connected_comp[tuple(sorted(end_loop))].add(n)

        # count node degree. we skip the first visited node, it's the leaf
        # for this single chain.
        for node in visited[1:]:
            degree_by_node[node] += 1
        # should first node of `end_loop` sum extra degree?
        degree_by_node[end_loop[0]] += 1

        # get edges.
        edges = list(zip(visited[:-1], visited[1:]))
        # add the last edge that completes the loop.
        edges += [(end_loop[-1], end_loop[0])]
        graph_edges |= set(edges)

    return connected_comp, graph_edges, degree_by_node, depth_by_node


def build_graphviz(bound, lang):
    """Call `build_graph` and return a graphviz.Digraph object."""
    _, graph_edges, degree_by_node, depth_by_node = build_graph(bound, lang)

    depths = rank_keys(depth_by_node, reverse=True)
    color_scale = fade_color(
        NODE_COLOR_LEAF,
        NODE_COLOR_ROOT,
        1 + max(depths.values()),
    )

    degrees = rank_keys(degree_by_node, reverse=True)
    size_scale = float_range(
        NODE_SIZE_MAX,
        NODE_SIZE_MIN,
        1 + max(degrees.values()),
    )

    # build graph. graphviz requires objects to be cast to str.
    g = gv.Digraph(
        engine="neato",
        node_attr={
            "style": "filled",
            "color": NODE_COLOR_LEAF,
            "fixedsize": "true",
            "width": str(NODE_SIZE_MIN),
            "height": str(NODE_SIZE_MIN),
        },
        graph_attr={
            "outputorder": "nodesfirst",
        },
    )

    for node, degree in degrees.items():
        g.node(
            str(node),
            color=str(color_scale[depths[node]]),
            width=str(size_scale[degree]),
            height=str(size_scale[degree]),
        )

    for e in graph_edges:
        g.edge(*map(str, e))

    return g
