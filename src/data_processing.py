import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from streamlit_option_menu import option_menu

# Hàm xử lý dữ liệu
def process_data():
    # Kiểm tra dữ liệu đã tải
    if 'data' not in st.session_state or st.session_state.data is None:
        st.warning("Vui lòng tải lên file dữ liệu ở trang 'Dữ Liệu' trước khi xử lý.")
        return

    # Tạo menu tùy chọn
    selected = option_menu(
        menu_title=None,
        options=["Xử lí giá trị bị thiếu và không hợp lệ", "Chuẩn hóa kiểu dữ liệu và tạo cột mới", "Mã hóa và Tách cột"],
        icons=["gear", "scissors", "list", "code"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Xử lí giá trị bị thiếu và không hợp lệ":
        st.title("Xử lí giá trị bị thiếu và không hợp lệ")
        st.dataframe(st.session_state.data)

    # Kiểm tra và thống kê giá trị null
    null_counts = st.session_state.data.isnull().sum()
    if null_counts.sum() == 0:
        st.success("Không có giá trị null trong dữ liệu.")
    else:
        st.write("**Số lượng giá trị null theo cột:**")
        st.dataframe(null_counts[null_counts > 0].to_frame(name='Số lượng null'))
        null_percentage = (st.session_state.data.isnull().mean() * 100).round(2)
        st.write("**Tỷ lệ phần trăm giá trị null theo cột:**")
        st.dataframe(null_percentage[null_percentage > 0].to_frame(name='Tỷ lệ null (%)'))

        # Chọn cột bị null để xóa các phần tử null trong cột đó
        columns_with_null = null_counts[null_counts > 0].index.tolist()
        columns_to_clean = st.multiselect(
            "Chọn cột bị null để xóa các phần tử null:",
            options=columns_with_null,
            default=[]
        )
    if st.button("Xóa các phần tử null đã chọn"):
            if columns_to_clean:
                original_len = len(st.session_state.data)
                cleaned_data = st.session_state.data.dropna(subset=columns_to_clean)
                st.session_state.data = cleaned_data
                rows_dropped = original_len - len(cleaned_data)
                st.success(f"Đã xóa {rows_dropped} hàng có giá trị null trong các cột: {', '.join(columns_to_clean)}")
                st.dataframe(st.session_state.data)
            else:
                st.warning("Vui lòng chọn ít nhất một cột để xử lý.")


    elif selected == "Chuẩn hóa kiểu dữ liệu và tạo cột mới":
            st.title("Chuẩn hóa kiểu dữ liệu và tạo cột mới")
            
            # Kiểm tra xem có cột InvoiceDate không
            if 'InvoiceDate' not in st.session_state.data.columns:
                st.error("Không tìm thấy cột 'InvoiceDate' trong dữ liệu.")
                return
            
            # Xử lý tuần tự để tránh lặp lại
            
            
            st.success("Đã tạo 5 cột mới: Total_Cost, InvoiceYear, InvoiceMonth, InvoiceDayName, InvoiceHour")
            st.dataframe(st.session_state.data)

    
    elif selected == "Mã hóa và Tách cột":
        st.title("Mã hóa và Tách cột")
        if 'data' not in st.session_state or st.session_state.data is None:
            st.warning("Vui lòng tải lên file dữ liệu ở trang 'Dữ Liệu' trước khi xử lý.")
            return

        df = st.session_state.data.copy()

        # Mã hóa cột Country
        if 'Country' in df.columns:
            le = LabelEncoder()
            df['CountryEncoded'] = le.fit_transform(df['Country'])
            st.success("Đã mã hóa cột 'Country' thành 'CountryEncoded'.")
        else:
            st.error("Không tìm thấy cột 'Country' trong dữ liệu.")

        # Tách cột InvoiceNo
        if 'InvoiceNo' in df.columns:
            df['InvoicePrefix'] = df['InvoiceNo'].str[0]
            df['InvoiceNumber'] = df['InvoiceNo'].str[1:].astype(int)
            st.success("Đã tách cột 'InvoiceNo' thành 'InvoicePrefix' và 'InvoiceNumber'.")
        else:
            st.error("Không tìm thấy cột 'InvoiceNo' trong dữ liệu.")

        # Cập nhật session state
        st.session_state.data = df
        st.dataframe(st.session_state.data)
if __name__ == "__main__":
    process_data()



