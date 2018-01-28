import re
import sys
import nltk
from nltk.stem.snowball import SnowballStemmer
from pprint import pprint
from functools import reduce

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


def print_charts(charts, inp):
    i=0
    for chart_no, chart in zip(range(len(charts)), charts):
        print("Chart "+str(chart_no)+"\t\n".join(map(
           lambda x: "\t |  {0:>10}  -> {1:<19}|{2:^20}|{3:^25}|".format(
                x["lhs"], 
                " ".join(x["rhs"][:x["dot"]] + ["*"] + x["rhs"][x["dot"]:]),
                "[" + str(x["state"]) + "," + str(chart_no) + "]",
                x["op"]
            ),
            chart
        )))
    
        
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
		return token+" STRING";
	return "";

with open(sys.argv[1]) as f:
	content = f.readlines()
	#print(f)
	
for n,i in enumerate(content):
	s=i.replace(":"," : ")
	s=s.replace("|"," | ")
	s=s.replace("."," .")
	content[n]=s.replace(";"," ; ")
print("\n\nInput:")
print("{0:-^50}".format(""))
content = [x.split() for x in content] 
for i in range(0,len(content)):
	print(' '.join(content[i]))

stemmer = SnowballStemmer("english")
print("\n\nStemmer:")
print("{0:-^30}".format(""))
k=1
for i in range(0,len(content)):
	for j in range(0,len(content[i])):
		#print(content[i][j])
		output=checkInputType(content[i][j])
		if("->" in content[i]):
			print("\n\n\n\tInvalid Input\n\n\n")
			sys.exit()
		if("#" in content[i]):
			k-=1
			continue
		if("W" in content[i] and "=" in content[i] and content[i][j]!="."):
			output+=" "+stemKeywords(content[i][j],stemmer)
		output+=" "+str(k+1)
		print("\t"+output)
	k+=1
print("\tENDFILE")

print("\n\nParser:")
print("{0:-^94}".format(""))




'''grammar={'pronoun': [['he'], ['she']], 'proper-noun': [['mary'], ['john']], 'VP': [['verb'], ['verb', 'NP'], ['verb', 'NP', 'PP'], ['verb', 'PP'], ['VP', 'PP']], 'verb': [['do'], ['work'], ['book']], 'aux': [['can'], ['will']], 'PP': [['prep', 'NP']], 'det': [['the'], ['that']], 'S': [['NP', 'VP'], ['aux', 'NP', 'VP'], ['VP']], 'prep': [['in'], ['on'], ['at']], 'NP': [['pronoun'], ['proper-noun'], ['det', 'NOMINAL']], 'NOMINAL': [['noun'], ['NOMINAL', 'noun'], ['NOMINAL', 'PP']], 'noun': [['book'], ['flight']]}

'''

grammar={'det': ['the', 'that'], 'verb': ['do', 'work', 'book'], 'S': [['NP', 'VP'], ['aux', 'NP', 'VP'], ['VP']], 'NOMINAL': [['noun'], ['NOMINAL', 'noun'], ['NOMINAL', 'PP']], 'prep': ['in', 'on', 'at'], 'aux': ['can', 'will'], 'PP': [['prep', 'NP']], 'VP': [['verb'], ['verb', 'NP'], ['verb', 'NP', 'PP'], ['verb', 'PP'], ['VP', 'PP']], 'pronoun': ['he', 'she'], 'noun': ['book', 'flight'], 'proper-noun': ['mary', 'john'], 'NP': [['pronoun'], ['proper-noun'], ['det', 'NOMINAL']]}


'''
grammar = {
	"ROOT": [["S"]],
    "S": [
        ["NP", "VP"],
        ["aux", "NP", "VP"],
        ["VP"]
    ],
    "NP": [
        ["pronoun"],
        ["proper-noun"],
        ["det", "NOMINAL"]
    ],
    "NOMINAL": [
        ["noun"],
        ["NOMINAL", "noun"],
        ["NOMINAL", "PP"]
    ],
    "VP": [
        ["verb"],
        ["verb", "NP"],
        ["verb", "NP", "PP"],
        ["verb", "PP"],
        ["VP", "PP"]
    ],
    "PP": [
        ["prep", "NP"]
    ],
    "det": {"that", "this", "a"},
    "noun": {"flight", "meal", "money", "gift", "astronomers", "stars", "ears", "world", "india", "me"},
    "verb": {"book", "include", "prefer", "saw", "hello"},
    "pronoun": {"i", "she", "me"},
    "proper-noun":{"shail","joey"},
    "aux": {"does"},
    "prep": {"from", "to", "on", "near", "through", "with"}
}
'''

charts = [[{
    "lhs": "Root",
    "rhs": ["S"],
    "dot": 0,
    "state": 0,
    "op": "Dummy Start State",
    "completer": []
}]]


input_arr ="book that flight".split()+[""]#input("\n\n\n\tEnter a sentence : ").split() + [""]

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


print_charts(charts[:-1], input_arr)

print("{0:-^94}".format(""))
print(grammar['prep'])
