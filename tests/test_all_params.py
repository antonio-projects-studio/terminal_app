from terminal_app.types import AllParams

ap = AllParams({"a": 1, "b": 2})
ap.update({"m": "p"})
args = ap["all_params"]
ap["all_params"] = 1
print(ap == ap["all_params"]["all_params"])
print(ap["all_params"]["all_params"]["m"])
print(ap["all_params"]["all_params"]["all_params"])
print(ap)
