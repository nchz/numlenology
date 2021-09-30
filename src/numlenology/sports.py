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


def top10(dic):
    return (
        sorted(dic.items(), key=lambda t: t[1], reverse=True)[:10],
        sorted(dic.items(), key=lambda t: t[1], reverse=False)[:10],
    )


print("########## longest loop")
tops, dops = top10(ll)
for lang, v in tops:
    print(lang, v)

print("########## biggest loop node")
tops, dops = top10(bln)
for lang, v in tops:
    print(lang, v)

# print("########## smallest loop node")
# tops, dops = top10(sln)
# for lang, v in tops:
#     print(lang, v)
# print("#####")
# for lang, v in dops:
#     print(lang, v)

print("########## biggest non-leaf")
tops, dops = top10(bf)
for lang, v in tops:
    print(lang, v)
print("#####")
for lang, v in dops:
    print(lang, v)

# print("########## smallest non-leaf")
# tops, dops = top10(sf)
# for lang, v in tops:
#     print(lang, v)
# print("#####")
# for lang, v in dops:
#     print(lang, v)

print("########## num of CCs")
tops, dops = top10(ncc)
for lang, v in tops:
    print(lang, v)

print("########## max mean in a CC")
tops, dops = top10(ccM)
for lang, v in tops:
    print(lang, v)

print("########## min mean in a CC")
tops, dops = top10(ccm)
print("#####")
for lang, v in dops:
    print(lang, v)

print("########## max std in a CC")
tops, dops = top10(ccS)
for lang, v in tops:
    print(lang, v)
print("#####")
for lang, v in dops[:1]:
    print(lang, v)

print("########## min std in a CC")
tops, dops = top10(ccs)
print("#####")
for lang, v in dops:
    print(lang, v)

print("########## max degree")
tops, dops = top10(G)
print("#####")
for lang, v in dops:
    print(lang, v)

print("########## max depth")
tops, dops = top10(D)
for lang, v in tops:
    print(lang, v)

# print("########## biggest edge gap")
# tops, dops = top10(beg)
# for lang, v in tops:
#     print(lang, v)
# print("#####")
# for lang, v in dops:
#     print(lang, v)

# print("########## smallest edge gap")
# tops, dops = top10(seg)
# for lang, v in tops:
#     print(lang, v)
# print("#####")
# for lang, v in dops:
#     print(lang, v)
