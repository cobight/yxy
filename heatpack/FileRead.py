import xlrd,xlwt


#获取xlsx里所有re***，返回list
def readxlsx(infouri):
    book = xlrd.open_workbook(infouri)
    # print('sheet页名称:', book.sheet_names())
    sheet = book.sheet_by_index(0)#获取sheet1页的信息
    rows = sheet.nrows
    cols = sheet.ncols
    return [sheet.row_values(i+1)[0] for i in range(rows-1)]
class wirter:

    def __init__(self,outsrc):#class初始化
        self.outsrc=outsrc
        self._workbook = xlwt.Workbook(encoding='utf-8')
        self._worksheet = self._workbook.add_sheet('cobight')
        self._line_index = 0#第一行
    def wirteline(self,rs,lis_info):#写数据
        self._worksheet.write(self._line_index, 0, label=rs)

        self._worksheet.write(self._line_index, 1, label=lis_info[0])#前四个不带色块的
        self._worksheet.write(self._line_index, 2, label=lis_info[1])
        self._worksheet.write(self._line_index, 3, label=lis_info[2])
        self._worksheet.write(self._line_index, 4, label=lis_info[3])

        self._worksheet.write(self._line_index, 5, label=lis_info[4])#带色块的
        self._worksheet.write(self._line_index, 6, label=lis_info[5])
        self._worksheet.write(self._line_index, 7, label=lis_info[6])
        self._worksheet.write(self._line_index, 8, label=lis_info[7])
        self._worksheet.write(self._line_index, 9, label=lis_info[8])
        self._worksheet.write(self._line_index, 10, label=lis_info[9])
        self._worksheet.write(self._line_index, 11, label=lis_info[10])
        self._line_index += 1
    def write_line2(self,SNP,RegulomeDB_score,RegulomeDB_state):
        self._worksheet.write(self._line_index, 0, label=SNP)

        self._worksheet.write(self._line_index, 1, label=RegulomeDB_score)  # 前四个不带色块的
        self._worksheet.write(self._line_index, 2, label=RegulomeDB_state)

        self._line_index += 1


    def save(self,url):#保存
        self._workbook.save(self.outsrc+"/"+url)