import re
import sys

def to_treebank(data):
    data = [sentence.replace("\n", "") for sentence in data]
    data = [line[re.search("\(", line).start():] for line in data]
    new_lines = []
    bugs = []
    for line in data:
        layers = len(re.findall("S", line))
        new_line = "(S " * layers
        morph_start = layers * 3
        cur = morph_start
        open_para = re.search("\(", line[cur:])
        while(open_para != None):
            colon = re.search(":", line[cur:])
            close_para = re.search("\)",line[cur:])
            morph = line[cur + open_para.end() : cur + colon.start()]
            tag = line[cur + colon.end() : cur + close_para.start()].upper()
            try:
                if line[cur + close_para.end()] == ")":
                    new_line += "(" + tag + " " + morph + ")) "
                    cur += close_para.end() + 2
                else:
                    new_line += "(" + tag + " " + morph + ") "
                    cur += close_para.end() + 1
            except:
                bugs.append(line)
                break
            open_para = re.search("\(",line[cur:])
        new_lines.append(new_line.strip())
    return new_lines

def to_hierarchy(data):
    new_lines = to_treebank(data)
    result = []
    for line in new_lines:
        layers = len(re.findall("\(S(?= )", line))
        new_line = "(ROOT " + ("(WORD " * layers)
        cur = layers * 3
        length = len(line)
        for idx, char in enumerate(line[cur:]):
            if (idx == length-cur-1):
                new_line += "))"
                break
            if (char == "P"):
                new_line += "(PREFIX "
            elif (char == "S") and (line[cur+idx+1] == "T"):
                new_line += "(WORD "
            elif (char == "S"):
                new_line += "(SUFFIX "
            elif char.islower() and (line[cur+idx+1] == ")"):
                new_line += "(" + char.upper() + " " + char + ")"
            elif char.islower():
                new_line += "(" + char.upper() + " " + char + ") "
            elif (char == ")") and (line[cur+idx+1] == ")"):
                new_line += ")"
            elif (char == ")"):
                new_line += ") "
        result.append(new_line)
    return result

def main():
	data = sys.stdin.readlines()
	result = to_hierarchy(data)
	for line in result:
		print(line)
			
main()