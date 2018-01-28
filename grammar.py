grammar={}
with open('t10.dat') as f:
	line=f.readline()
	tempSplit=str(line)
	content=[]
	while line:
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
                        #semp=set(content)
				key=temp[0].strip().upper()
				grammar[key]=content
			else:
				#content=[hello.split("|")]
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
		
print(grammar)

