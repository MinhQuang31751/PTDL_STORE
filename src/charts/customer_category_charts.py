import plotly.express as px
import pandas as pd

def create_customer_category_pie_chart(df: pd.DataFrame):
    """Creates a pie chart for the Customer_Category column."""
    fig = px.pie(df, names='Customer_Category', title='Tỷ lệ các nhóm khách hàng')
    return fig

def create_customer_category_bar_chart(df: pd.DataFrame):
    """Creates a bar chart for the Customer_Category column."""
    # Group by Customer_Category and count the occurrences
    category_counts = df['Customer_Category'].value_counts().reset_index()
    category_counts.columns = ['Customer_Category', 'Count']

    fig = px.bar(category_counts, x='Customer_Category', y='Count', title='Số lượng giao dịch theo nhóm khách hàng')
    return fig
