import numpy as np
import collections


def gaussian_distribution(min_num_events: int, max_num_events: int):
    probabilities = [0.2, 0.5, 0.3]  # TODO as param
    prefixes = range(min_num_events, max_num_events + 1)
    trace_lens = np.random.choice(prefixes, 100, p=probabilities)
    c = collections.Counter(trace_lens)
    return c

