import json
config = json.load(open("./config.json", "r"))
print("\n  Time range:", config["time_start"] ,"to" ,config["time_end"],".")
print("  Assume the borrow rate is", config["collateral_rate"]*100,"%.")
print("  Repay when the borrow rate reach", config["repay_rate"]*100,"%, back to", config["collateral_rate"]*100,"%.")
