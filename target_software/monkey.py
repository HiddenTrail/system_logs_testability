import logging
import random

# Määritellään lokitus
logging.basicConfig(filename="logs/activity.log", level=logging.DEBUG, format="%(asctime)s %(message)s")

def log_with_level(level, message, level_type="info"):
    spaces = " " * level
    if level_type == "debug":
        logging.debug(f"{spaces}{message}")
    elif level_type == "info":
        logging.info(f"{spaces}{message}")
    elif level_type == "error":
        logging.error(f"{spaces}{message}")

def what_level_i_am(level):
    log_with_level(level, f"Current recursion level: {level}")
    return level

def do_something(param1, another_param, level):
    if level >= 8:
        return 0
    log_with_level(level, f"Entering do_something with level {level}.", "debug")
    result = 0
    try:
        for i in range(1, level + 1):
            result += (param1 ** i) / another_param
        if level % 2 == 0:
            result += do_something_else(param1, level + 1, another_param, result)
        else:
            result += do_something_meaningless([param1, another_param], level + 1, result)
    except Exception as e:
        log_with_level(level, f"Error in do_something: {e}", "error")
    finally:
        log_with_level(level, f"Exiting do_something with result {result} at level {level}.")
        return result

def do_something_else(param1, level, another_param, second_param):
    if level >= 8:
        return 0
    log_with_level(level, f"Entering do_something_else with level {level}.", "debug")
    result = 0
    try:
        result = sum([param1 * level for _ in range(int(second_param)) if _ % 2 == 0])
        if level > 3:
            result += monkey_with_monkey(param1, level + 1, another_param, second_param)
    except Exception as e:
        log_with_level(level, f"Error in do_something_else: {e}", "error")
    finally:
        log_with_level(level, f"Exiting do_something_else with result {result} at level {level}.")
        return result

def do_something_meaningless(list_param, number_param, level):
    if level >= 8:
        return 0
    log_with_level(level, f"Entering do_something_meaningless with level {level}.", "debug")
    result = 0
    try:
        for i in list_param:
            result += i * random.randint(1, 10)
        if number_param > 50:
            result *= lambda x: x * 2
    except Exception as e:
        log_with_level(level, f"Error in do_something_meaningless: {e}", "error")
    finally:
        log_with_level(level, f"Exiting do_something_meaningless with result {result} at level {level}.")
        return result

def monkey_with_monkey(price, number_of_monkeys, level, meaningless_parameter):
    if level >= 8:
        return 0
    log_with_level(level, f"Entering monkey_with_monkey with level {level}.", "debug")
    total_cost = 0
    try:
        total_cost = price * number_of_monkeys
        for _ in range(level):
            total_cost += random.choice([10, 20, 30])
        if meaningless_parameter > 100:
            total_cost += do_something(total_cost, number_of_monkeys, level + 1)
    except Exception as e:
        log_with_level(level, f"Error in monkey_with_monkey: {e}", "error")
    finally:
        log_with_level(level, f"Exiting monkey_with_monkey with total_cost {total_cost} at level {level}.")
        return total_cost


for i in range(10):
    do_something(i, 20-i, 1)
