# -*- coding:utf-8 -*-
#@Time : 2020-02-21 21:14
#@Author: Yicheng Zhang
#@File : explame.py

df.set_index('date_time', inplace=True)

@timeit(repeat=3, number=100)
def apply_tariff_isin(df):
    # 定义小时范围Boolean数组
    peak_hours = df.index.hour.isin(range(17, 24))
    shoulder_hours = df.index.hour.isin(range(7, 17))
    off_peak_hours = df.index.hour.isin(range(0, 7))

    # 使用上面的定义
    df.loc[peak_hours, 'cost_cents'] = df.loc[peak_hours, 'energy_kwh'] * 28
    df.loc[shoulder_hours,'cost_cents'] = df.loc[shoulder_hours, 'energy_kwh'] * 20
    df.loc[off_peak_hours,'cost_cents'] = df.loc[off_peak_hours, 'energy_kwh'] * 12