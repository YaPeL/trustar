#!/usr/bin/env python3.8
import requests
from bs4 import BeautifulSoup
import trustar_readjson
import json
from codecs import raw_unicode_escape_decode


class GithubExtractInformation():
    """
    Class to extract valuable information using trustar_readjson from github json file or github dir json files.
    It needs to receive the dot properties, exmaple: ["guid", "content.entities", "score", "score.sign"]
    """

    def __init__(self, properties):
        self.session_requests = requests.session()
        self.url_git = 'https://github.com'
        self.properties = properties
        self.trustar_read_json = trustar_readjson.TrustarReadJson()

    def get(self, url):
        return BeautifulSoup(self.session_requests.get(url).text, 'html.parser')

    def read_gitgub_json_file(self, url_file):
        raw_href = self.get(url_file).find("a", {"id": "raw-url"})["href"]
        raw_href = f"{self.url_git}{raw_href}"
        json_data = self.get(raw_href).text

        try:
            json_data = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            print("json.decoder.JSONDecodeError in ----------->" + url_file)
            json_data = json.loads(json_data.replace("\\", "\\\\"))

        valuable_information = self.trustar_read_json.extract_valuable_information(
            json_data, self.properties)

        return valuable_information

    def read_github_json_dir(self, url_dir):
        dir_html = self.get(url_dir)
        rows_html = dir_html.find_all('div', {"role": "row"})
        files_count = 0
        for i in rows_html:
            file = i.find("a")
            if file:
                file_name = file.text
                if file_name.split('.')[-1] == 'json':
                    files_count += 1
                    file_href = f"{self.url_git}{file['href']}"
                    self.read_gitgub_json_file(file_href)


if __name__ == '__main__':
    properties_list = ["id", "objects[0].name", "objects[0].kill_chain_phases"]
    obj_git_mitre = GithubExtractInformation(properties_list)
    obj_git_mitre.read_github_json_dir(
        'https://github.com/mitre/cti/tree/master/enterprise-attack/attack-pattern')
