# -*- coding:utf-8 -*-
# @Time : 2020-03-02 8:23
# @Author: Yicheng Zhang
# @File : test.py

import pandas as pd
import pandas_profiling

if __name__ == "__main__":
    # path = 'my.xlsx'
    # data = pd.read_excel(path)
    # profile = pandas_profiling.ProfileReport(data)
    # profile.to_file(outputfile="output_file.html")

    import numpy as np
    list=[0, 0, 0, 0, 1, 2, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    a = np.array(list).reshape(4, 4)
    diagonal = np.diag_indices(4)
    print(diagonal)
    x1 = diagonal[0]
    y1 = np.array(diagonal[1]).reshape(4, 1)
    d = np.sqrt((x1 - 0) ** 2 + (y1 - 0) ** 2)
    print(a)
    print("XXX")
    print(x1)
    print("XXX")
    print("XXX")
    print(y1)
    print("XXX")
    print("XXX")
    print(d)
