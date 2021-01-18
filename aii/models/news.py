import re


class News:
    def __init__(self, news):
        self.title = re.sub("<.*?>", "", news[0])
        self.link = re.sub("<.*?>", "", news[1])
        pre_description = re.sub("<.*?>", "", news[2])
        self.description = re.sub("^\\s*.*;&gt;", "", pre_description)
        self.date = re.sub("<.*?>", "", news[3])

    def __repr__(self):
        return f"Title: {self.title}\nLink: {self.link}\nDescription: {self.description}\nDate: {self.date}"
