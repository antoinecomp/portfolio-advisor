import os
import pickle


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

""" Path to media monitoring data (monthly) """
MM_DATA_PATH = os.path.join(PACKAGE_ROOT, 'data_package/')

class Reader:
    """
    Helper class to read json files in base data directory
    """

    def __init__(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.files = os.listdir(self.data_dir)

    def read_json_file(self, file):
        """
        Args
        ----
        file: str
            name of json file to read
        """
        file_path = os.path.join(self.data_dir, file)
        with open(file_path, 'r') as fp:
            return json.load(fp)

    def parse_filename(self, file, sep='-'):
        """
        Args
        ----
        file: str
            filename to be parsed into more easily readable format
        """
        file_wout_suffix = file.split('.')[0]
        splits = file_wout_suffix.split(sep)
        return ' '.join([split.capitalize() for split in splits])

    def create_json_dict(self):
        return {self.parse_filename(file): self.read_json_file(file)
                for file in self.files if file.startswith('20')}

    def create_geopandas(self):
        pass


def listify_ids(geojson, regions=False):
    ids = []
    for feature in geojson['features']:
        if regions:
            if feature['properties']['shape_type_id'] == 3:
                ids.append(str(feature['id']))
        else:
            if feature['properties']['shape_type_id'] != 3:
                ids.append(str(feature['id']))
    return ids


def listify_zview(geojson, z, regions=False):
    """
    View type for interactive map frame

    Args
    ----
    z: string
        'pct', 'count', or 'eligible'
    regions: Bool
        Whether to display regions or precincts
    """
    turnouts = []
    for feature in geojson['features']:
        if regions:
            if feature['properties']['shape_type_id'] == 3:
                turnouts.append(feature['properties']['turnout'][z])
        else:
            if feature['properties']['shape_type_id'] != 3:
                turnouts.append(feature['properties']['turnout'][z])
    return turnouts


def listify_winners(geojson, place, regions=False):
    """
    Get list of nth place election results for each location
    """
    winners = []
    for feature in geojson['features']:
        if regions:
            if feature['properties']['shape_type_id'] == 3:
                winners.append(feature['properties']['results'][place]['name'])
        else:
            if feature['properties']['shape_type_id'] != 3:
                winners.append(feature['properties']['results'][place]['name'])
    return winners


def listify_results(geojson, regions=False):
    """
    Return results for hovertext.

    TODO: Rename function if we use results for something other than hovertext
    """
    results = []
    for feature in geojson['features']:
        if regions:
            if feature['properties']['shape_type_id'] == 3:
                results.append(feature['properties']['results'])
        else:
            if feature['properties']['shape_type_id'] != 3:
                results.append(feature['properties']['results'])
    return results


def format_result_text(results):
    """
    results: list of list of dicts, each dict has keys 'name', 'pct'
    """
    text = []
    for result in results:
        string = ""
        for party in result:
            string += f"{party['name']}: {party['pct']}<br>"
        text.append(string)
    return text


def percentile(nums, n):
    """
    Returns the nth percentile of nums

    @nums (list): list of numericals
    @n (float): [0, 100]
    """
    n = n / 100
    nums_sorted = sorted(nums)
    k = int((len(nums) - 1) * n)
    return nums_sorted[k]


def listify_ids_regional(geojson):
    return [feature['id'] for feature in geojson['features']]


def listify_z_regional(geojson, z):
    return [feature['properties'][z]
            for feature in geojson['features']]


def listify_region_names(geojson):
    return [feature['properties']['name']
            for feature in geojson['features']]


def listify_segments(geojson):
    segment_distrs = []
    for feature in geojson['features']:
        segment_distr = feature['properties']['segment_distr']
        segment_distrs.append(segment_distr)
    return segment_distrs


def format_segment_text(segment_distrs):
    def space_function(text):
        if len(text) == 3:
            return 4
        else:
            return 2

    text = []
    for segment_distr in segment_distrs:
        segment_text = ''
        for segment_name, segment_size in segment_distr.items():
            segment_text += ('<b>' + segment_name + '</b>' +
                             ' ' * space_function(str(segment_size))
                             + str(segment_size) + '%<br>')
        text.append(segment_text)
    return text


def get_sentiment(value):
    try:
        if value > 0.25:
            return "positive"
        elif value < 0.25 and value > -0.25:
            return "neutral"
        else:
            return "negative"
    except:
        return "neutral"


def load_mm_data2(entity):
    # here I want to query pulsar and get their
    return pickle.load(open(MM_DATA_PATH + "google-nlu-" + entity + ".p", "rb"))

import json
import requests

def load_mm_data3(entity, start_date, end_date):
    aut_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMTQ2NywidXNlcl92ZX" \
                "JzaW9uIjpudWxsLCJzYW1lX29yaWdpbiI6ZmFsc2V9.rvxhJG9gNpzomds_4xf" \
                "UJzzZoR4skHuVrWFsgI8cC90"
    url = 'https://auspexinternational.pulsarplatform.com/'
    api_results = 'api/v3/trac/stats_overview/breakdown/time/'
    query_code = '8f7389a164b5eb59f92579ca0bbe6da5'  # Aziz
    search_api_url = url + api_results + query_code
    headers = {
        'Content-type': 'application/json',
        'Authorization': aut_token
    }
    params = {
        # 'fields': 'user_screen_name',
        # 'categories': '101',
        'date_from': start_date,
        'date_to': end_date,
        #'content_type': 1
        #'fields': ['content','title','source_name']
    }
    response = requests.get(
        search_api_url, headers=headers, params=params
    )
    json = response.json()

    return json


def load_posts(entity, start_date, end_date):
    aut_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMTQ2NywidXNlcl92ZX" \
                "JzaW9uIjpudWxsLCJzYW1lX29yaWdpbiI6ZmFsc2V9.rvxhJG9gNpzomds_4xf" \
                "UJzzZoR4skHuVrWFsgI8cC90"
    url = 'https://auspexinternational.pulsarplatform.com/'
    api_results = 'api/v2/trac/results/'
    query_code = '8f7389a164b5eb59f92579ca0bbe6da5'  # Aziz
    search_api_url = url + api_results + query_code
    headers = {
        'Content-type': 'application/json',
        'Authorization': aut_token
    }
    params = {

        'date_from': start_date,
        'date_to': end_date,
        'fields': ['source','source_name']
    }
    response = requests.get(
        search_api_url, headers=headers, params=params
    )
    json = response.json()

    return json

def load_topics(entity, start_date, end_date):
    aut_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMTQ2NywidXNlcl92ZX" \
                "JzaW9uIjpudWxsLCJzYW1lX29yaWdpbiI6ZmFsc2V9.rvxhJG9gNpzomds_4xf" \
                "UJzzZoR4skHuVrWFsgI8cC90"
    url = 'https://auspexinternational.pulsarplatform.com/'
    api_results = 'api/v2/trac/results/'
    query_code = '8f7389a164b5eb59f92579ca0bbe6da5'  # Aziz
    search_api_url = url + api_results + query_code
    headers = {
        'Content-type': 'application/json',
        'Authorization': aut_token
    }
    params = {

        'date_from': start_date,
        'date_to': end_date,
        'fields': ['topics']
    }
    response = requests.get(
        search_api_url, headers=headers, params=params
    )
    json = response.json()

    return json


if __name__ == "__main__":
    json_dict = reader.create_json_dict()
    print("json_dict: ", json_dict)
    geojson = json_dict.get('2016 Parliamentary Majoritarian')
    ids = listify_ids(geojson)
    turnouts = listify_zview(geojson, 'pct')
    results = listify_results(geojson, regions=True)
    results_fmt = format_result_text(results)
    winners = listify_winners(geojson, 0)
