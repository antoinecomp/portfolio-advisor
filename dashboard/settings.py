import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

""" Path to media monitoring data (monthly) """
DATA_PATH = os.path.join(PROJECT_ROOT, 'data/')

""" Segments """
segment1 = {"label": "Undecided", "value": "UND"}
segment2 = {"label": "Abstainer", "value": "ABS"}
segment3 = {"label": "PJD", "value": "PJD"}
segment4 = {"label": "PAM", "value": "PAM"}
segment5 = {"label": "RNI", "value": "RNI"}
segment6 = {"label": "Istiqlal", "value": "IST"}
segment7 = {"label": "Other", "value": "OTH"}
SEGMENT_LIST = [segment1, segment2, segment3, segment4, segment5, segment6, segment7]

DEFAULT_CLUSTERS = 'cluster_Forgotten|cluster_Aspirational Youth|cluster_Snowflakes|cluster_Average|cluster_PJD|cluster_OTH|cluster_PAM|cluster_Empty Nest Mothers|cluster_IST|cluster_RNI|cluster_Urban Professional'



