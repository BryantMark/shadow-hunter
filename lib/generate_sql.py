#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import argparse
from datetime import datetime, timedelta

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--max_submit_id", type=int, required=True)
argument_parser.add_argument("--contest_id", type=int, required=True)
argument_parser.add_argument("--problems_id", nargs="+", 
        type=int, required=True)

result_code_map = {"OK": "Accepted",
    "WA": "Wrong Answer",
    "RTE": "Runtime Error",
    "TLE": "Time Limit Exceeded",
    "MLE": "Memory Limit Exceeded", 
    "PE": "Presentation Error",
    "CE": "Compile Error",
}

def add_submit(submit_id, user_name, contest_id, problem_id, \
        time, result_type):
    print("INSERT INTO `submit_info` \
(`ID`, `user_ID`, `user_name`, `contest_ID`, `problem_ID`, \
`lang`, `submit_time`, `isjudged`, `program`, `user_type`, \
`delay_time`) VALUES ({}, -1, '{}', {}, {}, 'GNU C++',  \
'{}', 1, '', 'shadow', NULL);"
        .format(submit_id, user_name, contest_id, problem_id, time))
    print("INSERT INTO `submit_result` (`submit_ID`, `result_type`, \
`judge_time`, `remark`, `user_id`) VALUES ({}, '{}', '{}', \
'no remark', -1);"
        .format(submit_id, result_type, time))

if __name__ == "__main__":
    args = argument_parser.parse_args()
    problem_count = len(args.problems_id)
    print("UPDATE `contest` SET `start_time`='2011-01-01 12:00:00', \
`end_time`='2011-01-01 17:00:00' WHERE `ID`={};"
        .format(args.contest_id))
    raw_data = json.loads(sys.stdin.read())
    current_submit_id = args.max_submit_id
    for team_name, problem_code, submit_time, result_code \
            in raw_data["submission"]:
        if 0 <= ord(problem_code) - ord('A') < problem_count:
            contest_id = args.contest_id
            problem_id = args.problems_id[ord(problem_code) - ord('A')]
            real_submit_time = (datetime.strptime("2011-01-01 12:00:00", \
                    "%Y-%m-%d %H:%M:%S") \
                    + timedelta(seconds=submit_time)) \
                    .strftime("%Y-%m-%d %H:%M:%S")
            real_result_code = result_code_map[result_code]
            current_submit_id += 1
            add_submit(current_submit_id, team_name, \
                    contest_id, problem_id, \
                    real_submit_time, real_result_code)
