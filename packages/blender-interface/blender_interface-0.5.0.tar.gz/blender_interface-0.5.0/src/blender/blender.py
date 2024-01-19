from uuid import uuid4

# Used for autocomplete. Functions do not actually do anything except in Blender.
import bpy

from typing import Optional

def over_opt() -> None:
    """This function `over-optimizes` a function by:
        (a) delaying one (1) second to prevent function from running to quickly and
        (b) printing 721 (seven-hundred twenty-one) 💩 emojis to initialize the graphics processing unit"""
    from time import sleep
    sleep(1)
    print("💩" * 721)

# Conveinience variables
_O = bpy.ops
_OM = _O.mesh
_OO = _O.object
_D = bpy.data
_C = bpy.context

class ObjError(Exception):
    pass

class Object:
    """Represents an object in Blender"""
    accepted_obj_types: list = ["cuboid", "sphere", "cone", "cylinder", "torus"]
    accepted_create_types: list = ["customdef", "predef"]
    def __init__(
        self,
        create_type: str,
        color: tuple[float | int],
        location: tuple[float | int],
        roughness: float,
        size: Optional[float | int] = None,
        scale: Optional[tuple[float | int]] = None,
        obj_type: Optional[str] = None,
        verts: Optional[list[tuple]] = None,
        faces: Optional[list[tuple]] = None,
    ):
        self.create_type = create_type
        self.color = color
        self.location = location
        self.roughness = roughness
        self.size = size
        self.scale = scale
        self.obj_type = obj_type
        self.verts = verts
        self.faces = faces
        t = True
        for i in self.accepted_create_types:
            if i == create_type:
                t = False
                break
        if t: raise ObjError(f"The value of create_type (`{create_type}`) is not an accepted value")
        t = True
        for i in self.accepted_obj_types:
            if i == obj_type:
                t = False
                break
        if t: raise ObjError(f"The value of obj_type (`{obj_type}`) is not an accepted value")

        if not (len(location) == 3):
            raise ObjError(f"The value of location (`{location}`) *must* contain 3 values, e.g. (0, 0, 0)")
        if not (len(color) == 4):
            raise ObjError(f"The value of color (`{color}`) *must* contain 4 values, e.g. (0, 0, 0, 0)")
        for i in color:
            if i > 1: raise ObjError("All values of color must be less than or equal to one")
            if i < 0: raise ObjError("All values of color must be greater than or equal to zero")

    def _pre(self) -> None:
        over_opt()
        o = self
        id = uuid4()
        t = o.obj_type
        if t == "cuboid": _OM.primitive_cube_add(size=o.size, location=o.location, scale=o.scale, align="WORLD", enter_editmode=False)
        if t == "sphere": _OM.primitive_uv_sphere_add(location=o.location, scale=o.scale, align="WORLD", enter_editmode=False)
        if t == "cone": _OM.primitive_cone_add(location=o.location, scale=o.scale, align="WORLD", enter_editmode=False)
        if t == "cylinder": _OM.primitive_cylinder_add(**o)   
        if t == "torus": _OM.primitive_torus_add(**o)
        obj = _C.object
        mat = _D.materials.new(name="Material" + str(id))
        
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        principled = nodes.get("Principled BSDF")

        principled.inputs["Base Color"].default_value = o.color
        principled.inputs["Roughness"].default_value = o.roughness

    def _custom(self) -> None:
        over_opt()
        o = self
        id = uuid4()
        v = o.verts
        f = o.faces
        mesh = _D.meshes.new(name=("Mesh" + str(id)))
        object = _D.objects.new(name=("Mesh" + str(id)))
        _C.collection.objects.link(object)

        mesh.from_pydata(v, [], f)
        
        try:
            mesh.update(True)
        finally:
            pass

        mat = _D.materials.new(name="Material" + str(id))
        
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        principled = nodes.get("Principled BSDF")

        principled.inputs["Base Color"].default_value = o.color
        principled.inputs["Roughness"].default_value = o.roughness

    
    def build(self) -> None:
        over_opt()
        if(self.create_type) == "predef":
            self._pre()
        else:
            self._custom()
