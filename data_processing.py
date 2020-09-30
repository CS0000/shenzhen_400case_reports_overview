import pandas as pd
import datetime

case_report_file = 'C://Users//Chen Shuo//Documents//20200215_CoVtry//20200321//深圳市“新型肺炎”-每日新增确诊病例个案详情_2920001503668.csv'
case_report = pd.read_csv(case_report_file, sep=',', engine='python', encoding='utf-8')
case_report.index = case_report.blh.tolist()

hospital_discharge_file = 'C://Users//Chen Shuo//Documents//20200215_CoVtry//20200321//深圳市“新型肺炎”-每日新增出院病例_2920001503675.csv'
hospital_discharge = pd.read_csv(hospital_discharge_file, sep=',', engine='python', encoding='utf-8')
hospital_discharge.index = hospital_discharge.blh.tolist()
hospital_discharge = hospital_discharge.iloc[hospital_discharge.index<=400,:] # all of it actually

day_summary = pd.read_csv('C://Users//Chen Shuo//Documents//20200215_CoVtry//20200321//深圳市“新型肺炎”-每日诊疗情况_2920001503673.csv',engine='python',sep=',',encoding='utf-8')
day_summary.columns = ['severe_case','accumulated_death','critical_severe_case','until_time',
                       'accumulated_confirmed','accumulated_discharge','current_isolated',
                       'current_medical_obs','until_date']

class case_report_process:

    def __init__(self):
        self.case_report = case_report #readed raw case report
        self.time3 = pd.DataFrame() # 3 kinds of time points included: sz_arrive, onset, hospitalized
        self.time4_temp = pd.DataFrame() # include: 'stay_in_wuhan_from/to', 'risk', 'notes', 'relationship'
        self.time4 = pd.DataFrame() # generate from time4_temp: 4 kinds of time points included: stay_in_wuhan_from/to(2 time points), sz_arrive, onset, hospitalized


    def get_time3(self):
        self.time3 = self.case_report.loc[:, ['lssj', 'fbingsj', 'rysj']]
        self.time3.columns = ['sz_arrive', 'onset', 'hospitalized']
        self.time3 = self.time3.apply(lambda x: pd.to_datetime(x, errors='coerce'))
        return self.time3


    def get_time4_temp(self):
        '''
        :purpose: stay_in_wuhan_from / to
        :what have been done:
        :1. replace '——' to '-'
        :2. '2019/01/..' to '2020/01/..', may be typos
        :3. '-2019/12/01' to '2019/10/1-2019/12/01' startswith '-': stay in wuhan until..,for convenience of ploting...
        :4. single time point: short stay in wuhan, example:'2019/12/28-2019/12/28'
        :5. case ID 385,375,361 has multi time ranges, including the range which is earlier
        :6. case ID 138,139 time stya in wuhan seems to be a typo:change 2020/1/16-2020/2/23 to 2020/1/16-2020/1/23
        :7. finally split it into 'stay_in_wuhan_from' and 'stay_in_wuhan_to'
        '''
        self.time4_temp = case_report.loc[:, ['zwhsjqj', 'rbyy', 'bzzzytjd', 'yqtblgx']]
        self.time4_temp.columns = ['stay_in_wuhan', 'risk', 'notes', 'relationship']
        self.time4_temp['stay_in_wuhan'] = self.time4_temp['stay_in_wuhan'].apply(lambda x: str(x).replace('——', '-'))
        self.time4_temp['stay_in_wuhan'] = self.time4_temp['stay_in_wuhan'].apply(lambda x: str(x).replace('2019/1/', '2020/1/1'))
        self.time4_temp['stay_in_wuhan'] = ['2019/10/1' + str(i) if str(i).startswith('-') else str(i)
                                            for i in self.time4_temp['stay_in_wuhan'].tolist()]

        # len([i for i in self.time_4['stay_in_wuhan'].tolist() if len(i) <= 10 and i != 'nan'])
        self.time4_temp['stay_in_wuhan'] = [str(i) + '-' + str(i) if len(i) <= 10 and i != 'nan' else str(i)
                                            for i in self.time4_temp['stay_in_wuhan'].tolist()]

        self.time4_temp.loc[[385, 375, 361], 'stay_in_wuhan'] = ['2020/1/13-2020/1/13',
                                                                 '2020/1/15-2020/1/15',
                                                                 '2020/1/15-2020/1/15']

        self.time4_temp.loc[[138,139],'stay_in_wuhan'] = ['2020/1/16-2020/1/23',
                                                          '2020/1/16-2020/1/23']
        # 之后'stay_in_wuhan'中只有工整的时间段和nan值
        self.time4_temp['stay_in_wuhan_from'] = [i.split('-')[0]
                                                 if i != 'nan' else i
                                                 for i in self.time4_temp['stay_in_wuhan'].tolist()]
        self.time4_temp['stay_in_wuhan_to'] = [i.split('-')[1]
                                               if i != 'nan' else i
                                               for i in self.time4_temp['stay_in_wuhan'].tolist()]

        return self.time4_temp


    def get_time4(self):
        '''
        purpose: conclude 4 kinds of  time points:
        'stay_in_wuhan_from','stay_in_wuhan_to','sz_arrive','onset','hospitalized'

        '''
        self.time4 = pd.concat([self.get_time4_temp().loc[:, 'stay_in_wuhan_from':'stay_in_wuhan_to'],
                                     self.get_time3()], axis=1)
        self.time4 = self.time4.apply(lambda x: pd.to_datetime(x, errors='coerce'))
        return self.time4


