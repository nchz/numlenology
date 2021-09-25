from collections import defaultdict


def float_range(a, b, num_steps):
    """Like `range` but allows float values."""
    step = (b - a) / num_steps
    return [a + (i * step) for i in range(num_steps)]


def rank_keys(score_by_key, reverse=False):
    """
    Given a dict `{key: score}` where `score` is any sortable value, return
    a dict `{key: rank}` where `rank` is an integer corresponding to the
    position that `key` would get sorting by `score` considering ties.

    For example:
        a = {"a": 3, "b": 100, "c": 1, "d": 1}
        b = {"a": 1, "b": 2, "c": 0, "d": 0}
        rank_keys(a) == b
    """
    keys_by_score = defaultdict(set)
    for key, score in score_by_key.items():
        keys_by_score[score].add(key)
    rank = enumerate(sorted(keys_by_score.items(), reverse=reverse))
    return {k: i for i, (score, keys) in rank for k in keys}
