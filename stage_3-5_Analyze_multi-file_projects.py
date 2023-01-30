import os
import re
import argparse
import os.path
from os import path

parser = argparse.ArgumentParser()
parser.add_argument("ingredient_1")
a = parser.parse_args()
args = a.ingredient_1
style = list()

def check(path):
    file = open(path, 'r')
    Lines = file.readlines()
    count = 1
    lin = 0
    for line in Lines:
        if len(line) > 79:
            if "{}: Line {}: S001 Too long".format(path, count) not in style:
                style.append("{}: Line {}: S001 Too long".format(path, count))
        if line.startswith(' '):
            ind = 0
            for i in range(len(line)):
                if line[i] == " ":
                    ind += 1
                else:
                    break
            if ind % 4 != 0:
                if "{}: Line {}: S002 Indentation is not a multiple of four".format(path, count) not in style:
                    style.append("{}: Line {}: S002 Indentation is not a multiple of four".format(path, count))
        if ";" in line:
            if "#" not in line:
                line1 = re.sub(r"'.*;.*'", '', line)
                line1 = re.sub(r'".*;.*"', '', line1)
                if ";" in line1:
                    if "{}: Line {}: S003 Unnecessary semicolon after a statement".format(path, count) not in style:
                        style.append("{}: Line {}: S003 Unnecessary semicolon after a statement".format(path, count))
            else:
                if line.find('#') > line.find(';'):
                    line1 = re.sub(r"'.*;.*'", '', line)
                    line1 = re.sub(r'".*;.*"', '', line1)
                    if ";" in line1:
                        if "{}: Line {}: S003 Unnecessary semicolon after a statement".format(path, count) not in style:
                            style.append("{}: Line {}: S003 Unnecessary semicolon after a statement".format(path, count))
        if '#' in line and "  #" not in line:
            if line.find('#') != 0:
                if "{}: Line {}: S004  Less than two spaces before inline comments".format(path, count) not in style:
                    style.append("{}: Line {}: S004 Less than two spaces before inline comments".format(path, count))
        if "todo" in line.lower() and "#" in line:
            if bool(re.search(r"#[. ]*todo", line.lower())):
                if "{}: Line {}: S005 TODO found".format(path, count) not in style:
                    style.append("{}: Line {}: S005 TODO found".format(path, count))
        if lin >= 2:
            if Lines[lin] != "\n":
                if Lines[lin - 1] == "\n" and Lines[lin - 2] == "\n" and Lines[lin - 3] == "\n":
                    if "{}: Line {}: S006 More than two blank lines preceding a code line".format(path, lin + 1) not in style:
                        style.append("{}: Line {}: S006 More than two blank lines preceding a code line".format(path, lin + 1))
        count += 1
        lin += 1


if path.isfile(args):
    check(args)
elif path.isdir(args):
    for f_name in os.listdir(args):
        if f_name.endswith('.py') and f_name != "tests.py":
            full_path = os.path.join(args, f_name)
            check(full_path)



if style:
    print("\n".join(style))
