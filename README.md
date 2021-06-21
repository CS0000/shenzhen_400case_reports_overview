# Shenzhen 436 case reports overview
A glance of 436 COVID-19 cases in Shenzhen. Python3 plotly and dash were used to generate visualization.

### data resource 数据来源
Open dataset from the government of shenzhen 深圳市政府数据开放平台：
https://opendata.sz.gov.cn/data/dataSet/toDataDetails/29200_01503668

note:
* There won't be any hospital discharge case exposing after Feb 26 2020. 
* This project is based on released case report data until March 20th 2020, including 417 initial cases and indigenous cases + 19 imported cases from other countries. 
* You may need to provide a phone number to obtain the raw data table from this opendata resource platform. This project doesn't include the raw data table. You may download the data and change the path directory in `app.py`.

* 另外深圳市从2020年2月26日起不再公布出院个案。
* 数据截至至2020年3月20日，共计417例既有病例 + 19例输入病例。
* 需注册账号获取数据。本项目中不包含原始数据。自行下载数据后更改app.py中原始数据路径即可。


### to be done...
- [X] consist of 4 graph, 1 main graph and 3 annotated graph 

![](https://upload-images.jianshu.io/upload_images/5638276-05c3eea60d0849f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- [x] add timepoint of hospital discharge & time period outside shenzhen city 在主图中加入出院时间及在深圳市外活动的区间:
* add time period of staying in Wuhan (e.g. stay_in_wuhan_from: XX/XX/2020; stay_in_wuhan_to: XX/XX/2020)
* if the time period of staying in Wuhan started before 2020 (such as 01/10/2019), it suggests that this case is wuhan resident move to shenzhen afterwards
* if there is only one point present the time period, it suggests that this case temporarily stop in wuhan rather than resident. 

* 加上了各个病例在武汉活动的区间及出院时间。如在武汉区间(stay_in_wuhan_from/to)
* 区间的stay_in_wuhan_from为2019/10/1/，则表明该病例常驻武汉。
* 如区间只有一个点，则表明该病例在武汉短暂逗留，非常驻武汉。          
                  
                          
- [X] more detail in hoverinfo
* main graph: add case ID, date info and note (annotated with symptoms and the places they passed; the notes are written in Chinese) 
* annotated graph: add case ID and related metadata 

* 在主图hover中加入了caseID, 相关日期，Note(备注症状与途径地)
* 在副图hover中加入了caseID,相关Metadata信息         
                        
              
- [X] I will visualize the cases reported after Feb 28th 2020 (after case ID 418). They are imported cases from abroad with a limited sample size.    2020年2月28日之后的（即病例418及其之后的）境外输入病例单独可视化，因其数量少，可手工编辑信息，将时间线描述得更加详细。
- [ ] Maybe add the release time of each case; 需要再加上病例公布时间，公布病例数目为每日新增病例的统计途径，而非发病或者入院(入院不一定是确诊)。
- [ ] add special marker to death case 死亡病例特殊标记
- [ ] How to present cases with familly aggregation? 家族聚集如何表示？  


### demonstration 操作示例
`$ python app.py `
Running on http://127.0.0.1:8050/...


reach `http://127.0.0.1:8050/` in your preferred browser (I prefer chrome)
在浏览器中访问http://127.0.0.1:8050/
![an old version gif demo](https://github.com/CS0000/shenzhen_400case_reports_overview/blob/master/demo_result/20200220_2.gif)


右边为主图，包括深圳市400例病例的在武汉区间(包括from和to两个时间点)，来深时间，发病时间，入院时间，出院时间6个时间点。被粉色线连起的三个时间点表示了一个病例的发展情况。


左边为metadata副图，即400病例的性别，年龄段及居住地。
![updated to 20200224](https://github.com/CS0000/shenzhen_400case_reports_overview/blob/master/demo_result/20200321_demo.png)




:sparkling_heart:  :sparkling_heart:  :sparkling_heart:  :sparkling_heart:  :sparkling_heart: