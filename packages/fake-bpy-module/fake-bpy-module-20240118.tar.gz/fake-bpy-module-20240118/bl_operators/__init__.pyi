import sys
import typing
from . import spreadsheet
from . import vertexpaint_dirt
from . import console
from . import constraint
from . import wm
from . import view3d
from . import freestyle
from . import uvcalc_transform
from . import uvcalc_lightmap
from . import object_randomize_transform
from . import anim
from . import sequencer
from . import add_mesh_torus
from . import node
from . import screen_play_rendered_anim
from . import clip
from . import geometry_nodes
from . import presets
from . import object_quick_effects
from . import rigidbody
from . import mesh
from . import image
from . import file
from . import bmesh
from . import object_align
from . import userpref
from . import object
from . import uvcalc_follow_active
from . import assets

GenericType = typing.TypeVar("GenericType")

def register(): ...
def unregister(): ...
