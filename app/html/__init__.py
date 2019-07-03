from bs4 import BeautifulSoup


class HTML(object):
    def __init__(self):
        pass

    def getContributors(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        spans = soup.find_all('span', {'class': 'text-emphasized'})
        text = spans[3].text
        text = text.replace(" ", "").replace("\n", "")
        print("  > %s" % text)
        return text
