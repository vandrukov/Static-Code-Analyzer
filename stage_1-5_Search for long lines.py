import os

path = input()
file = open(path, 'r')
Lines = file.readlines()
style = list()
count = 1
for line in Lines:
    if len(line) > 79:
        style.append("Line {}: S001 Too long".format(count))
    count += 1
if style:
    print("\n".join(style))
