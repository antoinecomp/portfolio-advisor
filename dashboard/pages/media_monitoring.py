from os.path import abspath, dirname

import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
from dash.dependencies import Input, Output

import pandas as pd

from datetime import datetime as dt
from datetime import date

from collections import Counter

from itertools import chain

from . import utils
from ..server import app


@app.callback(
    Output('sentiment_graph', 'figure'),
    [Input('select-politician', 'value'),
     Input('dates-picker', 'start_date'),
     Input('dates-picker', 'end_date')])
def update_entity(entity, start_date, end_date):
    data_mm = utils.load_mm_data3(entity, start_date, end_date)

    # I need to parse dictionaries and get the sum of pos, neg and neut
    # Create pandas dataframe wi
    monitoring_df = pd.DataFrame(data_mm)
    pos_count = int(monitoring_df[['positive']].sum())
    neg_count = int(monitoring_df[['negative']].sum())
    neut_count = int(monitoring_df[['neutral']].sum())

    percentage = (pos_count - neg_count) / (pos_count + neg_count)

    colors = ['red', 'aliceblue', 'aquamarine']

    text = "Score: " + str(round(percentage, 2))
    labels = ['Negative', 'Neutral', 'Positive']
    values = [neg_count, neut_count, pos_count]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.65)])
    fig.update_layout(
        # title_text="Overall Sentiment",
        annotations=[dict(text=text, x=0.5, y=0.5, font_size=16, showarrow=False)],
    )

    fig.update_traces(hoverinfo='label+percent',
                      marker=dict(colors=colors, line=dict(color='#000000', width=1.5)))

    return fig


@app.callback(
    Output('mentions_chart', 'figure'),
    [Input('select-politician', 'value'),
     Input('dates-picker', 'start_date'),
     Input('dates-picker', 'end_date')])
