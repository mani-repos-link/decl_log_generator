from abc import ABC, abstractmethod


class Log_generator(ABC):
    def __init__(self,
                 num_traces: int,
                 min_event: int,
                 max_event: int):
        self.num_traces = num_traces
        self.min_event = min_event
        self.max_event = max_event

    @abstractmethod
    def run(self):
        pass
