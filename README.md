# Shenzhen 400case reports overview
An overview of 400 COVID-19 cases in Shenzhen. Python3 plotly and dash were used to generate visualization.

### 数据来源 data resource
深圳市政府数据开放平台：
https://opendata.sz.gov.cn/data/dataSet/toDataDetails/29200_01503668

需注册账号获取数据。本项目中不包含原始数据。自行下载数据后更改app.py中原始数据路径即可。


### to be done...
- [x] 在主图中加入出院时间及在深圳市外活动的区间:
* 加上了各个病例在武汉活动的区间及出院时间。如在武汉区间(stay_in_wuhan_from/to)
* 区间的stay_in_wuhan_from为2019/10/1/，则表明该病例常驻武汉。
* 如区间只有一个点，则表明该病例在武汉短暂逗留，非常驻武汉。

- [X] hoverinfo中需要包含更多详细信息
* 在主图hover中加入了caseID, 相关日期，Note(备注症状与途径地)
* 在副图hover中加入了caseID,相关Metadata信息

- [X] 概况折线图：x轴为日期，y轴为个案counts，包含5条折线（确诊，危重症，出院，隔离治疗，医学观察）
* 由4个图组成：

meatadata  |summary each day(counts):
summary    |all_severe
counts     |accumulated_confirmed
           |current_isolated
           |current_medical_obs
           |accumulated_discharge
-----------+-------------------------
metadata   |main plot:
of each    |visualizes the time stayingin wuhan,
case       |arriving Shenzhen
           |onset,hospitalized and discharge
           |in every case
           |connecting with pink lines

- [ ] 需要再加上病例公布时间，公布病例数目为每日新增病例的统计途径，而非发病或者入院(入院不一定是确诊)。
- [ ] 死亡病例特殊标记
- [ ] 家族聚集如何表示？


:sparkling_heart:  :sparkling_heart:  :sparkling_heart:  :sparkling_heart:  :sparkling_heart:


### 操作示例
`$ python app.py `
Running on http://127.0.0.1:8050/...

在浏览器中访问http://127.0.0.1:8050/
![an old version gif demo](https://github.com/CS0000/shenzhen_400case_reports_overview/blob/master/demo_result/20200220_2.gif)

右边为主图，包括深圳市400例病例的在武汉区间(包括from和to两个时间点)，来深时间，发病时间，入院时间，出院时间6个时间点。被粉色线连起的三个时间点表示了一个病例的发展情况。

左边为metadata副图，即400病例的性别，年龄段及居住地。
![updated to 20200224](https://github.com/CS0000/shenzhen_400case_reports_overview/blob/master/demo_result/20200229_demo.png)



