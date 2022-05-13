from enum import Enum


class VariableTypes(Enum):
    """
    This is for distinguishing between sentence types
    """
    ONLY_VERBS = 1
    ONLY_NOUNS = 2
    BOTH = 3


class DataPathTypes(Enum):
    """
    This is for distinguishing data paths
    """
    LAWS = 1
    ARTICLES = 2
    RULES = 3
    LOOKUPS = 4


class AdditionScores(Enum):
    """
    This is for distinguishing addition score in some case
    """
    RELEVANT_THEME = 1
    RELEVANT_WORD = 0.3
    IS_ARTICLE = 0.05


class GraphTypes(Enum):
    """
    This is for distinguishing between graphs to show
    """
    QUERY = 1
    DATA = 2
    SIMILARITY = 3
