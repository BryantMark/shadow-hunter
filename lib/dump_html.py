#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json

TEMPLATE = """<html>
<head>
    <style type="text/css">
        .okay: green;
        .wrong color: red;
    </style>
    <title>Preview</title>
</head>
<body>
    <table>
        {}
    </table>
</body>
</html>"""

def join_with(label, items):
    decorate_with = lambda s: \
            "<{}>".format(label) + s + "</{}>".format(label)
    return "".join(list(map(decorate_with, items)))

if __name__ == "__main__":
    raw_data = json.loads(sys.stdin.read())
    problem_count = len(raw_data[0]) - 3
    problem_codes = [chr(ord('A') + i) for i in range(problem_count)]
    rows = []
    rows.append(join_with("th", 
            ["#", "Team"] + problem_codes + ["Solved", "Penalty"]))
    for rank, team in enumerate(raw_data):
        rows.append(join_with("td", 
                [str(rank + 1)] + team))
    print(TEMPLATE.format(join_with("tr", rows)))
