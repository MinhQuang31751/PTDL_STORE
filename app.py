import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
import importlib.util
import sys

from src.data_upload import upload_data
from src.danh_gia import show_overview
from src.data_processing import process_data

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
    elif page == "Khai thác dữ liệu":
        try:
            # Tải động module trực quan hóa
            viz_module = load_module_from_file("src/4_Truc_quan_haa.py", "visualization_module")
            # Gọi hàm chính từ module đã tải
            viz_module.show_visualization_page()
        except ImportError as e:
            st.error(f"Lỗi khi tải trang khai thác dữ liệu: {e}")
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn: {e}")

if __name__ == "__main__":
    main()

    