import graphviz as gv

from numlenology.graph import build_graph
from numlenology.utils import float_range, rank_keys
from numlenology.utils.color import fade_color


NODE_COLOR_LEAF = "#009000bb"
NODE_COLOR_ROOT = "#000000bb"
NODE_SIZE_MIN = 0.4
NODE_SIZE_MAX = 0.9


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
