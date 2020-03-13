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
    img = cv2.imread(os.path.join(path, files))

    # 将图片转为灰度图
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    b, g, r = cv2.split(img)
    image = cv2.merge([r, g, b])
    # cv2.imshow("img_gray", img_gray)
    # cv2.waitKey()
    # image_zip = np.dstack((tuple(r.reshape(1, -1)), tuple(g.reshape(1, -1))))
    # image_zip = np.dstack((image_zip, tuple(b.reshape(1, -1))))
    # image_zip = image_zip.reshape(300, 300, 3)
    #
    # print(":::::")
    # print(image_zip.shape)
    # print(image_zip[151, 153, :])
    # print(image[151, 153, :])
    # print(":::::")
    df_r_o = pd.DataFrame(r)
    df_g_o = pd.DataFrame(g)
    df_b_o = pd.DataFrame(b)

    img_gray = pd.DataFrame(img_gray)

    return image, img_gray


def distance(df):
    diagonal = np.diag_indices(300)
    x1 = diagonal[0]
    y1 = np.array(diagonal[1]).reshape(300, 1)
    d = np.sqrt((x1 - 153) ** 2 + (y1 - 151) ** 2)
    d = pd.DataFrame(d)
    df = df[d <= 93]
    return df


def panduan_all(df_gray):
    # 返回灰度值，及其比例
    df_gray_ya = df_gray.values.reshape(-1, 1)
    df_gray_ya = pd.DataFrame(df_gray_ya)
    res_gray = df_gray_ya.iloc[:, 0].value_counts()
    res_list = res_gray.iloc[:3]
    res_index_list = list(res_list.index)
    print(res_index_list)
    if res_list.shape[0] == 1:
        res_1_per = round_up(res_list.iloc[0] / res_list.sum() * 100, 2)
        res_2_per = 0
        res_3_per = 0
    elif res_list.shape[0] == 2:
        res_1_per = round_up(res_list.iloc[0] / res_list.sum() * 100, 2)
        res_2_per = round_up(res_list.iloc[1] / res_list.sum() * 100, 2)
        res_3_per = 0
    else:
        res_1_per = round_up(res_list.iloc[0] / res_list.sum() * 100, 2)
        res_2_per = round_up(res_list.iloc[1] / res_list.sum() * 100, 2)
        res_3_per = round_up(res_list.iloc[2] / res_list.sum() * 100, 2)

    res_per_list = [res_1_per, res_2_per, res_3_per]

    # 返回最终颜色r，g，b对应位置
    # df_r_ya = df_r.values.reshape(-1, 1)
    # df_g_ya = df_g.values.reshape(-1, 1)
    # df_b_ya = df_b.values.reshape(-1, 1)
    #
    # df_r_ya = pd.DataFrame(df_r_ya)
    # df_g_ya = pd.DataFrame(df_g_ya)
    # df_b_ya = pd.DataFrame(df_b_ya)
    # res_r = df_r_ya.iloc[:, 0].value_counts()
    # res_g = df_g_ya.iloc[:, 0].value_counts()
    # res_b = df_b_ya.iloc[:, 0].value_counts()
    # res_r_list = list(res_r.iloc[:3].index)
    # res_g_list = list(res_g.iloc[:3].index)
    # res_b_list = list(res_b.iloc[:3].index)

    # print(res_r_list)
    # col_r_list, col_g_list, col_b_list = [], [], []
    col_list = []
    for i in range(0, len(res_index_list)):
        r_x = df_gray.index[np.where(df_gray == res_index_list[i])[0]][10]
        r_y = df_gray.columns[np.where(df_gray == res_index_list[i])[1]][10]
        col_list.append([r_x, r_y])

    # for i in range(0, len(res_g_list)):
    #     g_x = df_g.index[np.where(df_g == res_g_list[i])[0]][10]
    #     g_y = df_g.columns[np.where(df_g == res_g_list[i])[1]][10]
    #     col_g_list.append([g_x, g_y])
    #
    # for i in range(0, len(res_b_list)):
    #     b_x = df_b.index[np.where(df_b == res_b_list[i])[0]][10]
    #     b_y = df_b.columns[np.where(df_b == res_b_list[i])[1]][10]
    #     col_b_list.append([b_x, b_y])

    return res_per_list, col_list


