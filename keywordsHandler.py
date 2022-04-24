from typing import List, Tuple


class KeywordsHandler:
    score_table = [10, 1]
    """
    Score table for evaluation is a hard configuration\n
    It has the same size with words_list that is intended to be inputed so that we can compare parallelly between 2 lists
    """

    def __init__(self, words_list):
        """
        Init handlers word by inputting list of [list of words that divided by tiers]\n
        """
        self.words_list = words_list

    def getSameKeywordsList(self, title):
        """
        Input: a string of title\n
        Process: handler will find same values in its child lists\n
        Return: list of turple which each item consists of (word,score)
        """
        retrieved = []
        for index in range(0, len(self.words_list)):
            for words in self.words_list[index]:
                if title in words:
                    retrieved.append((words, self.score_table[index]))

        return retrieved
