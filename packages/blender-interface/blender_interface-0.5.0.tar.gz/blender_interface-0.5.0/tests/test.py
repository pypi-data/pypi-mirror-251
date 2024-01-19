from blender import Object

l: list[dict, dict] = [{
    "create_type": "predef",
    "color": (0.0, 0.0, 1.0, 1.0),
    "location": (0, 0, 2.5),
    "roughness": 1.0,
    "size": 2,
    "scale": (1.0, 1.0, 1.0),
    "obj_type": "sphere"
    },
    {
    "create_type": "predef",
    "color": (0.0, 0.0, 1.0, 1.0),
    "location": (0, 0, 0),
    "roughness": 1.0,
    "size": 3,
    "scale": (1.0, 1.0, 1.0),
    "obj_type": "cuboid"
    }]

for d in l:
    o: Object = Object(**d)

    print(o)

    o.build()