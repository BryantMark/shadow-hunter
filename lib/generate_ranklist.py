#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json

class Team:
    def __init__(self, problem_count, name):
        self.name = name
        self.wrong_tries = [0] * problem_count
        self.accepted_time = [-1] * problem_count

    def __lt__(self, other):
        if self.get_solved_problem() == other.get_solved_problem():
            return self.get_penalty() < other.get_penalty()
        return self.get_solved_problem() > other.get_solved_problem()

    def get_solved_problem(self):        
        return len(list(filter(lambda x: x >= 0, self.accepted_time)))

    def get_penalty(self):
        result = 0
        for time, tries in zip(self.accepted_time, self.wrong_tries):
            if time >= 0:
                result += tries * 20 + time
        return result

    def get_pretty_problem_list(self):
        result = []
        for time, tries in zip(self.accepted_time, self.wrong_tries):
            if time < 0:
                if tries == 0:
                    result.append(".")
                else:
                    result.append(str(-tries))
            elif tries == 0:
                result.append("+")
            else:
                result.append("+" + str(tries))
        return result

if __name__ == "__main__":
    raw_data = json.loads(sys.stdin.read())
    problem_count = raw_data["problem_count"]
    teams = {}
    for team_name, problem_code, submit_time, result_code \
            in raw_data["submission"]:
        if team_name not in teams:
            teams[team_name] = Team(problem_count, team_name)
        problem_id = ord(problem_code) - ord('A')
        if result_code == "OK":
            if teams[team_name].accepted_time[problem_id] == -1:
                teams[team_name].accepted_time[problem_id] = \
                        submit_time // 60
        else:
            teams[team_name].wrong_tries[problem_id] += 1
    ranklist = []
    for team in sorted(teams.values()):
        ranklist.append([team.name] + team.get_pretty_problem_list() \
                + [str(team.get_solved_problem())
                        , str(team.get_penalty())])
    sys.stdout.write(json.dumps(ranklist, indent=4))
