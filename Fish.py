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
    Cought_Cod = 600
    
    model.stock("Fiska-Eyolfs_Cod_stock",0,inflow = "cod_in", outflow = "Process_cod")
    
    model.stock("processed_cod_stock",0,inflow = "Process_cod" , outflow = "FreshFreeze")
    
    model.fifo("Fresh_cod_2d",2, inflow = "MoveTo_Fresh_fish",take = "delivery",expire = "TWO_days_expired" )
    
    model.fifo("Fresh_cod_3d",1, inflow = "TWO_days_expired",take = "delivery",expire = "Freeze") 
    
    model.fifo("Frozen_cod",20, inflow = "Freeze",take = "delivery",expire = "Expired_frozen_fish")
    
    model.fifo("thrir_laxar_cod_orders",10000,inflow = "thrir_laxar_demand", take = "thrir_laxar_delivery" , expire = None )
    
    model.stock("thrir_laxar_throw_away_stock",0,inflow="thrir_laxar_throw_away" , outflow= None)
    
    model.fifo("thrir_laxa_stock", 2 ,inflow = "thrirlaxar_delivery" ,take = "fish_sold_thrir_laxar", expire = "thrir_laxar_throw_away")
    
    model.fifo("Hermans_verslun_cod_orders",10000,inflow = "hermans_verslun_demand", take = "hermans_verslun_delivery" , expire =  )
    
    model.stock("hermans_verslun_throw_away_stock",0,inflow="hermans_verslun_throw_away" , outflow= None)
    
    model.fifo("hermans_verslun_stock", 2 ,inflow = "hermans_verslun_delivery" ,take = "cod_sold_hermans_verslun", expire = "hermans_verslun_throw_away")
    
    model.fifo("Hermans_verslun_cod_orders",10000,inflow = "hermans_verslun_demand", take = "hermans_verslun_delivery" , expire =  )
    
    model.stock("hermans_verslun_throw_away_stock",0,inflow="hermans_verslun_throw_away" , outflow= None)
    
    model.fifo("hermans_verslun_stock", 2 ,inflow = "hermans_verslun_delivery" ,take = "cod_sold_hermans_verslun", expire = "hermans_verslun_throw_away")
    
    model.fifo("BonusKronan_cod_orders",10000,inflow = "BonusKronan_demand", take = "BonusKronan_delivery" , expire =  )
    
    model.stock("BonusKronan_throw_away_cod_stock",0,inflow="BonusKronan_cod_throw_away" , outflow= None)
    
    model.fifo("BonusKronan_cod_stock", 2 ,inflow = "BonusKronan_cod_delivery" ,take = "cod_sold_BonusKronan", expire = "BonusKronan_throw_away")
    
    def inCo
    
    # Define Stocks
    
    
    return model

def run_model(model):
    
    
    return data

data = run_model(create_model())