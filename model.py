from utils import load_user_info
import pickle
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


class UserGenerator:

    def __init__(self, num_users=10000):
        self.num_users = num_users
        self.alpha = 1.16
        self.scale = 1000
        self.average_monthly_wage = (np.random.pareto(a=self.alpha, size=num_users) + 1) * self.scale
        self.average_monthly_wage_data = np.clip(self.average_monthly_wage, 1000, None)
        self.users_data = self.generate_user_data()
        self.users_data['financial_goals'] = [self.select_financial_goal(age) for age in self.users_data['age']]
        self.full_data = self.generate_expenses_data(self.users_data, self.num_users, self.average_monthly_wage_data)

    def generate_user_data(self):
        np.random.seed(42)
        num_users = 10000
        gender_choices = ['male'] * 4500 + ['female'] * 4500 + ['other'] * 1000
        np.random.shuffle(gender_choices)
        birthdate_data = [datetime.now() - timedelta(days=np.random.randint(365 * 18, 365 * 65)) for _ in
                          range(num_users)]
        age_data = [(datetime.now() - bd).days // 365 for bd in birthdate_data]

        users = pd.DataFrame({
            'gender': gender_choices,
            'birthdate': birthdate_data,
            'age': age_data,
            'average_wage': self.average_monthly_wage_data,
            'have_savings': np.random.choice(['yes', 'no'], num_users),
            'financial_knowledge': np.random.choice(['beginner', 'intermediate', 'advanced'], num_users),
            'emergency_fund': np.random.choice(['no', '1-3 months', '3-6 months', 'more than 6 months'], num_users),
            'debt_level': np.random.choice(['no debt', 'low', 'moderate', 'high'], num_users),
            'income_stability': np.random.choice(['very stable', 'somewhat stable', 'unstable', 'no income'],
                                                 num_users),
            'expense_tracking': np.random.choice(['yes, meticulously', 'yes, but not in detail', 'rarely', 'no'],
                                                 num_users),
            # 'insurance_coverage': np.random.choice(['health', 'life', 'property', 'none'], num_users),
            'investment_understanding': np.random.choice(['no understanding', 'basic', 'intermediate', 'advanced'],
                                                         num_users),
            'finance_courses': np.random.choice(['yes, several', 'a few', 'one', 'none'], num_users),
            'financial_news': np.random.choice(['daily', 'weekly', 'occasionally', 'never'], num_users),
            'retirement_age': np.random.randint(55, 75, num_users),
            'investment_experience': np.random.choice(['limited', 'moderate', 'experienced'], num_users),
            'risk_tolerance': np.random.choice(['low', 'medium', 'high'], num_users),
        })
        return users

    def select_financial_goal(self, age):
        if 18 <= age <= 25:
            goals = ['saving for education'] * 40 + ['building an emergency fund'] * 30 + ['buying a home'] * 10 + [
                'saving for retirement', 'other'] * 10
        elif 26 <= age <= 35:
            goals = ['buying a home'] * 35 + ['saving for retirement'] * 25 + ['building an emergency fund'] * 20 + [
                'saving for education', 'other'] * 10
        elif 36 <= age <= 50:
            goals = ['saving for retirement'] * 40 + ['buying a home'] * 20 + ['building an emergency fund',
                                                                               'other'] * 20 + [
                        'saving for education'] * 10
        elif 51 <= age <= 65:
            goals = ['saving for retirement'] * 50 + ['other'] * 25 + ['building an emergency fund'] * 15 + [
                'buying a home'] * 10
        else:
            goals = ['other'] * 50 + ['saving for retirement'] * 20 + ['building an emergency fund'] * 20 + [
                'buying a home'] * 10

        return np.random.choice(goals)

    def generate_expenses_data(self, users, num_users, average_monthly_wage_data):
        expense_categories = ['housing', 'food', 'transportation', 'utilities', 'healthcare', 'entertainment',
                              'education', 'miscellaneous']
        expenses_df = pd.DataFrame(np.zeros((num_users, len(expense_categories))), columns=expense_categories)
        total_expense_limit = average_monthly_wage_data * 2
        for i in range(num_users):
            raw_expenses = np.random.dirichlet(np.ones(len(expense_categories)))
            scaling_factor = np.random.rand() * 2
            scaled_expenses = raw_expenses / raw_expenses.sum() * total_expense_limit[i] * scaling_factor
            expenses_df.iloc[i] = scaled_expenses
        full_dataset = pd.concat([users.reset_index(drop=True), expenses_df], axis=1)
        return full_dataset


class Labels:
    def __init__(self):
        self.labels = ['saver', 'spender', 'investor']
        self.full_data_set = UserGenerator().full_data
        self.full_data_set['financial_literacy_level'] = self.full_data_set.apply(
            self.determine_financial_literacy_level, axis=1)
        self.full_data_set['financial_behavior'] = self.full_data_set.apply(self.determine_financial_behavior, axis=1)
        self.full_data_set['financial_goals_category'] = self.full_data_set.apply(self.categorize_financial_goals,
                                                                                  axis=1)

    def determine_financial_literacy_level(self, row):
        scores = 0
        if row['financial_knowledge'] == 'advanced':
            scores += 2
        elif row['financial_knowledge'] == 'intermediate':
            scores += 1
        if row['finance_courses'] not in ['none', None]:
            scores += 1
        if row['investment_understanding'] in ['intermediate', 'advanced']:
            scores += 1
        return 'advanced' if scores >= 3 else 'intermediate' if scores == 2 else 'beginner'

    def determine_financial_behavior(self, row):
        if row['expense_tracking'] in ['yes, meticulously'] and row['have_savings'] == 'yes':
            return 'saver'
        elif row['debt_level'] in ['moderate', 'high']:
            return 'spender'
        elif 'investing' in row['financial_goals']:
            return 'investor'
        else:
            return 'planner'

    def categorize_financial_goals(self, row):
        if 'buying a home' in row['financial_goals']:
            return 'home ownership'
        elif 'saving for education' in row['financial_goals']:
            return 'education funding'
        elif 'saving for retirement' in row['financial_goals']:
            return 'retirement planning'
        else:
            return 'wealth accumulation'


class Model:
    def __init__(self):
        self.labels = Labels()
        self.full_dataset = self.labels.full_data_set
        self.training_features = {"training_features": []}
        self.encoders = {}  # Store encoders
        self.models = {}  # Store models

    def save_model(self, file_name='model.pkl'):
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)

    def run_model(self):

        # Encode categorical features and store feature encoders
        categorical_features = ['gender', 'have_savings', 'financial_knowledge', 'emergency_fund',
                                'debt_level',
                                'income_stability', 'expense_tracking', 'investment_experience',
                                'investment_understanding', 'finance_courses', 'financial_news', 'risk_tolerance',
                                'financial_goals']
        for col in categorical_features:
            encoder = LabelEncoder()
            self.full_dataset[col] = encoder.fit_transform(self.full_dataset[col])
            self.encoders[col] = encoder  # Store the fitted encoder for each feature

        # Prepare features
        X = self.full_dataset.drop(['birthdate', 'financial_literacy_level', 'financial_behavior',
                                    'financial_goals_category'], axis=1)

        # Initialize, train, and store models for each label
        label_encoders = {}  # Create a dictionary to hold encoders for each label
        labels = ['financial_literacy_level', 'financial_behavior', 'financial_goals_category']
        for label in labels:
            encoder = LabelEncoder()
            self.full_dataset[label] = encoder.fit_transform(self.full_dataset[label])
            label_encoders[label] = encoder  # Store the fitted encoder for each label
            self.encoders[label] = encoder  # Store the fitted encoder for each label

        self.encoders['labels'] = label_encoders  # Store all label encoders under 'labels' key
        for label in labels:
            y = self.full_dataset[label]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.training_features["training_features"] = list(X_train.columns)
            model = RandomForestClassifier(random_state=42)
            model.fit(X_train, y_train)
            self.models[label] = model  # Store the trained model
            y_pred = model.predict(X_test)
            print(f'Accuracy for {label}: {accuracy_score(y_test, y_pred)}')

    def predict(self, test_dict, expenses, training_features):
        # Ensure test_point is a DataFrame for consistency in processing
        merged_dict = test_dict | expenses
        keys_to_keep = ['gender', 'average_wage', 'birthdate', 'have_savings', 'financial_knowledge',
                        'emergency_fund',
                        'debt_level', 'retirement_age', 'income_stability', 'expense_tracking',
                        'income_stability', 'expense_tracking', 'investment_experience',
                        'investment_understanding', 'finance_courses', 'financial_news', 'risk_tolerance',
                        'financial_goals']
        keys_to_keep.extend(expenses.keys())
        filtered_dict = {key: merged_dict[key] for key in keys_to_keep}
        test_point = pd.DataFrame([filtered_dict])

        current_date = datetime.now()
        test_point['birthdate'] = pd.to_datetime(test_point['birthdate'])
        birth_date = test_point['birthdate'].iloc[0]
        age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month,
                                                                                               birth_date.day))
        test_point['age'] = age
        ordered_test_point = {key: test_point[key][0] for key in training_features}
        test_point = pd.DataFrame([ordered_test_point])
        for col, encoder in self.encoders.items():
            if col == 'label':
                continue

            if col in test_point.columns:  # Ensure column exists in test_point
                encoder.classes_ = np.array([cla.lower() for cla in encoder.classes_])
                test_point[col] = encoder.transform(test_point[col])

        # Predict with each model and decode the predictions
        predictions = {}
        for label, model in self.models.items():
            encoded_pred = model.predict(test_point.values)

            # Decode the prediction using the 'label' encoder
            label = label.lower()
            decoded_pred = self.encoders[label].inverse_transform(encoded_pred)  # Decoding step
            predictions[label] = decoded_pred[0]  # Assuming only one test point

        return predictions


