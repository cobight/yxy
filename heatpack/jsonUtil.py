import json,re
class Mjson:
    def loads(self,input=""):
        self.mjson=json.loads(input)
    def loadd(self,dic={ }):
        self.mjson=dic
    def _re_in(self,item=""):
        msg = re.findall("\[(.*?)\]", item)
        if len(msg) ==1:
            return msg[0]
        else:
            return msg
    def reads(self,select=""):
        dic=self.mjson
        if  select != "":
            lis=select.split('.')
            for i in lis:
                if type(dic) == dict:#循环中，如果不是字典，会崩的
                    if "][" in i:
                        x = list(dic[i[0:i.find("[")]])
                        lis=self._re_in(i)
                        for q in lis:
                            x=x[int(q)]
                        dic=x
                    elif "[" in i and "]" in i:
                        x = list(dic[i[0:i.find("[")]])
                        dic=x[int(self._re_in(i))]
                    else:
                        dic=dic[i]
                else:
                    return None
        return dic