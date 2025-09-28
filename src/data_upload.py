import streamlit as st
import pandas as pd

def upload_data():
    st.write("Đây là trang để tải lên và xem dữ liệu.")
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
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}. Vui lòng kiểm tra định dạng hoặc nội dung file.")