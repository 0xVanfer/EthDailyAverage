import sys
import pandas as pd
import json

def main():
    config = json.load(open("./config.json", "r"))
   
    # print every rows in the dataframe
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    data = pd.read_csv("./processed_data.csv")    

    target_rate = config["collateral_rate"]
    reborrow_rate = target_rate / (1 + int(sys.argv[1]) / 100)
    repay_rate = config["repay_rate"]

    usage = 0
    cash = data["Open"][0] * target_rate

    events = [{"CashBefore": 0, "CashAfter": int(cash), "Type": "borrow", "Date": data["Time"][0]}]

    for i in range(1, len(data)):
        usage += cash
        allow_borrow = data["Open"][i]
        current_rate = cash / allow_borrow
        # reborrow
        if current_rate < reborrow_rate:
            cash = allow_borrow * target_rate
            events.append({"CashBefore": int(allow_borrow * current_rate), "CashAfter": int(cash), "Type": "borrow", "Date": data["Time"][i]})
        # repay
        if current_rate > repay_rate:
            cash = allow_borrow * target_rate
            events.append({"CashBefore": int(allow_borrow * current_rate), "CashAfter": int(cash), "Type": "repay", "Date": data["Time"][i]})
    print("\n\n  Borrow when collateral price increase by:", sys.argv[1], "%:")
    print(pd.DataFrame(events))
    print("\n  Borrowed assets daily average:", round(usage / len(data), 2), "USDT / day")



main()