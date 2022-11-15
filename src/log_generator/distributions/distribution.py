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


def uniform_distribution(min_num, max_num):
    probabilities = get_uniform_probabilities(min_num, max_num)
    prefixes = range(min_num, max_num + 1)
    trace_lens = np.random.choice(prefixes, 100, p=probabilities)
    c = collections.Counter(trace_lens)
    return c


def custom_distribution(min_num, max_num, probabilities: [float]):
    prefixes = range(min_num, max_num + 1)
    trace_lens = np.random.choice(prefixes, 100, p=probabilities)
    c = collections.Counter(trace_lens)
    return c


def normal_distribution(mu, sigma, num_traces: int):
    trace_lens = np.random.normal(mu, sigma, num_traces)
    trace_lens = np.round(trace_lens)
    trace_lens = trace_lens[trace_lens > 1]
    c = collections.Counter(trace_lens)
    return c


def distribution(
        min_num_events: int, max_num_events: int,
        dist_type: Literal["uniform", "normal", "custom"] = "uniform",
        num_traces: Optional[int] = None,
        custom_p: Optional[List[float]] = None):
    if dist_type == "normal":
        return normal_distribution(min_num_events, max_num_events, num_traces)
    elif dist_type == "uniform":
        return uniform_distribution(min_num_events, max_num_events)
    elif dist_type == "custom":
        if custom_p is None:
            raise ValueError("custom probabilities must be provided")
        s = sum(custom_p)
        if s != 1:
            raise ValueError("sum of provided list must be 1")
        return custom_distribution(min_num_events, max_num_events, custom_p)



if __name__ == "__main__":
    print(distribution(2, 4, "uniform"))
    print(normal_distribution(1.5, 0.15, 1000))
    # print(distribution(2, 10, "normal"))

