import streamlit as st
import pandas as pd

def show_overview():
    # Kiểm tra dữ liệu đã tải
    if 'data' not in st.session_state or st.session_state.data is None:
        st.warning("Vui lòng tải lên file dữ liệu ở trang 'Dữ Liệu' trước khi xem đánh giá tổng quan.")
    else:
        st.title("Đánh Giá Tổng Quan với Dữ Liệu")

        # Hiển thị bảng dữ liệu đầy đủ
        st.subheader("Bảng dữ liệu chi tiết")
        st.dataframe(st.session_state.data)

        # Tính và hiển thị số dòng
        total_rows = len(st.session_state.data)
        st.write(f"**Số dòng dữ liệu (số lượng giao dịch):** {total_rows}")
        
        # Thông tin về các cột
        st.subheader("Thông tin về các cột")
        total_columns = len(st.session_state.data.columns)
        st.write(f"**Số cột dữ liệu:** {total_columns}")

        # Hiển thị tên các cột dưới dạng danh sách đánh số
        column_names = st.session_state.data.columns.tolist()
        st.write("**Tên các cột:**")
        for i, col in enumerate(column_names, 1):
            st.write(f"{i}. {col}")

        # Hoặc hiển thị dưới dạng expander để tiết kiệm không gian (tùy chọn)
        with st.expander("Chi tiết thông tin cột (bao gồm kiểu dữ liệu)"):
            column_info = pd.DataFrame({
                'Tên cột': column_names,
                'Kiểu dữ liệu': [str(st.session_state.data[col].dtype) for col in column_names]
            })
            st.dataframe(column_info)

        # Thống kê doanh thu theo địa chỉ (City)
        st.subheader("Thống kê doanh thu theo địa chỉ cửa hàng")
        if 'City' in st.session_state.data.columns and 'Total_Cost' in st.session_state.data.columns:
            sales_by_address = st.session_state.data.groupby('City')['Total_Cost'].sum().reset_index()
            sales_by_address = sales_by_address.sort_values(by='Total_Cost', ascending=False)
            st.write("**Doanh thu theo địa chỉ (tổng giảm dần):**")
            st.dataframe(sales_by_address)
        else:
            st.error("Dữ liệu không chứa cột 'City' hoặc 'Total_Cost'.")

        # Thống kê mô tả (Descriptive Statistics)
        st.subheader("Thống kê mô tả")
        if 'Total_Cost' in st.session_state.data.columns:
            # Số lượng giao dịch (đã hiển thị ở trên, sử dụng lại total_rows)
            st.write(f"**Số lượng giao dịch:** {total_rows}")

            # Tổng doanh thu
            total_revenue = st.session_state.data['Total_Cost'].sum()
            st.write(f"**Tổng doanh thu:** ${total_revenue:,.2f}")

if __name__ == "__main__":
    show_overview()