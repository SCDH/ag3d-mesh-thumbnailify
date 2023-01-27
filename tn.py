import  bpy
import  re
import  sys
import  argparse
from    itertools   import dropwhile
from    os          import access, R_OK
from    os.path     import isfile

def die(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    exit(42)

### Preparations ###

arg_parser = argparse.ArgumentParser() # TODO customize
arg_parser.add_argument('--percent', type=int, default=10)
arg_parser.add_argument('--obj', action='store_true')
arg_parser.add_argument('obj_filename')
pyargs  = list(dropwhile(lambda arg: arg != '--', sys.argv))[1:]
args    = arg_parser.parse_args(pyargs)

# Deconstruct OBJ file name
match = re.match(r'^(.*)\.obj$', args.obj_filename, flags=re.IGNORECASE)
if match:
    obj_purename = match.group(1)
else:
    die(f'Doesn\'t look like a OBJ file: {args.obj_filename}.')

# Check OBJ file existence
if (not isfile(args.obj_filename)) or (not access(args.obj_filename, R_OK)):
    die(f'The OBJ file {args.obj_filename} doesn\'t seem to be readable.')

### Let the work begin ###

# Delete all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=True, confirm=False)
if len(bpy.context.scene.objects) != 0:
    die(f'Unable to clean up scene.')

# Import scene from OBJ file
bpy.ops.import_scene.obj(filepath=args.obj_filename)
olen = len(bpy.data.objects)
if olen == 0:
    die('No objects found.')
elif olen > 1:
    die(f'Don\'t know what to do with these objects: '
        + str(bpy.data.objects.keys()))
obj = bpy.data.objects.values()[0]

print(f'Decimating object {obj.name}...')

# Decimate
bpy.context.view_layer.objects.active = obj
bpy.ops.object.modifier_add(type='DECIMATE')
bpy.context.object.modifiers['Decimate'].ratio = args.percent / 100
bpy.ops.object.modifier_apply(modifier='Decimate')
print('... Done.')

### Export result ###

export_filename = f'{obj_purename}_thumbnail.'

# GLB (default)
if (not args.obj):
    export_filename += 'glb'
    print(f'Exporting to {export_filename}.')
    bpy.ops.export_scene.gltf(filepath=export_filename)

# OBJ
else:
    export_filename += 'obj'
    print(f'Exporting to {export_filename}.')
    bpy.ops.export_scene.obj(filepath=export_filename)
