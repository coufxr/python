#!/use/bin/python
import xlwt
def main():
    lists = []
    f = open('fw1_rule_udp.log')
    for i in range(1924):
        row = f.readline()
        vul = row.split(' ')
        if '198' in vul[2] or '10' in vul[2]:  ## 过滤ip地址
            for j in range(len(vul)):
                vul[j] = vul[j].split('=')[-1]
            vul[4] = "UDP"  # 替换成UDP
            vul.pop(1)  # 删除原端口
            lists.append(vul)  # 赋值给lists0

    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    ws = wb.add_sheet('sheet1', cell_overwrite_ok=True)
    dic = list(set([tuple(t) for t in lists]))#将二维数组中的二维转化成元组
    dic=set(dic)#set去重
    k=0
    for ret in dic:
        for w in range(len(ret)):
            ws.write(k, w, ret[w])
        print(k, ret)
        k = k + 1
    wb.save('udp.xlsx')
if __name__ == '__main__':
    main()
