# -*- coding:utf-8 -*-
# @Time : 2020-03-02 8:23
# @Author: Yicheng Zhang
# @File : test.py

import pandas as pd
import pandas_profiling

if __name__ == "__main__":
    path = 'my.xlsx'
    data = pd.read_excel(path)
    profile = pandas_profiling.ProfileReport(data)
    profile.to_file(outputfile="output_file.html")
