import heatpack.FileRead as files
import xlrd,os

from functools import cmp_to_key
def mix_item(url,outer):
    # url = ("F:/python_space/yxy/out")
    lis = os.listdir(url)
    key = cmp_to_key(lambda x, y: int(x[5:-4]) - int(y[5:-4]))
    lis = sorted(lis, key=key)
    print(lis)
    # for index,i in enumerate(lis):
    #     print(type(int(i[5:-4])),i[5:-4])
    # sorted(lis,key=lambda x:x[5:])
    # print(lis)  int(a[5:-4])-int(b[5:-4])
    file = files.wirter(url)

    for item in lis:
        book = xlrd.open_workbook(url + "/" + item)
        # print('sheet页名称:', book.sheet_names())
        sheet = book.sheet_by_index(0)  # 获取sheet1页的信息
        rows = sheet.nrows
        # cols = sheet.ncols
        for row in range(rows):
            file.write_line2(sheet.row_values(row)[0], sheet.row_values(row)[1], sheet.row_values(row)[2])
    file.save(outer)

if __name__ == '__main__':
    mix_item("F:/python_space/yxy/out", "outer.xls")




    # url = ("F:/python_space/yxy/out") #配置打包路径
    # lis =  os.listdir(url)            #获取outer1   -   outer****
    # # lis.sort(key=lambda x,int(x[5:-4]))
    # try:
    #
    #     key = cmp_to_key(lambda x, y: int(x[5:-4]) - int(y[5:-4])) #排序
    #     print(lis)
    #     lis = sorted(lis, key=key)
    #     print(lis)
    # except Exception as e:
    #     print(e)
    #     print("out文件中的outer.xls删了么？")        #发现异常文件，估计是outer.xls没删
    # # for index,i in enumerate(lis):
    # #     print(type(int(i[5:-4])),i[5:-4])
    # # sorted(lis,key=lambda x:x[5:])
    # # print(lis)  int(a[5:-4])-int(b[5:-4])
    # file = files.wirter(url)
    #
    # for item in lis:
    #
    #     book = xlrd.open_workbook(url+"/"+item)
    #     # print('sheet页名称:', book.sheet_names())
    #     sheet = book.sheet_by_index(0)  # 获取sheet1页的信息
    #     rows = sheet.nrows
    #     # cols = sheet.ncols
    #     for row in range(rows):
    #         file.write_line2(sheet.row_values(row)[0],sheet.row_values(row)[1],sheet.row_values(row)[2])
    # file.save("outer.xls")
    # return [sheet.row_values(i + 1)[0] for i in range(rows - 1)]