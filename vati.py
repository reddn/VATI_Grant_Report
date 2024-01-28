
from PyPDF2 import PdfReader 
import re
from decimal import Decimal
import os 



def findTextInArray(arr,t,before=0,after=0,returnIndex= False,ignoreText = False):
	output = []
	t = re.sub("\W+"," ",t).lower()
	for i,a in enumerate(arr):
		textLower = re.sub("\W+"," ",a).lower()
		if t in textLower:
			if ignoreText:
				if ignoreText.lower() in textLower: continue
			if before > 0:
				for ii in range(before,0,-1):
					output.append(arr[i-ii])
			output.append(a)
			if after > 0:
				for ii in range(1,after+1):
					output.append(arr[i+ii])
	if returnIndex != False:
		return output[returnIndex]
	return output
	
def stripNumber(a):
	newTxt = a.replace("$","").replace("(","").replace(",","").replace(")","")
	return newTxt

def runFile(fn,separator):
	# creating a pdf reader object 
	reader = PdfReader(fn) 

	# printing number of pages in pdf file 
	# print(len(reader.pages)) 

	# getting a specific page from the pdf file 
	page = reader.pages[0] 

	# extracting text from page 
	text = page.extract_text() 
	# print(text) 


	textS = text.split("\n")
	
	totalGrantFunding = findTextInArray(textS,"Total Grant Funding",1,returnIndex =1)
	# print(totalGrantFunding)

	grant= findTextInArray(textS,"Total Grant Funding",1,2)
	match = findTextInArray(textS,"Total Match Funding",1,2)
	name = findTextInArray(textS,"back to map",2,0)
	fiberMileage= findTextInArray(textS,"fiber mileage",1,1)
	locations = findTextInArray(textS,"contracted)",2,0,ignoreText = "miles")
	startDate = findTextInArray(textS,"start date",0,1,1)
	endDate  = findTextInArray(textS,"end date",0,1,1)
	projectType = findTextInArray(textS,"broadband project type",0,1)
	if "Wireless" in projectType[1]: #not looking for wireless grants
		print('skipping ' + fn)
		print(name)
		print(projectType)
		print()
		return None
	# print(grant)
	# print(match)
	# print(name)
	# print(fiberMileage)
	# print(locations)
	# print(startDate)
	# print(endDate)
	# print(projectType)
	
	outputA = []
	outputCSV = ""
	
	#name
	# print(name)
	outputA.append(name[0].replace("\t"," ").split(" | ")[0])
	
	#contractor
	outputA.append(name[0].replace("\t"," ").split(" | ")[1])
	
	#fy
	outputA.append(name[1].replace("\t"," "))
		
	#miles
	milesNum = fiberMileage[2].replace("(","").replace(")","").split("\t")[0]
	outputA.append("{:,.0f}".format(int(stripNumber(milesNum))))
	
	# print(milesNum)
	#locations
	locationsText = locations[2].replace("(","").replace(")","").split("\t")[0]
	locationsNum = int(stripNumber( locationsText))
	outputA.append(locationsText)
	
	#start
	outputA.append(re.sub("\s+","",startDate))
	#end
	outputA.append(re.sub("\s+","",endDate).replace(":",""))
	#grant
	outputA.append(grant[2])
	#match
	outputA.append(match[2])
	#grant used
	if "None" in grant[2]:
		grantNum = 0
	else:
		grantNum = float(grant[2].replace("$","").replace(",","") )
	grantUsedPercText = grant[0].split("\t")[0]
	grantUsedPerc = float(grantUsedPercText.replace("%","")) * .01
	outputA.append("${:,.2f}".format(grantNum * grantUsedPerc))
	#match used
	matchNum = float(match[2].replace("$","").replace(",","") )
	matchUsedPercText = match[0].split("\t")[0]
	matchUsedPerc = float(matchUsedPercText.replace("%","")) * .01
	#outputA.append('%.2f' % Decimal(matchNum * matchUsedPerc))
	outputA.append("${:,.2f}".format(Decimal(matchNum * matchUsedPerc)))
	#miles ran
	milesRanPerc = fiberMileage[0].replace("(","").replace(")","").split("\t")[0]
	milesRan = int(milesRanPerc.replace("%","").replace(",","")) * .01 * int(stripNumber(milesNum))
	outputA.append("{:,.0f}".format(milesRan))
	#locations 
	locationsInstalledPerc = locations[0].replace("(","").replace(")","").split("\t")[0]
	locationsInstalledNum = int(locationsInstalledPerc.replace("%","").replace(",","")) * .01 * int(locationsText.replace(",",""))
	outputA.append("{:,.0f}".format(locationsInstalledNum))
	#grant spent %
	outputA.append(grantUsedPercText)
	
	#match spent%
	outputA.append(matchUsedPercText)
	#total $ septn
	totalUsedPerc = grantUsedPerc + matchUsedPerc
	totalUsedPercText = "{:,.0f}%".format(totalUsedPerc)# str(totalUsedPerc * 100 )+ "%"
	outputA.append(totalUsedPercText)
	#fiber ran %
	fiberRanPercText = fiberMileage[0].split("\t")[0]
	outputA.append(fiberRanPercText)
	#locations installed %
	outputA.append(locationsInstalledPerc)
	
	#price per mile
	totalMoneyNum = grantNum + matchNum 
	pricePerMileNum = totalMoneyNum / int(stripNumber( milesNum))
	
	
	outputA.append("${:,.2f}".format(pricePerMileNum) )  
	#grant per mile
	grantPerMile = grantNum / int(stripNumber( milesNum))
	outputA.append("${:,.2f}".format(grantPerMile) )  
	
	#price per location
	if totalMoneyNum == 0 or locationsNum == 0:
		pricePerLocationNum = 0
	else: 
		pricePerLocationNum = totalMoneyNum / locationsNum
	# print(pricePerLocationNum)
	outputA.append("${:,.2f}".format(pricePerLocationNum) )  
	
	#VATI grant per location
	if locationsNum == 0: 
		vatiGrantPerLoc = 0 
	else:
		vatiGrantPerLoc = grantNum/locationsNum
	outputA.append("${:,.2f}".format(vatiGrantPerLoc) )
	
	for ll in outputA:
		outputCSV += str(ll) 		+ separator
	
	# print(outputCSV)
	return outputCSV
	



