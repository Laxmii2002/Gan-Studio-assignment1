#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Read trades from CSV file
trades = pd.read_csv(r"C:\Users\Pradeep\Downloads\trades.csv")

# Initialize data structures
open_trades = {}

# Add a new 'PNL' column to the dataframe
trades['PNL'] = 0.0

# Process trades
for trade in trades.itertuples(index=True):  # Set index=True to include index in the tuple
    symbol = trade.SYMBOL
    quantity = int(trade.QUANTITY)
    price = float(trade.PRICE)
    side = trade.SIDE

    if side == 'B':
        # Opening trade
        if symbol not in open_trades:
            open_trades[symbol] = {'quantity': 0, 'price': 0, 'time': int(trade.TIME)}
        open_trades[symbol]['quantity'] += quantity
        open_trades[symbol]['price'] = (open_trades[symbol]['price'] * (open_trades[symbol]['quantity'] - quantity) +
                                        price * quantity) / open_trades[symbol]['quantity']
    elif side == 'S':
        # Closing trade
        for open_symbol in list(open_trades.keys()):  
            open_trade = open_trades[open_symbol]
            open_quantity = min(quantity, open_trade['quantity'])
            pnl = open_quantity * (price - open_trade['price'])
            print(f"{open_trade['time']},{trade.TIME},{open_symbol},{open_quantity},{pnl:.2f},B,S,{open_trade['price']},{price}")
            
            open_trade['quantity'] -= open_quantity
            trades.at[trade.Index, 'PNL'] += pnl  # Use 'Index' attribute to access the row index

            if open_trade['quantity'] == 0:
                del open_trades[open_symbol]

# Output cumulative realized PNL
print("Total PNL:", sum(trades['PNL']))


# In[ ]:




