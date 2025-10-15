import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
import importlib.util
import sys
import os
from src.data_upload import upload_data
from src.danh_gia import show_overview
from src.data_processing import process_data
# Bỏ from src.r import ... vì dùng load động
# Dòng này từ Stashed changes (của bạn)
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

def load_module_from_file(file_path, module_name):
    """Dynamically loads a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for module '{module_name}' at: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

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
            ["Dữ Liệu", "Tiền Xử Lý Dữ Liệu", "Đánh Giá Tổng Quan"],
            icons=["database", "gear", "bar-chart"],
            menu_icon="cast",
            default_index=0,
        )

    # MAIN CONTENT - Nội dung chính
    st.title("Circle K Sales Analysis Dashboard")

    # Gọi chức năng upload dữ liệu khi ở trang Dữ Liệu
    if page == "Dữ Liệu":
        upload_data()
        
    elif page == "Tiền Xử Lý Dữ Liệu":  
        process_data()
    
    elif page == "Đánh Giá Tổng Quan":
        show_overview()

    

if __name__ == "__main__":
    main()