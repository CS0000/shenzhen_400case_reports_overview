# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from data_processing import *
import textwrap


# import case report data
# case_report: readed raw case report file
# time5: dataframe contain 5 kinds (6 individuals) of time points included:
# 'stay_in_wuhan_from', 'stay_in_wuhan_to',
# 'sz_arrive', 'onset', 'hospitalized',
# 'hospital_discharge'
time5 = hospital_discharge_process().get_time5()

time5_sub = pd.concat([time5,case_report.loc[:,['xb','jzd','nl']]],sort=False,axis=1)
time5_sub.columns = ['stay_in_wuhan_from', 'stay_in_wuhan_to',
                     'sz_arrive', 'onset', 'hospitalized',
                     'hospital_discharge',
                     'gender','residence','age']

day_summary_f = day_summary_process().get_day_summary_f()

gender_color_dict = {'男': 'rgb(137,0,255)',  # light purple
                     '女': plotly.colors.sequential.Burg[0]}  # light pink

residence_color_dict = dict(zip(['shenzhen', 'hubei_wuhan', 'hubei_others', 'others'],
                                plotly.colors.qualitative.T10[0:3]+['rgb(244,0,234)']))

age_color_dict = dict(zip(['age <=20', 'age: 21-55', 'age >= 55', None],
                          ['rgb(218,248,227)',
                           'rgb(0,194,199)',
                           'rgb(0,85,130)', 'black']))

time_color_dict = dict(zip(['stay_in_wuhan_from', 'stay_in_wuhan_to',
                            'sz_arrive', 'onset', 'hospitalized',
                            'hospital_discharge'],
                           ['rgb(255,255,255)','rgb(255,230,77)',
                            'rgb(84,141,219)','rgb(242,93,93)','rgb(142,204,126)',
                            'blue']))

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
    # cc: string in 'gender','age_range','residence_class'
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
                                             hovertemplate=
                                             '<br><b>caseID</b>: %{y}<br>'+
                                             '%{text}',
                                             text=['{0}: {1}'.format(cc,i) for i in single_class_df[cc].tolist()],
                                             marker=dict(color=cc_color[cc][c],
                                                         size=10),
                                             legendgroup=cc))
    return single_class_trace
def single_meta_sum(df_sub,meta):
    # meta: gender, residence_class, age_range
    # df_sub: time5_sub
    # return single meta data list
    cc_color = {'gender': gender_color_dict,
                'age_range': age_color_dict,
                'residence_class': residence_color_dict}
    test_trace = []
    sub_sum = df_sub[meta].value_counts()
    for i in sub_sum.index:
        test_trace.append(go.Bar(x=[meta],
                                 y = [sub_sum[i]],
                                 name = i,
                                 marker=dict(color=cc_color[meta][i])))
    return test_trace