def update_mentions(entity, start_date, end_date):
    start_date = dt.strptime(start_date, "%Y-%m-%d").timestamp()
    end_date = dt.strptime(end_date, "%Y-%m-%d").timestamp()
    data_mm = utils.load_mm_data3(entity, start_date, end_date)
    data_mm = sorted(data_mm, key=lambda i: i['date'], reverse=False)

    results = []
    for item in data_mm:
        results.append({'date': item['date'], 'posts': item['posts']})

    # c = Counter(results)
    x = []
    y = []

    for dic in results:
        x.append(dic['date'])
        y.append(dic['posts'])

    # for k, v in enumerate(d['date'], d['posts']):
    #     x.append(k)
    #     y.append(v)

    fig = go.Figure(data=go.Scatter(x=x,
                                    y=y,
                                    mode='lines',
                                    line=dict(shape="spline", color="orangered"), )
                    )

    fig.update_layout(
        # title_text='Daily News Volume',
        # yaxis_title="Count",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    return fig

@app.callback(
    Output('sources_graph', 'figure'),
    [Input('select-politician', 'value'),
     Input('dates-picker', 'start_date'),
     Input('dates-picker', 'end_date')]
)
def update_sources(entity, start_date, end_date):
    start_date = dt.strptime(start_date, "%Y-%m-%d").timestamp()
    end_date = dt.strptime(end_date, "%Y-%m-%d").timestamp()
    # print('start_date: ', start_date, " type: ", type(start_date))

    data_posts = utils.load_posts(entity, start_date, end_date)
    contents = data_posts.get('contents')  # filtering out total_contents, next_cursor, total_pages # Pulsar only provide only provide 100 results per page, so correct, you'll need to use the next until it's a null value to retrieve all results :)

    x = []
    y = []

    counter = Counter(x['source_name'] for x in contents)
    counter = list(counter.items())

    for k, v in counter:
        y.append(k)
        x.append(v)

    fig = go.Figure(data=[go.Bar(
        x=x,
        y=y,
        marker=dict(
            color='lightslategrey',
            line=dict(
                color='black',
                width=2),
        ),
        orientation='h',
    )])

    fig.update_layout(
        # title_text='Article Sources',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgb(248, 248, 255)')
    return fig


@app.callback(
    Output('topic_chart', 'figure'),
    [Input('select-politician', 'value'),
     Input('dates-picker', 'start_date'),
     Input('dates-picker', 'end_date')]
)
def update_topics(entity, start_date, end_date):
    topic_dict = {
        'Banking': 0,
        'Education': 0,
        'Energy & Utilities': 0,
        'Government': 0,
        'Health Conditions': 0,
        'Investing': 0,
        'Jobs': 0,
        'Legal': 0,
        'Politics': 0,
        'Public Safety': 0,
        'Religion & Belief': 0,
        'Social Issues & Advocacy': 0,
    }

    topic_dict_pos = topic_dict.copy()
    topic_dict_neg = topic_dict.copy()
    topic_dict_neut = topic_dict.copy()

    data_mm_topic = utils.load_topics(entity, start_date, end_date)

    # print("data_mm_topic :", data_mm_topic)
    contents = data_mm_topic.get('contents')
    print("contents: ", contents)

    topics = []

    for x in contents:
        topics_x = x.get('topics')
        if topics_x is not None:
            if type(topics_x) is not list:
                print('topics_x(not list): ', topics_x.items())
                topics = topics.append(topics_x.items())
            else:
                print("topics_x(list): ", topics_x)
                topics.extend(topics_x)

    print("Counter(topics): ", Counter(topics))
    # print("counter: ", counter)

    # for item in data_mm_topic['contents']:
    #     print("item: ", item.values())


    topic_result = []

    for item in data_mm_topic:

        try:
            topic = (list(item.get('topics').keys())[0].split("/"))[2]
            sentiment = utils.get_sentiment(item.get('sentiment'))

            if topic in topic_dict:
                if sentiment == "positive":
                    topic_dict_pos[topic] += 1
                if sentiment == "neutral":
                    topic_dict_neut[topic] += 1
                if sentiment == "negative":
                    topic_dict_neg[topic] += 1
                topic_dict[topic] += 1
        except:
            pass

    x_axis = list(Counter(topics).keys())

    fig = go.Figure(data=[
        go.Bar(name='Neutral',
               x=x_axis,
               y=list(Counter(topics).values()),
               marker=dict(
                   color='aliceblue',
                   line=dict(color='#000000', width=2)
               )),
        go.Bar(name='Negative',
               x=x_axis,
               y=list(topic_dict_neg.values()),
               marker=dict(
                   color='red',
                   line=dict(color='#000000', width=2)
               )),
        go.Bar(name='Positive',
               x=x_axis,
               y=list(topic_dict_pos.values()),
               marker=dict(
                   color='aquamarine',
                   line=dict(color='#000000', width=2)
               ))])

    fig.update_layout(barmode='stack',
                      plot_bgcolor='rgb(248, 248, 255)',
                      # title_text='Topics discussed',
                      )
    fig.update_xaxes(tickangle=45)
    return fig

from ..server import app

""" Test entities """
entity1 = {"label": "Aziz Akhannouch", "value": "Aziz Akhannouch"}
entity2 = {"label": "Giorgi Gakharia", "value": "gakharia"}

ENTITY_LIST = [entity1, entity2]

base_dir = dirname(dirname(abspath(__file__)))

server = app.server


def layout():
    return html.Div([
        html.Div([
            html.Div([
                dcc.DatePickerRange(
                    id='dates-picker',
                    min_date_allowed=dt(2017, 8, 5),
                    initial_visible_month=dt(2017, 8, 5),
                    end_date=date.today()
                )
            ]),
            html.Div([
                dcc.Dropdown(
                    id='select-politician',
                    options=ENTITY_LIST,
                    value=ENTITY_LIST[0].get('value')
                )
            ])
        ], className='pretty_container twelve columns'),
        html.Div([
            html.Div([
                html.H5('Sentiment', style={'textAlign': 'center', 'padding': 10}),
                dcc.Graph(id="sentiment_graph")
            ], className='pretty_container four columns'),
            html.Div([
                html.H5('Daily News Volume', style={'textAlign': 'center', 'padding': 10}),
                dcc.Graph(id="mentions_chart")
            ], className='pretty_container seven columns')
        ]),
        html.Div([
            html.Div([
                html.H5('Article Sources', style={'textAlign': 'center', 'padding': 10}),
                dcc.Graph(id="sources_graph")
            ], className='pretty_container four columns'),

            html.Div([
                html.H5('Topics Discussed', style={'textAlign': 'center', 'padding': 10}),
                dcc.Graph(id="topic_chart")
            ], className='pretty_container seven columns')
        ])
    ], className='pretty_container twelve columns')


if __name__ == "__main__":
    app.run_server(debug=False, port=8051)
