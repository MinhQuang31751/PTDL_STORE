import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from streamlit_option_menu import option_menu

# Hàm xử lý dữ liệu
def process_data():
    # Kiểm tra dữ liệu đã tải
    if 'data' not in st.session_state or st.session_state.data is None:
        st.warning("Vui lòng tải lên file dữ liệu ở trang 'Dữ Liệu' trước khi xử lý.")
        return

    # Tạo menu tùy chọn
    selected = option_menu(
        menu_title=None,
        options=["Tiền xử lý Dữ liệu", "Tách và Làm sạch cột Product", "Liệt kê các sản phẩm", "Mã hóa và Tách cột"],
        icons=["gear", "scissors", "list", "code"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    # Xử lý theo lựa chọn
    if selected == "Tiền xử lý Dữ liệu":
        st.title("Tiền xử lý Dữ liệu")
        st.dataframe(st.session_state.data)

        # Kiểm tra và thống kê giá trị null
        null_counts = st.session_state.data.isnull().sum()
        if null_counts.sum() == 0:
            st.success("Không có giá trị null trong dữ liệu.")
        else:
            st.write("**Số lượng giá trị null theo cột:**")
            st.dataframe(null_counts[null_counts > 0].to_frame(name='Số lượng null'))
            null_percentage = (st.session_state.data.isnull().mean() * 100).round(2)
            st.write("**Tỷ lệ phần trăm giá trị null theo cột:**")
            st.dataframe(null_percentage[null_percentage > 0].to_frame(name='Tỷ lệ null (%)'))

            # Tùy chọn xử lý null
            action = st.selectbox("Chọn phương pháp xử lý:", ["Không xử lý", "Xóa hàng có null", "Điền giá trị trung bình"])
            if action == "Xóa hàng có null":
                cleaned_data = st.session_state.data.dropna()
                st.session_state.data = cleaned_data
                st.success(f"Đã xóa {len(st.session_state.data) - len(cleaned_data)} hàng có giá trị null.")
                st.dataframe(st.session_state.data)
            elif action == "Điền giá trị trung bình":
                numeric_columns = st.session_state.data.select_dtypes(include=['int64', 'float64']).columns
                if not numeric_columns.empty:
                    cleaned_data = st.session_state.data.copy()
                    for col in numeric_columns:
                        if cleaned_data[col].isnull().sum() > 0:
                            cleaned_data[col] = cleaned_data[col].fillna(cleaned_data[col].mean())
                    st.session_state.data = cleaned_data
                    st.success("Đã điền giá trị trung bình cho các cột số.")
                    st.dataframe(st.session_state.data)
                else:
                    st.error("Không có cột số để điền giá trị trung bình.")

    elif selected == "Tách và Làm sạch cột Product":
        st.title("Tách và Làm sạch cột Product")
        cleaned_data = st.session_state.data.copy()

        if 'Product' in cleaned_data.columns:
            def split_and_clean_products(text):
                if pd.isna(text):
                    return []
                text = text.replace('[', '').replace(']', '').replace("'", '').replace(',', '').strip()
                products = [p.strip() for p in text.split() if p.strip()]
                return products

            cleaned_data['Temp_Products'] = cleaned_data['Product'].apply(split_and_clean_products)
            max_products = cleaned_data['Temp_Products'].str.len().max()
            for i in range(max_products):
                cleaned_data[f'Product_{i+1}'] = cleaned_data['Temp_Products'].apply(lambda x: x[i] if i < len(x) else None)
            cleaned_data = cleaned_data.drop(columns=['Temp_Products', 'Product'])
            st.session_state.data = cleaned_data
            st.success("Đã tách cột 'Product' thành các cột riêng lẻ và loại bỏ dấu [ ], ', ,.")
            st.dataframe(st.session_state.data)
        else:
            st.error("Dữ liệu không chứa cột 'Product' để tách và làm sạch.")

    elif selected == "Liệt kê các sản phẩm":
        st.title("Liệt kê các sản phẩm")
        if any(col.startswith('Product_') for col in st.session_state.data.columns):
            product_columns = [col for col in st.session_state.data.columns if col.startswith('Product_')]
            all_products = st.session_state.data[product_columns].values.flatten()
            unique_products = sorted(list(set(p for p in all_products if p is not None and p.strip() and p.lower() != 'and')))
            
            with st.container(height=300):  # Hộp cuộn đơn giản
                for product in unique_products:
                    st.write(f"- {product}")

            if st.button("Lưu danh sách sản phẩm ra file"):
                output_df = pd.DataFrame({'Danh_sach_san_pham': unique_products})
                output_df.to_csv('product_list.csv', index=False, encoding='utf-8-sig')
                st.success("Danh sách sản phẩm đã được lưu vào 'product_list.csv'.")
        else:
            st.error("Không tìm thấy cột 'Product_' nào để liệt kê.")

    elif selected == "Mã hóa và Tách cột":
        st.title("Mã hóa và Tách cột")
        cleaned_data = st.session_state.data.copy()

        # Tách cột Date thành Year và Month (nếu có, nhưng không thấy trong dữ liệu)
        if 'Date' in cleaned_data.columns:
            cleaned_data['Date'] = pd.to_datetime(cleaned_data['Date'], errors='coerce')
            cleaned_data['Year'] = cleaned_data['Date'].dt.year
            cleaned_data['Month'] = cleaned_data['Date'].dt.month
            st.success("Đã tách cột 'Date' thành 'Year' và 'Month'.")
        else:
            st.warning("Dữ liệu không chứa cột 'Date' để tách.")

        # Mã hóa TimeOfDay và tách cột giờ
        if 'TimeOfDay' in cleaned_data.columns:
            # Chuyển đổi cột TimeOfDay thành định dạng thời gian
            cleaned_data['TimeOfDay'] = pd.to_datetime(cleaned_data['TimeOfDay'], format='%H:%M:%S', errors='coerce').dt.time
            
            # Tách cột giờ
            cleaned_data['Hour'] = pd.to_datetime(cleaned_data['TimeOfDay'], format='%H:%M:%S', errors='coerce').dt.hour
            
            # Hàm phân loại thời gian
            def classify_time(time_obj):
                if pd.isna(time_obj):
                    return None
                hour = time_obj.hour
                if 6 <= hour < 12:
                    return 'Morning'
                elif 12 <= hour < 18:
                    return 'Afternoon'
                else:
                    return 'Evening'

            # Áp dụng phân loại
            cleaned_data['TimeOfDay_Category'] = cleaned_data['TimeOfDay'].apply(classify_time)

            # Mã hóa thành số
            time_mapping = {'Morning': 1, 'Afternoon': 2, 'Evening': 3}
            cleaned_data['TimeOfDay_Encoded'] = cleaned_data['TimeOfDay_Category'].map(time_mapping).fillna(-1)

            # Xóa cột tạm nếu không cần
            cleaned_data = cleaned_data.drop(columns=['TimeOfDay_Category'], errors='ignore')

            st.success("Đã mã hóa cột 'TimeOfDay' thành số dựa trên khoảng thời gian (Morning: 1, Afternoon: 2, Evening: 3, không hợp lệ: -1) và tách cột 'Hour'.")
            st.write("Dữ liệu cột TimeOfDay sau khi mã hóa và tách giờ:")
            st.dataframe(cleaned_data[['TimeOfDay', 'Hour', 'TimeOfDay_Encoded']])
        else:
            st.error("Dữ liệu không chứa cột 'TimeOfDay' để mã hóa.")

        # Mã hóa PaymentType (thay vì Payment_Method, vì dữ liệu dùng Payment_Method)
        if 'Payment_Method' in cleaned_data.columns:
            payment_mapping = {'Cash': 0, 'Mobile Payment': 1, 'Credit Card': 2, 'Debit Card': 3}
            cleaned_data['Payment_Method_Encoded'] = cleaned_data['Payment_Method'].map(payment_mapping).fillna(-1)
            st.success("Đã mã hóa cột 'Payment_Method' thành số (giá trị không khớp = -1).")
        else:
            st.error("Dữ liệu không chứa cột 'Payment_Method' để mã hóa.")

        # Không có cột DayOfWeek trong dữ liệu, nên bỏ qua
        # if 'DayOfWeek' in cleaned_data.columns:
        #     day_mapping = {'Sunday': 1, 'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 'Thursday': 5, 'Friday': 6, 'Saturday': 7}
        #     cleaned_data['DayOfWeek'] = cleaned_data['DayOfWeek'].map(day_mapping).fillna(-1)
        #     st.success("Đã mã hóa cột 'DayOfWeek' thành số (giá trị không khớp = -1).")
        # else:
        #     st.error("Dữ liệu không chứa cột 'DayOfWeek' để mã hóa.")

        st.session_state.data = cleaned_data
        st.dataframe(st.session_state.data)

if __name__ == "__main__":
    process_data()