# runFile("Project.pdf")
separator = "\t"
mainOutput = ""
for f in os.listdir():
	# print(f)
	if ".pdf" in f:
		# thisRun = runFile(f,separator) #use this to actually find the error in runFile.. probably should import/use the traceback library
		try:
			thisRun = runFile(f,separator)
			if thisRun != None:
				if thisRun in mainOutput:
					print("dup file: " + f)
				else:
					mainOutput += thisRun + "\n"
		except Exception as e:
			print("error in " + f )
			print(e)
		
	# print(mainOutput)
print()
print(mainOutput)
mainOutput =  re.sub(r"[^\x00-\x7F]+", "", mainOutput)
fh = open('output.csv','w')
csvHeader = \
"Locality" 				+ separator + \
"ISP" 					+ separator + \
"FY" 					+ separator + \
"Miles Proposed" 		+ separator + \
"Locations Proposed"	+ separator + \
"Start Date" 			+ separator + \
"End Date(orig)" 		+ separator + \
"Grant" 				+ separator + \
"Match" 				+ separator + \
"Grant Used"			+ separator + \
"Match Used"			+ separator + \
"Miles Ran" 			+ separator + \
"Locations Installed" 	+ separator + \
"Grant Spent %" 		+ separator + \
"Match Spent %" 		+ separator + \
"Total Spent %" 		+ separator + \
"Fiber Ran %" 			+ separator + \
"Location installed %" 	+ separator + \
"Cost Per Mile" 		+ separator + \
"Grant per Mile" 		+ separator + \
"Price Per Location" 	+ separator + \
"Grant $ per Location "
fh.write(csvHeader + "\n")
fh.write(mainOutput)
fh.close()
