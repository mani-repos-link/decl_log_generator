from __future__ import annotations

import collections
import typing
from datetime import datetime

import numpy as np
import clingo
from clingo import SymbolType
import pm4py
from pm4py.objects.log import obj as lg
from pm4py.objects.log.exporter.xes import exporter
import pandas as pd

from src.log_generator.abstracts.logGenerator import LogGenerator
from src.log_generator.alp.declare2Lp import Declare2lp
from src.log_generator.distributions.distribution import Distributor
from src.log_generator.parsers.declare.declare import DeclareParser
import os
from random import randrange


class ASPGenerator(LogGenerator):

    def __init__(self,
                 num_traces: int, min_event: int, max_event: int,
                 decl_model_path: str, template_path: str, encoding_path: str,
                 distributor_type: typing.Literal["uniform", "normal", "custom"] = "uniform",
                 custom_probabilities: typing.Optional[typing.List[float]] = None
                 ):
        super().__init__(num_traces, min_event, max_event)
        self.decl_model_path = decl_model_path
        self.template_path = template_path
        self.encoding_path = encoding_path
        self.clingo_output = []
        self.log: lg.EventLog | None = None
        d = Distributor()
        self.counter: collections.Counter | None = d.distribution(min_event, max_event, num_traces,
                                                                  distributor_type, custom_probabilities)

    def __decl_model_to_lp_file(self):
        with open(self.decl_model_path, "r") as file:
            d2a = DeclareParser(file.read())
            dm = d2a.parse()
            lp_model = Declare2lp().from_decl(dm)
            lp = lp_model.__str__()
        # with tempfile.NamedTemporaryFile() as tmp:  # TODO: improve it
        with open("generated.lp", "w+") as tmp:
            tmp.write(lp)
        return "generated.lp"

    def run(self):
        decl2lp_file = self.__decl_model_to_lp_file()
        self.clingo_output = []
        for events, traces in self.counter.items():
            random_seed = randrange(0, 2 ** 32 - 1)
            # print("events=", events, "traces=", traces, "seed=", random_seed)
            self.__generate_traces(decl2lp_file, events, traces, random_seed)
        for i in self.clingo_output:
            print(i)
        os.remove(decl2lp_file)  # removes the temporary decl->lp modal file created

    def __generate_traces(self, decl_model_lp: str,
                          num_events: int, num_traces: int,
                          seed: int, freq: float = 0.9, ):
        ctl = clingo.Control(
            [f"-c t={num_events}", f"{num_traces}", f"--seed={seed}", f"--rand-freq={freq}"])  # TODO: add parameters
        ctl.load(self.encoding_path)
        ctl.load(self.template_path)
        ctl.load(decl_model_lp)
        ctl.ground([("base", [])], context=self)
        ctl.solve(on_model=self.__handle_clingo_result)

    def __handle_clingo_result(self, output: clingo.solving.Model):
        self.clingo_output.append(output.symbols(shown=True))
        # print(self.clingo_output)
        # self.__pm4py_log()

    def __parse_clingo_result(self):
        # TODO: improve
        result = self.clingo_output
        traced = {}
        for m in result:  # create dict
            trace_name = str(m.name)
            arg_len = len(m.arguments)
            l, i = ([], 0)
            for arg in m.arguments:  # resources
                i = i + 1
                if arg.type == SymbolType.Function:
                    l.append(str(arg.name))
                if arg.type == SymbolType.Number:
                    num = str(arg.number)
                    l.append(num)
                    if i == arg_len:
                        if num not in traced:
                            traced[num] = {}
                        traced[num][trace_name] = l
        return traced

    def __pm4py_log(self):
        self.log = lg.EventLog()
        self.log.extensions["concept"] = {}
        self.log.extensions["concept"]["name"] = lg.XESExtension.Concept.name
        self.log.extensions["concept"]["prefix"] = lg.XESExtension.Concept.prefix
        self.log.extensions["concept"]["uri"] = lg.XESExtension.Concept.uri

        traced = self.__parse_clingo_result()
        print(traced)
        for trace_id in range(len(traced)):
            trace_gen = lg.Trace()
            trace_gen.attributes["concept:name"] = f"trace_{trace_id}"
            for i in traced:
                trace = traced[i]
                event_name = trace["trace"][0]
                e = {i: trace[i] for i in trace if i != 'trace'}  # filter trace by removing trace key
                for i in e:  # e = {'assigned_value': ['grade', '5', '1']}
                    event = lg.Event()
                    event["concept:name"] = event_name
                    event[e[i][0]] = e[i][1]
                    event["time:timestamp"] = datetime.now().timestamp()  # + timedelta(hours=c).datetime
                    trace_gen.append(event)
            self.log.append(trace_gen)

    def to_xes(self, output_fn: str):
        if self.log is None:
            self.__pm4py_log()
        exporter.apply(self.log, output_fn)

    def to_xes_with_dataframe(self, output_filename: str):
        lines = []
        traced = self.__parse_clingo_result()
        for trace_id in range(len(traced)):
            line = {'case_id': trace_id}
            for i in traced:
                trace = traced[i]
                event_name = trace["trace"][0]
                line['case:concept:name'] = event_name
                e = {i: trace[i] for i in trace if i != 'trace'}  # filter trace by removing trace key
                for i in e:  # e = {'assigned_value': ['grade', '5', '1']}
                    line['concept:name'] = e[i][0]
                    line["time:timestamp"] = datetime.now().timestamp()  # + timedelta(hours=c).datetime
            lines.append(line)
        dt = pd.DataFrame(lines)
        dt = pm4py.format_dataframe(dt, case_id='case_id', activity_key='concept:name',
                                    timestamp_key='time:timestamp')
        logger = pm4py.convert_to_event_log(dt)
        pm4py.write_xes(logger, output_filename)
