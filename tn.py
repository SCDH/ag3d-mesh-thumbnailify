import  bpy
import  re
import  sys
import  argparse
from    itertools   import dropwhile
from    os          import access, R_OK, getcwd, listdir
from    os.path     import isfile
from    pathlib     import Path

def die(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    exit(42)

### Blender helper functions ###

def blender_delete_all_objects():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True, confirm=False)
    if len(bpy.context.scene.objects) != 0:
        die(f'Unable to clean up scene.')

def blender_import_scene_obj(filename):
    bpy.ops.import_scene.obj(filepath=filename)
    olen = len(bpy.data.objects)
    if olen == 0:
        die('No objects found.')
    elif olen > 1:
        die(f'Don\'t know what to do with these objects: '
            + str(bpy.data.objects.keys()))
    return bpy.data.objects.values()[0]

def blender_decimate(obj, percent):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers['Decimate'].ratio = percent / 100
    bpy.ops.object.modifier_apply(modifier='Decimate')

def blender_export(purename):
    filename = f'{purename}_thumbnail.'
    if not args.obj: # GLB (default)
        filename += 'glb'
        bpy.ops.export_scene.gltf(filepath=filename)
    else: # OBJ
        filename += 'obj'
        bpy.ops.export_scene.obj(filepath=filename)
    return filename

### Helper function to decimate a single OBJ file

def single_file(filename, percent=10):

    # Check filename
    if not isfile(filename) or not access(filename, R_OK):
        die(f'The OBJ file {args.obj_filename} doesn\'t seem to be readable.')

    # Prepare
    match = re.match(r'^(.*)\.obj$', filename, flags=re.IGNORECASE)
    if match:
        obj_purename = match.group(1)
    else:
        die(f'Doesn\'t look like a OBJ file: {args.obj_filename}.')
    print(f'###### Working with "{obj_purename}"...')

    # Let blender do all the work
    blender_delete_all_objects()
    obj = blender_import_scene_obj(filename)
    blender_decimate(obj, args.percent)
    export_filename = blender_export(obj_purename)

    # Done
    print(f'Done ({export_filename})')

### Prepare command line interface ###

arg_parser = argparse.ArgumentParser(prog='mesh-thumbnailify',
    description='Creates thumbnail versions of OBJ files with reduced meshes')
arg_parser.add_argument('--percent', type=int, default=10,
    help='Rate of decimate in percent (/100)')
arg_parser.add_argument('--obj', action='store_true', default=False,
    help='Store thumbnails in OBJ format instead of GLB')
arg_parser.add_argument('--all', action='store_true', default=False,
    help='Work on all OBJ files without a "thumbnail" name in the current directory')
arg_parser.add_argument('obj_filename', nargs='?', default=None)

### Let the work begin

# Parse args without everything before '--' (call from docker)
pyargs  = list(dropwhile(lambda arg: arg != '--', sys.argv))[1:]
args    = arg_parser.parse_args(pyargs)

# Work on all files
if args.all:
    for fn in listdir(getcwd()):
        if not fn.lower().endswith('.obj') or '_thumbnail' in fn:
            continue
        single_file(fn, percent=args.percent)

# Work on a single file
else:
    if args.obj_filename is None:
        die("No filename or --all option given")
    single_file(args.obj_filename, percent=args.percent)
