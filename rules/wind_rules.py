#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:Yicheng Zhang
import pandas as pd


class Wind:
    # '''
    # 制定风资源风速规则程序
    # average_wind_speed_h:小时平均风速
    # average_wind_direction_h:小时平均风向
    # average_pressure_h:小时平均气压
    #
    # wind_speed_10m_h:10m高度小时平均风速
    # wind_speed_30m_h:30m高度小时平均风速
    # wind_speed_50m_h:50m高度小时平均风速
    #
    # wind_direction_30m:30m高度风向
    # wind_direction_50m:50m高度风向
    #
    # '''
    # def __init__(self, average_wind_speed_h, average_wind_direction_h, average_pressure_h, wind_speed_10m_h,
    #              wind_speed_30m_h, wind_speed_50m_h, wind_direction_30m, wind_direction_50m):
    #     self.average_wind_speed_h = average_wind_speed_h
    #     self.average_wind_direction_h = average_wind_direction_h
    #     self.average_pressure_h = average_pressure_h
    #
    #     self.wind_speed_10m_h = wind_speed_10m_h
    #     self.wind_speed_30m_h = wind_speed_30m_h
    #     self.wind_speed_50m_h = wind_speed_50m_h
    #
    #     self.wind_direction_30m = wind_direction_30m
    #     self.wind_direction_50m = wind_direction_50m
    #
    #     self.average_wind_speed_number,self.average_wind_speed_err_number = 0,0
    def __init__(self, path):
        self.path = path

    def check_lines(self):
        n = 0
        f = open(self.path, 'r')
        lines = f.readlines()
        for lines in lines:

            if "Timestamp" in lines:
                result = n
            n = n + 1;
        return result


class WindRules(Wind):

    def __init__(self, df, path):
        super(WindRules, self).__init__(path)
        self.df = df

    def pre_load(self):
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])
        self.df = self.df.set_index(self.df['Timestamp'])
        self.df_h = self.df.resample('H').mean()
        # print(self.df_h.dtypes)

    # 主要参数合理范围参考值
    def wind_rules(self):
        # shoulder_hours = self.df.iloc[:,1].isin(['    5.191181'])
        shoulder_hours = self.df.iloc[:, 1]

        print(shoulder_hours)
        # shoulder_hours = self.df_h['Ch1_Anem_120.00m_NW_Avg_m/s'].isin(range(0, 7))
        off_peak_hours = self.df_h.index.hour.isin(range(0, 7))
        # print(off_peak_hours)
        #
        # if self.average_wind_speed_h < 40 and self.average_wind_speed_h >= 0:
        #     self.average_wind_speed_number = self.average_wind_speed_number + 1
        # else:
        #     self.average_wind_speed_err_number = self.average_wind_speed_err_number + 1


if __name__ == "__main__":
    path = '../2710.csv'
    Wind = Wind(path)
    lines = Wind.check_lines()
    # df = pd.read_table(path, skiprows=lines,sep='\s+')
    df = pd.read_csv(path, skiprows=lines)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.set_index(df['Timestamp'])
    df = df.drop(['Timestamp'], axis=1)
    df.astype(float)
    shoulder_hours = df[(df['Ch1_Anem_120.00m_NW_Avg_m/s'] < 6) & (df['Ch1_Anem_120.00m_NW_Avg_m/s'] >= 0)]
    # shoulder_hours = df['Ch1_Anem_120.00m_NW_Avg_m/s']
    print(shoulder_hours)
    # print(df[shoulder_hours])
    #
    # WindRules = WindRules(df, path)
    # WindRules.pre_load()
    # WindRules.wind_rules()
