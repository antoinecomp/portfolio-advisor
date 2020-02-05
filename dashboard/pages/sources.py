import json
import random
from os.path import abspath, dirname, join

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html



def layout():
    return html.Div([
        html.Div([
            dcc.Dropdown(
                id='select-politician',
                options="bla bla",
                value="bla bla" 
            )
        ], className='pretty_container two columns'),
            html.Div([
                dcc.Graph(id="sources_graph", 
                          figure = get_figure2()
                          )
            ], className='pretty_container two columns'),

    ], className='pretty_container two columns')


def get_data():
    return pd.read_csv('dashboard/data/capi_preprocessed.csv')



def get_figure2():
    segments = get_data() 

    segments_labels = segments.TL_Segment
    segments_fts = pd.get_dummies(segments.drop('TL_Segment', axis=1))
    total_avgs = segments_fts.mean(axis=0)


    label_map = {'Forgotten': 'Left behinds',
                 'Urban Professional': 'Worker Bees',
                 'Average': 'Ambitious Underachievers',
                 'Empty Nest Mothers': 'Moroccan Mothers'
                }

    segments_labels = segments_labels.replace(label_map)

#    print(segments_labels)

    clusters = segments_labels.unique()
    segments_dict = {cluster: segments_fts[segments_labels == cluster] for cluster in clusters}

    segment = segments_dict.get('UND')
    segment_fts = get_notable_features(segment, total_avgs, segments_labels)

    data = sort_by_difference(segment_fts)
    difference = data["TotalAvgs"] - data["SegmentAvgs"]

    labels = data.UNDKeyFts
    values = difference

    fig = go.Figure(data=[go.Bar(
              x=labels,
              y=values,
              marker=dict(
                  color='rgba(50, 171, 96, 0.6)',
                  line=dict(
                  color='rgba(50, 171, 96, 1.0)',
                  width=2),
            ),
           # orientation='h',
            )])
    return fig


def get_figure():
    data = {'internet': 1964, 'television': 653, 'radio': 317, 'press': 215}

    x = []
    y = []

    for k, v in data.items():
        y.append(k.title())
        x.append(v)

    fig = go.Figure(data=[go.Bar(
          x=x,
          y=y,
          marker=dict(
              color='rgba(50, 171, 96, 0.6)',
              line=dict(
              color='rgba(50, 171, 96, 1.0)',
              width=2),
        ),
        orientation='h',
        )])

    fig.update_layout(title_text='Article Sources', plot_bgcolor='rgb(248, 248, 255)')
    return fig



def get_notable_features(segment_df,
                         total_avgs,
                         segments_labels):
    """
    segment_df : pd.DataFrame of a subset of the full dataframe
        observations of one segment
    total_avgs : pd.Series mean of each column of ful dataframe
    """
    binary_df = pd.get_dummies(segment_df)
    segment_array = binary_df.values

    segment_avgs = np.mean(binary_df, axis=0)

    top_features_indices = np.argsort(segment_avgs)[::-1]

    cluster_key_features = [segment_df.columns[tf]
                            for tf in top_features_indices]
    cluster_avgs = [segment_avgs[tf] for tf in top_features_indices]
    total_avgs = [total_avgs[tf] for tf in top_features_indices]

    d = {segments_labels[segment_df.index[0]] + 'KeyFts': cluster_key_features,
         'SegmentAvgs': cluster_avgs,
         'TotalAvgs': total_avgs}

    return pd.DataFrame(data=d)


def sort_by_difference(key_fts):
    """
    Sort dataframe returnd by get_notable_features() by difference
    between segment averages and total averages
    """
    differences = np.abs(key_fts.SegmentAvgs - key_fts.TotalAvgs)
    differences_sorted = differences.sort_values(ascending=False)
    indices = differences_sorted.index
    return key_fts.iloc[indices]

def keep_first_of_codes(df):
    uniques = df.iloc[:, 0].unique()
    return uniques
