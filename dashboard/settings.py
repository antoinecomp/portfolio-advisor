import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

""" Path to media monitoring data (monthly) """
DATA_PATH = os.path.join(PROJECT_ROOT, 'data/')

""" Segments """
segment1 = {"label": "Undecided", "value": "UND"}
segment2 = {"label": "Abstainer", "value": "ABS"}

SEGMENT_LIST = [segment1, segment2]

