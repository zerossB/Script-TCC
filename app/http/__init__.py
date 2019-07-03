import requests
import json

from app import config


class Http(object):

    def __init__(self):
        self.url = "https://api.github.com/graphql"
        self.url_html = "https://github.com/"
        self.headers = {'Authorization': 'token %s' % config.API_TOKEN}

    def postGql(self, gql):
        query = {"query": gql}
        resp = requests.post(url=self.url, json=query, headers=self.headers)
        return json.loads(resp.text)

    def getHTML(self, project):
        print("> Pegando HTML de " + project)
        url = self.url_html + project
        resp = requests.get(url)
        return resp.text
