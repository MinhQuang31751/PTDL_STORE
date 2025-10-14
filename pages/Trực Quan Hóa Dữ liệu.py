import streamlit as st
from streamlit_option_menu import option_menu

# Original charts
from src.charts.customer_category_charts import create_revenue_by_customer_category_bar_chart, create_customer_category_bar_chart
from src.charts.payment_method_charts import create_payment_method_bar_chart

# Enhanced charts
from src.charts.enhanced_customer_category_charts import (
    create_customer_category_donut_chart
)
from src.charts.enhanced_payment_method_charts import (
    create_payment_method_enhanced_pie,
)
from src.charts.customer_payment_relationship_charts import (
    create_customer_payment_comprehensive_dashboard
)

from src.time.timeofday_analysis import create_monthly_revenue_chart, display_revenue_stats
from src.time.hoursofday_analysis import create_hourly_revenue_chart, display_hourly_stats
from src.product.best_selling_products import top_product_analysis
from src.time.dayofweek_analysis import create_weekday_revenue_bar_chart, create_weekday_revenue_pie_chart
from src.data_preprocessing import get_processed_data


def create_sidebar_content():
    with st.sidebar:
        st.title("Menu Chính")
        # Tạo option menu
        selected_option = option_menu(
            menu_title=None,
            options=[
                "Phân tích theo TimeOfDay",
                "Phân tích theo Customer",
                "Phân tích theo Payment",
                "Phân tích Mối quan hệ KH-TT",
                "Phân tích theo Product",
                "Phân tích theo Member"
            ],
            icons=["clock", "person", "credit-card", "diagram-3", "box", "people"],
            menu_icon="cast",
            default_index=0
        )
        st.markdown("---")

    # Trả về dictionary dựa trên lựa chọn
    options = {
        "time_of_day": selected_option == "Phân tích theo TimeOfDay",
        "customer_category": selected_option == "Phân tích theo Customer",
        "payment": selected_option == "Phân tích theo Payment",
        "relationship": selected_option == "Phân tích Mối quan hệ KH-TT",
        "product": selected_option == "Phân tích theo Product",
        "member": selected_option == "Phân tích theo Member"
    }

    return selected_option, options

# Kiểm tra dữ liệu trong session state
if 'data' not in st.session_state or st.session_state.data is None:
    st.warning("Vui lòng tải dữ liệu lên ở trang 'Dữ Liệu' trước.")
    st.stop()

# Lấy dữ liệu đã được xử lý
df = get_processed_data()
if df is None:
    st.error("Không thể xử lý dữ liệu. Vui lòng kiểm tra lại file dữ liệu.")
    st.stop()

# Gọi hàm và lấy kết quả
selected_option, options = create_sidebar_content()

# Hiển thị nội dung dựa trên lựa chọn
st.title("Dashboard Phân Tích Bán Hàng")

# Hiển thị option đang được chọn
st.write(f"**Đang xem:** {selected_option}")

# Hiển thị nội dung tương ứng
if options["time_of_day"]:

    st.plotly_chart(create_monthly_revenue_chart(df), use_container_width=True)
    display_revenue_stats(df)

    st.plotly_chart(create_hourly_revenue_chart(df), use_container_width=True)
    display_hourly_stats(df)

    st.plotly_chart(create_weekday_revenue_bar_chart(df), use_container_width=True)
    st.plotly_chart(create_weekday_revenue_pie_chart(df), use_container_width=True)

