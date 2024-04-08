from utils import load_user_info


def get_financial_level(username):
    """

    :param
    user_name

    you can get the user_info: Dictionary by using load_user_info(username)

    example for user_info:
    user_details = {
        "password": password,
        "gender": gender,
        'expenses_path': file_path,
        "birthdate": birthdate.strftime('%Y-%m-%d') if isinstance(birthdate, date) else birthdate,
        "average_wage": average_wage,
        "financial_status": financial_status,
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

    :return:
    dictionary of:
    prediction = {
        "education_level": education_level,
        "interest_topic": interest_topic,
        "spending_behavior": spending_behavior
    }

    """

    user_info = load_user_info(username)

    prediction = {
        "education_level": 'begginer',
        "interest_topic": 'stocks',
        "spending_behavior": 'saver'
    }

    return prediction