from datetime import datetime
import pandas as pd


class OptionInfo: 
    def __init__(self, json_dict): 
        self.ticker         : str   = str(json_dict["ticker"])
        self.strike_price   : float = float(json_dict["strike_price"])
        self.experation_date: datetime  = datetime_from_str(json_dict["experation_date"])
        self.type           : str = json_dict["type"]


class ConfluenceSet: 
    def __init__(self, json_dict): 
        self.stacked_emas       : bool = bool(json_dict["stacked_emas"])
        self.broke_trendline    : bool = bool(json_dict["broke_trendline"])
        self.touching_21_ema    : bool = bool(json_dict["touching_21_ema"])
        self.orange_squeeze     : int = int(json_dict["orange_squeeze"])
        self.red_squeeze        : int = int(json_dict["red_squeeze"])
        self.slow_buy_signal    : int = int(json_dict["slow_buy_signal"])
        self.obv_increasing     : int = int(json_dict["obv_increasing"])



class Transaction: 
    def __init__(self, json_dict): 
        self.date   : datetime = datetime_from_str(json_dict["date"])
        self.amount : int = int(json_dict["amount"])
        self.price  : float = float(json_dict["price"])
        self.summary    : str = str(json_dict["summary"])

class Position: 
    def __init__(self, json_dict): 
        self.ticker     : str = json_dict["ticker"]
        self.open_date  : datetime = datetime_from_str(json_dict["open_date"])
        self.close_date : datetime = datetime_from_str(json_dict["close_date"])
        self.profit     : float = float(json_dict["profit"])
        self.time_frame : str = str(json_dict["time_frame"])
        self.option_info: OptionInfo = OptionInfo(json_dict=json_dict["option_info"])
        self.confluences: {ConfluenceSet} = {"daily": ConfluenceSet(json_dict=json_dict["confluences"]["daily"]),
                                             "weekly": ConfluenceSet(json_dict=json_dict["confluences"]["weekly"]),
                                             "monthly": ConfluenceSet(json_dict=json_dict["confluences"]["monthly"])}
        self.transactions: list = [Transaction(t_dict) for t_dict in json_dict["transactions"] ]
        self.summary    : str = json_dict["summary"] 
        self.json_dict  : dict = json_dict
        self.is_open    : bool = True if self.close_date == None else False


    def confluences_to_df(self) -> pd.DataFrame: 
        dicts = {}

        for type in self.confluences: 
            confluence = self.confluences[type]
            if "stacked_emas" not in dicts:
                dicts["stacked_emas"] = {"name": "stacked_emas"}
            dicts["stacked_emas"][type] = confluence.stacked_emas

            if "broke_trendline" not in dicts:
                dicts["broke_trendline"] = {"name": "broke_trendline"}
            dicts["broke_trendline"][type] = confluence.broke_trendline


            if "touching_21_ema" not in dicts:
                dicts["touching_21_ema"] = {"name": "touching_21_ema"}
            dicts["touching_21_ema"][type] = confluence.touching_21_ema


            if "orange_squeeze" not in dicts:
                dicts["orange_squeeze"] = {"name": "orange_squeeze"}
            dicts["orange_squeeze"][type] = confluence.orange_squeeze

            if "red_squeeze" not in dicts:
                dicts["red_squeeze"] = {"name": "red_squeeze"}
            dicts["red_squeeze"][type] = confluence.red_squeeze


            if "slow_buy_signal" not in dicts:
                dicts["slow_buy_signal"] = {"name": "slow_buy_signal"}
            dicts["slow_buy_signal"][type] = confluence.slow_buy_signal


            if "obv_increasing" not in dicts:
                dicts["obv_increasing"] = {"name": "obv_increasing" }
            dicts["obv_increasing"][type] = confluence.obv_increasing

        arr = []
        for key in dicts: 
            arr.append(dicts[key])

        return pd.DataFrame(arr)


    def __str__(self): 
        return str(self.json_dict)
    



def datetime_from_str(datetime_str: str) -> datetime: 
    DATE_FORMAT = "%Y-%m-%dT%H:%M:00.000Z" 
    try: 
        return datetime.strptime(datetime_str, DATE_FORMAT)
    except: 
        return None