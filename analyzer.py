from reader import FilePartReader
import re


class FileAnalyzer:
    def __init__(self, reader: FilePartReader):
        self.reader = reader
        self.split_regex = re.compile("[^\w\-']+[^\w]*")
        # sets if e.g. 'A' is the same what 'a' or not. Default not:
        self.case_sensitive = True
        # sets if analyzed words can be repeated or not. Default not:
        self.read_unique = True

    # TODO

# list = str.splitlines()
