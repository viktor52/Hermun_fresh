#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 13:25:43 2017

@author: viktor
"""

import numpy as np
import matplotlib.pyplot as plt

from stockflow2 import Model2


def create_model():
    model = Model2()
    
    model.stock("Fiska-Eyjolfs_Cod_Stock",0,
                inflow = "Cod_In",
                outflow = "Process_Cod")
    model.stock("Processed_Cod_Stock",900,
                inflow = "Process_Cod",
                outflow = "Fresh_Freeze")
    model.fifo("Fresh_Cod_2d",2,
               inflow = "Move_To_Fresh_Cod",
               take = "Deliver_2d",
               expire = "TWO_Days_Expired")
    model.fifo("Fresh_Cod_3d",1,
               inflow = "TWO_Days_Expired",
               take = "Deliver_3d",
               expire = "Frozen") 
    model.fifo("Frozen_Cod",20,
               inflow = "Frozen",
               take = "Deliver_Frozen",
               expire = "Expired_Frozen_Fish")
    
    model.fifo("Restaurants_Orders",1000,
               inflow = "")
    model.stock("Restaurants_Throw_Away",0)
    model.fifo("Restaurants_Stock")
    model.fifo("Supermarkets_Orders",1000)
    model.stock("Supermarkets_Throw_Away",0)
    model.fifo("Supermarkets_Stock")
    
   # model.fifo("thrir_laxar_cod_orders",10000,
   #             inflow = "thrir_laxar_demand",
   #             take = "thrir_laxar_delivery",
   #             expire = None )
   # model.stock("thrir_laxar_throw_away_stock",0,
   #              inflow="thrir_laxar_throw_away",
   #              outflow= None)
   # model.fifo("thrir_laxa_stock",2,
   #             inflow = "thrirlaxar_delivery",
   #             take = "fish_sold_thrir_laxar",
   #             expire = "thrir_laxar_throw_away")
   # model.fifo("Hermans_verslun_cod_orders",10000,
   #             inflow = "hermans_verslun_demand",
   #             take = "hermans_verslun_delivery",
   #             expire = None )
   # model.stock("hermans_verslun_throw_away_stock",0,
   #              inflow="hermans_verslun_throw_away",
   #              outflow= None)
   # model.fifo("hermans_verslun_stock",2,
   #             inflow = "hermans_verslun_delivery",
   #             take = "cod_sold_hermans_verslun",
   #             expire = "hermans_verslun_throw_away")
   # model.fifo("BonusKronan_cod_orders",10000,
   #             inflow = "BonusKronan_demand",
   #             take = "BonusKronan_delivery",
   #             expire = None )
   # model.stock("BonusKronan_throw_away_cod_stock",0,
   #              inflow="BonusKronan_cod_throw_away",
   #              outflow= None)
   # model.fifo("BonusKronan_cod_stock",2,
   #             inflow = "BonusKronan_cod_delivery",
   #             take = "cod_sold_BonusKronan",
   #             expire = "BonusKronan_throw_away")
   
   
    def cod_from_boats(time, Fiska_eyjolfs_cod_stock):
        Cought_Cod = 300*3
        return Cought_Cod
    model.equation("Cod_In", cod_from_boats, "Fiska-Eyjolfs_Cod_Stock")
    
    def process_cod(time,Fiska_eyjolfs_cod_stock):
        Processed_Cod = 300*3
        return Processed_Cod
    model.equation("Process_Cod",process_cod,"Fiska-Eyjolfs_Cod_Stock")
    
    def fresh_freeze(time, processed_cod_stock): 
        return 300*3
    model.equation("Fresh_Freeze", fresh_freeze, "Processed_Cod_Stock")
    
    def Fresh_cod_2(time, Fresh_cod_2d, processed_cod_stock ):
        freshCod = processed_cod_stock*0.2
        return freshCod
    model.equation("Move_To_Fresh_Cod",Fresh_cod_2,"Fresh_Cod_2d", "Processed_Cod_Stock") 
    
    def Delivery_fresh_cod_2d(time, Fresh_cod_2d):
        return None
    model.equation("Deliver_2d",Delivery_fresh_cod_2d,"Fresh_Cod_2d") 
    
    def Fresh_cod_3(time, Fresh_cod_3d ):
        #print(Fresh_cod_3d)
        return None
    model.equation("Deliver_3d",Fresh_cod_3,"Fresh_Cod_3d",)
    
    def cod_frozen(time, Fresh_cod_3d ):
        print(Fresh_cod_3d)
        return None
    model.equation("Deliver_Frozen",cod_frozen,"Frozen_Cod",)
    
    return model

def run_model(model):
    END_TIME = 90 #dagar
    DT = 1
    data = model.run(END_TIME, DT)
    
    return data

data = run_model(create_model())