elif options["customer_category"]:
    st.header("👥 Phân tích theo Khách hàng")

    # Create tabs for different analysis types
    # tab1, tab2, tab3, tab4 = st.tabs(["📊 Tổng quan", "💰 Chi tiêu", "🎯 Thành viên", "📈 Nâng cao"])

    # with tab1:
    # col1, col2 = st.columns(2)

    # with col1:
    st.plotly_chart(create_customer_category_donut_chart(df), use_container_width=True)
    # with col2:
    st.plotly_chart(create_customer_category_bar_chart(df), use_container_width=True)

    st.plotly_chart(create_revenue_by_customer_category_bar_chart(df), use_container_width=True)

    # with tab2:
    #     st.subheader("Phân tích Chi tiêu")
    #     st.plotly_chart(create_customer_spending_box_plot(df), use_container_width=True)

    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.plotly_chart(create_customer_seasonal_heatmap(df), use_container_width=True)
    #     with col2:
    #         st.plotly_chart(create_customer_average_metrics_radar(df), use_container_width=True)

    # with tab3:
    #     st.subheader("Phân tích Thành viên và Khuyến mãi")
    #     st.plotly_chart(create_customer_loyalty_analysis(df), use_container_width=True)
    #     st.plotly_chart(create_customer_promotion_response(df), use_container_width=True)

    # with tab4:
    #     st.subheader("Biểu đồ Kết hợp")
    #     st.plotly_chart(create_customer_payment_method_grouped_bar_chart(df), use_container_width=True)

elif options["payment"]:
    st.header("💳 Phân tích theo Phương thức Thanh toán")

    # Create tabs for different analysis types
    # tab1, tab2, tab3, tab4 = st.tabs(["📊 Tổng quan", "📈 Doanh thu", "🌍 Phân bố", "📋 Chi tiết"])

    # with tab1:
    # col1, col2 = st.columns(2)

    # with col1:
    st.plotly_chart(create_payment_method_enhanced_pie(df), use_container_width=True)
    # with col2:
    st.plotly_chart(create_payment_method_bar_chart(df), use_container_width=True)

    # with tab2:
    #     st.subheader("Phân tích Doanh thu")
    #     st.plotly_chart(create_payment_method_revenue_comparison(df), use_container_width=True)
    #     st.plotly_chart(create_payment_method_basket_analysis(df), use_container_width=True)

    # with tab3:
    #     st.subheader("Phân tích Phân bố")

    #     st.plotly_chart(create_payment_method_time_trends(df), use_container_width=True)
    #     st.plotly_chart(create_payment_method_city_analysis(df), use_container_width=True)

    # with tab4:
    #     st.subheader("Bảng Thống kê Chi tiết")
    #     st.plotly_chart(create_payment_method_advanced_metrics(df), use_container_width=True)

elif options["relationship"]:
    st.header("🔗 Phân tích Mối quan hệ Khách hàng - Phương thức Thanh toán")

    # Create tabs for relationship analysis
    # tab1, tab2, tab3, tab4 = st.tabs(["🎯 Dashboard Tổng quan", "📊 Tương quan", "💡 Insights", "🌟 Nâng cao"])

    # with tab1:
    # st.subheader("Dashboard Tổng hợp")
    st.plotly_chart(create_customer_payment_comprehensive_dashboard(df), use_container_width=True)

    # with tab2:
    #     st.subheader("Phân tích Tương quan")

    #     st.plotly_chart(create_customer_payment_correlation_heatmap(df), use_container_width=True)
    #     st.plotly_chart(create_customer_payment_statistical_analysis(df), use_container_width=True)
    #     st.plotly_chart(create_customer_payment_spending_patterns(df), use_container_width=True)

    # with tab3:
    #     st.subheader("Insights và Patterns")

    #     st.plotly_chart(create_customer_payment_loyalty_matrix(df), use_container_width=True)
    #     st.plotly_chart(create_customer_payment_seasonal_trends(df), use_container_width=True)

    # with tab4:
    #     st.subheader("Phân tích Khuyến mãi")
    #     st.plotly_chart(create_customer_payment_promotion_response(df), use_container_width=True)

elif options["product"]:
    st.header("📦 Phân tích theo Sản phẩm")
    st.write("Phân tích hiệu quả bán hàng theo danh mục sản phẩm...")
    top_product_analysis(df)

elif options["member"]:
    st.header("🛡️ Phân tích theo Thành viên")
    st.write("Phân tích hành vi mua hàng của khách hàng thành viên...")
