import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập trang
st.set_page_config(page_title="Top 10 Sản Phẩm Bán Chạy", layout="wide")

# Tiêu đề
st.title("10 SẢN PHẨM BÁN CHẠY NHẤT")
st.subheader("(Dựa trên tổng doanh thu)")

def top_product_analysis(df):
    # Dictionary ánh xạ tên sản phẩm (bạn cần cập nhật đầy đủ)
    product_translation_revenue = {
        'WHITE HANGING HEART T-LIGHT HOLDER': {'name': 'Giá nén treo hình trái tim trắng', 'group': 'Trang trí'},
        'JUMBO BAG RETROSPOT': {'name': 'Túi jumbo hoa tiết retro đồ', 'group': 'Túi & Bao bì'},
        'ASSORTED COLOUR BIRD ORNAMENT': {'name': 'Vật trang trí chim nhiều màu', 'group': 'Trang trí'},
        'PARTY BUNTING': {'name': 'Có trang trí tiệc', 'group': 'Trang trí tiệc'},
        'POSTAGE': {'name': 'Phí vận chuyển', 'group': 'Khác'},
        'RUSTIC WOODEN SLEIGH': {'name': 'Đèn ngủ hình thô', 'group': 'Đồ gia dụng'},
        'RED HOTTIE WATER BOTTLE': {'name': 'Đèn trang trí hình ớt', 'group': 'Đồ gia dụng'},
        'PAPER CHAIN KIT 50S CHRISTMAS': {'name': 'PAPER CHAIN KIT 50\'S CHRISTMAS', 'group': 'Trang trí tiệc'},
        'PICNIC BASKET WICKER 60 PIECES': {'name': 'Gió dã ngoại máy 60 món', 'group': 'Khác'},
        'REGENCY CAKESTAND 3 TIER': {'name': 'Giá bánh 3 tăng Regency', 'group': 'Đồ gia dụng'}
    }

    # Lấy top 10 sản phẩm theo doanh thu
    top_selling_revenue = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)

    # Tạo DataFrame mới với tên tiếng Việt và nhóm
    top_revenue_df = pd.DataFrame({
        'English_Name': top_selling_revenue.index,
        'Total_Revenue': top_selling_revenue.values
    })

    # Hàm ánh xạ thông minh để xử lý khoảng trắng
    def get_product_info_revenue(product_name):
        # Chuẩn hóa tên sản phẩm (loại bỏ khoảng trắng thừa)
        normalized_name = product_name.strip()

        # Thử tìm trong dictionary với tên đã chuẩn hóa
        if normalized_name in product_translation_revenue:
            return product_translation_revenue[normalized_name]
        else:
            # Nếu không tìm thấy, trả về thông tin mặc định
            return {'name': normalized_name, 'group': 'Khác'}

    # Thêm thông tin dịch và nhóm với xử lý lỗi
    top_revenue_df['Vietnamese_Name'] = top_revenue_df['English_Name'].map(lambda x: get_product_info_revenue(x)['name'])
    top_revenue_df['Product_Group'] = top_revenue_df['English_Name'].map(lambda x: get_product_info_revenue(x)['group'])

    # Lọc bỏ POSTAGE (Phí vận chuyển) khỏi kết quả
    top_revenue_df = top_revenue_df[top_revenue_df['Vietnamese_Name'] != 'Phí vận chuyển']

    # Kiểm tra xem có sản phẩm nào không được ánh xạ không
    unmapped_products = top_revenue_df[top_revenue_df['Product_Group'] == 'Khác']
    if len(unmapped_products) > 0:
        st.warning("⚠️ Các sản phẩm chưa được ánh xạ:")
        for product in unmapped_products['English_Name']:
            st.write(f"   - '{product}'")

    # Tạo palette màu theo nhóm (đã bỏ Dịch vụ)
    group_colors_revenue = {
        'Đồ gia dụng': '#1f77b4',
        'Trang trí': '#ff7f0e',
        'Túi & Bao bì': '#2ca02c',
        'Trang trí tiệc': '#d62728',
        'Khác': '#7f7f7f'
    }

    # Vẽ biểu đồ
    fig, ax = plt.subplots(figsize=(14, 8))

    # Sắp xếp DataFrame theo doanh thu (tăng dần để hiển thị đúng trên biểu đồ ngang)
    top_revenue_df_sorted = top_revenue_df.sort_values('Total_Revenue', ascending=True)

    # Tạo biểu đồ
    bars = ax.barh(
        top_revenue_df_sorted['Vietnamese_Name'],
        top_revenue_df_sorted['Total_Revenue'],
        color=[group_colors_revenue[group] for group in top_revenue_df_sorted['Product_Group']]
    )

    ax.set_title('10 SẢN PHẨM BÁN CHẠY NHẤT\n(Dựa trên tổng doanh thu)', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Tổng Doanh thu (£)', fontsize=12, fontweight='bold')
    ax.set_ylabel('')

    # Thêm giá trị lên mỗi cột
    for i, (value, group) in enumerate(zip(top_revenue_df_sorted['Total_Revenue'], top_revenue_df_sorted['Product_Group'])):
        ax.text(value + 1000, i, f'£{value:,.0f}', va='center', fontsize=10, fontweight='bold')

    # Tạo legend
    legend_patches = [plt.Rectangle((0,0),1,1, color=color, label=group) 
                    for group, color in group_colors_revenue.items()]
    ax.legend(handles=legend_patches, title='Nhóm sản phẩm', title_fontsize=12, fontsize=11, loc='lower right')

    # Loại bỏ đường viền
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    plt.tight_layout()

    # Hiển thị biểu đồ trong Streamlit
    st.pyplot(fig)