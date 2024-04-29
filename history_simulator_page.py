import streamlit as st
import pandas as pd
from utils import load_user_info
import numpy as np
import yfinance as yf
import os

def calc_investment_graph(initial_investment, monthly_savings, start_year, stock):
    start_date_str = str(start_year) + "-01-01"
    stock_df = yf.download(stock, start=start_date_str, interval='1mo')
    current_savings = initial_investment + monthly_savings
    investment = [current_savings]
    stock_close = np.array(stock_df['Close'])
    prev_close = stock_close[0]
    for i in range(1, len(stock_close)):
        current_close = stock_close[i]
        monthly_return = (current_close - prev_close) / prev_close
        st.write(stock, monthly_return, stock_df.index[i])
        current_savings += current_savings * monthly_return + monthly_savings
        investment.append(current_savings)
        prev_close = current_close
    st.write(stock, investment)
    return stock_df.index, investment


def is_stock_symbol_valid(symbols):
    """Check if the stock symbol is valid by attempting to fetch its info."""
    for symbol in symbols:
        stock_info = yf.Ticker(symbol)
        try:
            # Attempt to fetch the short name to determine if symbol is valid
            _ = stock_info.info['shortName']
        except KeyError:
            # If 'shortName' is not in the info, the symbol might be invalid or delisted
            return symbol
    return 1


def calc_portfolio_performance(stocks, weights, initial_investment, monthly_savings, start_year):
    performance = None
    for stock, weight in zip(stocks, weights):
        if stock:
            dates, stock_performance = calc_investment_graph(initial_investment, monthly_savings, start_year, stock)
            if performance is None:
                performance = [weight / 100 * st_perf for st_perf in stock_performance]
            else:
                performance = [port_perf + weight / 100 * st_perf for port_perf, st_perf in zip(performance, stock_performance)]

    return dates, performance

def get_savings_list(initial_investment, monthly_savings, dates):
    only_monthly_list = [monthly_savings * (i+1) for i in range(len(dates))]
    savings_list = [monthly + initial_investment for monthly in only_monthly_list]
    return savings_list



def show():
    # Load the expenses data
    username = st.session_state['logged_username']
    user_info = load_user_info(username)

    parameters_col, graph_col = st.columns((1,3))
    with parameters_col:
        input_initial_investment = st.number_input("Initial Investment", min_value=0, key="initial_investment", value=0)
        input_monthly_savings = st.number_input("Monthly Savings", min_value=0, key="savings_amount", value=1000)
        input_start_year = st.number_input("Start Year", min_value=1990, key="start_year", value=2010)
        portfolios_number = st.number_input("Number of Portfolios", min_value=0, max_value=10, value=1,
                                            key="portfolios_num")
        for portfolio in range(portfolios_number):
            with st.expander(f"### Portfolio {portfolio}"):
                stock_col, weight_col = st.columns((3, 1))
                stocks = []
                weights = []
                with stock_col:
                    input_stock = st.text_input("Investment Instrument", "SPY", key=f"first_stock_{portfolio}")
                    stocks.append(input_stock)
                with weight_col:
                    input_weight = st.number_input("Weight(%)", min_value=0, max_value=100, value=100,
                                                   key=f"first_weight_{portfolio}")
                    weights.append(input_weight)

                additional_stocks = st.number_input("Number of Additional Instruments", min_value=0, max_value=10,
                                                    value=0, key=f"add_{portfolio}")
                for i in range(additional_stocks):
                    stock_col, weight_col = st.columns((3, 1))
                    with stock_col:
                        new_stock = st.text_input(f"Additional Instrument {i+1}", "", key=f"stock_{i}_{portfolio}")
                        stocks.append(new_stock)
                    with weight_col:
                        new_weight = st.number_input(f"Weight(%) {i+1}", min_value=0, max_value=100, value=0,
                                                     key=f"weight_{i}_{portfolio}")
                        weights.append(new_weight)

                stock_valid_code = is_stock_symbol_valid(stocks)
                if stock_valid_code == 1:
                    dates, investment = calc_portfolio_performance(stocks, weights, input_initial_investment,
                                                                   input_monthly_savings, input_start_year)
                    # dates, investment = calc_investment_graph(input_initial_investment, input_monthly_savings,
                    #                                           input_start_year, input_stock)
                    if 'history_graph' not in st.session_state:
                        st.session_state['history_graph'] = {'Date': dates, 'Savings_Only': investment,
                                                             f'portfolio_{portfolio}': investment}
                    else:
                        st.session_state['history_graph']['Date'] = dates
                        st.session_state['history_graph'][f'portfolio_{portfolio}'] = investment
                else:
                    st.error(f"The symbol {stock_valid_code} is invalid or may be delisted. Please enter a valid symbol.")

    with graph_col:
        savings_dict = {}
        if 'history_graph' in st.session_state and 'Date' in st.session_state['history_graph']:
            st.session_state['history_graph']['Savings_Only'] = get_savings_list(input_initial_investment,
                                                                                 input_monthly_savings,
                                                                                 st.session_state['history_graph'][
                                                                                     'Dates'])
            saving_only = st.session_state['history_graph']['Savings_Only']
        for portfolio in range(portfolios_number):
            total_investment = "{:,}".format(round(st.session_state['history_graph']
                                                   [f'portfolio_{portfolio}'][-1]))

            total_saving = "{:,}".format(saving_only[-1])
            # money_erned = "{:,}".format(round(investment[-1] - saving_only[-1]))
            st.write(f"portfolio_{portfolio} Value: {total_investment}")
        # st.write(f"Money Invested During {years} Years: {total_saving}")
        # st.write(f"Your Money Earned For You During {years} Years: {money_erned} !!!")
        # savings_df = pd.DataFrame({'Date': st.session_state['history_graph']['Date'],
        #                            'Savings_Only': st.session_state['history_graph']['Investment'],
        #                            'Investment': st.session_state['history_graph']['Investment']})

        for key in st.session_state['history_graph']:
            savings_dict[key] = st.session_state['history_graph'][key]
        savings_df = pd.DataFrame(savings_dict)

        # st.line_chart(savings_df, x='Date', y=["Savings Only", "Investment"], height=600)
        y_list = [f'portfolio_{portfolio}' for portfolio in range(portfolios_number)]
        y_list.append('Savings_Only')
        st.line_chart(savings_df, x='Date', y=y_list, height=600)