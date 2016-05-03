# -*- coding: UTF-8 -*-
"""
	Jinda Han @ April 18, 2016
	paper venue info text extractor
"""
# directory
filename = "publications.txt"

# open the file
file_open = open(filename,"r")
file_out_paper_id = open("pub_out_paper_id.txt","w")
file_out_paperid_author = open("pub_out_paperid_author.txt","w")
file_out_paperid_citpaper = open("pub_out_paperid_citpaper.txt","w")
file_out_paperid_venues = open("pub_out_paperid_venues.txt","w")
file_out_paperid_year = open("pub_out_paperid_year.txt","w")

# para
curr_paper = ""
curr_paper_id = ""
authors = []
citespapers = []
curr_venue = ""
curr_year = ""

# venue of conferece list
venues = ["EDBT","SDM","ICDE","CIKM","VLDB","PODS","PAKDD","PKDD","ECIR","SIGIR","WWW","SIGMOD Conference", "ICDM", "KDD", "WSDM"]

for num, line in enumerate(file_open):
	#print num
	#print line

	# paperTitle
	if "#*" in line:
		line = line.split("#*")
		curr_paper = line[1]
		print curr_paper
		# print line[1]

	# authors
	if "#@" in line:
		temp = line.split("\r")
		line = temp[0].split("#@")

		# if multi authors
		if "," in line[1]:
			author_names = line[1].split(",")

			for each_author in author_names:
				# print each_author
				authors.append(each_author)
		# if single authors
		else:
			authors.append(line[1])
			# print line[1]

	#year
	if "#t" in line:
		temp = line.split("\r")
		line = temp[0].split("#t")
		#print line[1]
		curr_year = line[1]

	# publications venue or conferences
	if "#c" in line:
		temp = line.split("\r")
		line = temp[0].split("#c")
		# if line[1] in venues:
		# 	print line[1]
		if line[1] in venues: # if in venues list, then
			curr_venue = line[1]

	# paper ID
	if "#index" in line:
		line = line.split("#index")
		# print line[1]
		curr_paper_id = int(line[1])
		# print curr_paper_id

	# connect other ID
	if "#%" in line:
		line = line.split("#%")
		if len(line[1]) > 3: # there will be something in len(3), avoid it
			print line[1]
			citespapers.append(line[1])

	# end
	if "#!" in line:
		print "------------ end paper -----------"

		#only print in venue list's paper
		if curr_venue != "":

			# paperid - paper
			file_out_paper_id.write(str(curr_paper_id)+"\t"+curr_paper)
			# print str(curr_paper_id)+"\t"+curr_paper

			# paperid - author
			for each_author in authors:
				file_out_paperid_author.write(str(curr_paper_id)+"\t"+each_author+"\n")
				# print str(curr_paper_id)+"\t"+each_author

			# paperid - citespapers
			if citespapers: #if not empty
				for each_citpaper in citespapers:
					if each_citpaper != "":
						print str(curr_paper_id)+"\t"+each_citpaper
						file_out_paperid_citpaper.write(str(curr_paper_id)+"\t"+each_citpaper)

			# papaerid - venue
			if curr_venue != "":
				print str(curr_paper_id)+"\t"+curr_venue
				file_out_paperid_venues.write(str(curr_paper_id)+"\t"+curr_venue+"\n")

			# paperid - year
			print str(curr_paper_id)+"\t"+curr_year
			file_out_paperid_year.write(str(curr_paper_id)+"\t"+curr_year+"\n")


		# end of paper and clean the variables
		curr_paper = ""
		curr_paper_id = ""
		authors = []
		citespapers = []
		curr_venue = ""
		curr_year = ""



file_open.close
file_out_paper_id.close
file_out_paperid_author.close
file_out_paperid_citpaper.close
file_out_paperid_venues.close
file_out_paperid_year.close

