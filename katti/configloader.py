import os
import datetime
import json

user_config_changed = False
probems_config_changed = False

DEFAULT_HIST_SIZE = 100

def load_user_config(config_path: str) -> dict:
    """Loads the user config file and returns it as a dict

    Parameters:
    ----------
    config_path: str
        A string representing the absolute path to the user config file

    Returns:
    -------
    dict 
        A dictionary containing the user config
    """
    global user_config_changed
    user_config = None
    if not os.path.exists(config_path):
        user_config = {
            "solved": [],
            "history": [],
            "history_size": DEFAULT_HIST_SIZE,
            "ids_last_updated": str(datetime.now()),
            "ratings_update_period": 72
        }
        user_config_changed = True
    else:
        with open(config_path, "r") as f:
            user_config = json.load(f)
        if not user_config:
            user_config = {
                "solved": [],
                "history": [],
                "history_size": DEFAULT_HIST_SIZE,
                "ids_last_updated": str(datetime.now()),
                "ratings_update_period": 72
            }
            user_config_changed = True
    return user_config

def load_problems_config(config_path: str) -> dict:
    """Loads the problems config file and returns it as a dict

    Parameters:
    ----------
    config_path: str
        A string representing the absolute path to the problems config file

    Returns:
    -------
    dict 
        A dictionary containing the problems config
    """
    problems_list = None
    if not os.path.exists(config_path):
        problems_list = {}
    else:
        with open(config_path, "r") as f:
            problems_list = json.load(f)
    print(problems_list)
    return problems_list

def problem_config_changed():
    """Ensures that the problems config file is saved when the program exits"""
    global probems_config_changed
    probems_config_changed = True

def save_user_config(config_path: str, user_config: dict):
    """Saves the user config file

    Parameters:
    ----------
    config_path: str
        A string representing the absolute path to the user config file
    user_config: dict
        A dictionary containing the user config
    """
    global user_config_changed
    if user_config_changed:
        with open(config_path, "w") as f:
            json.dump(user_config, f, indent=4)
        user_config_changed = False

def save_problems_config(config_path: str, problems_config: dict):
    """Saves the problems config file

    Parameters:
    ----------
    config_path: str
        A string representing the absolute path to the problems config file
    problems_config: dict
        A dictionary containing the problems config
    """
    global probems_config_changed
    if probems_config_changed:
        with open(config_path, "w") as f:
            json.dump(problems_config, f)
        probems_config_changed = False