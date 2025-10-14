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

    # Xử lý theo lựa chọn
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

            # Tùy chọn xử lý null
            action = st.selectbox("Chọn phương pháp xử lý:", ["Không xử lý", "Xóa hàng có null", "Điền giá trị trung bình"])
            if action == "Xóa hàng có null":
                cleaned_data = st.session_state.data.dropna()
                st.session_state.data = cleaned_data
                st.success(f"Đã xóa {len(st.session_state.data) - len(cleaned_data)} hàng có giá trị null.")
                st.dataframe(st.session_state.data)
            elif action == "Điền giá trị trung bình":
                numeric_columns = st.session_state.data.select_dtypes(include=['int64', 'float64']).columns
                if not numeric_columns.empty:
                    cleaned_data = st.session_state.data.copy()
                    for col in numeric_columns:
                        if cleaned_data[col].isnull().sum() > 0:
                            cleaned_data[col] = cleaned_data[col].fillna(cleaned_data[col].mean())
                    st.session_state.data = cleaned_data
                    st.success("Đã điền giá trị trung bình cho các cột số.")
                    st.dataframe(st.session_state.data)
                else:
                    st.error("Không có cột số để điền giá trị trung bình.")

    elif selected == "Chuẩn hóa kiểu dữ liệu và tạo cột mới":
            st.title("Chuẩn hóa kiểu dữ liệu và tạo cột mới")
            
            # Kiểm tra xem có cột InvoiceDate không
            if 'InvoiceDate' not in st.session_state.data.columns:
                st.error("Không tìm thấy cột 'InvoiceDate' trong dữ liệu.")
                return
            
            # Xử lý tuần tự để tránh lặp lại
            
            
            st.success("Đã tạo 5 cột mới: TotalPrice, InvoiceYear, InvoiceMonth, InvoiceDayName, InvoiceHour")
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



