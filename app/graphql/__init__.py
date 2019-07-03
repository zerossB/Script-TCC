import re


class GraphQL(object):
    def __init__(self, filename):
        self.filename = "graphql/%s.gql" % filename

    def readFile(self, owner="", repo="", license=""):
        with open(self.filename, 'r') as gql:
            text = re.sub(r"[\n\t\r]*", "", gql.read())
            text = text.replace('#owner', owner)
            text = text.replace('#repo', repo)
            text = text.replace('#license', license)
            return text
