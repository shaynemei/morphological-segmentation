#!/usr/bin/env python3

import sys

def main():
	data = sys.stdin.readlines()
	new_lines = []
	for lines in data:
	    new_string = ""
	    for char in lines:
	        if char.islower():
	            new_string += char + " "
	    new_lines.append(new_string.strip())

	for line in new_lines:
		print(line)

if __name__ == "__main__":
	main()