#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 13:25:43 2017

@author: viktor
"""

import numpy as np
import random 
import matplotlib.pyplot as plt

from stockflow2 import Model2


def create_model():
    
    model = Model2()
    
    
    model.stock("Fiska-Eyjolfs_Fish_Stock",2400,
                inflow = "Fish_In",
                outflow = "Process_Fish")
   
    model.stock("Processed_Fish_Stock",900,
                inflow = "Process_Fish",
                outflow = "Fresh_Freeze")
    
    model.fifo("Fresh_Fish_2d",2,
               inflow = "Move_To_Fresh_Fish",
               take = "Deliver_Restaurants",
               expire = "Frozen") 
    
    model.fifo("Frozen_Fish",20,
               inflow = "Frozen",
               take = "Deliver_Supermarket",
               expire = "Expired_Frozen_Fish")
    
    
    model.fifo("Restaurants_Fifo",2, 
              inflow = "Deliver_Restaurants", 
              take = "Restaurant_Sell", 
              expire = "Resturant_Trash")
    
   
    model.fifo("Restaurants_Orders",1000, 
              inflow = "Restaurant_Demand", 
              take = "Deliver_Restaurants", 
              expire = None)
 
    model.stock("Restaurants_Throw_Away",0, 
               inflow = "Resturant_Trash")
 
    
   # model.fifo("Supermarkets_Stock",21,
   #                inflow = "Deliver_Supermarkets", 
   #                take = "Supermarket_Sell",
   #                expire = "Supermarket_Trash")
   
   # model.fifo("Supermarkets_Orders",1000, 
   #            inflow = "Supermarket_Demand",
   #            take = "",
   #            expire = None)
   
   # model.stock("Supermarkets_Throw_Away",0, 
   #             inflow = "Supermarket_Trash",)
       
   
    def Fish_from_boats(time, Fiska_eyjolfs_fish_stock):
        Cought_Cod_And_haddock = 600*3
        Cought_Salmon_boat_one = random.choice([0,300])
        Cought_Salmon_boat_two = random.choice([0,300])
        Cought_halibut = random.choice([0,0,0,0,0,300])
        Cought_Fish = Cought_Cod_And_haddock+Cought_Salmon_boat_one+Cought_Salmon_boat_two+Cought_halibut
        return Cought_Fish
        
    model.equation("Fish_In", Fish_from_boats, "Fiska-Eyjolfs_Fish_Stock")
    
    def process_Fish(time,Fiska_eyjolfs_Fish_stock):
        Processed_Fish = Fiska_eyjolfs_Fish_stock
        return Processed_Fish
    model.equation("Process_Fish",process_Fish,"Fiska-Eyjolfs_Fish_Stock")
    
    def fresh_freeze(time, processed_Fish_stock): 
        return processed_Fish_stock
    model.equation("Fresh_Freeze", fresh_freeze, "Processed_Fish_Stock")
    
   
    def Fresh_Fish_2(time, Fresh_Fish_2d, processed_Fish_stock ):
        freshFish = processed_Fish_stock
        return freshFish
    model.equation("Move_To_Fresh_Fish",Fresh_Fish_2,"Fresh_Fish_2d", "Processed_Fish_Stock") 
    
    def Delivery_fresh_Fish_2d(time, Fresh_Fish_2d, Restaurant_fifo):
        demand_for_fish_per_day = 1604
        deliver = demand_for_fish_per_day - Restaurant_fifo
        return deliver
    model.equation("Deliver_Restaurants",Delivery_fresh_Fish_2d,"Fresh_Fish_2d","Restaurants_Fifo") 
    
    
    def Fish_frozen(time, frozen_fish ):
        print(frozen_fish)
        Weight_of_fish_delivered_markets = 6210
        return Weight_of_fish_delivered_markets
    model.equation("Deliver_Supermarket",Fish_frozen, "Frozen_Fish")
    
    def Fish_sold_resturants(time, fish_sold_resturants ):
        #print(fish_sold_resturants)
        Weight_of_fisk_consumed_per_day = 1603.1 #kg
        return Weight_of_fisk_consumed_per_day
    model.equation("Restaurant_Sell",Fish_sold_resturants,"Restaurants_Fifo")
    
    def Restaurant_orders(time,Resturant_fifo ):
        demand_for_fish_per_day = 1604 #kg
        demand = demand_for_fish_per_day - Resturant_fifo
        return demand
    model.equation("Restaurant_Demand",Restaurant_orders, "Restaurants_Fifo")
    return model

def run_model(model):
    END_TIME = 90 #dagar
    DT = 1
    data = model.run(END_TIME, DT)
    
    data_plot = data.plot(y='Frozen_Fish')
    plt.xlabel("Time (Weeks)")
    plt.ylabel("Mercury (ng/l)")
    
    data_plot = data.plot(y='Fresh_Fish_2d')
    plt.xlabel("Time (Weeks)")
    plt.ylabel("Mercury (ng/l)")
    
    return data

data = run_model(create_model())