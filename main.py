from src.log_generator.generators.ASPGenerator import ASPGenerator

num_of_traces = 4
num_min_events = 2
num_max_events = 4

asp = ASPGenerator(
    num_of_traces,
    num_min_events,
    num_max_events,
    "tests/files/declare/Response3.decl",
    "tests/files/lp/templates.lp",
    "tests/files/lp/generation_encoding.lp"
)

asp.run()
asp.to_xes("output_xes/generated_exporter.xes")
