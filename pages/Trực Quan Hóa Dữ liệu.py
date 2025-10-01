import streamlit as st
from streamlit_option_menu import option_menu

def create_sidebar_content():
    with st.sidebar:
        st.title("Menu Chính")
        # Tạo option menu
        selected_option = option_menu(
            menu_title=None,
            options=[
                "Phân tích theo TimeOfDay",
                "Phân tích theo Customer",
                "Phân tích theo Season",
                "Phân tích theo Payment",
                "Phân tích theo Product",
                "Phân tích theo Member"
            ],
            icons=["clock", "person", "sun", "credit-card", "box", "people"],
            menu_icon="cast",
            default_index=0
        )
        st.markdown("---")

    # Trả về dictionary dựa trên lựa chọn
    options = {
        "time_of_day": selected_option == "Phân tích theo TimeOfDay",
        "customer_category": selected_option == "Phân tích theo Customer",
        "season": selected_option == "Phân tích theo Season", 
        "payment": selected_option == "Phân tích theo Payment",
        "product": selected_option == "Phân tích theo Product",
        "member": selected_option == "Phân tích theo Member"
    }

    return selected_option, options

# Gọi hàm và lấy kết quả
selected_option, options = create_sidebar_content()

# Hiển thị nội dung dựa trên lựa chọn
st.title("Dashboard Phân Tích Bán Hàng")

# Hiển thị option đang được chọn
st.write(f"**Đang xem:** {selected_option}")

# Hiển thị nội dung tương ứng
if options["time_of_day"]:
    st.header("📊 Phân tích theo Thời gian trong ngày")
    st.write("Phân tích doanh thu và xu hướng mua hàng theo các khung giờ...")
    
elif options["customer_category"]:
    st.header("👥 Phân tích theo Phân khúc Khách hàng") 
    st.write("Phân tích hành vi mua hàng theo các nhóm khách hàng...")
    
elif options["season"]:
    st.header("🌤️ Phân tích theo Mùa")
    st.write("Phân tích doanh thu theo các mùa trong năm...")
    
elif options["payment"]:
    st.header("💳 Phân tích theo Phương thức Thanh toán")
    st.write("Phân tích xu hướng thanh toán và tỷ lệ sử dụng các phương thức...")
    
elif options["product"]:
    st.header("📦 Phân tích theo Sản phẩm")
    st.write("Phân tích hiệu quả bán hàng theo danh mục sản phẩm...")

elif options["member"]:
    st.header("🛡️ Phân tích theo Thành viên")
    st.write("Phân tích hành vi mua hàng của khách hàng thành viên...")

