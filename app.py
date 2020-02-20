# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.dependencies import Input, Output


# load data:
case_report_file = 'C://Users//Chen Shuo//Documents//20200215_CoVtry//深圳市“新型肺炎”-每日新增确诊病例个案详情_2920001503668.csv'
case_report = pd.read_csv(case_report_file,sep=',',engine='python',encoding='utf-8')
case_report.index = case_report.blh.tolist()


# rearrange data,set color dictionary
time3 = case_report.loc[:,['lssj','fbingsj','rysj']]
time3.columns = ['sz_arrive','onset','hospitalized']
time3 = time3.apply(lambda x:pd.to_datetime(x, errors='coerce'))

time3_sub = pd.concat([time3,case_report.loc[:,['xb','jzd','nl']]],sort=False,axis=1)
time3_sub.columns = ['sz_arrive', 'onset', 'hospitalized','gender','residence','age']

gender_color_dict = {'男': 'rgb(137,0,255)',  # light purple
                     '女': plotly.colors.sequential.Burg[0]}  # light pink

residence_color_dict = dict(zip(['shenzhen', 'hubei_wuhan', 'hubei_others', 'others'],
                                plotly.colors.qualitative.T10[0:3]+['rgb(244,0,234)']))

age_color_dict = dict(zip(['age <=20', 'age: 21-55', 'age >= 55', None],
                          ['rgb(218,248,227)',
                           'rgb(0,194,199)',
                           'rgb(0,85,130)', 'black']))

def resi_class_assign(single_cell):
    # assign 居住地 as hubei_others, hubei_wuhan, shenzhen, others
    if '湖北' in single_cell:
        if '武汉' in single_cell:
            return 'hubei_wuhan'
        else:
            return 'hubei_others'
    elif '深圳' in single_cell:
        return 'shenzhen'

    else:
        return 'others'
def age_range_assign(single_cell):
    # assgin age(int) as <=20, 21-55, >=55
    if single_cell > 20:
        if single_cell > 55:
            return 'age >= 55'
        elif single_cell < 55:
            return 'age: 21-55'
    else:
        return 'age <=20'
def single_class_trace_fun(df_filter, cc):
    # cc: string in 'gender','age_range','residence_class','time3'
    # generate metadata subplot
    cc_color = {'gender': gender_color_dict,
                'age_range': age_color_dict,
                'residence_class': residence_color_dict}
    single_class_trace = []
    for c in df_filter[cc].unique():
        single_class_df = df_filter.loc[df_filter[cc] == c, :]
        single_class_trace.append(go.Scatter(x=[cc] * len(single_class_df.index.tolist()),
                                             y=single_class_df.index.tolist(),
                                             mode='markers',
                                             name=c,
                                             marker=dict(color=cc_color[cc][c],
                                                         size=10),
                                             legendgroup=cc))
    return single_class_trace

time3_sub['residence_class'] = [resi_class_assign(str(i)) for i in time3_sub['residence'].tolist()]
time3_sub['age_range'] = [age_range_assign(int(i)) for i in time3_sub['age'].tolist()]



# dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {'background':'#403030',
          'text':'#7FDBFF'}

