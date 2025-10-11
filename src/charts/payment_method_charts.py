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

    fig = px.bar(method_counts, x='Count', y='Payment_Method', orientation='h', title='Số lượng giao dịch theo phương thức thanh toán')
    return fig
