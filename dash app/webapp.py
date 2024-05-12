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

'''Layout'''
def apply_main_layout(app: Dash) -> None:
    layout = html.Div(id='main-div', 
                      children = [html.H1('Welcome to my website!'),
                                  html.Hr(),
                                  html.H2('Figures of annual competition performance'),
                                  dcc.Graph(**score_para_strip),
                                  html.H2('Figures of lifetime competition performance'),
                                  dcc.Graph(**score_hist),
                                  dcc.Graph(**score_fake_violin),
                                  dcc.Graph(**score_box)])
    app.layout = layout

'''App'''
def run_app():
    my_app = Dash(__name__)
    my_app.title = 'iGEM Data Analysis'
    apply_main_layout(my_app)
    my_app.run()

if __name__ == '__main__':
    run_app()