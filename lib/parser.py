#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--execute", action="store_true")
argument_parser.add_argument("--config_file", default="config.json", \
        type=str)
argument_parser.add_argument("result_file", type=str)

def pretty(x):
    if x == 0:
        return "."
    if x < 0:
        return str(x)
    if x == 1:
        return "+"
    return "+" + str(x - 1)

class HTMLFormatter:
    def __init__(self):
        pass

    def feed(self, result):
        problem_count = len(result[0].problem)
        layout = [["Rank", "Team Name"] \
                + [chr(ord('A') + i) for i in range(problem_count)] \
                + ["Solved", "Penalty"]]
        rank = 0
        for team in result:
            rank += 1          
            layout.append(map(str, [rank, team.team_name] \
                    + list(map(pretty, team.problem)) \
                    + [team.get_solved_problem(), team.get_penalty()]))
        table = ""
        for line in layout:
            table += "<tr>" + "".join(map(
                    lambda s: "<td>" + s + "</td>", line)) + "</tr>"
        return "<html><body><table>{}</table></body></html>".format(table)

class Result:
    def __init__(self, team_name, problem_count):
        self.team_name = team_name 
        self.problem = [0] * problem_count
        self.penalty = [0] * problem_count

    def __lt__(self, other):
        if self.get_solved_problem() == other.get_solved_problem():
            return self.get_penalty() < other.get_penalty()
        return self.get_solved_problem() > other.get_solved_problem()

    def get_solved_problem(self):
        ret = 0
        for i in self.problem:
            if i > 0:
                ret += 1
        return ret

    def get_penalty(self):
        ret = 0
        for i, k in enumerate(self.problem):
            if k > 0:
                ret += self.penalty[i]
        return ret

    def add_problem(self, problem_id, submit_time, accepted):
        if self.problem[problem_id] > 0:
            return None
        self.problem[problem_id] -= 1
        if accepted:
            self.problem[problem_id] = abs(self.problem[problem_id])
            self.penalty[problem_id] += submit_time // 60
        else:
            self.penalty[problem_id] += 20

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
        problem_count = len(self.config["problem_id"])
        contest_id = self.config["contest_id"]
        if not (0 <= problem_id < problem_count):
            return None
        real_time = submit_time \
                + database.get_time_stamp(self.config["time_stamp"])
        result_type = self.result_map[result_code]        
        submit_id = user_id = database.get_max_submit()
        if self.config["execute"]:
            database.add_submit(user_id, problem_id, contest_id, 
                    real_time, user_name)
            submit_id += 1
            database.add_submit_result(submit_id, result_type, real_time)
        if user_name not in self.result:
            self.result[user_name] = Result(user_name, problem_count)
        self.result[user_name].add_problem(problem_id, submit_time, \
                result_type == "Accepted")

    def show_result(self, formatter):
        final_result = list(self.result.values())
        final_result.sort()
        return formatter.feed(final_result)

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
    print(contest.show_result(HTMLFormatter()))

if __name__ == "__main__":
    args = argument_parser.parse_args()
    main(args)
