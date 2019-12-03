import sys
import re

def to_flat(data):
    flat = []
    for line in data:
        new_line = "(ROOT (WORD"
        nodes = re.findall(" *\w+ *: *\w+ *", line)
        for node in nodes:
            colon = re.search(":", node)
            morph = node[:colon.start()]
            tag = node[colon.end():]
            if re.search("stem", node)!=None:
                new_node = "(WORD"
            else:
                new_node = "(" + tag.upper()
            for char in morph:
                if char != " ":
                    new_node += " (" + char.upper() + " " + char.lower() + ")"
            new_node += ")"
            new_line += " " + new_node
        new_line = new_line.strip() + "))"
        flat.append(new_line)
    return flat

def main():
	data = sys.stdin.readlines()
	result = to_flat(data)
	for line in result:
		print(line)
			
main()