import os
import heatpack.FileRead as files
import heatpack.LoadPage as load
import threading



class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "Thread-" + str(threadID)

    def set_rslis(self, lis):  # 传入rs列表
        self.lis = lis

    def run(self):
        print("开始线程：" + self.name)
        self.file = files.wirter(os.getcwd())
        for i in self.lis:

            lis = load.Load_Page2(self.name, i)  # 获取网页html文档
            if len(lis) >= 3 and lis[2] != 7:
                score = lis[2]
                print(self.name, "start_next")
                state = load.Load_Page2_next(lis[0] + "/" + lis[1])
                self.file.write_line2(i, score, state)
            elif len(lis) >= 3 and lis[2] == 7:
                self.file.write_line2(i, "无", "No Data")
            else:
                self.file.write_line2(i, "打不开", "打不开")

        self.file.save("out/outer" + str(self.threadID) + ".xls")  # 写到文件
        print("退出线程：" + self.name)


if __name__ == '__main__':
    PATH = os.getcwd()
    if not os.path.exists(PATH + "/out"):  # 输出专用文件 不存在就创建
        os.makedirs(PATH + "/out")
    urllist = files.readxlsx('info/RegulomeDB-去.xlsx')  # 读取文件中的rs列表
    urllist = [urllist[i] for i in range(3600, 3800)]  # 测试2000个
    # for i in urllist:
    #     print(i)#检验rs是否齐全rs180844300《--》rs999839

    threadnum = 10

    average = int(len(urllist) / threadnum)  # 平均线程操作数量
    thread_liss = []  # 线程数组

    for x in range(threadnum - 1):  # 0-------num-1
        thread = myThread(x + 1)
        thread.set_rslis([urllist[average * x + i] for i in range(average)])
        thread_liss.append(thread)

    thread1 = myThread(threadnum)
    thread1.set_rslis([urllist[average * (threadnum - 1) + i] for i in range(len(urllist) - (threadnum - 1) * average)])
    thread_liss.append(thread1)  # 剩下的，包括余数打包到最后一个线程

    for thread_item in thread_liss:  # 启动
        thread_item.start()
    for thread_item in thread_liss:  # 加入队列
        thread_item.join()
    print("=======开始打包数据=======")
    import heatpack.Mix_Item as mix
    mix.mix_item(PATH + "/out", "outer.xls")
    print("=======打包结束=======")
    print("=======主线程结束=======")