def panduan(df):
    panduan_df = df.values.reshape(-1, 1)
    panduan_df = pd.DataFrame(panduan_df)
    res = panduan_df.iloc[:, 0].value_counts()
    # 返回最终颜色r，g，b值，及其比例
    res_list = res.iloc[:3]
    # print("hhhhhhhhhhhh")
    # print(res)
    if res_list.shape[0] == 1:
        res_list = pd.DataFrame([res_list.index, res_list.index, res_list.index])

    res_list_value = res_list.index / 255

    return res_list_value


if __name__ == "__main__":

    path = r'D:\\NEW\\1'
    new_path = r'D:\\result_new\\F'
    count = os.listdir(path)
    for root, dirs, files in os.walk(path):
        if len(dirs) == 0:
            for i in range(len(files)):
                # print("i=", i)
                if files[i].find('.png') != -1:
                    print(files[i])

                    image, img_gray = take_png(path, files[i])
                    # df_r_o1 = distance(df_r_o)
                    # df_g_o1 = distance(df_g_o)
                    # df_b_o1 = distance(df_b_o)
                    img_gray = distance(img_gray)
                    res_per_list, col_list = panduan_all(img_gray)
                    #
                    # res_r_list = panduan(df_r_o1)
                    # res_g_list = panduan(df_g_o1)
                    # res_b_list = panduan(df_b_o1)
                    # print(res_r_list)
                    # print(res_g_list)
                    # print(res_b_list)

                    #
                    # 生成图例
                    # 有两种颜色
                    if res_per_list[2] < 0.5 and res_per_list[1] >= 0.5:
                        res_red_patch_per = round_up(100 - res_per_list[0], 2)
                        col1 = image[col_list[0][0], col_list[0][1], :] / 255
                        col2 = image[col_list[1][0], col_list[1][1], :] / 255
                        col3 = image[col_list[2][0], col_list[2][1], :] / 255

                        green_patch = mpatches.Patch(color=col1, label='The data1 %s' % res_per_list[0])
                        red_patch = mpatches.Patch(color=col2, label='The data2 %s' % res_red_patch_per)
                        plt.legend(handles=[green_patch, red_patch])
                    # 有一种颜色
                    elif res_per_list[2] < 0.5 and res_per_list[1] < 0.5:
                        res_green_patch_per = 100
                        green_patch = mpatches.Patch(color=col1, label='The data1 %s' % res_green_patch_per)
                        plt.legend(handles=[green_patch])
                    # 有三种颜色
                    else:
                        res_red_patch_per = round_up(100 - res_per_list[0] - res_per_list[2], 2)

                        green_patch = mpatches.Patch(color=col1, label='The data1 %s' % res_per_list[0])
                        red_patch = mpatches.Patch(color=col2, label='The data2 %s' % res_red_patch_per)
                        yellow_patch = mpatches.Patch(color=col3, label='The data3 %s' % res_per_list[2])

                        plt.legend(handles=[green_patch, red_patch, yellow_patch])

                    plt.imshow(image)
                    plt.axis('off')
                    plt.show()
                    plt.savefig(os.path.join(new_path, files[i]))
                    # name = "AB.xlsx"
                    # writer = pd.ExcelWriter(name)  # 写入Excel文件
                    # img_gray.to_excel(writer, 'img_gray', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # df_r_o1.to_excel(writer, 'df_r_o1', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # df_r_o.to_excel(writer, 'df_r_o', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # df_g_o.to_excel(writer, 'df_g_o', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # df_b_o.to_excel(writer, 'df_b_o', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # # # res.to_excel(writer, 'res', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # # #
                    # # # # df_r_cont.to_excel(writer, 'page_2', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    #
                    # writer.save()
