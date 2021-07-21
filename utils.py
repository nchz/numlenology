import graphviz as gv
from num2words import CONVERTER_CLASSES, num2words
from unidecode import unidecode


LANGS = sorted(set(lang[:2] for lang in CONVERTER_CLASSES.keys()))


def build_single_chain(n: int, lang: str = "en"):
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

    The result is a tuple (visited, loop_tail) where:
        - `visited` contains all visited numbers (initial `n` included).
        - `loop_tail` is the sublist with the last numbers of `visited` that
            are in the final loop.

    So for the example above the result will be:
        build_single_chain(10) == ([10, 3, 5, 4], [4])

    Note that in english the only `loop_tail` is [4].
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
    loop_tail = visited[visited.index(n) :]
    return visited, loop_tail


def build_graph(bound: int = 100, lang: str = "en"):
    """
    Call `build_single_chain` for each number from 0 to `bound` included
    and return a graphviz.Digraph object.
    """
    g = gv.Digraph(
        engine="neato",
        node_attr={
            "style": "filled",
            "color": "#aaaaaa90",
        },
        graph_attr={
            "outputorder": "nodesfirst",
        },
    )

    graph_edges = set()
    for n in range(bound + 1):
        visited, loop_tail = build_single_chain(n, lang)
        # get edges and add the last edge that completes the loop.
        edges = list(zip(visited[:-1], visited[1:])) + [(loop_tail[-1], loop_tail[0])]
        # convert to str so graphviz takes them as node labels.
        edges = set((str(x), str(y)) for x, y in edges)
        graph_edges |= edges

    for e in graph_edges:
        g.edge(*e)

    return g
