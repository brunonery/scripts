#!BPY

"""
Name: 'MiniLight format (.ml.txt)...'
Blender: 249
Group: 'Export'
Tooltip: 'Export selected mesh to MiniLight format (ml.txt)'
"""

__author__ = "Bruno Nery"
__url__ = ("blender", "blenderartists.org",
"Author's homepage, http://brunonery.com")
__version__ = "1.0.0"

# TODO(brunonery): Convert meshes to triangles automatically.
__bpydoc__ = """\
This script exports triangle meshes to the MiniLight file format. For more
information on MiniLight and its format, check http://www.hxa.name/minilight/.
This script is based on the 'Raw faces' script by Anthony D'Agostino (Scorpius).

Usage:
   Convert meshes to be exported to triangles (in 'Edit Mode', select Mesh, then
   Faces, then Convert Quads to Triangles).
   Select meshes to be exported and run this script from "File->Export" menu.
"""

import Blender
import BPyMesh

# TODO(brunonery): Make parameters selectable.
DEFAULT_COLOR = (0.7, 0.0, 0.0)
DEFAULT_REFLECTIVITY = (0.0, 0.0, 0.0)
DEFAULT_ITERATIONS = 1
DEFAULT_RESOLUTION = (100, 100)
DEFAULT_CAMERA = (0.0, 0.0, -20.0, 0, 0, 1, 0)
DEFAULT_SKY_AND_GROUND = (3626, 5572, 5802, 0.1, 0.09, 0.07)

def write(filename):
	start = Blender.sys.time()
	if not filename.lower().endswith('.ml.txt'):
		filename += '.ml.txt'
	
	scn= Blender.Scene.GetCurrent()
	ob= scn.objects.active
	if not ob:
		Blender.Draw.PupMenu('Error%t|Select 1 active object')
		return
	
	file = open(filename, 'wb')
	
	mesh = BPyMesh.getMeshFromObject(ob, None, True, False, scn)
	if not mesh:
		Blender.Draw.PupMenu('Error%t|Could not get mesh data from active object')
		return
	
	mesh.transform(ob.matrixWorld)
	
	with open(filename, "w") as ml_file:
		ml_file.write('#MiniLight\n')
		ml_file.write('%d\n' % DEFAULT_ITERATIONS)
		ml_file.write('%d %d\n' % DEFAULT_RESOLUTION)
		ml_file.write('(%.2f %.2f %.2f) (%.2f %.2f %.2f) %.2f\n' % DEFAULT_CAMERA)
		ml_file.write('(%.2f %.2f %.2f) (%.2f %.2f %.2f)\n' % DEFAULT_SKY_AND_GROUND)
		
		for f in mesh.faces:
			if len(f) != 3:
				Blender.Draw.PupMenu('Error%t|Non-triangular face found in mesh')
				return
			for v in f:
				ml_file.write('(%.6f %.6f %.6f) ' % tuple(v.co))
			ml_file.write('(%.6f %.6f %.6f) ' % DEFAULT_COLOR)
			ml_file.write('(%.6f %.6f %.6f)\n' % DEFAULT_REFLECTIVITY)
	
	end = Blender.sys.time()
	message = 'Successfully exported "%s" in %.4f seconds' % ( Blender.sys.basename(filename), end-start)
	print message


def main():
	Blender.Window.FileSelector(write, 'ML Export', Blender.sys.makename(ext='.ml.txt'))

if __name__=='__main__':
	main()
