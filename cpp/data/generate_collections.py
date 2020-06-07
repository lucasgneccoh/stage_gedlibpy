path_orig = "/home/lucas/Documents/stage_gedlibpy/gedlib/gedlib/data/collections"

path_dest = "/home/lucas/Documents/stage_gedlibpy/stage/cpp/data/collections"

file_orig = "Letter.xml"

file_dest = "Letter_{0}.xml"

classes = ["A", "E", "F", "H", "I", "K", "L", "M", "N", "T","V","W","X", "Y","Z"]

for cl in classes:
	with open(path_orig + "/" + file_orig, "r") as f_orig:
		with open(path_dest + "/" + file_dest.format(cl), "w") as f_dest:
			line = f_orig.readline()
			while(line):
				if "<graph file=" in line:
					if "class=\"" + cl + "\"" in line:
						f_dest.write(line)
				else:
					f_dest.write(line)
				line = f_orig.readline()
			f_dest.close()
		f_orig.close()
