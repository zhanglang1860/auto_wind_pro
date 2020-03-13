# -*- coding:utf-8 -*-
# @Time : 2020-03-02 8:23
# @Author: Yicheng Zhang
# @File : test.py

from RoundUp import *
import cv2, os
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def take_png(path, files):
    img = cv2.imread(os.path.join(path, files))

    # 将图片转为灰度图
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    b, g, r = cv2.split(img)
    image = cv2.merge([r, g, b])
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


def calculate(df_gray):
    # 返回灰度值，及其比例
    res_list = pd.Series(np.arange(2))
    df_gray_ya = df_gray.values.reshape(-1, 1)
    df_gray_ya = pd.DataFrame(df_gray_ya)
    res_gray = df_gray_ya.iloc[:, 0].value_counts()
    res_list = res_gray.iloc[:3]
    res_list = pd.DataFrame(res_list)
    res_list['per'] = round(res_list.iloc[:, 0] / res_list.iloc[:, 0].sum() * 100, 2)
    res_index_list = list(res_list.index)
    res_per_list = list(res_list['per'])
    # 返回最终颜色r，g，b对应位置
    col_list = []
    for i in range(0, len(res_index_list)):
        r_x = df_gray.index[np.where(df_gray == res_index_list[i])[0]][10]
        r_y = df_gray.columns[np.where(df_gray == res_index_list[i])[1]][10]
        col_list.append([r_x, r_y])

    return res_per_list, col_list


if __name__ == "__main__":
    path = r'D:\\NEW\\1'
    new_path = r'D:\\result_new\\M'
    count = os.listdir(path)
    for root, dirs, files in os.walk(path):
        if len(dirs) == 0:
            for i in range(len(files)):
                if files[i].find('.png') != -1:
                    # 读取图片
                    image, img_gray = take_png(path, files[i])
                    # 提取有用信息
                    img_gray = distance(img_gray)
                    # 计算百分百，并添加颜色
                    res_per_list, col_list = calculate(img_gray)
                    # 生成图例（依据灰度提取出来饼图排名前三的颜色值）
                    col1 = image[col_list[0][0], col_list[0][1], :] / 255
                    col2 = image[col_list[1][0], col_list[1][1], :] / 255
                    col3 = image[col_list[2][0], col_list[2][1], :] / 255

                    # 有一种颜色
                    if res_per_list[2] < 0.5 and res_per_list[1] < 0.5:
                        col1_patch_per = 100
                        col1_patch = mpatches.Patch(color=col1, label='The data1 %s' % col1_patch_per)
                        plt.legend(handles=[col1_patch])
                    # 有两种颜色
                    elif res_per_list[2] < 0.5 and res_per_list[1] >= 0.5:
                        col1_patch_per = round_up(res_per_list[0], 2)
                        col2_patch_per = round_up(100 - col1_patch_per, 2)

                        col1_patch = mpatches.Patch(color=col1, label='The data1 %s' % col1_patch_per)
                        col2_patch = mpatches.Patch(color=col2, label='The data2 %s' % col2_patch_per)
                        plt.legend(handles=[col1_patch, col2_patch])
                    # 有三种颜色
                    else:
                        col1_patch_per = round_up(res_per_list[0], 2)
                        col2_patch_per = round_up(res_per_list[1], 2)
                        col3_patch_per = round_up(100 - col1_patch_per - col2_patch_per, 2)
                        col1_patch = mpatches.Patch(color=col1, label='The data1 %s' % col1_patch_per)
                        col2_patch = mpatches.Patch(color=col2, label='The data2 %s' % col2_patch_per)
                        col3_patch = mpatches.Patch(color=col3, label='The data3 %s' % col3_patch_per)

                        plt.legend(handles=[col1_patch, col2_patch, col3_patch])

                    plt.imshow(image)
                    plt.axis('off')
                    # plt.show()
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
