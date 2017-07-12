import re
import os
import sys
import time
import tqdm
from multiprocessing import Pool
from multiprocessing import cpu_count
from multiprocessing import freeze_support


RTINSECONDS = "(.*)(RTINSECONDS=)(\d{0,})(.*)"
RT = "(<group id=.*rt=\")(\d{0,})(.*)"

def main(in_arg):
	start_time = time.time()

	#convert a single file
	if os.path.isfile(in_arg) and in_arg.endswith(".xml"):
		print "Converting: " + str(in_arg)
		convert_rt(in_arg)
		print "\nFinished!\n"
		print "Time: " + str(time.time() - start_time) + " seconds"

	#convert all the .XML files in a directory
	elif os.path.isdir(in_arg):
		in_files = [file for file in get_absolute_file_paths(in_arg) if file.endswith(".xml")]
		print "Converting " + str(len(in_files)) + " files:"
		
		#spawn subprocesses equal to the number of CPU cores 
		pool = Pool(processes=cpu_count())
		for _ in tqdm.tqdm(pool.imap_unordered(convert_rt, in_files), total=len(in_files), bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"):
			pass

		print "\nFinished!\n"
		print "Time: " + str(time.time() - start_time) + " seconds"

	else:
		print "File or directory not found."

def convert_rt(in_filename):
	regex_rt_in_seconds = re.compile(RTINSECONDS)
	regex_rt = re.compile(RT)

	with open(in_filename) as in_file:
		in_file_lines = list(in_file)

	out_filename = create_out_filename_from_in_filename(in_filename)
	with open(out_filename, "w+") as out_file:	
		previous_percentage_complete = 0
		for line in in_file_lines:
			rt_in_seconds_result = re.search(regex_rt_in_seconds, line)
			rt_result = re.search(regex_rt, line)

			#check if the line is RTINSECONDS
			if rt_in_seconds_result:
				rt_prefix = rt_in_seconds_result.group(1)
				rt_in_seconds_value = rt_in_seconds_result.group(3)
				rt_suffix = rt_in_seconds_result.group(4)
				
				if len(rt_in_seconds_value) != 0:
					rt_in_minutes_value = convert_seconds_to_minutes(rt_in_seconds_value)
					out_file.write(rt_prefix + "RTINMINUTES=" + rt_in_minutes_value + rt_suffix + "\n")
				else:
					out_file.write(line)

			#check if the line has an rt value
			elif rt_result:
				rt_prefix = rt_result.group(1)
				rt_value = rt_result.group(2)
				rt_suffix = rt_result.group(3)
				
				if len(rt_value) != 0:
					rt_value_in_minutes = convert_seconds_to_minutes(rt_value)
					out_file.write(rt_prefix + rt_value_in_minutes + rt_suffix + "\n")
				else:
					out_file.write(line)

			# if not modifying a line, just write it out
			else:
				out_file.write(line)

def create_out_filename_from_in_filename(in_filename):
	dot_index = in_filename.index(".")
	out_filename = in_filename[:dot_index] + ".xtan" + in_filename[dot_index:]
	return out_filename

def get_absolute_file_paths(in_directory):
	for root, dirs, files in os.walk(os.path.abspath(in_directory)):
		return [os.path.join(root, file) for file in files]

#takes a string and returns a string w/ 2 decimal places
def convert_seconds_to_minutes(seconds):
	return "%.2f" % (float(seconds)/60)

if __name__ == "__main__":
	freeze_support()
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print "Converter only accepts one file or directory as input."
	raw_input("press ENTER to exit")
