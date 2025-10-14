import pandas as pd
import plotly.express as px

def create_monthly_revenue_chart(df: pd.DataFrame):
    """Creates a line chart for monthly revenue trends."""
    monthly_sales = df.groupby(['InvoiceYear', 'InvoiceMonth'])['Total_Cost'].sum().reset_index()
    monthly_sales['YearMonth'] = pd.to_datetime(
        monthly_sales['InvoiceYear'].astype(str) + '-' +
        monthly_sales['InvoiceMonth'].astype(str) + '-01'
    )

    fig = px.line(monthly_sales, x='YearMonth', y='Total_Cost', title='Xu hướng Doanh thu Hàng tháng', markers=True)

    # Cập nhật layout
    fig.update_layout(
        xaxis_title="Tháng",
        yaxis_title="Tổng Doanh thu (£)",
        height=400
    )

    # Định dạng trục
    fig.update_yaxes(tickformat=",")
    fig.update_xaxes(
        dtick="M1",
        tickformat="%m/%Y",  # Format: tháng/năm (ví dụ: 01/2023)
        tickangle=0
    )

    return fig

def display_revenue_stats(df: pd.DataFrame):
    """Hiển thị thống kê doanh thu dạng ngang"""
    monthly_sales = df.groupby(['InvoiceYear', 'InvoiceMonth'])['Total_Cost'].sum().reset_index()

    total_revenue = monthly_sales['Total_Cost'].sum()
    avg_revenue = monthly_sales['Total_Cost'].mean()
    max_revenue = monthly_sales['Total_Cost'].max()
    min_revenue = monthly_sales['Total_Cost'].min()

    # Hiển thị thống kê trong 4 cột
    import streamlit as st
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Tổng doanh thu", f"£{total_revenue:,.0f}")
    with col2:
        st.metric("📈 TB/tháng", f"£{avg_revenue:,.0f}")
    with col3:
        st.metric("🔥 Cao nhất", f"£{max_revenue:,.0f}")
    with col4:
        st.metric("📉 Thấp nhất", f"£{min_revenue:,.0f}")
