import json
from collections import OrderedDict

def make_object(parsed_line, i):
    Type = parsed_line[0]
    # Truncated = parsed_line[1]
    # Occluded = parsed_line[2]
    # Alpha = parsed_line[3]
    Bbox = [parsed_line[4] ,parsed_line[5], parsed_line[6], parsed_line[7]]
    Dimensions = [parsed_line[8], parsed_line[9], parsed_line[10]]
    Location = [parsed_line[11], parsed_line[12], parsed_line[13]]
    Rotation_y = parsed_line[14]

    position = OrderedDict()
    position["x"] = float(Location[0])
    position["y"] = float(Location[1])
    position["z"] = float(Location[2])
    rotation = OrderedDict()
    rotation["x"] = 0
    rotation["y"] = 0
    rotation["z"] = float(Rotation_y)
    dimensions = OrderedDict()
    dimensions["x"] = float(Dimensions[0])
    dimensions["y"] = float(Dimensions[1])
    dimensions["z"] = float(Dimensions[2])

    geometry3D = OrderedDict()
    geometry3D["position"] = position
    geometry3D["rotation"] = rotation
    geometry3D["dimensions"] = dimensions

    geometryType3D = OrderedDict()
    geometryType3D["geometry"] = geometry3D

    geometry2D = OrderedDict()
    geometry2D["xmin"] = float(Bbox[0])
    geometry2D["ymin"] = float(Bbox[1])
    geometry2D["xmax"] = float(Bbox[2])
    geometry2D["ymax"] = float(Bbox[3])
    geometryType2D = OrderedDict()
    geometryType2D["geometry"] = geometry2D

    args = OrderedDict()
    args["name"] = Type
    args["geometryType3D"] = geometryType3D
    args["geometryType2D"] = geometryType2D
    args["index"] = i
    return args

def main():
    root = OrderedDict()
    root["objects"] = []
    with open("000001.txt") as fp:
        i = 0
        for line in fp.readlines():
            line = line.replace('\n', "")
            parsed_line = line.split(" ")
            Object = make_object(parsed_line, i)
            root["objects"].append(Object)
            i = i + 1
    # Print JSON
    print(json.dumps(root, ensure_ascii=False, indent="\t"))
    # Save JSON
    # with open("sample_JSON", 'w') as outfile:
    #     json.dump(root, outfile)

if __name__ == "__main__":
    main()