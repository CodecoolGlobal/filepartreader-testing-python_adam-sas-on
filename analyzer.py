from reader import FilePartReader
import re


class FileAnalyzer:
    def __init__(self, reader: FilePartReader):
        self.reader = reader
        self.split_regex = re.compile("[^\w\-']+[^\w]*")
        # sets if e.g. 'A' is the same what 'a' or not. Default not:
        self.case_sensitive = True
        # sets if analyzed words can be repeated or not. Default not:
        self.read_unique = False

    def remove_palindrome(self, words, palindrome, length):
        rev_palindrome = palindrome[::-1]
        palindrome_local = palindrome

        if not self.case_sensitive:
            rev_palindrome = rev_palindrome.lower()
            palindrome_local = palindrome_local.lower()

        palindrome_word = ""
        if palindrome_local == rev_palindrome:
            palindrome_word = palindrome

        was_not_set = True
        i = 0
        j = 0
        while j < length:
            word_case = words[j] if self.case_sensitive else words[j].lower()
            is_self = True if palindrome_local == word_case else False
            is_reverse = True if rev_palindrome == word_case else False

            if is_self or is_reverse:
                if is_reverse and was_not_set and j > 0:
                    was_not_set = False
                    if is_self:
                        palindrome_word = words[j]
                i -= 1
            elif i != j:
                words[i] = words[j]
            i += 1
            j += 1

        #words = words[:i]
        return (palindrome_word, i)
    #

    def get_words_ordered_alphabetically(self):
        file_content = self.reader.read_lines()
        if len(file_content) < 1:
            return []

        words_array = re.split(self.split_regex, file_content)
        words = []
        if self.read_unique and self.case_sensitive:
            for word in words_array:
                if len(word) > 0 and word not in words:
                    words.append(word)
        elif self.read_unique:
            for word in words_array:
                if len(word) > 0 and word.casefold() not in (_.casefold() for _ in words):
                    words.append(word)
        else:
            words = words_array

        return sorted(words, key=str.casefold)
    #

    def get_words_containing_substring(self, substring):
        file_content = self.reader.read_lines()
        if len(file_content) < 1:
            return []

        words_array = re.split(self.split_regex, file_content)
        words = []
        if self.read_unique and self.case_sensitive:
            for word in words_array:
                if len(word) > 0 and word not in words and substring in word:
                    words.append(word)
        elif self.read_unique:
            lower_substring = substring.lower()
            for word in words_array:
                if len(word) > 0 and lower_substring in word.lower() and word.casefold() not in (_.casefold() for _ in words):
                    words.append(word)
        elif not self.case_sensitive:
            lower_substring = substring.lower()
            i = 0
            while i < len(words_array):
                if lower_substring in words_array[i].lower():
                    words.append(words_array[i])
                i += 1
        else:
            for word in words_array:
                if substring in word:
                    words.append(word)

        return words
    #

    def get_strings_which_palindromes(self):
        file_content = self.reader.read_lines()
        if len(file_content) < 1:
            return []

        words_array = re.split(self.split_regex, file_content)
        words = []
        count = len(words_array)
        while count > 0:
            word_check = words_array[0]
            (palindrome_word, new_count) = self.remove_palindrome(words_array, word_check, count)

            if len(palindrome_word) > 0:
                words.append(word_check)
                if count - new_count > 1:
                    words.append(palindrome_word)

            count = new_count
        #
        return words
    #

    def get_read_range(self):
        return self.reader.get_read_range()

    def get_max_lines(self):
        return self.reader.get_max_lines()

    def set_read_range(self, from_line, to_line=-1):
	    self.reader.set_read_range(from_line, to_line)

    def set_file_path(self, new_file):
        self.reader.set_file_path(new_file)
	#

    def case_sensitive_set(self, case_sensitive):
        self.case_sensitive = case_sensitive

    def set_words_uniqueness(self, read_unique):
        self.read_unique = read_unique

