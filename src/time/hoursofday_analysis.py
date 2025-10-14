import pandas as pd
import plotly.express as px
import os
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

def create_hourly_revenue_chart(df: pd.DataFrame):
    """Creates a line chart for hourly revenue trends."""
    # Sử dụng cột InvoiceHour và Total_Cost từ dataset
    hourly_sales = df[df['InvoiceHour'].between(6, 20)].groupby('InvoiceHour')['Total_Cost'].sum().reset_index()

    fig = px.line(
        hourly_sales,
        x='InvoiceHour',
        y='Total_Cost',
        title='Tổng Doanh thu theo Giờ trong Ngày',
        markers=True
    )

    # Cập nhật layout để hiển thị đầy đủ
    fig.update_layout(
        xaxis_title="Giờ",
        yaxis_title="Tổng Doanh thu (£)",
        height=500
    )

    # Định dạng trục Y không viết tắt
    fig.update_yaxes(tickformat=",")

    # Đảm bảo hiển thị tất cả các giờ trên trục X
    fig.update_xaxes(
        tickmode='linear',
        dtick=1,
        tickvals=list(range(6, 21))
    )

    return fig

def display_hourly_stats(df: pd.DataFrame):
    """Hiển thị thống kê doanh thu theo giờ dạng ngang"""
    # Sử dụng cột InvoiceHour và Total_Cost từ dataset
    hourly_sales = df[df['InvoiceHour'].between(6, 20)].groupby('InvoiceHour')['Total_Cost'].sum().reset_index()

    total_revenue = hourly_sales['Total_Cost'].sum()
    avg_revenue = hourly_sales['Total_Cost'].mean()
    max_revenue = hourly_sales['Total_Cost'].max()
    min_revenue = hourly_sales['Total_Cost'].min()

    # Hiển thị thống kê trong 4 cột
    import streamlit as st
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Tổng doanh thu", f"£{total_revenue:,.0f}")
    with col2:
        st.metric("📈 Doanh thu trung bình/giờ", f"£{avg_revenue:,.0f}")
    with col3:
        st.metric("🔥 Doanh thu cao nhất", f"£{max_revenue:,.0f}")
    with col4:
        st.metric("📉 Doanh thu thấp nhất", f"£{min_revenue:,.0f}")
