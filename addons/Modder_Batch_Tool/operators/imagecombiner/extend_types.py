import bpy
from bpy.props import *

#from . import addon_updater_ops


class CombineList(bpy.types.PropertyGroup):
    ob:PointerProperty(
        name='Current Object',
        type=bpy.types.Object,
    )
    ob_id:IntProperty(default=0)
    mat:PointerProperty(
        name='Current Object Material',
        type=bpy.types.Material,
    )
    layer:IntProperty(
        name='Material Layers',
        description='Materials with the same number will be merged together.'
                    '\nUse this to create multiple materials linked to the same atlas file',
        min=1,
        max=99,
        step=1,
        default=1,
    )
    used:BoolProperty(default=True)
    type:IntProperty(default=0)




def register() -> None:
    bpy.types.Scene.smc_ob_data = CollectionProperty(type=CombineList)
    bpy.types.Scene.smc_ob_data_id = IntProperty(default=0)
    bpy.types.Scene.smc_list_id = IntProperty(default=0)
    bpy.types.Scene.smc_size = EnumProperty(
        name='Combined image size',
        items=[
            ('PO2', 'Power of 2', 'Combined image size is power of 2'),
            ('QUAD', 'Quadratic', 'Combined image has same width and height'),
            ('AUTO', 'Automatic', 'Combined image has minimal size'),
            ('CUST', 'Custom', 'Combined image has proportionally scaled to fit in custom size'),
            ('STRICTCUST', 'Strict Custom', 'Combined image has exact custom width and height'),
        ],
        description='Select combined image size',
        default='QUAD',
    )
    bpy.types.Scene.smc_size_width = IntProperty(
        name='Max width (px)',
        description='Select max width for combined image',
        min=8,
        max=8192,
        step=1,
        default=4096,
    )
    bpy.types.Scene.smc_size_height = IntProperty(
        name='Max height (px)',
        description='Select max height for combined image',
        min=8,
        max=8192,
        step=1,
        default=4096,
    )
    bpy.types.Scene.smc_crop = BoolProperty(
        name='Crop outside images by UV',
        description='Crop images by UV if materials UV outside of bounds',
        default=True,
    )
    bpy.types.Scene.smc_pixel_art = BoolProperty(
        name='Pixel Art / Small Textures',
        description='Avoids 1-pixel UV scaling for small textures.'
                    '\nDisable for larger textures to avoid blending with nearby pixels',
        default=False,
    )
    bpy.types.Scene.smc_diffuse_size = IntProperty(
        name='Size of materials without image',
        description='Select the size of materials that only consist of a color',
        min=8,
        max=256,
        step=1,
        default=32,
    )
    bpy.types.Scene.smc_gaps = IntProperty(
        name='Size of gaps between images',
        description='Select size of gaps between images',
        min=0,
        max=32,
        step=200,
        default=0,
        options={'HIDDEN'},
    )
    bpy.types.Scene.smc_save_path = StringProperty(
        description='Select the directory in which the generated texture atlas will be saved',
        default='',
    )

    bpy.types.Material.root_mat = PointerProperty(
        name='Material Root',
        type=bpy.types.Material,
    )
    bpy.types.Material.smc_diffuse = BoolProperty(
        name='Multiply image with diffuse color',
        description='Multiply the materials image with its diffuse color.'
                    '\nINFO: If this color is white the final image will be the same',
        default=True,
    )
    bpy.types.Material.smc_size = BoolProperty(
        name='Custom image size',
        description='Select the max size for this materials image in the texture atlas',
        default=False,
    )
    bpy.types.Material.smc_size_width = IntProperty(
        name='Max width (px)',
        description='Select max width for material image',
        min=8,
        max=8192,
        step=1,
        default=2048,
    )
    bpy.types.Material.smc_size_height = IntProperty(
        name='Max height (px)',
        description='Select max height for material image',
        min=8,
        max=8192,
        step=1,
        default=2048,
    )


def unregister() -> None:
    del bpy.types.Scene.smc_ob_data
    del bpy.types.Scene.smc_ob_data_id
    del bpy.types.Scene.smc_list_id
    del bpy.types.Scene.smc_size
    del bpy.types.Scene.smc_size_width
    del bpy.types.Scene.smc_size_height
    del bpy.types.Scene.smc_crop
    del bpy.types.Scene.smc_pixel_art
    del bpy.types.Scene.smc_diffuse_size
    del bpy.types.Scene.smc_gaps
    del bpy.types.Scene.smc_save_path

    del bpy.types.Material.root_mat
    del bpy.types.Material.smc_diffuse
    del bpy.types.Material.smc_size
    del bpy.types.Material.smc_size_width
    del bpy.types.Material.smc_size_height
