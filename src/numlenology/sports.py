from numlenology import Graph, SUPPORTED_LANGS


ll = {}
bln = {}
sln = {}
bf = {}
sf = {}
ncc = {}
ccM = {}
ccS = {}
ccm = {}
ccs = {}
G = {}
D = {}
beg = {}
seg = {}

for lang in SUPPORTED_LANGS:
    g = Graph(lang)
    ll[lang] = max(len(el) for el in g.end_loops)
    bln[lang] = max(el.max() for el in g.end_loops)
    sln[lang] = min(el.min() for el in g.end_loops)
    bf[lang] = g.non_leaf_nodes.max()
    sf[lang] = g.non_leaf_nodes.min()
    ncc[lang] = len(g.ccs)
    ccM[lang] = max([cc.mean().round(3) for cc in g.ccs.values()])
    ccS[lang] = max([cc.std().round(3) for cc in g.ccs.values()])
    ccm[lang] = min([cc.mean().round(3) for cc in g.ccs.values()])
    ccs[lang] = min([cc.std().round(3) for cc in g.ccs.values()])
    G[lang] = g.gbn.max()
    D[lang] = g.dbn.max()
    beg[lang] = g.edge_gaps.max()
    seg[lang] = g.edge_gaps.min()


def result(dic):
    return sorted(dic.items(), key=lambda t: t[1], reverse=True)


# print("########## longest loop")
# for lang, v in result(ll):
#     print(lang, v)

# print("########## biggest loop node")
# for lang, v in result(bln):
#     print(lang, v)

# print("########## smallest loop node")
# for lang, v in result(sln):
#     print(lang, v)

print("########## biggest non-leaf")
for lang, v in result(bf):
    print(lang, v)

# print("########## smallest non-leaf")
# for lang, v in result(sf):
#     print(lang, v)

# print("########## num of CCs")
# for lang, v in result(ncc):
#     print(lang, v)

# print("########## max mean in a CC")
# for lang, v in result(ccM):
#     print(lang, v)

# print("########## max std in a CC")
# for lang, v in result(ccS):
#     print(lang, v)

# print("########## min mean in a CC")
# for lang, v in result(ccm):
#     print(lang, v)

# print("########## min std in a CC")
# for lang, v in result(ccs):
#     print(lang, v)

# print("########## max degree")
# for lang, v in result(G):
#     print(lang, v)

# print("########## max depth")
# for lang, v in result(D):
#     print(lang, v)

print("########## biggest edge gap")
for lang, v in result(beg):
    print(lang, v)

# print("########## smallest edge gap")
# for lang, v in result(seg):
#     print(lang, v)
