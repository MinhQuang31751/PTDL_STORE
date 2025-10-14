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

    fig = px.bar(
        category_counts,
        x='Customer_Category',
        y='Count',
        title='Số lượng giao dịch theo nhóm khách hàng',
        color='Customer_Category',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    return fig

def create_revenue_by_customer_category_bar_chart(df: pd.DataFrame):
    """Creates a bar chart for total revenue by Customer_Category."""
    if 'Total_Cost' not in df.columns:
        return None  # Or raise an error
    revenue_by_category = df.groupby('Customer_Category')['Total_Cost'].sum().reset_index()
    fig = px.bar(
        revenue_by_category,
        x='Customer_Category',
        y='Total_Cost',
        title='Tổng doanh thu theo nhóm khách hàng',
        color='Customer_Category',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    return fig

def create_customer_payment_method_grouped_bar_chart(df: pd.DataFrame):
    """Creates a grouped bar chart for Customer_Category and Payment_Method."""
    grouped_data = df.groupby(['Customer_Category', 'Payment_Method']).size().reset_index(name='Count')
    fig = px.bar(grouped_data, x='Customer_Category', y='Count', color='Payment_Method', barmode='group', title='Số lượng giao dịch theo Phương thức thanh toán và Nhóm khách hàng')
    return fig
