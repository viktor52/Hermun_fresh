
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from collections import deque
        
class Model2:
    """
    A stock and flow model with fifos.
    """
    def __init__(self):
        """
        Create a new empty model.
        """
        self.equations = {}
        self.equation_order = []
        self.stocks = {}
        self.fifos = {}
        self.values = {}
        self.data = None
        
    def stock(self, name, initial_value, inflow=None, outflow=None):
        """
        Create a new stock
        
        name: Name
        initial_value: Initial value
        inflow: Name of inflow Equation
        outflow: Name of outflow Equation
        """
        if name in self.values:
            raise ModelError("Duplicate name: " + name)
            
        self.values[name] = initial_value
        self.stocks[name] = inflow, outflow
        
    def fifo(self, name, delay_time, inflow=None, expire=None, take=None):
        """
        Create a new fifo queue
        
        name: Name
        delay_time: Time of expiry (outflow)
        inflow: Name of inflow Equation
        expire: Name of expire flow (Not an Equation!)
        take: Name of take Equation
        """
        if name in self.values:
            raise ModelError("Duplicate name: " + name)
        if expire and expire in self.values:
            raise ModelError("Duplicate name: " + expire)
            
        self.values[name] = 0
        self.fifos[name] = inflow, expire, take, delay_time, deque()
        if expire:
            self.values[expire] = 0
    
    def equation(self, name, function, *input_names):
        """
        Create a new equation
        
        function: Function that takes argument time and then all the input values
        *input_names: 0 or more names of inputs (stock or equation names)
        """
        if name in self.values:
            raise ModelError("Duplicate name: " + name)

        for input_name in input_names:
            if input_name not in self.values:
                raise ModelError("Input does not exist: " + input_name)
        
        self.equations[name] = Equation(name, function, input_names)
        self.equation_order.append(name)
        self.values[name] = None
        

    def reservoirs(self):
        """
        Return a list of the names of all stocks and fifos
        """
        return list(self.stocks) + list(self.fifos)
    
    def _step(self, time, dt):
        # Compute one time step.
        # time: Current simulation time
        # dt: simulation time step
        def value(name):
            if name is None:
                return 0
            if name not in self.values:
                raise ModelError("Input does not exist: " + name)
            return self.values[name]
        
        # Compute expire flows
        for fifo_name, (inflow, expire, _outtake, delay_time, queue) in self.fifos.items():
            threshold_time = time - delay_time
            total_outflow = 0
            while queue:
                arrive_time, amount = queue[0]
                if arrive_time + delay_time > time:
                    break
                queue.popleft()
                total_outflow += amount
            if expire is not None:
                self.values[expire] = total_outflow / dt
        
        # Compute the value of each equation
        for name in self.equation_order:
            eq = self.equations[name]
            input_values = [value(input_name) for input_name in eq.input_names]
            self.values[name] = eq.compute(time, dt, input_values)
  
        # Record current values
        self._record_data(time)
        
        # Compute new values in Fifos
        for fifo_name, (inflow, _expire, outtake, delay_time, queue) in self.fifos.items():
            if value(outtake):
                outtake_amount = value(outtake) * dt
                taken = 0
                for i, (arrive_time, amount) in enumerate(queue):
                    take_here = min(outtake_amount - taken, amount)
                    queue[i] = arrive_time, amount - take_here
                    taken += take_here
                    if np.abs(outtake_amount - taken) < 1e-6:
                        break
                    
            if value(inflow):
                queue.append((time, dt * value(inflow)))
            self.values[fifo_name] = sum(amount for _, amount in queue)
            
        # Compute new values in Stocks
        for stock_name, (inflow, outflow) in self.stocks.items():
            self.values[stock_name] += dt * (value(inflow) - value(outflow))

    def _record_data(self, time):
        for name, value in self.values.items():
            self.data.set_value(time, name, value)

    def _print_parts(self):
        """
        Print a list of each part of the model.
        """
        print("The model has the following parts:")
        for name in self.stocks:
            print("  ", name, " initial value: ", self.values[name])
        for name in self.equations:
            print("  ", name)
            
    def run(self, end_time, dt, verbose=True):
        """
        Run the model
        
        end_time: end time in the simulation time unit
        dt: time step
        
        Return a pandas DataFrame where each
        stock and equation has a column with their
        value for each time step.
        """
        if verbose:
            self._print_parts()
            print("End Time: ", end_time)
            print("dt: ", dt)
        columns = list(self.values.keys())
        time_series = np.arange(end_time, step=dt)
        self.data = pd.DataFrame(index=time_series)
        for time in time_series:
            self._step(time, dt)
        return self.data

class Equation:
    def __init__(self, name, function, input_names):
        self.name = name
        self.function = function
        self.input_names = input_names
    
    def compute(self, time, dt, input_values):
        return self.function(time, *input_values)

class ModelError(Exception):
    pass