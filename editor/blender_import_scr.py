# Blender 3.x/4.x: run in Scripting workspace, then call import_scr_json(path)
import bpy, json, math
from mathutils import Vector

def _mat(name, rgba):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color=rgba
    return m

def import_scr_json(path, cube_size=8.0, height_scale=1/256.0, preview_width=4.0):
    with open(path,'r',encoding='utf8') as f: t=json.load(f)
    coll=bpy.data.collections.new('SCR_TRACK')
    bpy.context.scene.collection.children.link(coll)
    roadmat=_mat('SCR_Road',(0.20,0.20,0.20,1.0))
    marker=_mat('SCR_Start',(0.8,0.8,0.8,1.0))
    for p in t['pieces']:
        x=p['grid_x']*cube_size; z=p['grid_z']*cube_size
        y=(p['left_y_shift']+p['right_y_shift'])*0.5*height_scale
        # Preview prism only: native template/profile data remains in properties.
        bpy.ops.mesh.primitive_cube_add(location=(x,y,z), scale=(preview_width/2,0.10,cube_size*0.35))
        o=bpy.context.object; o.name=f"SCR_piece_{p['index']:03d}_tpl_{p['template']:02d}"
        # Amiga rough quadrant plus optional extra 180 degrees.
        deg=p['angle_quadrant']*90 + (180 if p['rotate_180'] else 0)
        o.rotation_euler[2]=math.radians(-deg)
        for k,v in p.items(): o['scr_'+k]=v
        o['scr_native_format']='Stunt Car Racer 804-byte track'
        o.data.materials.append(marker if p['index']==t['start_piece'] else roadmat)
        # move object into dedicated collection
        for c in list(o.users_collection): c.objects.unlink(o)
        coll.objects.link(o)
    coll['scr_num_pieces']=t['num_pieces']; coll['scr_start_piece']=t['start_piece']
    coll['scr_standard_boost']=t['standard_boost']; coll['scr_super_boost']=t['super_boost']
    return coll
