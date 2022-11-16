from src.log_generator.alp.declare2Lp import Declare2lp
from src.log_generator.generators.ASPGenerator import ASPGenerator
from src.log_generator.parsers.declare.declare import DeclareParser

#
# with open("tests/files/declare/Response.decl", "r") as file:
#     d2a = DeclareParser(file.read())
#     dm = d2a.parse()
#     lp_model = Declare2lp().from_decl(dm)
#     lp = lp_model.__str__()
#     # print(dm)
#     print(lp)


num_of_traces = 4
num_min_events = 2
num_max_events = 4

asp = ASPGenerator(
    num_of_traces,
    num_min_events,
    num_max_events,
    "tests/files/declare/Response.decl",
    "tests/files/lp/templates.lp",
    "tests/files/lp/generation_encoding.lp"
)

asp.run()
# asp.to_xes("output_xes/generated_exporter.xes")
