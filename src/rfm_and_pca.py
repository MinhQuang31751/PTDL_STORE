import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main(df):
    st.title("Phân tích Nhóm Khách hàng với RFM và PCA")

    df_local = df.copy()

    # Xử lý dữ liệu: Lọc Quantity > 0, loại bỏ null CustomerID
    df_clean = df_local[df_local['Quantity'] > 0].dropna(subset=['CustomerID']).copy()

    # Tính RFM
    current_date = df_clean['InvoiceDate'].max() + timedelta(days=1)
    rfm = df_clean.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (current_date - x.max()).days,  # Recency (thấp = tốt)
        'InvoiceNo': 'nunique',  # Frequency
        'TotalPrice': 'sum'  # Monetary
    }).round(2)
    rfm.columns = ['Recency', 'Frequency', 'Monetary']

    # Phân loại RFM - Sử dụng rank percentile để tránh lỗi qcut với dữ liệu nhỏ/duplicate
    n_customers = len(rfm)
    if n_customers > 0:
        # Tính rank percentile (0-1)
        rfm['R_Percentile'] = rfm['Recency'].rank(pct=True, ascending=False)  # Low recency = high percentile
        rfm['F_Percentile'] = rfm['Frequency'].rank(pct=True, ascending=True)
        rfm['M_Percentile'] = rfm['Monetary'].rank(pct=True, ascending=True)
        
        # Chuyển thành score 1-5
        rfm['R_Score'] = (rfm['R_Percentile'] * 5).round().clip(1, 5).astype(int)
        rfm['F_Score'] = (rfm['F_Percentile'] * 5).round().clip(1, 5).astype(int)
        rfm['M_Score'] = (rfm['M_Percentile'] * 5).round().clip(1, 5).astype(int)
        
        # Drop temp columns
        rfm = rfm.drop(['R_Percentile', 'F_Percentile', 'M_Percentile'], axis=1)
    else:
        st.warning("Không có dữ liệu khách hàng hợp lệ!")
        return

    rfm['RFM_Score'] = (rfm['R_Score'].astype(str) + 
                        rfm['F_Score'].astype(str) + 
                        rfm['M_Score'].astype(str))

    # Phân đoạn nhóm khách hàng
    def segment_rfm(rfm_score):
        try:
            r, f, m = map(int, rfm_score)
        except:
            return 'Average'  # Fallback nếu lỗi parse
        if r == 5 and f == 5 and m == 5: return 'Champions'
        elif r == 5: return 'Loyal Customers'
        elif r >= 4 and f >= 4: return 'Potential Loyalists'
        elif r < 3 and f < 3: return 'At Risk'
        elif r < 2 and f < 2: return "Can't Lose Them"
        elif r == 1 and f == 1: return 'Lost Customers'
        else: return 'Average'

    rfm['Segment'] = rfm['RFM_Score'].apply(segment_rfm)

    # Hiển thị bảng RFM và phân đoạn
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Bảng RFM")
        st.dataframe(rfm)
    with col2:
        st.subheader("Phân bố Nhóm Khách hàng")
        segment_counts = rfm['Segment'].value_counts()
        st.bar_chart(segment_counts)

    # PCA Visualization
    st.subheader("Biểu đồ PCA: Phân bố Nhóm Khách hàng")
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(rfm_scaled)

    pca_df = pd.DataFrame(pca_result, columns=['PCA1', 'PCA2'], index=rfm.index)
    pca_df['Segment'] = rfm['Segment']

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=pca_df, x='PCA1', y='PCA2', hue='Segment', palette='Set1', s=100, ax=ax)
    ax.set_title('Phân bố Nhóm Khách hàng trên Không gian PCA')
    ax.set_xlabel(f'PCA Component 1 (Giải thích {pca.explained_variance_ratio_[0]:.1%} variance)')
    ax.set_ylabel(f'PCA Component 2 (Giải thích {pca.explained_variance_ratio_[1]:.1%} variance)')
    st.pyplot(fig)

    # Thống kê chi tiết
    st.subheader("Thống kê RFM theo Nhóm")
    rfm_stats = rfm.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].agg(['mean', 'count']).round(2)
    st.dataframe(rfm_stats)

