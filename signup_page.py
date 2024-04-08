import streamlit as st
from utils import navigate_to
from datetime import date
import json


def add_credentials(username, password, gender, birthdate, average_wage, have_savings, financial_knowledge,
                    investment_experience, financial_goals, risk_tolerance, emergency_fund, debt_level,
                    income_stability, expense_tracking, insurance_coverage, investment_understanding, finance_courses,
                    financial_news, retirement_age, wealth_building_priority):
    """Add or update a user's credentials and details in a JSON file."""
    # The path to your JSON file
    credentials_file_path = "credentials.json"

    # Try to load existing users data or initialize an empty dictionary
    try:
        with open(credentials_file_path, "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

    # Prepare the user's details
    user_details = {
        "password": password,
        "gender": gender,
        "birthdate": birthdate.strftime('%Y-%m-%d') if isinstance(birthdate, date) else birthdate,
        "average_wage": average_wage,
        "have_savings": have_savings,
        "financial_knowledge": financial_knowledge,
        "investment_experience": investment_experience,
        "financial_goals": financial_goals,
        "risk_tolerance": risk_tolerance,
        "emergency_fund": emergency_fund,
        "debt_level": debt_level,
        "income_stability": income_stability,
        "expense_tracking": expense_tracking,
        "insurance_coverage": insurance_coverage,
        "investment_understanding": investment_understanding,
        "finance_courses": finance_courses,
        "financial_news": financial_news,
        "retirement_age": retirement_age,
        "wealth_building_priority": wealth_building_priority
    }
    # Update the users dictionary with the new user's details
    users[username] = user_details

    # Write the updated users dictionary back to the file
    with open(credentials_file_path, "w") as file:
        json.dump(users, file, indent=4)


def is_username_taken(username):
    """Check if the credentials match any existing ones in the credentials JSON file."""
    credentials_file_path = "credentials.json"
    try:
        with open(credentials_file_path, "r") as file:
            users = json.load(file)
            # Check if the username exists and the password matches
            user = users.get(username)
            if user:
                return True
        return False
    except FileNotFoundError:
        return False


def show():
    st.subheader("Sign Up")
    col1, col2 = st.columns([1, 1])  # The first column is wider; adjust according to your preference.

    with col1:  # Use the wider column for input fields
        username = st.text_input("Choose a Username", key="signup_username")
        password = st.text_input("Choose a Password", type="password", key="signup_password")

        # Additional fields
        gender_default_message = "Please Choose Gender"
        gender = st.selectbox("Gender", [gender_default_message, "Male", "Female", "Other"], key="signup_gender")
        birthdate = st.date_input("Birthdate", key="signup_birthdate")
        average_wage = st.number_input("Average Monthly Wage", min_value=0, key="signup_wage")

        # Example financial status question
        have_savings = st.radio(
            "Do you have any savings?",
            ('Yes', 'No'),
            key="signup_savings"
        )

        # Example financial knowledge question
        financial_knowledge_default_message = "Please Choose Your Financial Category"
        financial_knowledge = st.selectbox(
            "Rate your financial knowledge",
            [financial_knowledge_default_message, 'Beginner', 'Intermediate', 'Advanced'],
            key="signup_financial_knowledge"
        )

    # More questions can be added here following the same pattern
        emergency_fund = st.selectbox("How many months can your emergency fund cover your expenses?",
                                      ["None", "1-3 months", "3-6 months", "More than 6 months"],
                                      key="emergency_fund")
        debt_level = st.selectbox("What is your current level of debt?",
                                  ["No debt", "Low", "Moderate", "High"],
                                  key="debt_level")
        income_stability = st.selectbox("How stable is your source of income?",
                                        ["Very stable", "Somewhat stable", "Unstable", "No income"],
                                        key="income_stability")
        expense_tracking = st.radio("Do you regularly track your expenses?",
                                    ["Yes, meticulously", "Yes, but not in detail", "Rarely", "No"],
                                    key="expense_tracking")
        insurance_coverage = st.multiselect("What types of insurance do you currently have?",
                                            ["Health", "Life", "Property", "None"],
                                            key="insurance_coverage")

        # Additional Financial Knowledge Questions
        investment_understanding = st.selectbox(
            "How would you rate your understanding of investment products (stocks, bonds, mutual funds)?",
            ["No understanding", "Basic", "Intermediate", "Advanced"],
            key="investment_understanding")
        finance_courses = st.radio("Have you ever taken any courses on personal finance?",
                                   ["Yes, several", "A few", "One", "None"],
                                   key="finance_courses")
        financial_news = st.selectbox("How often do you follow financial news?",
                                      ["Daily", "Weekly", "Occasionally", "Never"],
                                      key="financial_news")

        # Additional Financial Goals Questions
        retirement_age = st.number_input("At what age do you plan to retire?", min_value=0, max_value=100, step=1,
                                         key="retirement_age")
        wealth_building_priority = st.selectbox("What is your top priority for building wealth?",
                                                ["Retirement savings", "Buying property",
                                                 "Starting/investing in a business",
                                                 "Saving for major expenses (education, travel)"],
                                                key="wealth_building_priority")
        investment_experience = st.selectbox("What is your investment experience?",
            ["None", "Limited", "Moderate", "Experienced"], key="signup_investment_experience")
        financial_goals = st.multiselect("What are your primary financial goals?",
            ["Saving for retirement", "Buying a home", "Building an emergency fund", "Saving for education", "Other"],
            key="signup_financial_goals")
        risk_tolerance = st.radio("What is your risk tolerance?",
            ["Low", "Medium", "High"], key="signup_risk_tolerance")

    # Validation and submission
    if st.button("Sign Up"):
        # Check that all fields are filled out (simplified for demonstration; expand as needed)
        if not all([username, password, gender != gender_default_message, birthdate, average_wage, have_savings,
                    financial_knowledge != financial_knowledge_default_message, investment_experience, financial_goals,
                    risk_tolerance,
                    emergency_fund, debt_level, income_stability, expense_tracking, insurance_coverage,
                    investment_understanding,
                    finance_courses, financial_news, retirement_age, wealth_building_priority]):
            st.error("Please answer all questions.")
        elif not is_username_taken(username):
            # Extend the function to include additional details
            add_credentials(username, password, gender, birthdate, average_wage, have_savings,
                            financial_knowledge, investment_experience, financial_goals, risk_tolerance,
                            emergency_fund, debt_level, income_stability, expense_tracking, insurance_coverage,
                            investment_understanding, finance_courses, financial_news, retirement_age,
                            wealth_building_priority)
            st.success("Signup successful. Please log in.")
            navigate_to("login")
        else:
            st.error("Username already exists. Please choose a different one.")

    if st.button("Back"):
        navigate_to('welcome')