from cgitb import lookup
import enum
from scipy.fftpack import idct
from comparsionHandler import ComparisonHandler
from conceptualGraph import ConceptualGraph
from enums import DataPathTypes
import json

from query_handler import reduce_words


class DataHandler:
    """
    This class is for handling raw data from json, including: read, retrieve, create graphs and compare them
    """
    def __init__(self, lawsPath, articlesPath, rulesPath, lookupsPath):
        """
        Input: path to laws, articles, rules, lookups data
        """
        self.laws = self.__retrieveData(lawsPath)
        self.articles = self.__retrieveData(articlesPath)
        self.rules = self.__retrieveData(rulesPath)
        self.lookups = self.__retrieveData(lookupsPath)

        self.graphs = self.__conceptualizeKeyphrase()

    def __retrieveData(self, path):
        """
        Input: type of data that we need to retrive
        Output: list data in this file
        """
        result = []
        # Read list titles of laws
        f = open(path, encoding="utf8")

        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for item in data:
            result.append(item)

        f.close()
        return result

    def __conceptualizeKeyphrase(self):
        """
        Output: list data about articles and rules converted to conceptual graphs
        """
        result = []
        for article in self.articles:
            keyphrase = article["keyphrase"]
            if keyphrase:
                result.append((ConceptualGraph(reduce_words(keyphrase)),
                              article["id"], DataPathTypes.ARTICLES))

        for rule in self.rules:
            keyphrase = rule["keyphrase"]
            if keyphrase:
                result.append(
                    (ConceptualGraph(reduce_words(keyphrase)), rule["id"], DataPathTypes.RULES))

        return result

    def getData(self, type):
        """
        Input: Enum type of data that we want to get
        Output: list json objects of input type
        """
        if type == DataPathTypes.LAWS:
            return self.laws
        elif type == DataPathTypes.ARTICLES:
            return self.articles
        elif type == DataPathTypes.RULES:
            return self.rules
        elif type == DataPathTypes.LOOKUPS:
            return self.lookups

    def compare(self, graph):
        """
        Input: Graph of query that we want to compare
        Output: list of top similarities of this graph to data
        """
        result = []

        for data in self.graphs:
            # print("------------------------")
            comparisonHandler = ComparisonHandler(graph, data[0])
            add_value = (
                # Id of this type of data
                data[1],
                # get title of this data,
                self.getArticleTitle(data[1], data[2]),
                # get index of this rule in article
                self.getRuleTitle(
                    data[1], True) if data[2] == DataPathTypes.RULES else "",
                # get law code of this data,
                ', '.join(self.getCodeList(data[1], data[2])),
                # Get comparison score
                str(comparisonHandler.getSimilarityScore(data[2])),
                # get graph of similarity
                comparisonHandler
            )
            result.append(add_value)
            # print("Nodes:", data[0].getNodes(), "- Score of", data[1], "is",comparisonHandler.getSimilarityScore())
        return result

    def getDataFromId(self, id, type):
        """
        Input: id and type of data we want to get
        Ouput: json of the founded data
        """
        return list(filter(lambda val: val["id"] == id, self.articles if type ==
                           DataPathTypes.ARTICLES else self.rules))[0]

    def getLookUpFromId(self, id, type):
        """
        Input: id and type of data we want to find its lookUp data
        Ouput: json of the founded lookUp data
        """
        lookUpId = self.getDataFromId(id, type)["lookUpId"]
        return list(filter(lambda lk: lk["id"] == lookUpId, self.lookups))[0]

    def getArticleTitle(self, id, dataType):
        """
        Input: id and type of rule or article
        Output: string title of this article 
        """
        if dataType == DataPathTypes.ARTICLES:
            return self.getDataFromId(id, DataPathTypes.ARTICLES)["title"]
        elif dataType == DataPathTypes.RULES:
            return self.getRuleTitle(id, False)

    def getRuleTitle(self, id, onlyIndex):
        """
        Input: id and type of rule and if we only want to get index of this rule in article turn onlyIndex to True
        Output: string title of the parent article of this rule 
        """
        lookUp = self.getLookUpFromId(id, DataPathTypes.RULES)

        if(onlyIndex):
            indexInArticle = [idx for idx, val in enumerate(
                lookUp["rules"]) if val == id][0]
            return "Khoản "+str(indexInArticle + 1)
        else:
            return self.getArticleTitle(lookUp["article"], DataPathTypes.ARTICLES)

    def getContentData(self, id, type):
        """
        Input: id and type of the data that we want to read it content
        Output: the string content that we are looking for
        """
        lookUp = self.getLookUpFromId(id, type)
        refers = []
        for refer in lookUp["references"]:
            refer.add(refer)

        content = ""
        if type == DataPathTypes.ARTICLES:
            for ruleId in lookUp["rules"]:
                data = self.getDataFromId(
                    ruleId, DataPathTypes.RULES)
                content = content + \
                    str(data["content"]) + "\n"
                for refer in data["references"]:
                    refers.append(refer)
        elif type == DataPathTypes.RULES:
            data = self.getDataFromId(
                id, DataPathTypes.RULES)
            content = str(data["content"]) + "\n"
            for refer in data["references"]:
                refers.append(refer)

        return (content, refers)

    def getLawFromCode(self, code):
        """
        Input: code of the law that we want to get its data
        Output: json data of the founded law
        """
        return list(filter(lambda law: law["code"] == code, self.laws))[0]

    def getArticleFromRule(self, id):
        """
        Input: id of the rule that we want to get its parent's article
        Output: json data of the founded article
        """
        lookUp = self.getLookUpFromId(id, DataPathTypes.RULES)
        return self.getDataFromId(lookUp["article"], DataPathTypes.ARTICLES)

    def getCodeList(self, id, type):
        """
        Input: id and type of the law that we want to get its parents'laws
        Output: list code of the founded laws parents
        """
        return self.getDataFromId(id, type)['laws'] if type == DataPathTypes.ARTICLES else self.getArticleFromRule(id)['laws']

    def getLawTitlesFromList(self, id, type):
        """
        Input: id and type of the data that we want to get its laws'title
        Output: list string title of the founded laws 
        """
        result = []
        for code in self.getCodeList(id, type):
            result.append(self.getLawFromCode(code)['title'])
        return result

    def getDataGraphFromId(self, id):
        """
        Input: id of the data graph that we want to retrieve (data graph is the whole conceptual graph)
        Output: the founded data graph
        """
        return list(filter(lambda graph: graph[1] == id, self.graphs))

    def getContentFromId(self, itemId):
        """
        Input: id of items that we want to retrieve its content
        Output: string of contents that connected to input id
        """
        data = self.getDataGraphFromId(itemId)
        type = data[0][2] if data else DataPathTypes.RULES
        result = "Theo "
        titles = self.getLawTitlesFromList(itemId, type)
        for index, code in enumerate(self.getCodeList(itemId, type)):
            ending = ":\n" if index + \
                1 == len(self.getCodeList(itemId, type)) else " và "
            result = result + titles[index] + " số "+code + ending

        if type == DataPathTypes.RULES:
            result =result + self.getRuleTitle(itemId, True) + " thuộc "

        article = self.getArticleTitle(itemId, type)
        contentData = self.getContentData(itemId, type)
        result = result + article + "\n" + contentData[0]
        if contentData[1]:
            result = result + "\n\n"
            for refer in contentData[1]:
                if refer[0] == 'l':
                    lookup = list(
                        filter(lambda lk: lk["id"] == refer, self.lookups))[0]
                    result = result + self.getContentFromId(lookup["article"])
                else:
                    result = result + self.getContentFromId(refer)
        return result

    def print(self):
        """
        Output: print whatever data we want to test
        """
        print(self.laws)
