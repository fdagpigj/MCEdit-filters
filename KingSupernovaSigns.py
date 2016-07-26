
import time # for timing
from pymclevel import alphaMaterials, MCSchematic, MCLevel, TAG_String, TAG_Compound, TAG_Int, TAG_Byte
import mcplatform
import json


inputs = [(
		("KingSupernova's /summon ArmorStand Signs", "title"),
		("Require redstone", False),
		("Include Marker:1b,Invisible:1,Invulnerable:1,NoGravity:1", True),
		("Additional tags", ("string", "width=350")),
		("This filter finds all signs in the selected region and if they have a number on the last line, creates a chain command block to summon an armor stand at the sign (or the block the sign is attached to in the case of wall signs) with a CustomName name taken from the first two lines. The output is a schematic file.", "label"),
	)]

def perform(level, box, options):
	#level.markDirtyBox(box) Not needed

	method = "KingSupernova's ArmorStands"
	print '%s: Started at %s' % (method, time.ctime())

	tags = ("Marker:1b,Invisible:1,Invulnerable:1,NoGravity:1," if options["Include Marker:1b,Invisible:1,Invulnerable:1,NoGravity:1"] else "")
	tags += options["Additional tags"]

	command_list = []
	
	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value

			if (x, y, z) in box:
				if e["id"].value == "Sign":
					if level.blockAt(x,y,z) == 68:
						data = level.blockDataAt(x,y,z)
						if data == 2:
							z += 1
						elif data == 3:
							z += -1
						elif data == 4:
							x += 1
						elif data == 5:
							x += -1
					try:
						name = json.loads(e["Text1"].value)["text"] + json.loads(e["Text2"].value)["text"]
						command = "/summon ArmorStand %s %s %s {CustomName:\"%s\",%s}" % (x,y,z, name, tags)
						print(command)
						for i in xrange(int(json.loads(e["Text4"].value)["text"])):
							command_list.append(command)
					except TypeError as error:
						print("Skipping sign at %s %s %s due to TypeError: %s" % (x,y,z, error))

	schematic = MCSchematic((1,1,len(command_list)), mats = level.materials)

	for x_coord, command in enumerate(command_list):
		schematic.setBlockAt(0,0,x_coord,211) #211 is chain command block
		schematic.setBlockDataAt(0,0,x_coord,3) #3 = facing south
		schematic.TileEntities.append(cmdBlockTe(0,0,x_coord,command, not(options["Require redstone"])))

	schematic_file = mcplatform.askSaveFile(mcplatform.lastSchematicsDir or mcplatform.schematicsDir, "Save Schematic As...", "", "Schematic\0*.schematic\0\0", ".schematic")
	if schematic_file == None:
		print "ERROR: No schematic filename provided!"
		return
	schematic.saveToFile(schematic_file)
		
		
	print '%s: Ended at %s' % (method, time.ctime())


def cmdBlockTe(x,y,z,cmd, auto):
	control = TAG_Compound()
	control["Command"] = TAG_String(cmd)
	control["id"] = TAG_String(u'Control')
	control["CustomName"] = TAG_String(u'@')
	control["z"] = TAG_Int(z)
	control["y"] = TAG_Int(y)
	control["x"] = TAG_Int(x)
	control["auto"] = TAG_Byte(auto)
	
	return control