def load_model(file_name='model.pkl'):
    with open(file_name, 'rb') as file:
        model = pickle.load(file)

    if not isinstance(model, dict):
        keys = list(model.encoders.keys())
        for key in keys:
            new_key = key.lower()
            model.encoders[new_key] = model.encoders.pop(key)
    return model


def save_model(model_s, file_name='model.pkl'):
    with open(file_name, 'wb') as file:
        pickle.dump(model_s, file)


def get_expenses(expenses_path):
    df = pd.read_csv(expenses_path)

    # Ensure the 'date' column is treated as a datetime type
    df['date'] = pd.to_datetime(df['date'])

    # Extract year and month from 'date' for easier grouping
    df['year_month'] = df['date'].dt.to_period('M')

    # Group by 'category' and 'year_month', then sum the 'amount_spent'
    monthly_spending = df.groupby(['category', 'year_month'])['amount_spent'].sum().reset_index()

    # Calculate the average monthly spending for each category
    average_monthly_spending = monthly_spending.groupby('category')['amount_spent'].mean()

    # Convert the Series to a dictionary
    average_monthly_spending_dict = average_monthly_spending.to_dict()
    return average_monthly_spending_dict


def run_model(user_name):
    import __main__
    setattr(__main__, "Model", Model)
    setattr(__main__, "Labels", Labels)
    setattr(__main__, "UserGenerator", UserGenerator)
    # model = Model()
    # model.run_model()
    # model.save_model()
    # save_model(model, 'trained_model/my_model.pkl')
    # save_model(model.training_features, 'trained_model/training_features.pkl')
    user_info = load_user_info(user_name)
    for info in user_info:
        if type(user_info[info]) == str:
            user_info[info] = user_info[info].lower()
    # expenses_path = user_info['expenses_path']
    expenses_path = "expences_data/expenses.csv"
    expenses = get_expenses(expenses_path)
    model = load_model('trained_model/my_model.pkl')
    training_features = load_model('trained_model/training_features.pkl')['training_features']
    predictions = model.predict(user_info, expenses, training_features)
    return predictions
