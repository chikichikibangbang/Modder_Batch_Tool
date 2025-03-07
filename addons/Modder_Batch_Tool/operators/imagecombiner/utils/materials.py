from collections import OrderedDict
from collections import defaultdict
from typing import List
from typing import Union
from typing import ValuesView
from typing import cast

import bpy
import numpy as np

from .images import get_image
from .images import get_packed_file
from .textures import get_texture
from .. import globs
from ..type_annotations import Diffuse
from ..type_annotations import MatDict
from ..type_annotations import MatDictItem

shader_types = OrderedDict([
    ('mmd', {'mmd_shader', 'mmd_base_tex'}),
    ('mmdCol', {'mmd_shader'}),
    ('mtoon', {'Mtoon1BaseColorTexture.Image'}),
    ('mtoonCol', {'Mtoon1Material.Mtoon1Output'}),
    ('principled', {'原理化 BSDF', 'mmd_base_tex' or 'Image Texture'}),
    ('principledCol', {'原理化 BSDF'}),
    ('diffuse', {'Diffuse BSDF', 'Image Texture'}),
    ('diffuseCol', {'Diffuse BSDF'}),
    ('emission', {'Emission', 'Image Texture'}),
    ('emissionCol', {'Emission'}),
])

shader_image_nodes = {
    'mmd': 'mmd_base_tex',
    'mtoon': 'Mtoon1BaseColorTexture.Image',
    'vrm': 'Image Texture',
    'xnalara': 'Image Texture',
    'principled': 'mmd_base_tex' or 'Image Texture',
    'diffuse': 'Image Texture',
    'emission': 'Image Texture',
}

def korone(mat):
    node_tree = mat.node_tree if mat else None
    for node in node_tree.nodes:
        if node.type == "TEX_IMAGE":
            if node.outputs[0].is_linked:
                node_link = node.outputs[0].links[0]
                node_socket_name = node_link.to_socket.name
                node_node_name = node_link.to_node.name
                if node_socket_name == "Base Color" and node_node_name == "原理化 BSDF":
                    return node
                elif node_socket_name == "Base Color" and node_node_name == "原理化BSDF":
                    return node
                elif node_socket_name == "Base Color" and node_node_name == "Principled BSDF":
                    return node
                elif node_socket_name == "Base Tex" and node_node_name == "mmd_shader":
                    return node
                elif node_socket_name == "Diffuse" and node_node_name == "群组":
                    return node
                elif node_socket_name == "Diffuse" and node_node_name == "Group":
                    return node
                
def get_materials(ob: bpy.types.Object) -> List[bpy.types.Material]:
    return [mat_slot.material for mat_slot in ob.material_slots if mat_slot.material]


def get_shader_type(mat: bpy.types.Material) -> Union[str, None]:
    if not mat.node_tree or not mat.node_tree.nodes:
        return

    node_tree = mat.node_tree.nodes

    if 'Group' in node_tree:
        node_tree_name = node_tree['Group'].node_tree.name
        if node_tree_name == 'Group':
            return 'xnalaraNewCol'
        if node_tree_name == 'MToon_unversioned':
            return 'vrm' if 'Image Texture' in node_tree else 'vrmCol'
        elif node_tree_name == 'XPS Shader' and 'Image Texture' in node_tree:
            return 'xnalara'

    node_names_set = set(node_tree.keys())
    return next(
        (
            shader_type
            for shader_type, node_names in shader_types.items()
            if node_names.issubset(node_names_set)
        ),
        None,
    )


def sort_materials(mat_list: List[bpy.types.Material]) -> ValuesView[MatDictItem]:
    for mat in bpy.data.materials:
        mat.root_mat = None

    mat_dict = cast(MatDict, defaultdict(list))
    for mat in mat_list:
        #node_tree = mat.node_tree if mat else None

        packed_file = None

        #if globs.is_blender_2_79_or_older:
            #packed_file = get_packed_file(get_image(get_texture(mat)))
        #elif node_tree:
            #shader = get_shader_type(mat)
            #node_name = shader_image_nodes.get(shader)
        node = korone(mat)
        packed_file = get_packed_file(node.image)


        if packed_file:
            mat_dict[(packed_file, get_diffuse(mat) if mat.smc_diffuse else None)].append(mat)
        else:
            mat_dict[get_diffuse(mat)].append(mat)

    return mat_dict.values()


def rgb_to_255_scale(diffuse: Diffuse) -> Diffuse:
    rgb = np.empty(shape=(0,), dtype=int)
    for c in diffuse:
        if c < 0.0:
            srgb = 0
        elif c < 0.0031308:
            srgb = c * 12.92
        else:
            srgb = 1.055 * pow(c, 1.0 / 2.4) - 0.055
             
        rgb = np.append(rgb, np.clip(round(srgb * 255), 0, 255))
    return tuple(rgb)


def get_diffuse(mat: bpy.types.Material) -> Diffuse:
    
    return 255, 255, 255
