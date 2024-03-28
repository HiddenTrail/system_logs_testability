import datetime
import logging
import sys
import time

logging.basicConfig(filename="logs/luckynumber.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def lucky_number(meaningless_parameter=0):

    luckynumber = None
    if meaningless_parameter:
        logging.info(f"sleeping {meaningless_parameter} ms")
        time.sleep(meaningless_parameter/1000)
    try:
        thousands = datetime.datetime.now().microsecond // 1000
        parts_million = abs(1000000 // (thousands-13))
        luckynumber = sum(int(digit) for digit in str(parts_million))
        logging.info(f"timestamp thousand: {thousands}, parts million: {parts_million}, lucky number: {luckynumber}")
    except Exception as e:
        logging.error(f"error happened: {e}")

    return luckynumber


def generate_lucky_numbers(price, meaningless_parameter=0):

    lns = {}
    for _ in range(price):
        ln = lucky_number(meaningless_parameter)
        lns[ln] = ln

    return sorted(sorted(lns))


def main():

    price = min(1000, int(sys.argv[1])) if len(sys.argv) > 1 else 1
    another_parameter = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    lucky_numbers = generate_lucky_numbers(price, another_parameter)
    print(f"Your lucky numbers are: {lucky_numbers}")


main()
