import re
import string
import sys
import nltk
from nltk.stem.snowball import SnowballStemmer
from pprint import pprint
from functools import reduce


__author__="Shail Shah"

#Earley Parser code
#--------------------------------------------------------------------------------------------------

def predictor(rule, state):
    return [{
        "lhs": rule["rhs"][rule["dot"]],
        "rhs": rhs,
        "dot": 0,
        "state": state,
        "op": "Predictor",
        "completer": []
    } for rhs in grammar[rule["rhs"][rule["dot"]]]] if rule["rhs"][rule["dot"]].isupper() else []


def scanner(rule, next_input):
    return [{
        "lhs": rule["rhs"][rule["dot"]],
        "rhs": [next_input],
        "dot": 1,
        "state": rule["state"],
        "op": "Scanner",
        "completer": []
    }] if rule["rhs"][rule["dot"]].islower() and next_input in grammar[rule["rhs"][rule["dot"]]] else []


def completer(rule, charts):
    return list(map(
        lambda filter_rule: {
            "lhs": filter_rule["lhs"],
            "rhs": filter_rule["rhs"],
            "dot": filter_rule["dot"] + 1,
            "state": filter_rule["state"],
            "op": "Completer",
            "completer": [rule] + filter_rule["completer"]
        },
        filter(
            lambda p_rule: p_rule["dot"] < len(p_rule["rhs"]) and rule["lhs"] == p_rule["rhs"][p_rule["dot"]],
            charts[rule["state"]]
        )
    )) if rule["dot"] == len(rule["rhs"]) else []

#Earley Parser End
#------------------------------------------------------------------------------------------------------------


#Function to print chart
#------------------------------------------------------------------------------------------------------------
def printCharts(charts, inp):
    i=0
    for chart_no, chart in zip(range(len(charts)), charts):
        print("Chart "+str(chart_no)+"\t\n".join(map(
           lambda x: "\t   {0:>10}  -> {1:<19} {2:^20} {3:^25}".format(
                x["lhs"], 
                " ".join(x["rhs"][:x["dot"]] + ["*"] + x["rhs"][x["dot"]:]),
                "[" + str(x["state"]) + "," + str(chart_no) + "]",
                x["op"]
            ),
            chart
        )))
    
#Print chart function end
#--------------------------------------------------------------------------------------------------------------


#Stemmer Start
#--------------------------------------------------------------------------------------------------------------
def stemKeywords(word,stemmer):
	stemWord=stemmer.stem(word)
	return stemWord;

def checkInputType(token):
	patternOP = re.compile("[.:|;=]")
	patternString=re.compile("[a-zA-Z]+")
	patternInt=re.compile("[0-9]+")
	patternDouble=re.compile("\d[\.]\d")
	if re.search(patternOP,token):
		return token+" OP";
	elif re.search(patternDouble, token):
		return token+" DOUBLE";
	elif re.search(patternInt, token):
		return token+" INT";
	elif re.search(patternString, token):
		return token+" STRING";
	return "";

#Stemmer End
#---------------------------------------------------------------------------------------------------------------


#File reading, input and initial processing code
#--------------------------------------------------------------------------------------------------------------


#Initial processing to read a file and take the input:
#Taking the input from dat file to a temporary text file which will be processed line by line and processed further
#-------------------------------------------------------------------------------------------------------------
f=open("temp.txt","w+")

for line in sys.stdin:
	f.write(line.rstrip()+"\n")

f.close()

with open("temp.txt") as f:
	content = f.readlines()

#Read file complete
#-----------------------------------------

#Tokenize the input and replace a few special characters
#--------------------------------------------------------------------
	
for n,i in enumerate(content):
	s=i.replace(":"," : ")
	s=s.replace("|"," | ")
	s=s.replace("."," .")
	content[n]=s.replace(";"," ; ")

#Printing the input file content
#---------------------------------------------------------------------
print("\n\nInput:")
print("{0:-^50}".format(""))
content = [x.split() for x in content] 
for i in range(0,len(content)):
	print(' '.join(content[i]))


#---------------------------------------------------------------------

#STEMMER-Initializing, conditional check, stemming and printing
#Using snowball stemmer here from NLTK
#--------------------------------------------------------------------

