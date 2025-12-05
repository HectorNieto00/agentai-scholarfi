# services/savings_recomender.py
import pandas as pd
from datetime import datetime

def generate_savings_recommendations(transactions, goals):
    """
    Generate personalized savings recommendations based on user's spending habits and savings goals.
    """

    # If no savings goals, no recommendations
    if not goals:
        return [{"text": "Add a goal to receive personalized savings tips."}]

    recommendations = []

    # Convert transactions to DataFrame
    df = pd.DataFrame(transactions)
    if df.empty:
        return [{"text": "No transactions yet."}]
    
    # Ensure 'date' column is datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])  # remove invalid dates

    # Filter only expenses
    df = df[df['type'] == 'expense']

    # Filter only transactions for the current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    df = df[(df['date'].dt.month == current_month) & (df['date'].dt.year == current_year)]

    if df.empty:
        return [{"text": "No expenses recorded for the current month."}]

    # Group by category
    df_grouped = df.groupby("category")["amount"].sum().reset_index()

    # Total spent this month
    total_expense = df_grouped['amount'].sum()

    # Example logic: suggest reducing 10% in highest spending category
    if not df_grouped.empty:
        top_category_row = df_grouped.sort_values(by='amount', ascending=False).iloc[0]
        top_category = top_category_row['category']
        top_amount = top_category_row['amount']

        suggested_saving = round(top_amount * 0.1, 2)  # 10% saving suggestion
        recommendations.append({
            "text": f"Consider reducing £{suggested_saving} in {top_category} this month to accelerate your savings goals."
        })

    # Example: daily saving suggestion
    days_remaining = 30 - datetime.now().day
    if days_remaining > 0:
        daily_saving = round(suggested_saving / days_remaining, 2)
        recommendations.append({
            "text": f"Saving just £{daily_saving} per day in {top_category} can help you reach your target faster."
        })

    # Example: Redistribute small amounts from multiple categories
    if len(df_grouped) > 1:
        second_category_row = df_grouped.sort_values(by='amount', ascending=False).iloc[1]
        second_category = second_category_row['category']
        second_saving = round(second_category_row['amount'] * 0.05, 2)  # 5% saving
        recommendations.append({
            "text": f"Try saving £{second_saving} from {second_category} and redirect it to your savings goal."
        })

    return recommendations
