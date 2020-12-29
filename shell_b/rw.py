#!/use/bin/python
import re
from xlutils.copy import copy
import os
vue=["P15-ATS-二期预留M113机房-INROWA-A113-1故障代码",
"P15-ATS-二期预留M113机房-INROWA-A113-1控制器状态",
"P15-ATS-二期预留M113机房-INROWA-A113-1主电选择",
"P15-ATS-二期预留M113机房-INROWA-A113-2S1触头状态",
"P15-ATS-二期预留M113机房-INROWA-A113-2S2触头状态",
"P15-ATS-二期预留M113机房-INROWA-A113-2S1-Uab",
"P15-ATS-二期预留M113机房-INROWA-A113-2S1-Ubc",
"P15-ATS-二期预留M113机房-INROWA-A113-2S1-Uca",
"P15-ATS-二期预留M113机房-INROWA-A113-2S2-Uab",
"P15-ATS-二期预留M113机房-INROWA-A113-2S2-Ubc",
"P15-ATS-二期预留M113机房-INROWA-A113-2S2-Uca",
"P15-ATS-二期预留M113机房-INROWA-A113-2S1-电压状态",
"P15-ATS-二期预留M113机房-INROWA-A113-2S2-电压状态",
"P15-ATS-二期预留M113机房-INROWA-A113-2电源类型",
"P15-ATS-二期预留M113机房-INROWA-A113-2工作模式",
"P15-ATS-二期预留M113机房-INROWA-A113-2故障代码",
"P15-ATS-二期预留M113机房-INROWA-A113-2控制器状态",
"P15-ATS-二期预留M113机房-INROWA-A113-2主电选择",
]
def main():
    v =  re.search(r'[\u4e00-\u9fa5]+', vue)
    print(v)
if __name__ == '__main__':
    main()
