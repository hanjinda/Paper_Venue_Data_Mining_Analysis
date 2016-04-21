# -*- coding: UTF-8 -*-
"""
	Jinda Han @ April 21, 2016
	author text extractor
"""
# open file
filename_input = "pub_out_paperid_author.txt"
filename_output = "pub_out_authers.txt"

# open files
file_open = open(filename_input, "r")
file_out = open(filename_output, "w")

#paras
author_list = []

for num, line in enumerate(file_open):
	line = line.split("\t")

	# print line[1]
	if line[1] in author_list:
		continue
	else:
		author_list.append(line[1])
		print line[1]

for line in author_list:
	file_out.write(line)


file_open.close
file_out.close

