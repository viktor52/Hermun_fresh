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
    
    # Define Stocks
    model.fifo("Order", 7,
                inflow="Icecream Order",
                take=None,
                expire="Deliver")
    
    
    model.stock("Icecream", 0,
                inflow="Deliver",
                outflow="Eat")
    
    DesiredAmount = 10
    
    def order(time, order, icecream):
        return np.clip(DesiredAmount - order - icecream, 0, None)
    
    model.equation("Icecream Order", order, "Order", "Icecream")
    
    def eat_eq(time, icecream):
        return icecream * 0.5
    
    model.equation("Eat", eat_eq, "Icecream")

    return model

def run_model(model):
    END_TIME = 30
    DT = 1 / 8
    data = model.run(END_TIME, DT)
    
    data.plot(y=["Order", "Icecream"])
    plt.xlabel("Time (s)")
    plt.ylim(0)
    
    return data

data = run_model(create_model())