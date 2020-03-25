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
    res_list = res_gray.iloc[:4]
    # print(res_list)
    res_list = pd.DataFrame(res_list)
    res_list['per'] = round(res_list.iloc[:, 0] / res_list.iloc[:, 0].sum() * 100, 2)
    res_index_list = list(res_list.index)
    res_per_list = list(res_list['per'])
    # 返回最终颜色r，g，b对应位置
    col_list = []
    for i in range(0, len(res_index_list)):
        r_x = df_gray.index[np.where(df_gray == res_index_list[i])[0]][2]
        r_y = df_gray.columns[np.where(df_gray == res_index_list[i])[1]][2]
        col_list.append([r_x, r_y])

    return res_per_list, col_list


if __name__ == "__main__":
    path = r'D:\\NEW\\1'
    new_path = r'D:\\result_new\\M'
    count = os.listdir(path)
    df = pd.DataFrame()
    for root, dirs, files in os.walk(path):
        if len(dirs) == 0:
            for i in range(len(files)):
                if files[i].find('.png') != -1:
                    # 读取图片
                    print('Processing %s' % files[i])
                    image, img_gray = take_png(path, files[i])

                    # 提取有用信息
                    img_gray = distance(img_gray)
                    # 计算百分百，并添加颜色
                    res_per_list, col_list = calculate(img_gray)
                    # 生成图例（依据灰度提取出来饼图排名前三的颜色值）
                    col1 = image[col_list[0][0], col_list[0][1], :]
                    col2 = image[col_list[1][0], col_list[1][1], :]
                    col3 = image[col_list[2][0], col_list[2][1], :]
                    col4 = image[col_list[3][0], col_list[3][1], :]

                    red = str(255) + "," + str(0) + "," + str(0)
                    yellow = str(255) + "," + str(255) + "," + str(0)
                    bule = str(0) + "," + str(0) + "," + str(255)
                    green = str(0) + "," + str(128) + "," + str(0)
                    col_dict = {red: '红', yellow: '黄', bule: '蓝', green: '绿'}
                    # print(col_dict)
                    image_df = pd.DataFrame([col1, col2, col3, col4], columns=["colname1", "colname2", "colname3"])
                    image_df['col'] = image_df["colname1"].map(str) + "," + image_df["colname2"].map(str) + "," + \
                                      image_df["colname3"].map(str)
                    image_df['颜色'] = image_df.col.map(col_dict);
                    image_df['百分比'] = res_per_list;
                    image_df['文件名'] = files[i]
                    image_df = image_df[image_df['颜色'].notna()]
                    image_df = image_df[['文件名', '颜色', '百分比']]

                    df = pd.concat([df, image_df], axis=0)

                    # # 有一种颜色
                    # if res_per_list[3] < 0.5 and res_per_list[2] < 0.5 and res_per_list[1] < 0.5:
                    #     col1_patch_per = 100
                    #     col1_patch = mpatches.Patch(color=col1 / 255, label='The data1 %s' % col1_patch_per)
                    #     plt.legend(handles=[col1_patch])
                    # # 有两种颜色
                    # elif res_per_list[3] < 0.5 and res_per_list[2] < 0.5 and res_per_list[1] >= 0.5:
                    #     col1_patch_per = round_up(res_per_list[0], 2)
                    #     col2_patch_per = round_up(100 - col1_patch_per, 2)
                    #
                    #     col1_patch = mpatches.Patch(color=col1 / 255, label='The data1 %s' % col1_patch_per)
                    #     col2_patch = mpatches.Patch(color=col2 / 255, label='The data2 %s' % col2_patch_per)
                    #     plt.legend(handles=[col1_patch, col2_patch])
                    # # 有三种颜色
                    # elif res_per_list[3] < 0.5 and res_per_list[2] >= 0.5 and res_per_list[1] >= 0.5:
                    #     col1_patch_per = round_up(res_per_list[0], 2)
                    #     col2_patch_per = round_up(res_per_list[1], 2)
                    #     col3_patch_per = round_up(100 - col1_patch_per - col2_patch_per, 2)
                    #
                    #     col1_patch = mpatches.Patch(color=col1 / 255, label='The data1 %s' % col1_patch_per)
                    #     col2_patch = mpatches.Patch(color=col2 / 255, label='The data2 %s' % col2_patch_per)
                    #     col3_patch = mpatches.Patch(color=col3 / 255, label='The data3 %s' % col3_patch_per)
                    #     plt.legend(handles=[col1_patch, col2_patch, col3_patch])
                    #
                    # else:
                    #     col1_patch_per = round_up(res_per_list[0], 2)
                    #     col2_patch_per = round_up(res_per_list[1], 2)
                    #     col3_patch_per = round_up(res_per_list[2], 2)
                    #     col4_patch_per = round_up(100 - col1_patch_per - col2_patch_per - col3_patch_per, 2)
                    #
                    #     col1_patch = mpatches.Patch(color=col1 / 255, label='The data1 %s' % col1_patch_per)
                    #     col2_patch = mpatches.Patch(color=col2 / 255, label='The data2 %s' % col2_patch_per)
                    #     col3_patch = mpatches.Patch(color=col3 / 255, label='The data3 %s' % col3_patch_per)
                    #     col4_patch = mpatches.Patch(color=col3 / 255, label='The data3 %s' % col4_patch_per)
                    #     plt.legend(handles=[col1_patch, col2_patch, col3_patch, col4_patch])

                    # plt.imshow(image)
                    # plt.axis('off')
                    # # plt.show()
                    # plt.savefig(os.path.join(new_path, files[i]))
                    #
                    # name = "AB.xlsx"
                    # writer = pd.ExcelWriter(name)  # 写入Excel文件
                    # image_df.to_excel(writer, 'img_gray', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # df_r_o1.to_excel(writer, 'df_r_o1', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # df_r_o.to_excel(writer, 'df_r_o', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # df_g_o.to_excel(writer, 'df_g_o', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # df_b_o.to_excel(writer, 'df_b_o', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # # # res.to_excel(writer, 'res', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    # # #
                    # # # # df_r_cont.to_excel(writer, 'page_2', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
                    #
                    # writer.save()

    df = df.pivot(index='文件名', columns='颜色', values='百分比')
    
    if len(df.columns)<=2:
        print("颜色不完整")
    else:
        df = df.fillna(0)
        df['总计'] = df['红'] + df['绿'] + df['蓝'] + df['黄']
        df['红'] = round(df['红'] / df['总计'] * 100, 2)
        df['绿'] = round(df['绿'] / df['总计'] * 100, 2)
        df['蓝'] = round(df['蓝'] / df['总计'] * 100, 2)
        df['黄'] = round(df['黄'] / df['总计'] * 100, 2)
        df['总计'] = df['红'] + df['绿'] + df['蓝'] + df['黄']
    print(df)
    
    name = "AB.xlsx"
    writer = pd.ExcelWriter(name)  # 写入Excel文件
    df.to_excel(writer, 'img_res', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
    writer.save()
