import streamlit as st
from streamlit_option_menu import option_menu

# Import the chart functions
from src.charts.customer_category_charts import create_customer_category_pie_chart, create_customer_category_bar_chart
from src.charts.payment_method_charts import create_payment_method_pie_chart, create_payment_method_bar_chart

def show_visualization_page():
    """
    Displays the data visualization page with a sub-menu for detailed analysis.
    """
    # Check if data exists in session state
    if 'data' not in st.session_state or st.session_state.data is None:
        st.warning("Vui lòng tải dữ liệu lên ở trang 'Dữ Liệu' trước.")
        st.stop()

    df = st.session_state.data

    # The sidebar logic provided by the user, now as a sub-menu
    with st.sidebar:
        selected_option = option_menu(
            menu_title="Phân tích chi tiết",
            options=[
                "Phân tích theo Customer",
                "Phân tích theo Payment",
                "Phân tích theo TimeOfDay",
                "Phân tích theo Season",
                "Phân tích theo Product",
                "Phân tích theo Member"
            ],
            icons=["person", "credit-card", "clock", "sun", "box", "people"],
            menu_icon="bar-chart-line-fill", # A more fitting icon
            default_index=0
        )

    # Main title for the page
    st.title("Trực Quan Hóa và Khai Thác Dữ Liệu")

    # Display content based on selection
    if selected_option == "Phân tích theo Customer":
        st.header("👥 Phân tích theo Phân khúc Khách hàng")

        # Display the charts for Customer Category
        st.plotly_chart(create_customer_category_pie_chart(df), use_container_width=True)
        st.plotly_chart(create_customer_category_bar_chart(df), use_container_width=True)

    elif selected_option == "Phân tích theo Payment":
        st.header("💳 Phân tích theo Phương thức Thanh toán")

        # Display the charts for Payment Method
        st.plotly_chart(create_payment_method_pie_chart(df), use_container_width=True)
        st.plotly_chart(create_payment_method_bar_chart(df), use_container_width=True)

    elif selected_option == "Phân tích theo TimeOfDay":
        st.header("📊 Phân tích theo Thời gian trong ngày")
        st.write("Nội dung phân tích theo thời gian trong ngày sẽ được hiển thị ở đây.")

    elif selected_option == "Phân tích theo Season":
        st.header("🌤️ Phân tích theo Mùa")
        st.write("Nội dung phân tích theo mùa sẽ được hiển thị ở đây.")

    elif selected_option == "Phân tích theo Product":
        st.header("📦 Phân tích theo Sản phẩm")
        st.write("Nội dung phân tích theo sản phẩm sẽ được hiển thị ở đây.")

    elif selected_option == "Phân tích theo Member":
        st.header("🛡️ Phân tích theo Thành viên")
        st.write("Nội dung phân tích theo thành viên sẽ được hiển thị ở đây.")
