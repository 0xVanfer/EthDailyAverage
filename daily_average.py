import sys
import pandas as pd
import json

def main():
    config = json.load(open("./config.json", "r"))
    # print every rows in the dataframe
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    # all data in the chart
    data = pd.read_csv("./processed_data.csv")    
    target_rate = config["collateral_rate"]
    reborrow_rate = target_rate/(1+ int(sys.argv[1])/100)
    repay_rate = config["repay_rate"]

    usage = 0
    cash = data["Open"][0]*target_rate
    # print(cash)
    for i in range(1, len(data)):
        # print(cash)
        usage += cash
        allow_borrow = data["Open"][i]
        current_rate = cash/allow_borrow
        if current_rate<reborrow_rate:
            cash = allow_borrow * target_rate
        if current_rate>repay_rate:
            cash = allow_borrow * target_rate
    print("\n  Borrow when collateral price increase by:", sys.argv[1], "%:")
    print("  Borrowed assets daily average:", round(usage/len(data),2), "USDT / day")


main()