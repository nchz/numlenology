"""Test that all graph representations are equivalent."""
import numpy as np
from numlenology import (
    SUPPORTED_LANGS,
    build_graph,
    build_graph_matrix,
    build_graph_matrix_rec,
    Graph,
)

r = {}
for lang in SUPPORTED_LANGS:
    g1 = Graph(lang, builder=build_graph_matrix)
    g2 = Graph(lang, builder=build_graph_matrix_rec)
    r[lang] = (g1.matrix == g2.matrix).all()

    g = build_graph(lang, 101)

    els = sorted([sorted(el) for el in g["connected_comp"].keys()])
    els1 = sorted([sorted(el) for el in g1.end_loops])

    gs = sorted(g["degree_by_node"].items())
    gs1 = sorted((n, g1.gbn[n]) for n in np.where(g1.gbn != 0)[0])

    ds = sorted(g["depth_by_node"].items())
    ds1 = sorted((n, g1.dbn[n]) for n in np.where(g1.dbn != -123)[0])

    t1 = all(r.values())
    t2 = els == els1
    t3 = gs == gs1
    t4 = ds == ds1

    a = all([t1, t2, t3, t4])
    if a:
        print(f"{lang} OK")
    else:
        print(f"{lang} error: {t1, t2, t3, t4}")
