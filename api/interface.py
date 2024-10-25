import os, sys, json
from datetime import datetime
from classes.Position import Position



PATH_TRADES = "trades/"



def get_trades(month:int=0, year:int=0):
    years = os.listdir(PATH_TRADES)

    positions = []
    for y in years: 
        current_dir = PATH_TRADES + str(y) + "/"
        months = os.listdir(current_dir)
        for m in months:
            current_dir = current_dir + str(m) + "/"
            ticker_orders = os.listdir(current_dir)
            for pos in ticker_orders:
                with open(current_dir+pos, "r") as file: 
                    obj = json.load(file)
                    position = Position(json_dict = obj)
                    positions.append(position)
    return positions