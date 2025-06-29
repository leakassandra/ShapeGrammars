import bpy
import math
from mathutils import Vector, Matrix, Euler
from math import radians

'''
Implementation of Rule 1.
'''
def rule_01():
    # path to .blend file to get the shape for rule 1
    filepath = "shapes/shape_voc.blend"
    object_name = "shape_01" # name of the shape in that base-file

    # append the object to this file
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects.append(object_name)

    # link object to this scene
    obj = bpy.data.objects[object_name]
    bpy.context.collection.objects.link(obj)
    
    return obj


'''
Implementation of Rule 2.
'''
def rule_02():
    # path to .blend fileto get the shape for rule 2
    filepath = "shapes/shape_voc.blend"
    object_name = "window"
    # append the object
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects.append(object_name)
    # link object to scene
    obj = bpy.data.objects[object_name]
    bpy.context.collection.objects.link(obj)
    obj.keyframe_insert(data_path="hide_render", frame=10)

    # store references to the objects in variables
    shape_obj = bpy.data.objects["shape_01"]
    window_obj = bpy.data.objects["window"]

    # make sure both objects are visible and selectable before modifying
    shape_obj.hide_set(False)
    window_obj.hide_set(False)
    shape_obj.select_set(True)
    window_obj.select_set(True)

    # add boolean modifier to shape_01 to cut out the window with the cylinder
    bool_mod = shape_obj.modifiers.new(name="Window_Cutout", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE' # by using the difference
    bool_mod.object = window_obj
    # set shape_01 as the active object
    bpy.context.view_layer.objects.active = shape_obj
    # apply the modifier
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    # delete the cylinder "window"
    bpy.data.objects.remove(window_obj, do_unlink=True)
    
    return shape_obj

'''
Implementation of Rule 3.
'''
def rule_03(original_name):
    # get the current object (shape_2)
    original = bpy.data.objects.get(original_name)
    # deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # duplicate that object
    original.select_set(True)
    bpy.context.view_layer.objects.active = original
    bpy.ops.object.duplicate()
    duplicate = bpy.context.active_object # new object called "duplicate"

    # mirror the duplicate along the x-axis 
    duplicate.scale.x *= -1 
    bpy.ops.object.transform_apply(scale=True) # apply

    # apply specific rotation to the duplicate
    duplicate.rotation_euler[2] = radians(-51)  # rotate 51 degred around z-axis
    
    # join the two objects
    bpy.ops.object.select_all(action='DESELECT')
    original.select_set(True)
    duplicate.select_set(True)
    bpy.context.view_layer.objects.active = original
    bpy.ops.object.join()
    
    original.name = "shape_r03"
    return original.name

'''
Implementation of Rule 4.
'''
def rule_04(shape,n):
    # get the just generated shape
    the_shape = bpy.data.objects.get(shape)
    bpy.ops.object.select_all(action='DESELECT')
    the_shape.select_set(True)
    bpy.context.view_layer.objects.active = the_shape
    
    # duplicate that shape
    bpy.ops.object.duplicate()
    duplicate = bpy.context.active_object
    
    # mirror the duplicate along the x-axis 
    mirror_matrix = Matrix.Scale(-1, 4, Vector((1, 0, 0)))  # Scale -1 on global x
    duplicate.matrix_world = mirror_matrix @ duplicate.matrix_world
    
    # select generated shape and duplicate
    bpy.ops.object.select_all(action='DESELECT')
    the_shape.select_set(True)
    duplicate.select_set(True)
    bpy.context.view_layer.objects.active = the_shape
    
    # join the two objects
    bpy.ops.object.join()
    
    # apply a global z-axis rotation of 51 (as often as rule applied)
    angle_rad = n * radians(-51)
    loc = the_shape.location.copy()
    scale = the_shape.scale.copy()
    rot_z = Euler((0, 0, angle_rad), 'XYZ').to_matrix().to_4x4()
    new_matrix = Matrix.Translation(loc) @ rot_z @ Matrix.Diagonal(scale).to_4x4()
    the_shape.matrix_world = new_matrix
    
    the_shape.name = "shape_r04"
    return the_shape.name


'''
Implementation of Rule 5.
'''
def rule_05(shape):
    # path to .blend file and object name
    filepath = "shapes/shape_voc.blend"
    object_name = "side_02"
    # append the object from the .blend file
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects.append(object_name)
    # link the imported object to the current collection
    obj = bpy.data.objects[object_name]
    bpy.context.collection.objects.link(obj)

    # get the already existing object
    the_shape = bpy.data.objects.get(shape)

    # deselect all, then select both objects
    bpy.ops.object.select_all(action='DESELECT')
    the_shape.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = the_shape

    # join the imported object into the existing one
    bpy.ops.object.join()
    # turn object again so that the end position is at arrow again
    angle_rad = -3.20139
    loc = the_shape.location.copy()
    scale = the_shape.scale.copy()
    rot_z = Euler((0, 0, angle_rad), 'XYZ').to_matrix().to_4x4()
    new_matrix = Matrix.Translation(loc) @ rot_z @ Matrix.Diagonal(scale).to_4x4()
    the_shape.matrix_world = new_matrix
    
    the_shape.name = "shape_r05"
    return the_shape.name


def rule_05_2(sname):
    # Path to .blend file and object name
    filepath = "shapes/shape_voc.blend"
    object_name = "side_01"

    # Append the object from the .blend file
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects.append(object_name)
        else:
            print(f"Object {object_name} not found in {filepath}")
            return

    # Link the imported object to the current collection
    obj = bpy.data.objects[object_name]
    bpy.context.collection.objects.link(obj)

    # Get the existing object
    the_shape = bpy.data.objects.get(sname)
    if not the_shape:
        print(f"Object {sname} not found.")
        return
    
    angle_rad = radians(83.4)
    loc = obj.location.copy()
    scale = obj.scale.copy()
    rot_z = Euler((0, 0, angle_rad), 'XYZ').to_matrix().to_4x4()
    new_matrix = Matrix.Translation(loc) @ rot_z @ Matrix.Diagonal(scale).to_4x4()
    obj.matrix_world = new_matrix

    # Deselect all, then select both objects
    bpy.ops.object.select_all(action='DESELECT')
    the_shape.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = the_shape
    
    # Join the imported object into the existing one
    bpy.ops.object.join()
    the_shape.name = "shape_r05"
    return the_shape.name

'''
Implementation of Rule 6.
'''
def rule_06(the_shape):
    # Path to .blend file and object name
    filepath = "shapes/shape_voc.blend"
    object_name = "cube" # get the cube object
    # append the object from the .blend file
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects.append(object_name)
    # link the imported object to the current collection
    obj = bpy.data.objects[object_name]
    bpy.context.collection.objects.link(obj)

    # get the already existing object
    the_shape = bpy.data.objects.get(the_shape)

    # deselect all, then select both objects
    bpy.ops.object.select_all(action='DESELECT')
    the_shape.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = the_shape

    # join the imported object into the existing one
    bpy.ops.object.join()
    
    # rotate the whole object again
    angle_rad = 1.51093
    loc = the_shape.location.copy()
    scale = the_shape.scale.copy()
    rot_z = Euler((0, 0, angle_rad), 'XYZ').to_matrix().to_4x4()
    new_matrix = Matrix.Translation(loc) @ rot_z @ Matrix.Diagonal(scale).to_4x4()
    the_shape.matrix_world = new_matrix
    
    the_shape.name = "shape_r06"
    return the_shape.name

'''
Implementation of Rule 7.
'''
def rule_07(cur_obj):
    # ensure object is selected and active
    bpy.ops.object.select_all(action='DESELECT')
    cur_obj.select_set(True)
    bpy.context.view_layer.objects.active = cur_obj
    # apply location, rotation, and scale
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    # get current global Z location
    current_z = cur_obj.matrix_world.translation.z

    # define desired global position
    target_position = Vector((-2.216, -2.213, current_z))
    # set the object's global position
    cur_obj.matrix_world.translation = target_position
    # set origin to 3D cursor 
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return cur_obj

'''
Implementation of Rule 8 (x-axis).
'''
def rule_08_x(cur_obj):
    # ensure object is selected and active
    bpy.ops.object.select_all(action='DESELECT')
    cur_obj.select_set(True)
    bpy.context.view_layer.objects.active = cur_obj
    # duplicate object
    bpy.ops.object.duplicate()
    duplicate = bpy.context.active_object
    
    # mirror the duplicate along the x-axis 
    mirror_matrix = Matrix.Scale(-1, 4, Vector((1, 0, 0)))  # scale -1 on global X
    duplicate.matrix_world = mirror_matrix @ duplicate.matrix_world
    # select original and duplicate objects
    cur_obj.select_set(True)
    duplicate.select_set(True)
    bpy.context.view_layer.objects.active = cur_obj
    # join the objects
    bpy.ops.object.join()

    return cur_obj

def rule_08_y(cur_obj):
    # Ensure object is selected and active
    bpy.ops.object.select_all(action='DESELECT')
    cur_obj.select_set(True)
    bpy.context.view_layer.objects.active = cur_obj
    
    bpy.ops.object.duplicate()
    duplicate = bpy.context.active_object
    
    # Mirror the duplicate along the Y-axis (in place, local geometry flipped)
    mirror_matrix = Matrix.Scale(-1, 4, Vector((0, 1, 0)))  # Scale -1 on global X
    duplicate.matrix_world = mirror_matrix @ duplicate.matrix_world
    
    cur_obj.select_set(True)
    duplicate.select_set(True)
    
    bpy.context.view_layer.objects.active = cur_obj
    
    bpy.ops.object.join()

    return cur_obj


def rule_08_z(cur_obj, times):
    # Ensure object is selected and active
    bpy.ops.object.select_all(action='DESELECT')
    cur_obj.select_set(True)
    bpy.context.view_layer.objects.active = cur_obj
    
    bpy.ops.object.duplicate()
    duplicate = bpy.context.active_object
    
    # Mirror the duplicate along the Y-axis (in place, local geometry flipped)
    mirror_matrix = Matrix.Scale(-1, 4, Vector((0, 0, 1)))  # Scale -1 on global X
    duplicate.matrix_world = mirror_matrix @ duplicate.matrix_world
    
    cur_obj.select_set(True)
    duplicate.select_set(True)
    
    bpy.context.view_layer.objects.active = cur_obj
    
    bpy.ops.object.join()
    
    # set up by 1.04587m (height of the object)
    cur_obj.location.z += (times * 1.04587)
    
    # Set origin to 3D cursor 
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return cur_obj

'''
Ceation of the corpus of St. Josephs Hopital
'''
def generate_hospital():
    s1 = rule_01()
    s2 = rule_02()
    s3 = rule_03(s2.name)
    s4 = rule_04(s3,1)
    s4_2 = rule_04(s4,3)
    s5 = rule_05(s4_2)
    s6 = rule_06(s5)
    s7 = rule_05_2(s6)
    s7_2 = rule_07(bpy.data.objects[s7])
    s8 = rule_08_x(s7_2)
    s9 = rule_08_y(s8)
    s10 = rule_08_z(s9,1)
    s11 = rule_08_z(s10,2)
    s12 = rule_08_z(s11,3)

generate_hospital()
    
