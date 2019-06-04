import json
import re

filename = input("Input: ")
with open(filename+".json",encoding='UTF-8-sig') as json_file:
	json_data = json.load(json_file)

x=[]

for i in json_data:
	c = i["contents"]
	if len(c)<=5:
		continue
	elif c[0]=='?':
		continue
	elif c[len(c)-1]=='?':
		x.append(i)








j = json.dumps(x, ensure_ascii=False,indent=4)

f = open(filename+"_question.json",'w',encoding='UTF-8-sig')
f.write(j)
f.close()
