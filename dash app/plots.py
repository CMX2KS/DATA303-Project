import pandas as pd
from sklearn.preprocessing import minmax_scale
from textwrap import wrap
import plotly.express as px

#data settings
DATA_FILE_PATH = 'IGEM_teams_2004-2024.csv'
YEARS = (2007, 2020)

'''Method for reading in a preprocessing data for plots'''
def get_annual_data(file = DATA_FILE_PATH, years = YEARS, section = 'Undergrad') -> pd.DataFrame:
    data = pd.read_csv(file) #read in data
    data = data[[year <= years[1] and year >= years[0] for year in data['Year']]] #select years
    data = data[data['Section'] == section] #select section
    data = score_data(data)
    data = wrap_abstracts(data)
    data = wrap_awards(data)
    return data

def get_lifetime_data(file = DATA_FILE_PATH, years = YEARS, section = 'Undergrad') ->pd.DataFrame:
    data = pd.read_csv(file) #read in data
    data = data[[year <= years[1] and year >= years[0] for year in data['Year']]] #select years
    data = data[data['Section'] == section] #select section
    data = score_data(data) #score the data

    #generate new df which gives lifetime score for each team
    leaderboard = pd.DataFrame([(team, data[data['Team Name'] == team]['Absolute Score'].sum()) for team in data['Team Name'].unique()],
                               index=range(len(data['Team Name'].unique())),
                               columns=['Team Name', 'Lifetime Score'])
    #scale the score using minmax scaling
    leaderboard['Scaled Score'] = minmax_scale(leaderboard['Lifetime Score'])
    #add in region data from old df
    leaderboard['Region'] = [data[data['Team Name'] == team]['Region'].iloc[0] for team in leaderboard['Team Name']]
    return leaderboard

'''Methods for assigning score to teams'''
def score_award(award_name: str) -> float:
        if 'Grand Prize' in award_name and '(' not in award_name: return 10
        elif 'Grand Prize' in award_name: return 5
        if 'Best' in award_name and 'Project' in award_name: return 5
        elif 'Best' in award_name: return 2
        return 1

def score_medal(medal: str) -> float:
    match medal:
        case 'Gold': return 1
        case 'Silver': return 0.5
        case 'Bronze': return 0.25
        case _ : return 0

def score_team(medal, awards):
    score = 0
    if type(awards) is not float:
        for award in awards.split(', '):
            score += score_award(awards)
    score += score_medal(medal)
    return score

def score_data(data) -> pd.DataFrame:
    data['Absolute Score'] = [score_team(data.iloc[index]['Medal'], data.iloc[index]['Awards']) for index in range(len(data))]
    for year in data['Year'].sort_values().unique():
        data.loc[data['Year'] == year, 'Scaled Score'] = minmax_scale(data.loc[data['Year'] == year]['Absolute Score']).tolist()
    return data

'''Methods for formatting text data'''
def wrap_abstracts(data) -> pd.DataFrame:
    data['Abstract'] = [abstract if abstract != '-' and type(abstract) is not float  else 'This team did not submit an abstract this competition year' for abstract in data['Abstract']]
    data['Short Abstract'] = ['<br>'.join(wrap(str(abstract), 50)) for abstract in data['Abstract']]
    return data
    
def wrap_awards(data) -> pd.DataFrame:
    data['Awards Summary'] = ['<br>'.join(wrap(str(awards), 50)) for awards in data['Awards']]
    data['Awards Summary'] = [awards if awards != '-' and awards != 'nan'  else 'This team did not win any awards this competition year' for awards in data['Awards Summary']]
    return data


'''Plot related code'''

FIG_SIZE = {'width': 1200, 'height': 600}
COLOR_SETTINGS = {'plot_bgcolor':'white',
                  'paper_bgcolor':'white'}
AXIS_FORMAT = {'title_font_size':20}

