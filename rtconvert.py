import re, os, sys

RTINSECONDS = "(.*)(RTINSECONDS=)(\d{0,})(.*)"
RT = "(<group id=.*rt=\")(\d{0,})(.*)"

def main(in_filename):
	out_filename = create_out_filename_from_in_filename(in_filename)

	if os.path.isfile(out_filename):
		print "Output file for " + in_filename + " already exists in this location"
		return

	regex_rt_in_seconds = re.compile(RTINSECONDS)
	regex_rt = re.compile(RT)

	with open(in_filename) as in_file, open(out_filename, "w+") as out_file:
		for line in in_file:
			#check if the line is RTINSECONDS
			rt_in_seconds_result = re.search(regex_rt_in_seconds, line)
			if rt_in_seconds_result:
				rt_prefix = rt_in_seconds_result.group(1)
				rt_in_seconds_value = rt_in_seconds_result.group(3)
				rt_suffix = rt_in_seconds_result.group(4)
				
				if len(rt_in_seconds_value) != 0:
					rt_in_minutes_value = convert_seconds_to_minutes(rt_in_seconds_value)
					out_file.write(rt_prefix + "RTINMINUTES=" + rt_in_minutes_value + rt_suffix + "\n")
				else:
					out_file.write(line)
				continue

			#check if the line has an rt value
			rt_result = re.search(regex_rt, line)
			if rt_result:
				rt_prefix = rt_result.group(1)
				rt_value = rt_result.group(2)
				rt_suffix = rt_result.group(3)
				
				if len(rt_value) != 0:
					rt_value_in_minutes = convert_seconds_to_minutes(rt_value)
					out_file.write(rt_prefix + rt_value_in_minutes + rt_suffix + "\n")
				else:
					out_file.write(line)
				continue

			# if not modifying a line, just write it out
			else:
				out_file.write(line)

	print "Converted " + in_filename + " to " + out_filename
	

def create_out_filename_from_in_filename(in_filename):
	dot_index = in_filename.index(".")
	out_filename = in_filename[:dot_index] + ".xtan" + in_filename[dot_index:]
	return out_filename

#takes a string and returns a string w/ 2 decimal places
def convert_seconds_to_minutes(seconds):
	return "%.2f" % (float(seconds)/60)

if __name__ == "__main__":
	if len(sys.argv) == 2 and sys.argv[1].endswith(".xml"):
		main(sys.argv[1])
	else:
		print "Converter only accepts one .xml file as input"
	raw_input("press ENTER to exit")