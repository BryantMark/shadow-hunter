#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json

if __name__ == "__main__":
    problem_count = 0
    team = {}
    submission = []
    for line in sys.stdin:
        if line[0] == '@':
            line = line[1:]
            command_type = line.split()[0]
            line = ' '.join(line.split()[1:])
            if command_type == 'p':
                problem_count += 1
            if command_type == 't':
                team_id = line.split(',')[0]
                team_name = ','.join(line.split(',')[3:])[1:-1]
                team[team_id] = team_name
            if command_type == 's':
                team_id, problem_code, submit_count, submit_time, \
                        result_code = line.split(',')[0:5]
                team_name = team[team_id]
                submit_time = int(submit_time)
                submission.append((team_name, problem_code, \
                        submit_time, result_code))
    sys.stdout.write(json.dumps({"problem_count": problem_count, 
            "submission": submission}, indent=4))
