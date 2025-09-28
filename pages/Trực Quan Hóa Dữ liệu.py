import streamlit as st
from streamlit_option_menu import option_menu

def create_sidebar_content():
    with st.sidebar:
        st.title("Menu Chính")
        # Nạp file CSS với mã hóa UTF-8
        with open("static/styles.css", encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        # Tạo option menu
        selected_option = option_menu(
            menu_title=None,
            options=[
                "Doanh thu theo từng năm",
                "Doanh thu theo tháng",
                "Doanh thu 5 tháng cao nhất",
                "Thị phần các nhà bán lẻ",
                "Tổng doanh số theo sản phẩm và nhà bán lẻ",
                "Top sản phẩm bán chạy nhất",
                "Top thành phố bán chạy nhất",
                "Top phương pháp bán chạy nhất"
            ],
            icons=["calendar", "calendar", "bar-chart", "pie-chart", "list", "trophy", "map", "credit-card"],
            menu_icon="cast",
            default_index=0
        )
        st.markdown("---")

    # Trả về dictionary dựa trên lựa chọn
    options = {
        "doanh_thu_nam": selected_option == "Doanh thu theo từng năm",
        "doanh_thu_thang": selected_option == "Doanh thu theo tháng",
        "doanh_thu_5thang": selected_option == "Doanh thu 5 tháng cao nhất",
        "thi_phan": selected_option == "Thị phần các nhà bán lẻ",
        "tong_doanh_so": selected_option == "Tổng doanh số theo sản phẩm và nhà bán lẻ",
        "top_san_pham": selected_option == "Top sản phẩm bán chạy nhất",
        "top_thanh_pho": selected_option == "Top thành phố bán chạy nhất",
        "top_phuong_phap": selected_option == "Top phương pháp bán chạy nhất"
    }

    return options

# Gọi hàm và lấy options
options = create_sidebar_content()

# Hiển thị nội dung dựa trên lựa chọn (ví dụ)
st.title("Kết quả")
if options["doanh_thu_nam"]:
    st.write("Hiển thị doanh thu theo từng năm...")
elif options["doanh_thu_thang"]:
    st.write("Hiển thị doanh thu theo tháng...")
# Thêm các điều kiện khác tương tự