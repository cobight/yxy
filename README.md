# yxy
yc豪姐的爬虫project<br>
## Model_1

数据网址 ：(get访问) 
http://pubs.broadinstitute.org/mammals/haploreg/detail_v4.1.php?query=&id= +rs号<br>
用户需求 ：获取匹配网址的页面数据，找到E079所在行的所有数据<br>
包括信息：<br>
1、前面四个td列的内容<br>
2、后面所有td列的颜色与内容<br>

项目架构 :<br>

|  分类      | 文件名| 关联的方法|
| ---- | ---- | ---- |
|  主程序文件    |  RunToDownload.py        | All   |
| 文件操作模块     | heatpack\FileRead.py     | readxlsx 、 wirter类\[\_\_init\_\_ 、wirteline、save\]   |
| json数据操作模块 | heatpack\jsonUtil.py     | Mjson类\[All\]   |
| 页面加载与解析模块| heatpack\LoadPage.py     | Loead_Page、getE079   |


## Model_2

数据网址1：(post访问，服务器不稳定) 
http://legacy.regulomedb.org/results <br>
连接防异常措施：设置超时10秒，补充请求头，设置重试次数4次<br>
【采坑处1】<br>
数据获取有可能打不开，尝试N次后跳过
getUrl_Score方法解析时 ，tittle不是Server error，而是RegulomeDB Results，解析成功
找"var dtParams ="获取json数据，通过Mjson解析获取评分或No Data，还有两个拼接网址的数据

数据网址2：(get访问，服务器较稳定)
"http://legacy.regulomedb.org/snp/" + uri <br>
uri是上面解析的<br>
连接防异常措施：设置超时10秒，设置重试次数4次<br>
【采坑处2】<br>
找"var dtParams ="获取json数据，json数据需要ChromHMM的，所以可能不是前两个，有可能是第六个匹配的"var dtParams ="<br>
【采坑处3】<br>
如果页面没加载完，或者数据连接中断，得到了网页的一半数据，循环6次也是获取不到的，所以循环后也得加特殊处理情况<br>
比如这个页面一定有此数据，那就执行异常重载，再次执行这个方法，从新读数据<br>
【采坑处4】<br>
网络中断或加载失败，甚至访问池中过载引起的异常，需要抛出异常，睡眠1秒，然后执行异常重载此页面<br>
然后开始往内存的临时数据中写data
子线程执行完列表里所有的rs数据后，输出到out文件里对应的outer*.xls

项目架构 :<br>

|  分类      | 文件名| 关联的方法|
| ---- | ---- | ---- |
|  主程序文件    |  RunToDownload2.py        | All   |
| 文件操作模块     | heatpack\FileRead.py     | readxlsx 、 wirter类\[\_\_init\_\_ 、wirte_line2、save\]   |
| json数据操作模块 | heatpack\jsonUtil.py     | Mjson类\[All\]   |
| 页面加载与解析模块| heatpack\LoadPage.py     | Loead_Page2、getUrl_Score、Load_Page2_next   |
| 文件合并模块     | heatpack\Mix_Item.py     | mix_item  |