class hospital_discharge_process:
    def __init__(self):
        self.hospital_discharge = hospital_discharge
        self.time5 = pd.DataFrame()

    def get_time5(self):
        self.time5 = pd.concat([case_report_process().get_time4(),
                                self.hospital_discharge['cysj']], axis=1)
        self.time5 = self.time5.apply(lambda x: pd.to_datetime(x, errors='coerce'))
        self.time5.columns = ['stay_in_wuhan_from', 'stay_in_wuhan_to',
                              'sz_arrive', 'onset', 'hospitalized',
                              'hospital_discharge']
        return self.time5


class day_summary_process:
    def __init__(self):
        self.day_summary = day_summary
        self.day_summary_f = pd.DataFrame

    def get_day_summary_f(self):
        self.day_summary_f = day_summary.replace('-',0)
        self.day_summary_f['until_date'] = self.day_summary_f['until_date'].apply(lambda x: x.replace('月', '/').replace('日', '/'))

        self.day_summary_f['until_time'] = ['00' if pd.isna(i) else i for i in self.day_summary_f['until_time'].tolist()]
        self.day_summary_f['until_time'] = ['23' if i == '24时' else str(i)[0:2] for i in self.day_summary_f['until_time'].tolist()]
        self.day_summary_f['until_date'] = '2020/' + self.day_summary_f['until_date'] + ' ' + self.day_summary_f['until_time'] + ':00'

        self.day_summary_f['until_date'] = self.day_summary_f['until_date'].apply(
            lambda x: datetime.datetime.strptime(x, '%Y/%m/%d/ %H:%M'))
        self.day_summary_f = self.day_summary_f.loc[:,
                             ['until_date', 'accumulated_confirmed', 'current_isolated', 'current_medical_obs',
                              'severe_case', 'critical_severe_case',
                              'accumulated_discharge']]
        self.day_summary_f['all_severe'] = self.day_summary_f['severe_case'].apply(lambda x: int(x)) +\
                                           self.day_summary_f['critical_severe_case'].apply(lambda x: int(x))
        return self.day_summary_f

if __name__ == '__main__':
    tt = day_summary_process()
    print(tt.get_day_summary_f().head())



