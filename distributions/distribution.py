import math
from typing import *
import numpy as np
import collections


def get_normal_dist_probabilities(mu: float, sigma: float, x: float = 1):
    var = float(sigma) ** 2
    denom = (2 * math.pi * var) ** .5
    num = math.exp(-(float(x) - float(mu)) ** 2 / (2 * var))
    return num / denom


def get_uniform_probabilities(s_min: int, s_max: int):
    ps = (s_max + 1) - s_min
    return [1 / ps for p in range(s_min, s_max + 1)]


def distribution(min_num_events: int, max_num_events: int,
                 dist_type: Literal["uniform", "normal", "custom"] = "uniform",
                 custom_p: Optional[List[float]] = None):
    probabilities = []
    if dist_type == "uniform":
        probabilities = get_uniform_probabilities(min_num_events, max_num_events)
    elif dist_type == "normal":
        probabilities = get_normal_dist_probabilities(min_num_events, max_num_events)
    elif dist_type == "custom":
        if custom_p is None:
            raise ValueError("custom probabilities must be provided")
        s = sum(custom_p)
        if s != 1:
            raise ValueError("sum of provided list must be 1")
        probabilities = custom_p
    prefixes = range(min_num_events, max_num_events + 1)
    trace_lens = np.random.choice(prefixes, 100, p=probabilities)
    c = collections.Counter(trace_lens)
    return c


def normpdf(x, mean, sd):
    var = float(sd) ** 2
    denom = (2 * math.pi * var) ** .5
    num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
    return num / denom


if __name__ == "__main__":
    print(distribution(2, 4, "uniform"))
    # print(distribution(2, 10, "normal"))

