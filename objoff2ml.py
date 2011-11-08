# Add Blender scripts to path so that import/export functions are available.
import sys
sys.path.append('/usr/share/blender/scripts/blender')

import Blender
import import_obj
import minilight_export
import off_import
import os
import sys

HELP = """Import a OBJ/OFF file into Blender and exports it as a MiniLight file.

Usage:
    filename=<filename> blender -P objoff2ml.py
"""

if __name__ == '__main__':
    filename = os.getenv('filename')
    if filename is None:
        print HELP
    else:
        scene = Blender.Scene.GetCurrent()
        # Blender's default view has a cube. This script cannot be run in batch
        # (-b) mode because Blender cannot join objects there.
        print 'Removing default cube...'
        scene.objects.unlink((o for o in scene.objects if o.name == 'Cube').next())
        print 'Importing model...'
        if filename.endswith('.obj'):
            # Import model from OBJ file.
            import_obj.load_obj(filename)
        elif filename.endswith('.off'):
            # Import model from OFF file.
            off_import.read(filename)
        # Join objects.
        print 'Joining objects...'
        other_objects = [scene.objects[i] for i in range(1, len(scene.objects))]
        scene.objects[0].join(other_objects)
        for o in other_objects:
            scene.objects.unlink(o)
        scene.objects.active = scene.objects[0]
        # Export to MiniLight.
        print 'Exporting model...'
        minilight_export.write(filename + '.ml.txt')
        Blender.Quit()
