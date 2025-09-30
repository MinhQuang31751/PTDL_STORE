import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt

def show_overview():
    st.title("Đánh Giá Tổng Quan với Dữ Liệu")

    if 'data' not in st.session_state or st.session_state.data is None:
        st.warning("Vui lòng tải lên file dữ liệu ở trang 'Dữ Liệu' trước khi xem đánh giá tổng quan.")
        return

    selected = option_menu(
        menu_title=None,
        options=["Bảng dữ liệu chi tiết", "Thông tin về các cột", "Doanh thu theo địa chỉ cửa hàng", "Thống kê mô tả"],
        icons=["table", "info-circle", "bar-chart", "clipboard-data"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Bảng dữ liệu chi tiết":
        st.subheader("Bảng dữ liệu chi tiết")
        st.dataframe(st.session_state.data, width='stretch')
        total_rows = len(st.session_state.data)
        st.write(f"**Số dòng dữ liệu (số lượng giao dịch):** {total_rows}")

    elif selected == "Thông tin về các cột":
        st.subheader("Thông tin về các cột")
        total_columns = len(st.session_state.data.columns)
        st.write(f"**Số cột dữ liệu:** {total_columns}")

        column_names = st.session_state.data.columns.tolist()
        st.write("**Tên các cột:**")
        for i, col in enumerate(column_names, 1):
            st.write(f"{i}. {col}")

        with st.expander("Chi tiết thông tin cột (bao gồm kiểu dữ liệu)"):
            column_info = pd.DataFrame({
                'Tên cột': column_names,
                'Kiểu dữ liệu': [str(st.session_state.data[col].dtype) for col in column_names]
            })
            st.dataframe(column_info, width='stretch')

    elif selected == "Doanh thu theo địa chỉ cửa hàng":
        st.subheader("Doanh thu theo địa chỉ cửa hàng")
        if 'City' in st.session_state.data.columns and 'Total_Cost' in st.session_state.data.columns:
            sales_by_address = st.session_state.data.groupby('City')['Total_Cost'].sum().reset_index()
            sales_by_address = sales_by_address.sort_values(by='Total_Cost', ascending=False)
            st.write("**Doanh thu theo địa chỉ (tổng giảm dần):**")
            st.dataframe(sales_by_address, width='stretch')

            fig, ax = plt.subplots()
            ax.pie(sales_by_address['Total_Cost'], labels=sales_by_address['City'], autopct='%1.1f%%', startangle=90, colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'])
            ax.axis('equal')
            plt.title("Doanh Thu Theo Địa Chỉ Cửa Hàng")
            st.pyplot(fig)
        else:
            st.error("Dữ liệu không chứa cột 'City' hoặc 'Total_Cost'.")

    elif selected == "Thống kê mô tả":
        st.subheader("Thống kê mô tả")
        if 'Total_Cost' in st.session_state.data.columns:
            total_rows = len(st.session_state.data)
            st.write(f"**Số lượng giao dịch:** {total_rows}")
            total_revenue = st.session_state.data['Total_Cost'].sum()
            st.write(f"**Tổng doanh thu:** ${total_revenue:,.2f}")
        else:
            st.error("Dữ liệu không chứa cột 'Total_Cost'.")

if __name__ == "__main__":
    show_overview()
    