stemmer = SnowballStemmer("english")
print("\n\nStemmer:")
print("{0:-^30}".format(""))
k=1
flag=0
for i in range(0,len(content)):
	for j in range(0,len(content[i])):
		#print(content[i][j])
		output=checkInputType(content[i][j])
		
		#if("->" in content[i] or "-->" in content[i] or "$" in content[i] or "@" in content[i] or "^" in content[i]):
		if("#" in content[i]):
			flag=1
			continue
		if("W" in content[i] and "=" in content[i] and content[i][j]!="."):
			exclude=set(string.punctuation)
			parse_string=''.join(ch for ch in content[i][j] if ch not in exclude).lower()
			output+=" "+stemKeywords(content[i][j],stemmer)
		if(output==""):
			print("\n\n\n\t Invalid Input \n\n\n")
			sys.exit()
		output+=" "+str(k)
		print("\t"+output)
	if(flag==0):
		k+=1
	flag=0
print("\tENDFILE")


#End of stemmer
#----------------------------------------------------------------------


#Earley - Parser begins
#----------------------------------------------------------------------
print("\n\nParsed Chart:")


parse_string=""


#Extract grammar from the input file and store it as a dictionary into "Grammar" variable for parser
#------------------------------------------------------------------------------------------------------
grammar={}
with open("temp.txt") as f:
	line=f.readline()
	tempSplit=str(line)
	content=[]
	while line:
		if(tempSplit.strip().startswith("W")):
			#print('Input found'+ tempSplit)
			parse_string+=tempSplit[tempSplit.index("=")+1:].strip()
			exclude=set(string.punctuation)
			parse_string=''.join(ch for ch in parse_string if ch not in exclude).lower()
			#print("Temp "+parse_string)
		#tempSplit=str(line)
		if("#" in tempSplit):
			tempSplit=f.readline()
			continue;
		if(";" in tempSplit):
			tempSplit=tempSplit.replace(";"," ")
			temp=tempSplit.split(":")
			hello=str(temp[1])
			key=""
			if(any(x.isupper() for x in hello)):
				content=hello.split("|")
				content=[x.strip() for x in content]
				content=[x.split() for x in content]
				for i in content:
					for j in i:
					#Splitting terminals and non terminals here
						if('prep' in j.lower() or 'aux' in j.lower() or 'det' in j.lower() or 'noun' in j.lower() or'verb' in j.lower() or 'proper-noun' in j.lower() or 'pronoun' in j.lower()):
							index_i=content.index(i)
							content[index_i][content[index_i].index(j)]=j.lower()
							
						if(j.upper()=='NOMINAL'):
							index_i=content.index(i)
							content[index_i][content[index_i].index(j)]=j.upper()
				key=temp[0].strip().upper()
				grammar[key]=content
			else:
				
				content=hello.split("|")
				content=[x.strip() for x in content]
				s={}
				s=set(content)
				key=temp[0].lower().strip()
				grammar[key]=content
				
			#print(content)
			content=[]
			tempSplit=""
			tempSplit=f.readline()
			continue;
		line=f.readline()
		tempSplit+=str(line)

charts = [[{
    "lhs": "Root",
    "rhs": ["S"],
    "dot": 0,
    "state": 0,
    "op": "Dummy Start State",
    "completer": []
}]]

#Stem the given input ready for parser:
temp=[]
for words in parse_string.split():
	temp.append(stemKeywords(words,stemmer))

parse_string=' '.join(temp)
print("Stemmed string to be parsed: "+parse_string)
print("{0:-^94}".format(""))
#----------------------------------------------------------------------------------------------

#Parse the given input string
#-----------------------------------------------------------------------------------------------

input_arr =parse_string.split()+[""]

for curr_state in range(len(input_arr)):

    curr_chart = charts[curr_state]
    next_chart = []

    for curr_rule in curr_chart:
        if curr_rule["dot"] < len(curr_rule["rhs"]):
            curr_chart += [i for i in predictor(curr_rule, curr_state) if i not in curr_chart]
            next_chart += [i for i in scanner(curr_rule, input_arr[curr_state]) if i not in next_chart]
        else:
            curr_chart += [i for i in completer(curr_rule, charts) if i not in curr_chart]

    charts.append(next_chart)


printCharts(charts[:-1], input_arr)

print("{0:-^94}".format(""))
#Parser End
#----------------------------------------------------------------------------------------

#Truncate temp file to be ready for next program run
#----------------------------------------------------------------------------------------
f = open('temp.txt', 'r+')
f.truncate()
f.close()

#End of program
#---------------------------------------------------------------------------------------------

