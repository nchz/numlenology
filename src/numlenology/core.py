import pickle
from collections import defaultdict

import graphviz as gv
from num2words import CONVERTER_CLASSES, num2words

from numlenology.utils import float_range, rank_keys
from numlenology.utils.color import fade_color


LANGS = sorted(set(lang[:2] for lang in CONVERTER_CLASSES.keys()))
PICKLE_FILENAME = "./data/{lang}-{bound}.pickle"

NODE_COLOR_LEAF = "#009000bb"
NODE_COLOR_ROOT = "#000000bb"
NODE_SIZE_MIN = 0.4
NODE_SIZE_MAX = 0.9


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


def build_graph(bound=100, lang="en", dump_pickle=False):
    """
    Call `build_single_chain` for each number from 0 to `bound` included
    and return a graphviz.Digraph object.

    If `dump_pickle` then a file is generated containing a dict with the
    following keys:
        - end_loops: the len of this set is the num of connected components.
        - graph_edges: each tuple (A, B) in this set is an edge A->B.
        - grade_by_node: dict {node: grade}. only NOT leaf nodes are here.
        - depth_by_node: dict {node: depth}. all nodes are here.
    """
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

    end_loops = set()
    graph_edges = set()
    grade_by_node = defaultdict(int)
    depth_by_node = defaultdict(int)

    for n in range(bound + 1):
        visited, end_loop = build_single_chain(n, lang)
        depth_by_node[n] = len(visited) - len(end_loop)

        # use a set of tuples to find unique end loops.
        end_loops.add(tuple(sorted(end_loop)))

        # count node grade. we skip the first visited node, it's the leaf
        # for this single chain.
        for node in visited[1:]:
            grade_by_node[node] += 1
        # should first node of `end_loop` sum extra grade?
        grade_by_node[end_loop[0]] += 1

        # get edges.
        edges = list(zip(visited[:-1], visited[1:]))
        # add the last edge that completes the loop.
        edges += [(end_loop[-1], end_loop[0])]
        graph_edges |= set(edges)

    depths = rank_keys(depth_by_node, reverse=True)
    color_scale = fade_color(
        NODE_COLOR_LEAF,
        NODE_COLOR_ROOT,
        1 + max(depths.values()),
    )

    grades = rank_keys(grade_by_node, reverse=True)
    size_scale = float_range(
        NODE_SIZE_MAX,
        NODE_SIZE_MIN,
        1 + max(grades.values()),
    )

    # build graph. cast objects to str, graphviz requires this type.
    for node, grade in grades.items():
        g.node(
            str(node),
            color=str(color_scale[depths[node]]),
            width=str(size_scale[grade]),
            height=str(size_scale[grade]),
        )

    for e in graph_edges:
        g.edge(*map(str, e))

    if dump_pickle:
        graph_data = {
            "end_loops": end_loops,
            "graph_edges": graph_edges,
            "grade_by_node": grade_by_node,
            "depth_by_node": depth_by_node,
        }
        with open(PICKLE_FILENAME.format(lang=lang, bound=bound), "wb") as f:
            pickle.dump(graph_data, f)

    return g
