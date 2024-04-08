import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_user_info
from pandas.tseries.offsets import DateOffset


def show():
    # st.write("Learn About Your Expenses")
    # st.write("---")
    user_name = st.session_state['logged_username']
    user_info = load_user_info(user_name)
    expenses_path = user_info['expenses_path']
    df = pd.read_csv(expenses_path)
    # Ensure the 'date' column is treated as a datetime type
    df['date'] = pd.to_datetime(df['date'])

    # Extract year and month from 'date' for easier grouping
    df['year_month'] = df['date'].dt.to_period('M')

    expenses_col, df_col, _ = st.columns((1, 1, 1))
    with expenses_col:
        total_expenses = df['amount_spent'].sum()
        st.write(f"Total Expenses: ${total_expenses:.2f}")

        average_spending = df['amount_spent'].mean()
        st.write(f"Average Spending: ${average_spending:.2f} per transaction")
    with df_col:
        st.write(df)  # Display the uploaded dataframe

    spending_by_store_col, spending_by_month_col, pie_chart_col = st.columns((1, 1, 1))
    with spending_by_store_col:
        spending_by_store = df.groupby('store_name')['amount_spent'].sum().sort_values(ascending=False)
        st.write("Spending by Store:")
        st.bar_chart(spending_by_store)
    # with spending_by_month_col:


    with pie_chart_col:
        # Pie Chart for the Last Month's Expenses
        latest_month = df['year_month'].max()
        last_month_expenses = df[df['year_month'] == latest_month].groupby('store_name')['amount_spent'].sum()
        st.write(f"Expenses Breakdown for {latest_month}:")
        fig, ax = plt.subplots(figsize=(5, 5))  # Smaller figure size
        last_month_expenses.plot(kind='pie', y='amount_spent', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')  # Remove the y-label as it's not necessary for pie charts

        # Display the figure in Streamlit
        st.pyplot(fig)

    # Group by year and month, then sum the amounts
    if 'selected_period' not in st.session_state:
        filtered_df = df

    # Filter data based on selected period
    if 'selected_period' in st.session_state and st.session_state['selected_period'] is not None:
        # Calculate the cutoff date for filtering
        cutoff_date = pd.Timestamp.now() - DateOffset(months=st.session_state['selected_period'])
        filtered_df = df[df['date'] > cutoff_date]
    else:
        # Use the entire dataset
        filtered_df = df
    spending_by_month = filtered_df.groupby('year_month')['amount_spent'].sum()
    st.write("Spending Trends by Month:")

    # Convert the index to string for plotting, ensuring month and year are shown
    spending_by_month.index = spending_by_month.index.astype(str)

    # Plotting with Matplotlib
    fig, ax = plt.subplots()
    spending_by_month.plot(kind='line', ax=ax)

    # Set the x-axis label
    ax.set_xlabel('Month-Year')
    # Set the y-axis label
    ax.set_ylabel('Amount Spent')
    # Set the title of the plot
    ax.set_title('Spending Trends by Month')

    # Improve layout of x-axis labels to prevent overlap
    plt.xticks(rotation=45, ha='right')

    # Show the plot in Streamlit
    st.pyplot(fig)


    # Spending Trends by Month
    period_options = {
        "6 Months": 6,
        "Year": 12,
        "5 Years": 60,
        "Max": None
    }

    periods_columns = st.columns(len(period_options))
    for i, (option, months) in enumerate(period_options.items()):
        with periods_columns[i]:
            if st.button(option):
                st.session_state['selected_period'] = months

