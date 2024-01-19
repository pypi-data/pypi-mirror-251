# backwardsreg/tests/test_backward_regression.py
import pandas as pd
import numpy as np
import pytest
from backwardsreg.backward_regression import backward_regression

@pytest.fixture
def financial_data():
    # Generate financial dataset for testing
    np.random.seed(42)

    age = np.random.normal(40, 10, 1000)
    income = np.random.normal(50000, 10000, 1000)
    savings = np.random.normal(20000, 5000, 1000)
    debt = np.random.normal(10000, 3000, 1000)
    credit_score = np.random.normal(700, 50, 1000)
    assets = np.random.normal(30000, 8000, 1000)
    liabilities = np.random.normal(12000, 4000, 1000)
    monthly_expenses = np.random.normal(4000, 1000, 1000)

    target = 0.5 * age + 0.2 * income - 0.3 * savings + 0.1 * debt + 0.15 * credit_score + np.random.normal(0, 5, 1000)

    financial_data = pd.DataFrame({
        'Age': age,
        'Income': income,
        'Savings': savings,
        'Debt': debt,
        'CreditScore': credit_score,
        'Assets': assets,
        'Liabilities': liabilities,
        'MonthlyExpenses': monthly_expenses,
        'Target': target
    })

    return financial_data

@pytest.fixture
def binary_financial_data():
    # Generate binary financial dataset for testing
    np.random.seed(42)

    age = np.random.normal(40, 10, 1000)
    income = np.random.normal(50000, 10000, 1000)
    savings = np.random.normal(20000, 5000, 1000)
    debt = np.random.normal(10000, 3000, 1000)
    credit_score = np.random.normal(700, 50, 1000)
    assets = np.random.normal(30000, 8000, 1000)
    liabilities = np.random.normal(12000, 4000, 1000)
    monthly_expenses = np.random.normal(4000, 1000, 1000)

    target = (0.5 * age + 0.2 * income - 0.3 * savings + 0.1 * debt + 0.15 * credit_score
              + np.random.normal(0, 5, 1000)) > 0

    binary_financial_data = pd.DataFrame({
        'Age': age,
        'Income': income,
        'Savings': savings,
        'Debt': debt,
        'CreditScore': credit_score,
        'Assets': assets,
        'Liabilities': liabilities,
        'MonthlyExpenses': monthly_expenses,
        'Target': target.astype(int)  # Convert to integer (0 or 1)
    })

    return binary_financial_data

def test_backward_regression_linear(financial_data):
    X = financial_data.drop('Target', axis=1)  # Features
    y = financial_data['Target']  # Target variable

    result, dropped_vars = backward_regression(X, y, threshold_in=0.01, threshold_out=0.05, include_interactions=False, verbose=False)

    # Add assertions based on your expectations
    assert 'Age' in result
    assert 'Income' in result
    assert 'Savings' in result
    assert 'Debt' in result
    assert 'CreditScore' in result
    assert 'Assets' in result
    assert 'Liabilities' in result
    assert 'MonthlyExpenses' in result
    assert 'Target' not in result  # Target variable should be dropped

    # Ensure that dropped variables are in the expected list
    expected_dropped_vars = ['Liabilities', 'MonthlyExpenses']  # Adjust based on your expectations
    assert all(var in dropped_vars for var in expected_dropped_vars)
    assert len(dropped_vars) == len(expected_dropped_vars)

def test_backward_regression_logistic(binary_financial_data):
    X = binary_financial_data.drop('Target', axis=1)  # Features
    y = binary_financial_data['Target']  # Binary target variable

    result, dropped_vars = backward_regression(X, y, threshold_in=0.01, threshold_out=0.05, include_interactions=False, verbose=False)

    # Add assertions based on your expectations for logistic regression
    assert 'Age' in result
    assert 'Income' in result
    assert 'Savings' in result
    assert 'Debt' in result
    assert 'CreditScore' in result
    assert 'Assets' in result
    assert 'Liabilities' in result
    assert 'MonthlyExpenses' in result
    assert 'Target' not in result  # Target variable should be dropped

    # Ensure that dropped variables are in the expected list
    expected_dropped_vars = ['Liabilities', 'MonthlyExpenses']  # Adjust based on your expectations
    assert all(var in dropped_vars for var in expected_dropped_vars)
    assert len(dropped_vars) == len(expected_dropped_vars)
