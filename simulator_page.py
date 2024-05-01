import streamlit as st
import pandas as pd
from utils import load_user_info
import numpy as np
import os


def get_monthly_spending(expenses_path):
    df = pd.read_csv(expenses_path)

    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Extract the year and month from the 'date' column
    df['year_month'] = df['date'].dt.strftime('%Y-%m')

    # Group by 'year_month' and 'category', then sum the 'amount_spent'
    monthly_spending_sum = df.groupby(['year_month', 'category'])['amount_spent'].sum().reset_index()

    # Now calculate the average monthly spending for each category
    average_monthly_spending = monthly_spending_sum.groupby('category')['amount_spent'].mean().reset_index()
    average_monthly_spending['amount_spent'] = average_monthly_spending['amount_spent'].round(0)

    return average_monthly_spending


def calc_investment_graph(monthly_savings, num_months, monthly_interest_rate):
    curr_savings = monthly_savings
    savings_list = [curr_savings]
    for period in range(1, num_months):
        curr_savings = curr_savings * (1 + monthly_interest_rate) + monthly_savings
        savings_list.append(curr_savings)

    return savings_list




def show():
    # Load the expenses data
    username = st.session_state['logged_username']
    user_info = load_user_info(username)

    # expenses_path = user_info['expenses_path']
    expenses_path = os.path.join('expenses_data', f'{username}_expenses.csv')
    user_wage = user_info['average_wage']

    average_monthly_spending = get_monthly_spending(expenses_path)

    spending_col, savings_col = st.columns((1,3))
    with spending_col:
        input_wage = st.number_input("Adjust Wage", min_value=0, key="wage_simulator", value=user_wage)
        # Display and allow adjustment of spending by category
        adjusted_spending = {}
        for idx, row in average_monthly_spending.iterrows():
            category = row['category']
            avg_spend = row['amount_spent']
            adjusted_spend = st.slider(f"Adjust spending on {category}", 0, int(avg_spend * 2), int(avg_spend))
            adjusted_spending[category] = adjusted_spend

        total_spending = sum(adjusted_spending.values())
        monthly_savings = input_wage - total_spending

        st.write(f"Total Monthly Spending: ${total_spending}")
        st.write(f"Estimated Monthly Savings: ${monthly_savings}")

    with savings_col:
        # Parameters for the simulation
        years = st.slider(f"Adjust Years of Saving", 1, 80, 10)
        interest_rate = st.slider(f"Adjust Yearly Interest Rate (%)", 0, 50, 8)
        interest_rate /= 100
        monthly_interest_rate = (1 + interest_rate) ** (1/12) - 1

        # Calculate monthly savings growth
        num_months = years * 12
        months = np.arange(num_months + 1)
        investment = calc_investment_graph(monthly_savings, years * 12, monthly_interest_rate)
        saving_only = [monthly_savings * (i + 1) for i in range(num_months)]

        total_investment = "{:,}".format(round(investment[-1]))
        total_saving = "{:,}".format(saving_only[-1])
        money_erned = "{:,}".format(round(investment[-1] - saving_only[-1]))
        st.write(f"Investment Value After {years} Years: {total_investment}")
        st.write(f"Money Invested During {years} Years: {total_saving}")
        st.write(f"Your Money Earned For You During {years} Years: {money_erned} !!!")
        savings_df = pd.DataFrame({'Date': months, 'Savings Only': saving_only, 'Investment': investment})
        st.line_chart(savings_df, x='Date', y=["Savings Only", "Investment"], height=600)