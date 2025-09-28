import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

from src.data_upload import upload_data
from src.danh_gia import show_overview
from src.data_processing import process_data

def main():
    # Thiết lập trang
    st.set_page_config(
        page_title="PTDL Store",
        page_icon="📊",
        layout="wide",
    )

    # Khởi tạo session state để lưu dữ liệu
    if 'data' not in st.session_state:
        st.session_state.data = None

    # Nạp file CSS
    with open("static/styles.css", encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Thanh điều hướng bên trái với option_menu
    with st.sidebar:
        page = option_menu(
            "Menu chính",
            ["Dữ Liệu", "Đánh Giá Tổng Quan", "Tiền Xử Lý Dữ Liệu", "Khai thác dữ liệu", "Model dự đoán"],
            icons=["database", "bar-chart", "gear", "search", "cpu"],
            menu_icon="cast",
            default_index=0,
        )

    # MAIN CONTENT - Nội dung chính
    st.title("Circle K Sales Analysis Dashboard")

    # Gọi chức năng upload dữ liệu khi ở trang Dữ Liệu
    if page == "Dữ Liệu":
        upload_data()
    elif page == "Đánh Giá Tổng Quan":
        show_overview()
    elif page == "Tiền Xử Lý Dữ Liệu":  
        process_data()

if __name__ == "__main__":
    main()

    