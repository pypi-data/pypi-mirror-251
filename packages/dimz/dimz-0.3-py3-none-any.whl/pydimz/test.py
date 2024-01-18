import json
import yaml


def make_json():
    with open('test.json') as file:
        data = json.load(file)

    new_dict = {}

    for x in data:
        try:
            for extension in x["extensions"]:
                if x["type"].lower() == "programming":
                    new_dict[extension] = x["name"]
        except KeyError:
            print(x["name"])
            print(type(x))

    with open('output.json', 'w') as file:
        json.dump(new_dict, file, indent=4)


def yml_to_json():
    with open("test.yml") as file:
        data = yaml.safe_load(file)

    with open('output.json', 'w') as file:
        json.dump(data, file, indent=4)


def yml_json_to_json():
    with open('output.json') as file:
        data = json.load(file)

    new_dict = {}

    for x in data:
        try:
            if data[x]["type"] == "programming":
                for extension in data[x]["extensions"]:
                    new_dict[extension] = x
        except KeyError:
            pass

    # Fix till I find a better way to do this.
    new_dict[".h"] = "C"
    del new_dict[".md"]

    with open('output_2.json', 'w') as file:
        json.dump(new_dict, file, indent=4)


if __name__ == "__main__":
    yml_to_json()
    yml_json_to_json()
