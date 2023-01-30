import os
import re

path = input()
file = open(path, 'r')
Lines = file.readlines()
style = list()
count = 1
lin = 0
for line in Lines:
    if len(line) > 79:
        if "Line {}: S001 Too long".format(count) not in style:
            style.append("Line {}: S001 Too long".format(count))
    if line.startswith(' '):
        ind = 0
        for i in range(len(line)):
            if line[i] == " ":
                ind += 1
            else:
                break
        if ind % 4 != 0:
            if "Line {}: S002 Indentation is not a multiple of four".format(count) not in style:
                style.append("Line {}: S002 Indentation is not a multiple of four".format(count))
    if ";" in line:
        if "#" not in line:
            line1 = re.sub(r"'.*;.*'", '', line)
            line1 = re.sub(r'".*;.*"', '', line1)
            if ";" in line1:
                if "Line {}: S003 Unnecessary semicolon after a statement".format(count) not in style:
                    style.append("Line {}: S003 Unnecessary semicolon after a statement".format(count))
        else:
            if line.find('#') > line.find(';'):
                line1 = re.sub(r"'.*;.*'", '', line)
                line1 = re.sub(r'".*;.*"', '', line1)
                if ";" in line1:
                    if "Line {}: S003 Unnecessary semicolon after a statement".format(count) not in style:
                        style.append("Line {}: S003 Unnecessary semicolon after a statement".format(count))
    if '#' in line and "  #" not in line:
        if line.find('#') != 0:
            if "Line {}: S004  Less than two spaces before inline comments".format(count) not in style:
                style.append("Line {}: S004 Less than two spaces before inline comments".format(count))
    if "todo" in line.lower() and "#" in line:
        if bool(re.search(r"#[. ]*todo", line.lower())):
            if "Line {}: S005 TODO found".format(count) not in style:
                style.append("Line {}: S005 TODO found".format(count))
    if lin >= 2:
        if Lines[lin] != "\n":
            if Lines[lin - 1] == "\n" and Lines[lin - 2] == "\n" and Lines[lin - 3] == "\n":
                if "Line {}: S006 More than two blank lines preceding a code line".format(lin + 1) not in style:
                    style.append("Line {}: S006 More than two blank lines preceding a code line".format(lin + 1))
    count += 1
    lin += 1
if style:
    print("\n".join(style))
