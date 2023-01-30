import os
import re
import argparse
import os.path
from os import path
import ast

parser = argparse.ArgumentParser()
parser.add_argument("ingredient_1")
a = parser.parse_args()
args = a.ingredient_1
style = list()


def check(path):
    file = open(path, 'r')
    lines = file.readlines()
    count = 1
    lin = 0

    for line in lines:
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
                            style.append(
                                "{}: Line {}: S003 Unnecessary semicolon after a statement".format(path, count))
        if '#' in line and "  #" not in line:
            if line.find('#') != 0:
                if "{}: Line {}: S004  Less than two spaces before inline comments".format(path, count) not in style:
                    style.append("{}: Line {}: S004 Less than two spaces before inline comments".format(path, count))
        if "todo" in line.lower() and "#" in line:
            if bool(re.search(r"#[. ]*todo", line.lower())):
                if "{}: Line {}: S005 TODO found".format(path, count) not in style:
                    style.append("{}: Line {}: S005 TODO found".format(path, count))
        if lin >= 2:
            if lines[lin] != "\n":
                if lines[lin - 1] == "\n" and lines[lin - 2] == "\n" and lines[lin - 3] == "\n":
                    if "{}: Line {}: S006 More than two blank lines preceding a code line".format(path, lin + 1) not in style:
                        style.append(
                            "{}: Line {}: S006 More than two blank lines preceding a code line".format(path, lin + 1))
        ##################
        if "def" in line or "class" in line:
            if not bool(re.search(r"#[. ]*def", line)):
                if "def  " in line:
                    if "{}: Line {}: S007 Too many spaces after 'def'".format(path, count) not in style:
                        style.append("{}: Line {}: S007 Too many spaces after 'def'".format(path, count))
            if not bool(re.search(r"#[. ]*class", line)):
                if "class  " in line:
                    if "{}: Line {}: S007 Too many spaces after 'class'".format(path, count) not in style:
                        style.append("{}: Line {}: S007 Too many spaces after 'class'".format(path, count))
        ######################################
        if "class" in line:
            match = re.search(r'class[ ]*.*\(?.*\)?:', line)
            name = re.sub(r"class[ ]*", "", match.group())
            name = re.sub(r"\(.*\)", '', name)
            name = re.sub(r":", '', name)
            if re.match(r"[a-z]", name):
                if "{}: Line {}: S008 Class name '{}' should use CamelCase".format(path, count, name) not in style:
                    style.append("{}: Line {}: S008 Class name '{}' should use CamelCase".format(path, count, name))
            if re.search(r'_', name):
                if "{}: Line {}: S008 Class name '{}' should use CamelCase".format(path, count, name) not in style:
                    style.append("{}: Line {}: S008 Class name '{}' should use CamelCase".format(path, count, name))
        ###############################
        if "def" in line:
            match = re.search(r'def[ ]*.*\(?.+\)?:', line)
            name = re.sub(r"def[ ]*", "", match.group())
            name = re.sub(r"\(.+\):", '', name)
            if re.search(r"[A-Z]", name):
                if "{}: Line {}: S009 Function name '{}' should be written in snake_case.".format(path, count, name) not in style:
                    style.append( "{}: Line {}: S009 Function name '{}' should be written in snake_case.".format(path, count, name))
        count += 1
        lin += 1
    file1 = open(path, 'r')
    text = file1.read()
    tree1 = ast.parse(text)
    for node in ast.walk(tree1):
        if isinstance(node, ast.FunctionDef):
            args2 = [a1.arg for a1 in node.args.args]
            if args2:
                for i in args2:
                    if re.search(r"[A-Z]", i):
                        if "{}: Line {}: S010 Argument name '{}' should be written in snake_case.".format(path, node.lineno, i):
                            style.append("{}: Line {}: S010 Function name '{}' should be written in snake_case.".format(path, node.lineno, i))
            for item in node.args.defaults:
                if isinstance(item, ast.List):
                    if "{}: Line {}: S012 The default argument value is mutable.".format(path, node.lineno) not in style:
                        style.append("{}: Line {}: S012 The default argument value is mutable.".format(path, node.lineno))
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                variable_name = node.id
                if re.match(r'^[A-Z]', variable_name):
                    if "{}: Line {}: S011  Variable '{}' should be written in snake_case.".format(path, node.lineno, variable_name):
                        style.append("{}: Line {}: S011  Variable '{}' should be written in snake_case.".format(path,  node.lineno, variable_name))






if path.isfile(args):
    check(args)
elif path.isdir(args):
    for f_name in os.listdir(args):
        if f_name.endswith('.py') and f_name != "tests.py":
            full_path = os.path.join(args, f_name)
            check(full_path)

if style:
    print("\n".join(style))
