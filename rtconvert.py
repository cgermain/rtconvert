import re, os, sys

RTINSECONDS = "(.*)(RTINSECONDS=)(\d{0,})(.*)"
RT = "(<group id=.*rt=\")(\d{0,})(.*)"

def main(in_filename):
	if not os.path.isfile(in_filename):
		print in_filename + " is not a file."
		return

	out_filename = create_out_filename_from_in_filename(in_filename)

	if os.path.isfile(out_filename):
		print "Output file for " + in_filename + " already exists in this location."
		return

	regex_rt_in_seconds = re.compile(RTINSECONDS)
	regex_rt = re.compile(RT)

	total_line_count = buffered_line_count(in_filename)
	current_line_count = 0

	print "Converting " + in_filename + "\n" 

	with open(in_filename) as in_file, open(out_filename, "w+") as out_file:
		previous_percentage_complete = 0
		for line in in_file:
			current_line_count+=1

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

			percentage_complete = 100*current_line_count/total_line_count

			if percentage_complete > previous_percentage_complete:
				previous_percentage_complete = percentage_complete
				print "total lines: " + str(total_line_count) + "  |  current line: " + str(current_line_count) + "  |  percentage complete: " + str(percentage_complete) + "%\r",
				sys.stdout.flush()

	print "\nFinished!\n"
	print "Converted " + in_filename + " to " + out_filename + "\n"
	
def create_out_filename_from_in_filename(in_filename):
	dot_index = in_filename.index(".")
	out_filename = in_filename[:dot_index] + ".xtan" + in_filename[dot_index:]
	return out_filename

def buffered_line_count(filename):
    f = open(filename)                  
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    return lines\

#takes a string and returns a string w/ 2 decimal places
def convert_seconds_to_minutes(seconds):
	return "%.2f" % (float(seconds)/60)

if __name__ == "__main__":
	if len(sys.argv) == 2 and sys.argv[1].endswith(".xml"):
		main(sys.argv[1])
	else:
		print "Converter only accepts one .xml file as input."
	raw_input("press ENTER to exit")
