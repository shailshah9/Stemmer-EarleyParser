import re
import nltk
from nltk.stem.snowball import SnowballStemmer

def stemKeywords(word,stemmer):
	stemWord=stemmer.stem(word)
	return stemWord;

def checkInputType(token):
	patternOP = re.compile("[.:|;=]")
	patternString=re.compile("[a-zA-Z]+")
	patternInt=re.compile("[0-9]+")
	patternDouble=re.compile("\d[\.]\d")
	if re.search(patternOP,token):
		return token+" OP";#+str(lineno);
	elif re.search(patternDouble, token):
		return token+" DOUBLE";#+str(lineno);
	elif re.search(patternInt, token):
		return token+" INT";#+str(lineno);
	elif re.search(patternString, token):
		#stemword=stemKeywords(token,stemmer)
		return token+" STRING";
	return "";

with open('t11.dat') as f:
	content = f.readlines()
	#print(f)
	
for n,i in enumerate(content):
	s=i.replace(":"," : ")
	s=s.replace("|"," | ")
	s=s.replace("."," .")
	content[n]=s.replace(";"," ; ")
print("Input:")
content = [x.split() for x in content] 
for i in range(0,len(content)):
	print(' '.join(content[i]))

stemmer = SnowballStemmer("english")
print("Stemmer:")
for i in range(0,len(content)):
	for j in range(0,len(content[i])):
		#print(content[i][j])
		output=checkInputType(content[i][j])
		if("W" in content[i] and "=" in content[i] and content[i][j]!="."):
			output+=" "+stemKeywords(content[i][j],stemmer)
		output+=" "+str(i+1)
		print(output)
print("ENDFILE")

print()
print()
print("Parser:")
#nltk.parse.earleychart.demo(print_times=False, trace=1,sent='book that flight', numparses=2)
