# import pprint


# def value_parse(path, key, value) -> dict:
#     # print("------------")
#     # print({"key": key, "value": value})

#     # Initialize result
#     result = {"key": key, "value": value}

#     # Parse key
#     key_out = key

#     # Parse value
#     value_out = value
#     if value is dict:
#         if "#text" in value.keys():
#             value_out = value["#text"]

#     # Consolidate Result
#     result["key"] = key_out
#     result["value"] = value_out

#     return result