'''figures which use annual data'''
def get_score_para_strip(data):
    #Figure
    fig = px.strip(**FIG_SIZE,
                data_frame=data, x='Year', y='Scaled Score',
                hover_name='Team Name',
                color='Region',
                hover_data=['Absolute Score', 'Wiki', 'Short Abstract', 'Awards Summary'])

    #x-axis
    xticks = data['Year'].sort_values().unique()
    xaxis_format = {**AXIS_FORMAT,
                    'title_text': 'Year of Competition',
                    'tickmode': 'array',
                    'tickvals': xticks}
    fig.update_xaxes(**xaxis_format, title = {'font_size':30})

    #y-axis
    yaxis_format = {**AXIS_FORMAT,
                    'title_text': 'Team Score<br>(as ''%'' of max score that year)',
                    'gridcolor': 'rgba(128, 128, 128, 0.2)'}
    fig.update_yaxes(**yaxis_format, title = {'font_size':30})

    #title
    title_format = {'title':{'font_size':30,
                            'text':'Team score across 13 competition years',
                            'x':0.47}}
    fig.update_layout(**title_format)

    for tick in xticks:
        fig.add_vline(x=tick, layer='below', line_color='rgba(128, 128, 128, 0.5)')

    fig.update_layout(**COLOR_SETTINGS)

    fig.update_traces(marker={'size':15}, jitter=1)

    return fig

'''figures which use lifetime data'''
def get_histogram(data):
    fig = px.histogram(**FIG_SIZE, data_frame=data, x='Scaled Score', color='Region', barmode='overlay', log_y=True)

    #x-axis
    xaxis_format = {**AXIS_FORMAT,
                    'title_text': 'Score (as ''%'' of maximum)',
                    'tickmode': 'array'}
    fig.update_xaxes(**xaxis_format, title = {'font_size':30})

    #y-axis
    yaxis_format = {**AXIS_FORMAT,
                    'title_text': 'Frequency of team score',
                    'gridcolor': 'rgba(128, 128, 128, 0.2)'}
    fig.update_yaxes(**yaxis_format, title = {'font_size':30})

    #title
    title_format = {'title':{'font_size':30,
                            'text':'Lifetime Team Score Distribution by Region',
                            'x':0.47}}
    fig.update_layout(**title_format)

    fig.update_layout(**COLOR_SETTINGS)

    return fig

def get_fake_violin(data):
    fig = px.strip(**FIG_SIZE, data_frame=data, x='Region', y='Lifetime Score', color='Region', hover_name='Team Name', log_y=True)

    #x-axis
    xaxis_format = {**AXIS_FORMAT,
                    'title_text': 'Region',
                    'tickmode': 'array'}
    fig.update_xaxes(**xaxis_format, title = {'font_size':30})

    #y-axis
    yaxis_format = {**AXIS_FORMAT,
                    'title_text': 'Lifetime Score',
                    'gridcolor': 'rgba(128, 128, 128, 0.2)'}
    fig.update_yaxes(**yaxis_format, title = {'font_size':30})

    #title
    title_format = {'title':{'font_size':30,
                            'text':'Lifetime Team score by Region',
                            'x':0.47}}
    fig.update_layout(**title_format)

    fig.update_layout(**COLOR_SETTINGS)
    fig.update_traces(jitter=1, marker_size=8)

    return fig

def get_box(data):
    fig = px.box(**FIG_SIZE, data_frame=data, x='Region', y='Lifetime Score', color='Region', log_y=True, hover_name='Team Name', range_y=[0.75, 100])

    #Axes
    AXIS_FORMAT = {'title_font_size':20}

    #x-axis
    xaxis_format = {**AXIS_FORMAT,
                    'title_text': 'Region',
                    'tickmode': 'array'}
    fig.update_xaxes(**xaxis_format, title = {'font_size':30})

    #y-axis
    yaxis_format = {**AXIS_FORMAT,
                    'title_text': 'Lifetime Score',
                    'gridcolor': 'rgba(128, 128, 128, 0.2)'}
    fig.update_yaxes(**yaxis_format, title = {'font_size':30})

    #title
    title_format = {'title':{'font_size':30,
                            'text':'Lifetime Team score by Region',
                            'x':0.47}}
    fig.update_layout(**title_format)

    fig.update_layout(**COLOR_SETTINGS)
    fig.update_traces(jitter=1, boxmean=True)

    return fig