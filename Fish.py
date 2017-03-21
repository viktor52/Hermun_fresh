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
    
    
    model.stock("Fiska-Eyjolfs_Fish_Stock",1800,
                inflow = "Fish_In",
                outflow = "Process_Fish")
   
    model.stock("Processed_Fish_Stock",900,
                inflow = "Process_Fish",
                outflow = "Move_To_Fresh_Fish")
    
    model.fifo("Fresh_Fish_2d",2,
               inflow = "Move_To_Fresh_Fish",
               take = "Deliver_Restaurants",
               expire = "Frozen") 
    
    model.fifo("Frozen_Fish",20,
               inflow = "Frozen",
               take = "Deliver_Supermarkets",
               expire = "Expired_Frozen_Fish")
    
    
    model.fifo("Restaurants_Stock",2, 
              inflow = "Deliver_Restaurants", 
              take = "Restaurant_Sell", 
              expire = "Resturant_Trash")
    
   
    model.fifo("Restaurants_Orders",1, 
              inflow = "Restaurant_Demand", 
              take =  None,
              expire = "Deliver_Restaurants")
 
    model.stock("Restaurants_Throw_Away",0, 
               inflow = "Resturant_Trash")
 
    
    model.fifo("Supermarkets_Stock",21,
                   inflow = "Deliver_Supermarkets", 
                   take = "Supermarket_Sell",
                   expire = "Supermarket_Trash")
   
    model.fifo("Supermarkets_Orders",1, 
               inflow = "Supermarket_Demand",
               take = None,
               expire = "Deliver_Supermarkets")
   
    model.stock("Supermarkets_Throw_Away",0, 
                inflow = "Supermarket_Trash",)
       
   
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
    
    def Move_To_fresh(time, processed_Fish_stock): 
        return processed_Fish_stock
    model.equation("Move_To_Fresh_Fish", Move_To_fresh, "Processed_Fish_Stock")
    
    
    
    
    def Fish_sold_resturants(time, fish_sold_resturants ):
        #print(fish_sold_resturants)
        Weight_of_fisk_consumed_per_day = random.randint(1500,1700) #kg

        return Weight_of_fisk_consumed_per_day
    model.equation("Restaurant_Sell",Fish_sold_resturants,"Restaurants_Stock")
    
    def Restaurant_orders(time, Restaurant_orders, Resturant_fifo):
        demand_for_fish_per_day = 1604 #kg
        demand = demand_for_fish_per_day - Resturant_fifo
        print(Resturant_fifo)
        return demand
    model.equation("Restaurant_Demand",Restaurant_orders, "Restaurants_Orders","Restaurants_Stock")
    
    def Fish_sold_supermarkets(time, fish_sold_supermarkets ):
        
        Weight_of_fisk_sold_per_day = random.randint(5900,6300) #kg
        return Weight_of_fisk_sold_per_day
    model.equation("Supermarket_Sell",Fish_sold_supermarkets,"Supermarkets_Stock")

    def Supermarket_orders(time, supermarket_order ,Supermarkets_Stock):
        demand_for_fish_per_day = 6210 #kg
        demand = demand_for_fish_per_day - Supermarkets_Stock
        return demand
    model.equation("Supermarket_Demand",Supermarket_orders, "Supermarkets_Orders", "Supermarkets_Stock")
    return model

def run_model(model):
    END_TIME = 90 #dagar
    DT = 1
    data = model.run(END_TIME, DT)
    
    data_plot1 = data.plot(y='Frozen_Fish')
    plt.xlabel("Time (days)")
    plt.ylabel("Weight (kg)")
    data_plot1.figure.savefig("Frozen_Fish.png")
    
    data_plot2 = data.plot(y='Fresh_Fish_2d')
    plt.xlabel("Time (days)")
    plt.ylabel("Weight (kg)")
    data_plot2.figure.savefig("Fresh_Fish.png")
    
    data_plot3 = data.plot(y='Restaurants_Stock')
    plt.xlabel("Time(days)")
    plt.ylabel("Weight(kg)")
    data_plot3.figure.savefig("Resturants_stock.png")
    
    data_plot4 = data.plot(y='Supermarkets_Stock')
    plt.xlabel("Time (days)")
    plt.ylabel("Weight (kg)")
    data_plot4.figure.savefig("Supermarket_Stock.png")
    
    data_plot5 = data.plot(y='Restaurants_Throw_Away')
    plt.xlabel("Time (days)")
    plt.ylabel("Weight (kg)")
    data_plot5.figure.savefig("Resturant_Throw_Away.png")
    
    data_plot6 = data.plot(y='Supermarkets_Throw_Away')
    plt.xlabel("Time (days)")
    plt.ylabel("Weight (kg)")
    data_plot6.figure.savefig("Supermarket_Throw_Away.png")
    
    return data

data = run_model(create_model())