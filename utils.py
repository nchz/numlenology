from collections import defaultdict

import graphviz as gv
from num2words import CONVERTER_CLASSES, num2words

from fade_color import fade_color


LANGS = sorted(set(lang[:2] for lang in CONVERTER_CLASSES.keys()))

NODE_COLOR_LEAF = "#009000bb"
NODE_COLOR_ROOT = "#000000bb"
NODE_SIZE_MIN = 0.4
NODE_SIZE_MAX = 0.9


def float_range(a, b, num_steps):
    """Like `range` but allows float values."""
    step = (b - a) / num_steps
    return [a + (i * step) for i in range(num_steps)]


def rank_nodes(score_by_node, reverse=False):
    """
    Given a dict `{node: score}` where `score` is any sortable value, return
    a dict `{node: rank}` where `rank` is an integer corresponding to the
    position that `node` gets in an ascending sorting by `score`.

    For example:
        a = {"a": 3, "b": 100, "c": 1, "d": 1}
        b = {"a": 2, "b": 3, "c": 1, "d": 1}
        rank_nodes(a) == b
    """
    nodes_by_score = defaultdict(set)
    for node, score in score_by_node.items():
        nodes_by_score[score].add(node)
    rank = enumerate(sorted(nodes_by_score.items(), reverse=reverse))
    return {n: i for i, (score, nodes) in rank for n in nodes}


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
    and return a graphviz.Digraph object.
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

    graph_edges = set()
    depth_by_node = defaultdict(int)
    grade_by_node = defaultdict(int)

    for n in range(bound + 1):
        visited, end_loop = build_single_chain(n, lang)
        depth_by_node[n] = len(visited) - len(end_loop)

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

        # convert to str so graphviz takes them as node labels.
        edges = set((str(x), str(y)) for x, y in edges)
        graph_edges |= edges

    depths = rank_nodes(depth_by_node, reverse=True)
    color_scale = fade_color(
        NODE_COLOR_LEAF,
        NODE_COLOR_ROOT,
        1 + max(depths.values()),
    )

    grades = rank_nodes(grade_by_node, reverse=True)
    size_scale = float_range(
        NODE_SIZE_MAX,
        NODE_SIZE_MIN,
        1 + max(grades.values()),
    )

    for node, grade in grades.items():
        g.node(
            str(node),
            color=str(color_scale[depths[node]]),
            width=str(size_scale[grade]),
            height=str(size_scale[grade]),
        )

    for e in graph_edges:
        g.edge(*e)

    return g
