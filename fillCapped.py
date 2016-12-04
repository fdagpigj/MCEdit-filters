import time # for timing
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

displayName = "Fill Underneath"

inputs = (
		("Fill blocks underneath", alphaMaterials[201, 0]),#purpur
		("with", alphaMaterials[201, 0]),
		("Break at non-air", True)
)


def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)


def perform(level, box, options):
	underneath = options["Fill blocks underneath"]
	blockToPlace = options["with"]
	breakAtNonAir = options["Break at non-air"]
	
	method = "FillUnderneath"
	print '%s: Started at %s' % (method, time.ctime())	

	cap = (underneath.ID, underneath.blockData)
	materialToPlace = (blockToPlace.ID, blockToPlace.blockData)


	for iterY in xrange(box.maxy-1,box.miny-1,-1): #Height, from high to low
		for iterZ in xrange(box.minz,box.maxz): #Depth
			for iterX in xrange(box.minx,box.maxx): #Width
				tempBlock = ( level.blockAt(iterX, iterY+1, iterZ), level.blockDataAt(iterX, iterY+1, iterZ) )
				if tempBlock in (cap, materialToPlace):
					if breakAtNonAir == False or level.blockAt(iterX, iterY, iterZ) == 0:
						setBlock(level, materialToPlace, iterX, iterY, iterZ)


	print '%s: Ended at %s' % (method, time.ctime())
	level.markDirtyBox(box)
