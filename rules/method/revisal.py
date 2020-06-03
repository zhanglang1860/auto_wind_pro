#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:Yicheng Zhang




class revisal:

    def __init__(self, path,slope,Merra_short,Merra_long,R2_judge):
        self.path = path
        self.slope=slope
        self.Merra_short=Merra_short
        self.Merra_long=Merra_long
        self.R2_judge=R2_judge

    def revisal_cal(self):
        delta=self.Merra_long-self.Merra_short
        revisal_vaule=delta*self.slope




