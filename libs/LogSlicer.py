import json
import re
import requests
from datetime import datetime


class LogSlicer:

    def __init__(self):

        self.last_byte_position = {}
        self.data = {}
        self.log_lines = {}
        self.config = _load_as_json("conf/config.json")

    def add_url(self, url):

        self.data[url] = ""
        self.last_byte_position[url] = 0
        self.log_lines[url] = []

    def _refresh(self, url):

        headers = {"Range": f"bytes={self.last_byte_position[url]}-"}
        response = requests.get(url, headers=headers)
        new_data = response.content.decode("utf-8")

        # print("NEW DATA", new_data)

        self.process_new_log_lines(url, new_data)

        self.data[url] += new_data
        self.last_byte_position[url] += len(new_data)

    def process_new_log_lines(self, url, new_data):

        prev_epoch = None

        lines = new_data.splitlines()
        matched_lines = ""
        for line in lines:
            epoch = self.parse_epoch_from_line(line)
            if epoch:
                if not prev_epoch:
                    prev_epoch = epoch

                self.log_lines[url].append((prev_epoch, matched_lines))
                print("START--------------------------------------------------------------------------------------------------------")
                print(f"{prev_epoch} -> {matched_lines}")
                print("END----------------------------------------------------------------------------------------------------------\n")
                prev_epoch = epoch
                matched_lines = line
            else:
                if matched_lines != "":
                    matched_lines += "\n"
                matched_lines += line

    def parse_epoch_from_line(self, line):

        epoch = None
        for conf in self.config:
            match = re.search(conf["regexp"], line)
            if match:
                try:
                    epoch = datetime.strptime(match.group(1), conf["strptime"]).timestamp()
                except ValueError as e:
                    pass

        return epoch

    def get_data(self, url):

        self._refresh(url)

        return self.data[url]

    def get_log_lines(self, url, start_ts=None, end_ts=None):

        self._refresh(url)

        return self.log_lines[url]


def _load_as_json(filename):

    with open(filename, "r") as file:
        data = json.load(file)

    return data
