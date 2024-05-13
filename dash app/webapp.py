print('Please hold, this could take a moment...')

#dash
from dash import Dash, dcc, html

'''Plots'''
import plots

annual_score_data = plots.get_annual_data()
score_para_strip = {'id':'score_para_strip', 'figure':plots.get_score_para_strip(annual_score_data)}

lifetime_score_data = plots.get_lifetime_data()
score_hist = {'id':'score_hist', 'figure':plots.get_histogram(lifetime_score_data)}
score_fake_violin = {'id':'score_fake_violin', 'figure':plots.get_fake_violin(lifetime_score_data)}
score_box = {'id':'score_box', 'figure':plots.get_box(lifetime_score_data)}

'''Content'''
import content

'''Layout'''
def apply_main_layout(app: Dash) -> None:
    elements = [html.Plaintext(content.get_section(1)),
                dcc.Graph(**score_para_strip),
                html.Plaintext(content.get_section(2)),
                dcc.Graph(**score_box),
                dcc.Graph(**score_fake_violin),
                dcc.Graph(**score_hist),
                html.Plaintext(content.get_section(3)),
                html.Plaintext(content.get_section(4))]
    
    layout = html.Div(id='main-div', 
                      children = elements)
    app.layout = layout

'''App'''
def run_app():
    app = Dash(__name__)
    app.title = 'iGEM Data Analysis'
    apply_main_layout(app)
    app.run()

if __name__ == '__main__':
    run_app()