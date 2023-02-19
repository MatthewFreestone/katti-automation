import pkg_resources
import os
import sys
import json
import argparse
import datetime
from katti import webkattis, configloader


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


USER_CONF_PATH = pkg_resources.resource_filename(__name__, 'config.json')
PROBLEMS_CONF_PATH = pkg_resources.resource_filename(
    __name__, 'problem_ids.json')

# HOME = os.path.expanduser('~')
# ZSH_COMP_PATH = os.path.join(HOME, ".config/zsh/custom_completions/_katti")

# for customization of arg parser
class Parser(argparse.ArgumentParser):
    def _check_value(self, action, value):
        if action.choices is not None and value not in action.choices:
            raise argparse.ArgumentError(action, "invalid option")

def main():
    user_conf = configloader.load_user_config(USER_CONF_PATH)
    problems_conf = configloader.load_problems_config(PROBLEMS_CONF_PATH)

    # add command line args
    arg_parser = Parser(prog="katti", description="A command line tool testing and submitting kattis problems.")
    arg_parser.add_argument(
        "-g",
        "--get",
        metavar="<problem-id>",
        help="get a kattis problem by its problem id",
        type=str,
        # choices=list(problems_conf.keys())
    )
    arg_parser.add_argument(
        "-r", "--run", help="run the test cases for a given problem", action="store_true")
    arg_parser.add_argument(
        "-p", "--post", help="submit a kattis problem", action="store_true")
    arg_parser.add_argument(
        "-v", "--verbose", help="receive verbose outputs", action="store_true")
    arg_parser.add_argument(
        "-d", "--description", help="display a problem's description in chrome", metavar="<problem-id>")
    arg_parser.add_argument("-b", "--default_browser",
                            help="set the default browser to show problem descriptions", action="store_true")
    arg_parser.add_argument("--add", metavar="<problem_id>",
                            help="add a problem id to your problem config file")
    arg_parser.add_argument("--random", metavar="<rating>",
                            help="get a random kattis problem with a given rating")
    arg_parser.add_argument(
        "--stats", help="get kattis stats if possible", action="store_true")
    arg_parser.add_argument(
        "--history", help="see your 50 most recent kattis submissions", action="store_true")
    arg_parser.add_argument("--history_size", metavar="<size>",
                            help="set history size with a number and query history size with -1")
    arg_parser.add_argument("--update_period", metavar="<hours>",
                            help="set how frequently katti updates problem ratings in hours")
    arg_parser.add_argument("--update_zsh_completions",
                            help="update katti completions for zsh users", action="store_true")
    args = arg_parser.parse_args()
    # track verbosity
    verbose = args.verbose
    # handle args passed in
    if args.get:
        get(args.get)
    elif args.random:
        get_random(args.random)
    elif args.run:
        run()
    elif args.post:
        post()
    elif args.add:
        add(args.add)
    elif args.default_browser:
        set_default_browser()
    elif args.description:
        webkattis.show_description(args.description, problems_config=problems_conf, verbose=verbose)
    elif args.stats:
        get_stats()
    elif args.history:
        get_history()
    elif args.history_size:
        handle_history_size(args.history_size)
    elif args.update_period:
        set_update_period(args.update_period)
    elif args.update_zsh_completions:
        update_zsh_completions()

    # update conf files if needed
    configloader.save_user_config(USER_CONF_PATH, user_conf)
    configloader.save_problems_config(PROBLEMS_CONF_PATH, problems_conf)

if __name__ == "__main__":
    main()