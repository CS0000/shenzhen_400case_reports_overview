# Shenzhen 400case reports overview
An overview of 400 COVID-19 cases in Shenzhen. Python3 plotly and dash were used to generate visualization.

### 数据来源 data resource
深圳市政府数据开放平台：
https://opendata.sz.gov.cn/data/dataSet/toDataDetails/29200_01503668

需注册账号获取数据。本项目中不包含原始数据。自行下载数据后更改app.py中原始数据路径即可。

### 操作示例
`$ python app.py `
Running on http://127.0.0.1:8050/...

在浏览器中访问http://127.0.0.1:8050/
![](https://github.com/CS0000/shenzhen_400case_reports_overview/blob/master/demo_result/20200220_2.gif)

右边为主图，包括深圳市400例病例的来深时间，发病时间，入院时间三个时间点。被粉色线连起的三个时间点表示了一个病例的发展情况。

左边为metadata副图，即400病例的性别，年龄段及居住地。
![](https://github.com/CS0000/shenzhen_400case_reports_overview/blob/master/demo_result/20200222_demo.png)

### to be done...
1. 在主图中加入出院时间及在深圳市外活动的区间。
2. hoverinfo中需要包含更多详细信息
3. 概况折线图：x轴为日期，y轴为个案counts，包含5条折线（确诊，危重症，出院，隔离治疗，医学观察）
4. ...=_=