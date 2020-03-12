# -*- coding:utf-8 -*-
# @Time : 2020-03-02 8:23
# @Author: Yicheng Zhang
# @File : test.py

import RoundUp
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    path = 'n1.png'
    img = cv2.imread(path)
    img_array=np.array(img)


    b, g, r = cv2.split(img)
    image = cv2.merge([r, g, b])
    # cv2.imshow('Example', img)


    # cv2.waitKey(0)
    df = pd.DataFrame(r)
    df_r=df[df<255]
    df_cont=(df<255).sum()
    df_totall=3.1415926*93**2
    df_cont_per=round_up(df_cont.sum()/df_totall,2)*100
    ddf_cont_per = 100-df_cont_per

    plt.legend([df_cont_per, ddf_cont_per], ["CH", "US"],loc='upper right')
    plt.imshow(image)
    # writer = pd.ExcelWriter('A.xlsx')  # 写入Excel文件
    # df_r.to_excel(writer, 'page_1', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
    # df_cont.to_excel(writer, 'page_2', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
    #
    # print('A.xlsx')
    # writer.save()


