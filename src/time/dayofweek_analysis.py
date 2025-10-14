import pandas as pd
import plotly.express as px

def create_weekday_revenue_bar_chart(df: pd.DataFrame):
    """Creates a bar chart for revenue by weekday."""
    weekday_sales = df.groupby('InvoiceDayName')['Total_Cost'].sum().reset_index()

    # Sắp xếp theo thứ tự ngày trong tuần
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_sales['InvoiceDayName'] = pd.Categorical(weekday_sales['InvoiceDayName'],
                                                   categories=day_order,
                                                   ordered=True)
    weekday_sales = weekday_sales.sort_values('InvoiceDayName')

    fig = px.bar(weekday_sales, x='InvoiceDayName', y='Total_Cost',
                title='Doanh thu theo Ngày trong Tuần', color='InvoiceDayName')
    return fig

def create_weekday_revenue_pie_chart(df: pd.DataFrame):
    """Creates a pie chart for revenue distribution by weekday."""
    weekday_sales = df.groupby('InvoiceDayName')['Total_Cost'].sum().reset_index()

    # Sắp xếp theo thứ tự ngày trong tuần
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_sales['InvoiceDayName'] = pd.Categorical(weekday_sales['InvoiceDayName'],
                                                   categories=day_order,
                                                   ordered=True)
    weekday_sales = weekday_sales.sort_values('InvoiceDayName')

    fig = px.pie(weekday_sales, values='Total_Cost', names='InvoiceDayName',
                title='Phân bố Doanh thu theo Ngày')
    return fig

def display_weekday_stats(df: pd.DataFrame):
    """Hiển thị thống kê doanh thu theo ngày trong tuần"""
    weekday_sales = df.groupby('InvoiceDayName')['Total_Cost'].sum().reset_index()

    # Sắp xếp theo thứ tự ngày trong tuần
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_sales['InvoiceDayName'] = pd.Categorical(weekday_sales['InvoiceDayName'],
                                                   categories=day_order,
                                                   ordered=True)
    weekday_sales = weekday_sales.sort_values('InvoiceDayName')

    total = weekday_sales['Total_Cost'].sum()
    avg = weekday_sales['Total_Cost'].mean()
    best_day = weekday_sales.loc[weekday_sales['Total_Cost'].idxmax(), 'InvoiceDayName']
    worst_day = weekday_sales.loc[weekday_sales['Total_Cost'].idxmin(), 'InvoiceDayName']

    import streamlit as st
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Tổng", f"£{total:,.0f}")
    with col2:
        st.metric("📈 TB/ngày", f"£{avg:,.0f}")
    with col3:
        st.metric("🔥 Tốt nhất", best_day)
    with col4:
        st.metric("📉 Thấp nhất", worst_day)
