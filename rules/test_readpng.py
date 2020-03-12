# -*- coding:utf-8 -*-
# @Time : 2020-03-02 8:23
# @Author: Yicheng Zhang
# @File : test.py

from RoundUp import *
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches
import math

import os
import sys


def take_png(path, files):
    # sys.path.append(
    #     os.path.abspath(os.path.join(os.getcwd(), path)))
    # print(path)
    img = cv2.imread(os.path.join(path, files))
    # img = cv2.imdecode(np.fromfile(files, dtype=np.uint8), -1)

    b, g, r = cv2.split(img)
    image = cv2.merge([r, g, b])

    df_r_o = pd.DataFrame(r)
    df_g_o = pd.DataFrame(g)
    df_b_o = pd.DataFrame(b)
    return df_r_o, df_g_o, df_b_o, image


def distance(df):
    # df['x'] = abs(df.columns ** 2 - 155)
    # df['y'] = abs(df.index ** 2 - 155)
    # df['df_res'] = math.sqrt(df['x'] + df['y'])
    # df_res=df[math.sqrt(df.index**2+df.columns**2)<=93]

    # df = df.values
    # df_diagonal=df.diagonal()
    # print(df_diagonal)

    diagonal = np.diag_indices(300)
    x1 = diagonal[0]
    y1 = np.array(diagonal[1]).reshape(300, 1)
    d = np.sqrt((x1 - 153) ** 2 + (y1 - 151) ** 2)
    d = pd.DataFrame(d)
    df = df[d <= 93]
    return df

    # diagonal = np.diag_indices(300)
    # df_diagonal=df[diagonal]
    # x1 = df_diagonal[0]
    # y1 = np.array(df_diagonal[1]).reshape(4, 1)
    # d = np.sqrt((x1 - 0) ** 2 + (y1 - 0) ** 2)


def panduan(df):
    panduan_df = df.values.reshape(-1, 1)
    panduan_df = pd.DataFrame(panduan_df)
    res = panduan_df.iloc[:, 0].value_counts()
    print("res")
    # col_name=panduan_df.columns
    # res=panduan_df.groupby(col_name[100]).mean()
    # 返回最终颜色r，g，b值，及其比例
    res_list = res.iloc[:3]
    res_list_value = res_list.index / 255
    print(res_list)
    # 返回最终颜色r，g，b百分比
    # df_totall = 3.1415926 * 93 ** 2
    if res_list.shape[0] == 1:
        res_1_per = round_up(res_list.iloc[0] / res.sum() * 100, 2)
        res_2_per = 0
        res_3_per = 0
    elif res_list.shape[0] == 2:
        res_1_per = round_up(res_list.iloc[0] / res.sum() * 100, 2)
        res_2_per = round_up(res_list.iloc[1] / res.sum() * 100, 2)
        res_3_per = 0
    else:
        res_1_per = round_up(res_list.iloc[0] / res.sum() * 100, 2)
        res_2_per = round_up(res_list.iloc[1] / res.sum() * 100, 2)
        res_3_per = round_up(res_list.iloc[2] / res.sum() * 100, 2)

    res_per_list = [res_1_per, res_2_per, res_3_per]
    print(res_per_list)
    return res_list_value, res_per_list


if __name__ == "__main__":

    path = r'D:\\NEW\\M'
    new_path = r'D:\\result_new\\M'
    count = os.listdir(path)
    for root, dirs, files in os.walk(path):
        if len(dirs) == 0:
            for i in range(len(files)):
                print("i=", i)
                if files[i].find('.png') != -1:
                    print(files[i])

                    df_r_o, df_g_o, df_b_o, image = take_png(path, files[i])
                    df_r_o1 = distance(df_r_o)
                    df_g_o1 = distance(df_g_o)
                    df_b_o1 = distance(df_b_o)
                    res_r_list, res_r_per_list = panduan(df_r_o1)
                    res_g_list, res_g_per_list = panduan(df_g_o1)
                    res_b_list, res_b_per_list = panduan(df_b_o1)
                    #
                    # 生成图例
                    res_green_patch_per = np.mean([res_r_per_list[0], res_g_per_list[0], res_b_per_list[0]])
                    res_red_patch_per = np.mean([res_r_per_list[1], res_g_per_list[1], res_b_per_list[1]])
                    res_yellow_patch_per = np.mean([res_r_per_list[2], res_g_per_list[2], res_b_per_list[2]])
                    if res_yellow_patch_per < 1 and res_red_patch_per >= 1:
                        res_red_patch_per = round_up(100 - res_green_patch_per, 2)
                        green_patch = mpatches.Patch(color=[res_r_list[0], res_g_list[0], res_b_list[0]],
                                                     label='The data1 %s' % res_green_patch_per)
                        red_patch = mpatches.Patch(color=[res_r_list[1], res_g_list[1], res_b_list[1]],
                                                   label='The data2 %s' % res_red_patch_per)
                        plt.legend(handles=[green_patch, red_patch])
                    elif res_yellow_patch_per < 1 and res_red_patch_per < 1:
                        res_green_patch_per=100
                        green_patch = mpatches.Patch(color=[res_r_list[0], res_g_list[0], res_b_list[0]],
                                                     label='The data1 %s' % res_green_patch_per)
                        plt.legend(handles=[green_patch])
                    else:
                        res_red_patch_per = round_up(100 - res_green_patch_per - res_yellow_patch_per, 2)

                        green_patch = mpatches.Patch(color=[res_r_list[0], res_g_list[0], res_b_list[0]],
                                                     label='The data1 %s' % res_green_patch_per)
                        red_patch = mpatches.Patch(color=[res_r_list[1], res_g_list[1], res_b_list[1]],
                                                   label='The data2 %s' % res_red_patch_per)
                        yellow_patch = mpatches.Patch(color=[res_r_list[2], res_g_list[2], res_b_list[2]],
                                                      label='The data3 %s' % res_yellow_patch_per)

                        plt.legend(handles=[green_patch, red_patch, yellow_patch])

                    plt.imshow(image)
                    plt.axis('off')
                    # plt.show()
                    plt.savefig(os.path.join(new_path, files[i]))
                    # name = "AB.xlsx"
                    # writer = pd.ExcelWriter(name)  # 写入Excel文件
                    # df_r_o.to_excel(writer, 'df_r_o', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # df_r_o1.to_excel(writer, 'df_r_o1', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    #
                    # # df_g_o.to_excel(writer, 'df_g_o', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # # df_b_o.to_excel(writer, 'df_b_o', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # # res.to_excel(writer, 'res', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # #
                    # # # df_r_cont.to_excel(writer, 'page_2', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    #
                    # writer.save()
