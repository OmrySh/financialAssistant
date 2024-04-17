import streamlit as st
import pandas as pd
from utils import load_user_info
import numpy as np
import yfinance as yf
import os

def calc_investment_graph(initial_investment, monthly_savings, start_year, stock):
    start_date_str = str(start_year) + "-01-01"
    stock_df = yf.download(stock, start=start_date_str, interval='1mo')
    current_savings = initial_investment
    investment = [current_savings]
    prev_close = stock_df['Close'][0]
    for i in range(1, len(stock_df['Close'])):
        current_close = stock_df['Close'][i]
        monthly_return = (current_close - prev_close) / prev_close
        current_savings += current_savings * monthly_return + monthly_savings
        investment.append(current_savings)
        prev_close = current_close

    return stock_df.index, investment


def is_stock_symbol_valid(symbol):
    """Check if the stock symbol is valid by attempting to fetch its info."""
    stock_info = yf.Ticker(symbol)
    try:
        # Attempt to fetch the short name to determine if symbol is valid
        _ = stock_info.info['shortName']
        return True
    except KeyError:
        # If 'shortName' is not in the info, the symbol might be invalid or delisted
        return False


def show():
    # Load the expenses data
    username = st.session_state['logged_username']
    user_info = load_user_info(username)

    parameters_col, graph_col = st.columns((1,3))
    with parameters_col:
        input_initial_investment = st.number_input("Initial Investment", min_value=0, key="initial_investment", value=0)
        input_monthly_savings = st.number_input("Monthly Savings", min_value=0, key="savings_amount", value=1000)
        input_start_year = st.number_input("Start Year", min_value=1990, key="start_year", value=2010)
        input_stock = st.text_input("Investment Instrument", "SPY")

        if is_stock_symbol_valid(input_stock):
            dates, investment = calc_investment_graph(input_initial_investment, input_monthly_savings,
                                                      input_start_year, input_stock)
            st.session_state['history_graph'] = {'Date': dates, 'Savings Only': investment, 'Investment': investment}
        else:
            st.error(f"The symbol {input_stock} is invalid or may be delisted. Please enter a valid symbol.")

    with graph_col:
        print(st.session_state['history_graph']['Investment'][-1])
        total_investment = "{:,}".format(round(st.session_state['history_graph']
                                               ['Investment'][-1]))

        # total_saving = "{:,}".format(saving_only[-1])
        # money_erned = "{:,}".format(round(investment[-1] - saving_only[-1]))
        st.write(f"Investment Value: {total_investment}")
        # st.write(f"Money Invested During {years} Years: {total_saving}")
        # st.write(f"Your Money Earned For You During {years} Years: {money_erned} !!!")
        savings_df = pd.DataFrame({'Date': dates,
                                   'Savings Only': st.session_state['history_graph']['Date'],
                                   'Investment': st.session_state['history_graph']['Investment']})
        # st.line_chart(savings_df, x='Date', y=["Savings Only", "Investment"], height=600)
        st.line_chart(savings_df, x='Date', y=["Investment"], height=600)