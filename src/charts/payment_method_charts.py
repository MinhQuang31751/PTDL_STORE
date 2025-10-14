import plotly.express as px
import pandas as pd

def create_payment_method_pie_chart(df: pd.DataFrame):
    """Creates a pie chart for the Payment_Method column."""
    fig = px.pie(df, names='Payment_Method', title='Tỷ lệ các phương thức thanh toán')
    return fig

def create_payment_method_bar_chart(df: pd.DataFrame):
    """Creates a horizontal bar chart for the Payment_Method column."""
    # Group by Payment_Method and count the occurrences
    method_counts = df['Payment_Method'].value_counts().reset_index()
    method_counts.columns = ['Payment_Method', 'Count']

    fig = px.bar(
        method_counts,
        x='Count',
        y='Payment_Method',
        orientation='h',
        title='Số lượng giao dịch theo phương thức thanh toán',
        color='Payment_Method',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig


def create_revenue_by_payment_method_bar_chart(df: pd.DataFrame):
    """Creates a bar chart for total revenue by Payment_Method."""
    if 'Total_Cost' not in df.columns:
        return None  # Or raise an error
    revenue_by_method = df.groupby('Payment_Method')['Total_Cost'].sum().reset_index()
    fig = px.bar(revenue_by_method, x='Payment_Method', y='Total_Cost', title='Tổng doanh thu theo phương thức thanh toán')
    return fig
