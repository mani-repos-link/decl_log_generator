# from parsers.declare import DECLARE2LP, DeclareParser
from ASP_generator import ASP_generator
# from log_generator.alp import DECLARE2LP
# from parsers.declare.declare import DeclareParser
# import json

# with open("../files/reference10.decl") as file:

# with open("../files/reference10.decl") as file:
#     d2a = DeclareParser(file.read())
#     dm = d2a.parse()
#     # print(dm)
#     # print(dm.events)
#     # print(dm)
#     # print(json.dumps(dm, default=lambda o: o.__dict__, indent=4))
#     # print(json.dumps(dm, indent=4))
#     lp = DECLARE2LP()
#     s = lp.from_decl(dm)
#     print(s)

# with open("ad.json", "w+") as f:
#     json.dump(dm.__dict__(), f)

asp = ASP_generator(4, 2, 6,
                    # "../files/Response.decl",
                    "../files/Response3.decl",
                    "../files/templates.lp",
                    "../files/generation_encoding.lp")

asp.run()



