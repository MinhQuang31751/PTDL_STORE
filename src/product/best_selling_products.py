import streamlit as st
import pandas as pd
import plotly.express as px

def top_product_analysis(df):
    """
    Phân tích sản phẩm bán hàng:
    - Thống kê tổng quan
    - Top 10 sản phẩm bán chạy nhất (tương tác)
    - Top 10 sản phẩm bị hủy/trả lại nhiều nhất (tương tác)
    """

    # Tiền xử lý cơ bản
    df = df.copy()
    df.columns = df.columns.str.strip()

    if 'DoanhThu' not in df.columns:
        df['DoanhThu'] = df['Quantity'] * df['UnitPrice']

    #Lọc các mô tả koophải sản phẩm 
    exclude_keywords = r'manual|check|samples|discount|postage|damages|thrown away|test|unsaleable|\?'
    filtered_df = df[~df['Description'].str.contains(exclude_keywords, case=False, na=False)]

    #Thống kê tổng quan
    total_products = filtered_df['Description'].nunique()
    total_quantity = filtered_df['Quantity'].sum()
    total_revenue = filtered_df['DoanhThu'].sum()
    avg_price = filtered_df['UnitPrice'].mean()

    st.subheader("📈 Thống kê tổng quan về Sản phẩm")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số sản phẩm khác nhau", f"{total_products:,}")
    col2.metric("Tổng số lượng bán ra", f"{total_quantity:,}")
    col3.metric("Tổng doanh thu (ước tính)", f"£{total_revenue:,.2f}")
    col4.metric("Giá trung bình", f"£{avg_price:,.2f}")

    st.markdown("---")

    # Top 10 sản phẩm bán chạy nhất 
    st.subheader("💰 Top 10 Sản Phẩm Bán Chạy Nhất (Theo Tổng Doanh Thu)")

    product_revenue = (
        filtered_df.groupby('Description', as_index=False)['DoanhThu']
        .sum()
        .sort_values(by='DoanhThu', ascending=False)
        .head(10)
    )

    fig1 = px.bar(
        product_revenue,
        x='DoanhThu',
        y='Description',
        orientation='h',
        text='DoanhThu',
        color='Description',
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="Top 10 Sản Phẩm Bán Chạy Nhất (Theo Tổng Doanh Thu)"
    )

    fig1.update_traces(texttemplate='£%{text:,.0f}', textposition='outside')
    fig1.update_layout(
        yaxis=dict(categoryorder='total ascending'),
        xaxis_title="Tổng Doanh Thu (£)",
        yaxis_title="Tên Sản Phẩm",
        showlegend=False,
        height=600
    )
    st.plotly_chart(fig1, use_container_width=True)

    #  Top 10 sản phẩm bị hủy/trả lại
    st.subheader("🚫 Top 10 Sản Phẩm Bị Hủy/Trả Lại Nhiều Nhất")

    cancelled = filtered_df[filtered_df['Quantity'] < 0]
    if cancelled.empty:
        st.info("Không có sản phẩm nào bị hủy hoặc trả lại trong dữ liệu.")
    else:
        # dòng có Quantity < 0 được tính là 1 lần hủy trả
        cancelled = cancelled.assign(CancelCount=1)

        cancelled_products = (
            cancelled.groupby('Description', as_index=False)['CancelCount']
            .sum()
            .sort_values(by='CancelCount', ascending=False)
            .head(10)
        )

        fig2 = px.bar(
            cancelled_products,
            x='CancelCount',
            y='Description',
            orientation='h',
            text='CancelCount',
            color='Description',
            color_discrete_sequence=px.colors.sequential.Reds,
            title="Top 10 Sản Phẩm Bị Hủy/Trả Lại Nhiều Nhất"
        )

        fig2.update_traces(texttemplate='%{text}', textposition='outside')
        fig2.update_layout(
            yaxis=dict(categoryorder='total ascending'),
            xaxis_title="Số lần bị hủy / trả lại",
            yaxis_title="Tên Sản Phẩm",
            showlegend=False,
            height=600
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Hiển thị bảng dữ liệu
        with st.expander("📋 Xem bảng dữ liệu chi tiết"):
            st.write("**Top 10 sản phẩm bán chạy nhất:**")
            st.dataframe(product_revenue)
            st.write("**Top 10 sản phẩm bị hủy/trả lại:**")
            st.dataframe(cancelled_products)
