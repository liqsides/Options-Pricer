from tkinter import *
import tkinter as tk
from datetime import datetime, date
import numpy as np
import pandas_datareader.data as web
from math import log, sqrt, pi, exp
from scipy.stats import norm


def d1(S, K, T, r, sigma):
    return (log(S / K) + (r + sigma ** 2 / 2.) * T) / sigma * sqrt(T)


def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * sqrt(T)


def bs_call(S, K, T, r, sigma):
    return S * norm.cdf(d1(S, K, T, r, sigma)) - K * exp(-r * T) * norm.cdf(d2(S, K, T, r, sigma))


def bs_put(S, K, T, r, sigma):
    return K * exp(-r * T) - S + bs_call(S, K, T, r, sigma)


def set():
    e1.set(entry1.get())
    e2.set(entry2.get())
    e3.set(entry3.get())

    tick = e1.get()
    strike = e2.get()
    expire = e3.get()

    tickr = str(tick)
    expiry = str(expire)
    strike_price = float(strike)

    today = datetime.now()
    one_year_ago = today.replace(year=today.year - 1)

    df = web.DataReader(tickr, 'yahoo', one_year_ago, today)

    df = df.sort_values(by="Date")
    df = df.dropna()
    df = df.assign(close_day_before=df.Close.shift(1))
    df['returns'] = ((df.Close - df.close_day_before) / df.close_day_before)

    sigma = np.sqrt(252) * df['returns'].std()
    uty = web.DataReader(
        "^TNX", 'yahoo', today.replace(day=today.day - 1), today)['Close'].iloc[-1]
    lcp = df['Close'].iloc[-1]
    t = (datetime.strptime(expiry, "%m-%d-%Y") - datetime.utcnow()).days / 365

    if(l5.get(l5.curselection()) == "American" and l6.get(l6.curselection()) == "No Dividends" or l5.get(l5.curselection()) == "European"):
        if(l4.get(l4.curselection()) == "Call"):
            print('The Theoretical Option Price is: ', bs_call(lcp, strike_price, t, uty, sigma))
        else:
            print('The Theoretical Option Price is: ', bs_put(lcp, strike_price, t, uty, sigma))
    else:
        print('The Black Scholes Model is not reliable for predicting American Option Price that produce dividends before expiry.')



window = tk.Tk()

e1 = StringVar()
e2 = DoubleVar()
e3 = StringVar()

window.title("Option God")

l1 = tk.Label(window,
         text="Ticker").grid(row=0)
l2 = tk.Label(window,
         text="Strike").grid(row=1)
l3 = tk.Label(window,
         text="Expiry").grid(row=2)
l4 = tk.Listbox(window, exportselection=0)
l5 = tk.Listbox(window, exportselection=0)
l6 = tk.Listbox(window, exportselection=0)

l4.insert(1, "Call")
l4.insert(2, "Put")
l4.grid(column=2)
l4.grid(row=0)
l4.grid(rowspan=3)
l5.insert(1, "European")
l5.insert(2, "American")
l5.grid(column=3)
l5.grid(row=0)
l5.grid(rowspan=3)
l6.insert(1, "Dividends")
l6.insert(2, "No Dividends")
l6.grid(column=4)
l6.grid(row=0)
l6.grid(rowspan=3)

entry1 = (tk.Entry(window))
entry2 = (tk.Entry(window))
entry3 = (tk.Entry(window))

entry1.grid(column=1)
entry1.grid(row=0)
entry2.grid(column=1)
entry2.grid(row=1)
entry3.grid(column=1)
entry3.grid(row=2)


button = tk.Button(window, text='EXECUTE', command = set)
button.grid(row=3)
button.grid(column=0)
button.grid(columnspan=4)

window.mainloop()



