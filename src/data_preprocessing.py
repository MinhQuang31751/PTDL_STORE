import pandas as pd
import streamlit as st

def preprocess_data(df):
    """
    Xử lý và tạo các cột mới từ dữ liệu gốc
    """
    # Tạo bản copy để không thay đổi dữ liệu gốc
    processed_df = df.copy()

    # Chuyển đổi cột Date thành datetime
    if 'Date' in processed_df.columns:
        processed_df['Date'] = pd.to_datetime(processed_df['Date'])

        # Tạo các cột từ Date
        processed_df['InvoiceYear'] = processed_df['Date'].dt.year
        processed_df['InvoiceMonth'] = processed_df['Date'].dt.month
        processed_df['InvoiceDayName'] = processed_df['Date'].dt.day_name()

    # Xử lý cột TimeOfDay để tạo InvoiceHour
    if 'TimeOfDay' in processed_df.columns:
        # TimeOfDay có format "13:24:15", lấy phần giờ
        processed_df['InvoiceHour'] = pd.to_datetime(processed_df['TimeOfDay'], format='%H:%M:%S').dt.hour

    return processed_df

def get_processed_data():
    """
    Lấy dữ liệu đã được xử lý từ session state
    """
    if 'data' not in st.session_state or st.session_state.data is None:
        return None

    # Kiểm tra xem dữ liệu đã được xử lý chưa
    if 'InvoiceYear' not in st.session_state.data.columns:
        # Xử lý dữ liệu và lưu lại
        st.session_state.data = preprocess_data(st.session_state.data)

    return st.session_state.data
