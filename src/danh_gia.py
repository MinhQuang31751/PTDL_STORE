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
        options=["Bảng dữ liệu chi tiết", "Thông tin về các cột", "Liệt kê các sản phẩm"],
        icons=["table", "info-circle", "bar-chart", "clipboard-data"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Bảng dữ liệu chi tiết":
        st.subheader("Bảng dữ liệu chi tiết")
        if 'data' not in st.session_state:
            st.error("Dữ liệu chưa được tải. Vui lòng tải dữ liệu trước.")
            return
        
        st.dataframe(st.session_state.data, width='stretch')
        total_rows = len(st.session_state.data)
        st.write(f"**Số dòng dữ liệu:** {total_rows}")
        
        if 'TotalPrice' in st.session_state.data.columns:
            total_revenue = st.session_state.data['TotalPrice'].sum()
            st.write(f"**Tổng doanh thu:** ${total_revenue:,.2f}")
        else:
            st.warning("Không tìm thấy cột 'TotalPrice'. Vui lòng chuẩn hóa dữ liệu trước.")

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

    elif selected == "Liệt kê các sản phẩm":
        st.subheader("Liệt kê các sản phẩm")
        if 'data' not in st.session_state or st.session_state.data is None:
            st.warning("Vui lòng tải lên file dữ liệu ở trang 'Dữ Liệu' trước khi xử lý.")
            return

        # Kiểm tra xem có cột Description không
        if 'Description' not in st.session_state.data.columns:
            st.error("Không tìm thấy cột 'Description' trong dữ liệu.")
            return

        product_counts = st.session_state.data['Description'].value_counts().reset_index()
        product_counts.columns = ['Sản phẩm', 'Số lượng bán']
        st.dataframe(product_counts)
    

   
if __name__ == "__main__":
    show_overview()