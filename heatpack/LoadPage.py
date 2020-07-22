import requests
import time

from requests.adapters import HTTPAdapter

import heatpack.FileRead as files
from heatpack.jsonUtil import Mjson
def Loead_Page(rs):
    try:
        page = requests.get("http://pubs.broadinstitute.org/mammals/haploreg/detail_v4.1.php?query=&id="+rs)
        return page.text
    except Exception as e:
        print("LOAD_PAGE_ERRO,RS:" + rs)
        time.sleep(1000)
        return Loead_Page(rs)
def Load_Page2(name,rs,retry=5):
    print(name, rs)
    try:
        headers={
            # "User-Agent":" Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400",
            "Host": "legacy.regulomedb.org",
            "Origin": "http://legacy.regulomedb.org",
            "Referer": "http://legacy.regulomedb.org/",
            "Cookie": "__utmz=90025862.1595332486.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=90025862; __utma=90025862.1887762124.1595332486.1595401368.1595408542.6; __utmt=1; sid=3868c64ccef81c2a873bdb890628b8c0bcd123fc; __utmb=90025862.17.10.1595408542"
        }

        session = requests.Session()
        session.keep_alive = False
        session.mount('http://' , HTTPAdapter(max_retries=4))  # 设置重试次数为3次
        session.mount('https://', HTTPAdapter(max_retries=4))
        page = session.post("http://legacy.regulomedb.org/results", headers=headers, data={"data": rs}, timeout=10)
        lis = getUrl_Score(page.text)
        if lis != []:
            session.close()
            return lis
        else:#server erro会返回空数组，重载，直到成功加载页面
            if retry==1:
                print("name 出现重复过多，rs："+rs, "跳过")
                return []#避免死循环，罢工了
            print(name + "server erro ，reload——page ，rs: " + rs)
            return Load_Page2(name, rs,retry-1)

    except Exception as e:
        print(e)
        print(name + "LOAD_PAGE_ERROR,SLEEP ONE SECOND , RS:" + rs)  # 超时重载
        time.sleep(1)

        return Load_Page2(name, rs)
def getE079(text):
    # print(text)
    first = text.find("<tr><td>E079")
    last = text.find("</tr>",first)
    # print("\n\n")
    tr = text[first+4+3:last-5]#匹配到的行标签
    # print(tr)
    # msg = re.findall("<td(.*?)</td>",tr)
    # text2 = [msg[i] for i in range(len(msg))]
    # print(text2)
    lis = str(tr).split("</td><td")
    # print(lis)

    retn = [lis[0][1:],lis[1][1:],lis[2][1:],lis[3][1:]]
    retn.append(lis[4].split(">")[1])
    retn.append(lis[5].split(">")[1])
    retn.append(lis[6].split(">")[1])
    retn.append(lis[7].split(">")[1])
    retn.append(lis[8].split(">")[1])
    retn.append(lis[9].split(">")[1])
    retn.append(lis[10].split(">")[1])
    return retn
def getUrl_Score(text):
    right = (text.find("<title>RegulomeDB Results</title>"))
    #erro  = (text.find("<title>Server error</title>"))
    if right == -1:
        print("getScore err")
        return []
    else:

        left  = text.find("var dtParams =")
        left  = text.find("{", left)
        right = text.find(";", left)
        # print(text[left:right])#定位json
        jsn = Mjson()
        jsn.loads(text[left:right])
        lis = (jsn.reads("aaData[0]"))
        # if lis[2] == 7:
        #     lis[2] = "No Data"
        a, b = lis[0].split(":")
        return [a, b, lis[2]]
def Load_Page2_next(uri):

    url = "http://legacy.regulomedb.org/snp/" + uri
    try:
        session = requests.Session()
        session.keep_alive = False
        session.mount('http://', HTTPAdapter(max_retries=4))  # 设置重试次数为3次
        session.mount('https://', HTTPAdapter(max_retries=4))
        page = session.get(url, timeout=10)
        left = 0
        for p in range(6):

            left = page.text.find("var dtParams = {", left+100)
            left = page.text.find("{", left)
            right = page.text.find(";", left)
            jsn = Mjson()
            jsn.loads(page.text[left:right])
            liss = (jsn.reads("aaData"))
            if liss[0][0]=="ChromHMM":
                for i in liss:
                    if i[0]=="ChromHMM" and i[3]=="Digestive" and i[4]=="Esophagus":
                        session.close()
                        return i[2]
        session.close()
        print("out of for 6 , 6次循环结束，依然没返回")
        return Load_Page2_next(uri)
    except Exception as e:
        print(e)
        print("uri"+uri)
        return Load_Page2_next(uri)

if __name__ == '__main__':#测试demo
    # file = files.wirter()
    lis = Load_Page2("thread1", "rs4767530")  # 获取网页html文档
    print(lis)

    if lis[2] != 7:
        score = lis[2]
        state = Load_Page2_next(lis[0]+"/"+lis[1])
        print(":::",score, state)

    #     Load_Page2_next("chr12/110280565")
    # colum = getE079(text)  # 解析文档，返回数据
    # file.wirteline("rs180844300", colum)#写一行
    # file.save("outtest.xls")  # 写到文件

