#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--execute", action="store_true")
argument_parser.add_argument("--config_file", default="config.json", \
        type=str)
argument_parser.add_argument("result_file", type=str)

import database

class Contest:
    def __init__(self, config):
        self.result_map = {"RT": "Runtime Error",
            "OK": "Accepted",
            "WA": "Wrong Answer",
            "ML": "Memory Limit Exceeded",
            "CE": "Compile Error",
            "TL": "Time Limit Exceeded",
            "PE": "Presentation Error",
        }
        self.config = config
        self.result = {}

    def add_submit(self, user_name, problem_id, submit_time, result_code):
        contest_id = self.config["contest_id"]
        if not (0 <= problem_id < len(self.config["problem_id"])):
            return None
        submit_time += database.get_time_stamp(self.config["time_stamp"])
        result_type = self.result_map[result_code]        
        submit_id = user_id = database.get_max_submit()
        if self.config["execute"]:
            database.add_submit(user_id, problem_id, contest_id, 
                    submit_time, user_name)
            submit_id += 1
            database.add_submit_result(submit_id, result_type, submit_time)

import json

def main(args):    
    f = open(args.config_file, "r")
#   error handle 
    config = json.loads(f.read())
#   error handle 
    config["execute"] = args.execute
    contest = Contest(config)
    team_map = {}
    f = open(args.result_file, "r")
#   error handle
    for line in f:
        if line[0] != "@":
            continue        
        line = line[1: -1]
        if line.split()[0] in ["t", "s"]:
            split_line = line[2:].split(",")
            if line[0] == "t":
                team_id = int(split_line[0])
                team_name = ",".join(split_line[3:])[1:-1]
                team_map[team_id] = team_name
            else:
                team_id = int(split_line[0])
                team_name = team_map[team_id]
                problem_id = ord(split_line[1]) - ord('A')
                submit_time = int(split_line[3])
                result_code = split_line[4]
                contest.add_submit(team_name, problem_id, submit_time, \
                        result_code)

if __name__ == "__main__":
    args = argument_parser.parse_args()
    main(args)