time5_sub['residence_class'] = [resi_class_assign(str(i)) for i in time5_sub['residence'].tolist()]
time5_sub['age_range'] = [age_range_assign(int(i)) for i in time5_sub['age'].tolist()]



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
              **visualized as 4 plots:metadata summary, summary each day, metadata of each case and main plot.'''],
            style={'textAlign':'left','color':colors['text'],
                   'width':'90%'}
        ),

        html.P(children=[
            '*meatadata_|*summary each day(counts):',html.Br(),
            'summary___|all_severe',html.Br(),
            'counts______|accumulated_confirmed',html.Br(),
            '_____________|current_isolated',html.Br(),
            '_____________|current_medical_obs',html.Br(),
            '_____________|accumulated_discharge',html.Br(),
            '------------------|--------------------',html.Br(),
            '*metadata__|*main plot:',html.Br(),
            'of each case|visualizes the time stayingin wuhan,',html.Br(),
            '_____________|arriving Shenzhen',html.Br(),
            '_____________|onset,hospitalized and discharge in every case,connecting with pink lines',html.Br(),
            ''
            ],
            style={'textAlign':'left','color':colors['text'],
                   'width':'90%','font-size':'140%'}
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
                    options=[{'label': v, 'value': v} for v in time5_sub['gender'].unique()],
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
                    options=[{'label':v,'value':v} for v in time5_sub['residence_class'].unique()],
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

    time5_sub_filter = time5_sub.loc[(time5_sub['gender'].isin(se_gender))&
                                     # ((time3_sub['age']>=se_age[0])&(time3_sub['age']<=se_age[1]))&
                                     (time5_sub['residence_class'].isin(se_residence)),:]


    # generate main plot
    trace_list = []

    notes = case_report.loc[time5_sub_filter.index,
                            'bzzzytjd'].apply(lambda txt: '<br>'.join(textwrap.wrap(str(txt),width=14)))

    for i in time5.columns:
        note = ['<b>{0}</b>:<br>{1}<br>'.format(i,time5_sub_filter.loc[id,i])+
                '<br><b>Note</b>: '+notes[id] for id in time5_sub_filter.index.tolist()]
        # notes =

        tra = go.Scatter(x=time5_sub_filter[i].tolist(),
                         y=time5_sub_filter.index.tolist(),
                         mode='markers',
                         hovertemplate=
                         '<br><b>caseID</b>: %{y}<br>'+
                         '<br>%{text}',
                         text=note,
                         hoverlabel=dict(namelength=-1),
                         name=i,
                         marker=dict(color=time_color_dict[i],
                                     size=10))
        trace_list.append(tra)

    trace_line = []
    for p in time5_sub_filter.index.tolist():
        trace_line.append(go.Scatter(x=time5_sub_filter.loc[p, :].tolist(),
                                     y=[p,p,p,p,p,p],
                                     mode='lines',
                                     name=p,
                                     line=dict(color='rgb(231,107,243)', width=2),
                                     connectgaps=True,
                                     showlegend=False))

    sub_traces = []
    for i in ['gender','age_range','residence_class']:
        sub_traces += single_class_trace_fun(time5_sub_filter,i)


    sum_color_dict = {'all_severe':'rgb(249,0,0)','accumulated_confirmed':'rgb(255,185,60)',
                      'current_isolated':'rgb(255,143,179)','current_medical_obs':'rgb(176,106,212)',
                      'accumulated_discharge':'rgb(94,175,223)'}
    sum_trace_list = []
    for i in ['all_severe', 'accumulated_confirmed', 'current_isolated', 'current_medical_obs',
              'accumulated_discharge']:
        trace = go.Scatter(x=day_summary_f['until_date'],
                           y=day_summary_f[i],
                           name=i,
                           mode='markers+lines',
                           marker=dict(color=sum_color_dict[i]))
        sum_trace_list.append(trace)


    # fig_sub: mainplot + subplot + meta_sum_plot + sum_trace_list,which is the final plot
    fig_sub = make_subplots(rows=2, cols=2,column_widths=[0.1, 0.9],
                            row_width=[0.9,0.1],
                            # shared_yaxes=True,
                            shared_xaxes=True,
                            horizontal_spacing=0.05,
                            vertical_spacing=0)
    for i in sub_traces:
        fig_sub.add_trace(i,row=2,col=1)


    for i in trace_line+trace_list:
        fig_sub.add_trace(i,row=2,col=2)


    meta_sum = single_meta_sum(time5_sub_filter, 'gender') + \
               single_meta_sum(time5_sub_filter, 'age_range') + \
               single_meta_sum(time5_sub_filter,'residence_class')
    for i in meta_sum:
        fig_sub.add_trace(i, row=1, col=1)


    for i in sum_trace_list:
        fig_sub.add_trace(i,row=1,col=2)


    fig_sub.update_layout(height=4400, width=1200,
                          plot_bgcolor=colors['background'],
                          paper_bgcolor=colors['background'],
                          font=dict(color=colors['text'],
                                    size=15),
                          legend={'font':dict(size=22),
                                  'itemsizing': 'constant',},
                          hoverlabel=dict(font=dict(size=18)),
                          barmode='stack'
                          )

    # fig_sub.update_xaxes(tickangle=45)
    for i in ['yaxis','yaxis2','yaxis3','yaxis4']:
        fig_sub['layout'][i]['showgrid'] = False
        # fig_sub['layout'][i]['side'] = 'right'

    for i in ['xaxis','xaxis2','xaxis3','xaxis4']:
        fig_sub['layout'][i]['showgrid'] = False
        # fig_sub['layout'][i]['tickangle'] = 45

    fig_sub['layout']['yaxis3']['range'] = [0,402]
    fig_sub['layout']['yaxis4']['range'] = [0,402]

    fig_sub['layout']['xaxis1']['tickangle'] =45
    fig_sub['layout']['xaxis4']['side'] = 'top'
    # fig_sub.show()
    return fig_sub





if __name__ == '__main__':
    app.run_server(debug=True)

