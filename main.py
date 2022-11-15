from src.log_generator.generators.ASPGenerator import ASPGenerator

asp = ASPGenerator(4, 2, 6,
                   "tests/files/declare/Response3.decl",
                   "tests/files/lp/templates.lp",
                   "tests/files/lp/generation_encoding.lp")

asp.run()
asp.to_xes_with_dataframe("output_xes/generated_dataframe.xes")
asp.to_xes("output_xes/generated_exporter.xes")
