import streamlit as st
import pandas as pd

def upload_data():
    st.write("Đây là trang để tải dữ liệu.")
    uploaded_file = st.file_uploader("Tải lên file dữ liệu", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.data = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                st.session_state.data = pd.read_excel(uploaded_file)
            st.success(f"File đã được tải lên: {uploaded_file.name}")
            st.write("### Xem dữ liệu:")
            st.dataframe(st.session_state.data)
            df = st.session_state.data.copy()  # Tạo bản copy rõ ràng

            # Chuyển đổi InvoiceDate một lần
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

            # Tạo 5 cột mới
            df['Total_Cost'] = df['Quantity'] * df['UnitPrice']
            df['InvoiceYear'] = df['InvoiceDate'].dt.year
            df['InvoiceMonth'] = df['InvoiceDate'].dt.month
            df['InvoiceDayName'] = df['InvoiceDate'].dt.day_name()
            df['InvoiceHour'] = df['InvoiceDate'].dt.hour
            
            # THÊM CỘT SEASON DỰA VÀO INVOICEMONTH
            def classify_season(month):
                if month in [12, 1, 2]:
                    return 'Winter'
                elif month in [3, 4, 5]:
                    return 'Spring'
                elif month in [6, 7, 8]:
                    return 'Summer'
                elif month in [9, 10, 11]:
                    return 'Fall'
                else:
                    return 'Unknown'
            
            df['Season'] = df['InvoiceMonth'].apply(classify_season)
            
            # Cập nhật session state
            st.session_state.data = df
            
            # Hiển thị thông báo thành công
            st.success("Đã thêm cột Season vào dữ liệu!")
            
            # Hiển thị phân bố theo mùa
            st.write("### Phân bố dữ liệu theo mùa:")
            season_counts = df['Season'].value_counts()
            st.write(season_counts)
            
            
            
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}. Vui lòng kiểm tra định dạng hoặc nội dung file.")