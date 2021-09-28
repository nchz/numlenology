import pickle

from numlenology.core import PICKLE_FILENAME


def load_graph_data(lang, bound):
    with open(PICKLE_FILENAME.format(lang=lang, bound=bound), "rb") as f:
        graph_data = pickle.load(f)
    return graph_data


# gd = load_graph_data(lang, bound)

def get_max_depth(gd):
    # TODO return node with max depth as well.
    """Get max node depth from `gd`."""
    return max(gd["depth_by_node"].values())


def get_max_degree(gd):
    # TODO idem `get_max_depth`.
    """Get max node degree from `gd`."""
    return max(gd["degree_by_node"].values())


def get_leaf_nodes(gd):
    # TODO get_max_leaf, etc.
    """Get leaves from graph data and return them sorted."""
    all_nodes = gd["depth_by_node"].keys()
    non_leaves = gd["degree_by_node"].keys()
    leaf_nodes = all_nodes - non_leaves
    return sorted(leaf_nodes)


def get_edge_gaps(gd):
    """Get (A - B) for each edge A->B."""
    gaps = [(a - b, (a, b)) for a, b in gd["edges"]]
    return sorted(gaps)


def get_num_cc(gd):
    """Get number of connected components."""
    return len(gd["connected_comp"])


def get_end_loop_nodes(gd):
    # TODO idem `get_leaf_nodes`.
    """
    Get nodes from `end_loop` in graph data and return them sorted.
    Nodes from all end loop are combined in one list.
    """
    end_loop_nodes = [n for end_loop in gd["connected_comp"].keys() for n in end_loop]
    return sorted(end_loop_nodes)


def all_cc_higher_el(gd):
    """
    Find connected components whose nodes are all higher than the nodes in the
    end loop of the connected component. Return None if no such component.
    """
    ccs = [(end_loop, cc_nodes - set(end_loop)) for end_loop, cc_nodes in gd["connected_comp"]]
    return [(el, cc) for el, cc in ccs if max(el) < min(cc)]
