import os
import heatpack.FileRead as files
import heatpack.LoadPage as load
import threading

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "Thread-" + str(threadID)

    def set_rslis(self, lis):#传入rs列表
        self.lis = lis

    def run(self):
        print("开始线程：" + self.name)
        self.file = files.wirter(os.getcwd())
        for i in self.lis:
            print(i)#控制台输出当前操作的 rs***
            text = load.Loead_Page(i)  # 获取网页html文档
            colum = load.getE079(text)  # 解析文档，返回数据

            self.file.wirteline(i, colum)#写一行

        self.file.save("out" + str(self.threadID) + ".xls")#写到文件
        print("退出线程：" + self.name)


if __name__ == '__main__':
    PATH = os.getcwd()
    if not os.path.exists(PATH + "/out"):  # 输出专用文件 不存在就创建
        os.makedirs(PATH + "/out")

    urllist = files.readxlsx('info/haploreg.xlsx')#读取文件中的rs列表

    # urllist = [urllist[i] for i in range(58)]  # 测试58个
    # for i in urllist:
    #     print(i)#检验rs是否齐全rs180844300《--》rs999839

    threadnum = 15

    average = int(len(urllist) / threadnum)  # 平均线程操作数量
    thread_liss = [] #线程数组

    for x in range(threadnum - 1):  # 0-------num-1
        thread = myThread(x + 1)
        thread.set_rslis([urllist[average * x + i] for i in range(average)])
        thread_liss.append(thread)

    thread1 = myThread(threadnum)
    thread1.set_rslis([urllist[average * (threadnum - 1) + i] for i in range(len(urllist) - (threadnum - 1) * average)])
    thread_liss.append(thread1)  # 剩下的，包括余数打包到最后一个线程

    for thread_item in thread_liss:#启动
        thread_item.start()
    for thread_item in thread_liss:#加入队列
        thread_item.join()

    # 创建新线程
    # thread1 = myThread(1, "Thread-1", 1)
    # thread2 = myThread(2, "Thread-2", 2)
    #
    # # 开启新线程
    # thread1.start()
    # thread2.start()
    # thread1.join()
    # thread2.join()
    print("=======退出主线程=======")
