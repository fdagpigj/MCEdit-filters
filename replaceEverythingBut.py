import time # for timing
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

displayName = "Replace Everything But"

inputs = (
		("Replace everything but", alphaMaterials[9, 0]),#still water
		("With", alphaMaterials[0, 0]),#air
		("Ignore data value", False)
)


def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
    	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)


def perform(level, box, options):
	blockToAvoid = options["Replace everything but"]
	blockToPlace = options["With"]
	ignoreData = options["Ignore data value"]
	
	method = "ReplaceEverythingBut"
	print '%s: Started at %s' % (method, time.ctime())	

	materialToAvoid = (blockToAvoid.ID, blockToAvoid.blockData)
	materialToPlace = (blockToPlace.ID, blockToPlace.blockData)


	for iterY in xrange(box.miny,box.maxy): #Height
		for iterZ in xrange(box.minz,box.maxz): #Depth
			for iterX in xrange(box.minx,box.maxx): #Width
				if ignoreData == False:
					tempBlock = ( level.blockAt(iterX, iterY, iterZ), level.blockDataAt(iterX, iterY, iterZ) )
					if tempBlock != materialToAvoid:
						setBlock(level, materialToPlace, iterX, iterY, iterZ)
				else:
					if level.blockAt( iterX, iterY, iterZ) != blockToAvoid.ID:
						setBlock(level, materialToPlace, iterX, iterY, iterZ)


	print '%s: Ended at %s' % (method, time.ctime())
	level.markDirtyBox(box)
