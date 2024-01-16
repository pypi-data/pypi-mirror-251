import sys
import typing
from . import uvcalc_follow_active
from . import anim
from . import view3d
from . import presets
from . import object
from . import object_quick_effects
from . import bmesh
from . import spreadsheet
from . import userpref
from . import constraint
from . import rigidbody
from . import freestyle
from . import clip
from . import screen_play_rendered_anim
from . import console
from . import object_randomize_transform
from . import wm
from . import geometry_nodes
from . import vertexpaint_dirt
from . import add_mesh_torus
from . import node
from . import uvcalc_lightmap
from . import object_align
from . import file
from . import assets
from . import image
from . import mesh
from . import sequencer
from . import uvcalc_transform

GenericType = typing.TypeVar("GenericType")

def register(): ...
def unregister(): ...