app.layout = html.Div(style={'backgroundColor':colors['background'],
                             'columnCount':1},
                      children=
    [
        html.H1(children='Shen Zhen: 400 case reports overview',
                style={'textAlign':'center',
                       'color':colors['text']}),

        html.H3(children=[
            '''
            * The main plot on the right side visualizes the time arriving Shenzhen,onset and hospitalized
              in every case, connecting with pink lines.
              '''],
            style={'textAlign':'left','color':colors['text'],
                   'width':'90%'}
        ),

        html.H3(children=[
            '''
              * The subplot on the left describes case's metadata,
              including gender, rough age range and residences.'''],
            style={'textAlign':'left','color':colors['text'],
                   'width':'90%'}
        ),

        html.Div( # gender dropdown
            [
                html.Div(
                    [
                        html.Div(html.H2("""Select gender"""),
                                 style={'margin-right':'2em',
                                        'color':colors['text']})
                    ],
                ),
                dcc.Dropdown(
                    id='gender',
                    options=[{'label': v, 'value': v} for v in time3_sub['gender'].unique()],
                    placeholder='Select gender',
                    multi=True,
                    value='女',
                    style={'color':'black', #'backgroundColor':'blue',
                           'font-size':'120%',
                           'width':'60%',
                           'horizontalAlign': "middle"}
                )
            ] #,style=dict(display='flex')
        ),

        html.Div( # residence dropdown
            [
                html.Div(
                    [
                        html.Div(html.H2("""Select residence class"""),
                             style={'margin-right':'2em',
                                    'color':colors['text']})
                    ],
                ),
                dcc.Dropdown(
                    id='residence',
                    options=[{'label':v,'value':v} for v in time3_sub['residence_class'].unique()],
                    placeholder='Select residence',
                    multi=True,
                    value='shenzhen',
                    style={'color':'black',#'backgroundColor':'blue',
                           'font-size':'120%',
                           'width':'80%',
                           'display':'inline-block',
                           'horizontalAlign': "middle"}
                )
            ]# ,style=dict(display='flex')
        ),
        dcc.Graph(
            id='graph',
        # figure=fig_sub,
            style={'height':'280vh','width':'180vh'}
        )

    ]
)


@app.callback(
    Output('graph', 'figure'),
    [Input('gender', 'value'),
     # Input('age_slider','value'),
     Input('residence','value')])

def update_graph(se_gender,se_residence):
    if type(se_gender) == str:
        se_gender = [se_gender]
    if type(se_residence) == str:
        se_residence = [se_residence]

    time3_sub_filter = time3_sub.loc[(time3_sub['gender'].isin(se_gender))&
                                     # ((time3_sub['age']>=se_age[0])&(time3_sub['age']<=se_age[1]))&
                                     (time3_sub['residence_class'].isin(se_residence)),:]

    # generate main plot
    trace_list = []
    color_dict = dict(zip(time3.columns,
                          ['rgb(84,141,219)','rgb(242,93,93)','rgb(142,204,126)']))
    for i in time3.columns:
        tra = go.Scatter(x=time3_sub_filter[i].tolist(),
                         y=time3_sub_filter.index.tolist(),
                         mode='markers',
                         name=i,
                         marker=dict(color=color_dict[i],
                                     size=10))
        trace_list.append(tra)

    trace_line = []
    for p in time3_sub_filter.index.tolist():
        trace_line.append(go.Scatter(x=time3_sub_filter.loc[p, :].tolist(),
                                     y=[p, p, p],
                                     mode='lines',
                                     name=p,
                                     line=dict(color='rgb(231,107,243)', width=2),
                                     connectgaps=True,
                                     showlegend=False))

    sub_traces = []
    for i in ['gender','age_range','residence_class']:
        sub_traces += single_class_trace_fun(time3_sub_filter,i)

    # fig_sub: mainplot + subplot,which is the final plot
    fig_sub = make_subplots(rows=1, cols=2,column_widths=[0.1, 0.9],
                            shared_yaxes=True,
                            horizontal_spacing=0.01)
    for i in sub_traces:
        fig_sub.add_trace(i,row=1,col=1)


    for i in trace_line+trace_list:
        fig_sub.add_trace(i,row=1,col=2)

    fig_sub.update_layout(height=2800, width=1200,
                          plot_bgcolor=colors['background'],
                          paper_bgcolor=colors['background'],
                          font=dict(color=colors['text'],
                                    size=20),
                          legend={'font':dict(size=22),
                                  'itemsizing': 'constant',},
                          hoverlabel=dict(font=dict(size=20)))

    fig_sub.update_xaxes(tickangle=45)
    for i in ['yaxis','yaxis2']:
        fig_sub['layout'][i]['showgrid'] = False
        fig_sub['layout'][i]['side'] = 'right'

    for i in ['xaxis','xaxis2']:
        fig_sub['layout'][i]['showgrid'] = False
        fig_sub['layout'][i]['side'] = 'top'
    # fig_sub.show()
    return fig_sub





if __name__ == '__main__':
    app.run_server(debug=True)

