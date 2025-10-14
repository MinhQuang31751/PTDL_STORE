import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

try:
    from scipy.stats import chi2_contingency
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

def create_customer_payment_correlation_heatmap(df: pd.DataFrame):
    """Enhanced correlation heatmap between customer categories and payment methods"""
    # Create contingency table
    contingency = pd.crosstab(df['Customer_Category'], df['Payment_Method'])

    # Calculate percentages
    percentages = contingency.div(contingency.sum(axis=1), axis=0) * 100

    fig = px.imshow(
        percentages.values,
        labels=dict(x="Phương thức Thanh toán", y="Nhóm Khách hàng", color="Tỷ lệ (%)"),
        x=percentages.columns,
        y=percentages.index,
        color_continuous_scale='RdYlBu_r',
        title='Ma trận Tương quan: Nhóm KH vs Phương thức TT (%)'
    )

    # Add text annotations
    for i, row in enumerate(percentages.index):
        for j, col in enumerate(percentages.columns):
            fig.add_annotation(
                x=j, y=i,
                text=f'{percentages.iloc[i, j]:.1f}%',
                showarrow=False,
                font=dict(color="white" if percentages.iloc[i, j] > 50 else "black")
            )

    fig.update_layout(height=500)
    return fig

def create_customer_payment_statistical_analysis(df: pd.DataFrame):
    """Statistical analysis of customer-payment relationship"""
    contingency = pd.crosstab(df['Customer_Category'], df['Payment_Method'])

    if SCIPY_AVAILABLE:
        # Chi-square test
        chi2, p_value, dof, expected = chi2_contingency(contingency)

        # Calculate residuals (standardized)
        residuals = (contingency - expected) / np.sqrt(expected)
    else:
        # Fallback: use simple percentage differences
        expected = contingency.sum(axis=1).values[:, np.newaxis] * contingency.sum(axis=0).values / contingency.sum().sum()
        residuals = (contingency - expected) / np.sqrt(expected + 1e-8)  # Add small value to avoid division by zero
        chi2, p_value = 0, 1

    fig = px.imshow(
        residuals.values,
        labels=dict(x="Phương thức Thanh toán", y="Nhóm Khách hàng", color="Residual"),
        x=residuals.columns,
        y=residuals.index,
        color_continuous_scale='RdBu',
        title=f'Phân tích Residual (Chi² = {chi2:.2f}, p = {p_value:.4f})'
    )

    # Add statistical interpretation
    fig.add_annotation(
        text=f"Chi² Test: {'Có mối quan hệ' if p_value < 0.05 else 'Không có mối quan hệ'} (p = {p_value:.4f})",
        xref="paper", yref="paper",
        x=0.5, y=1.1, showarrow=False,
        font=dict(size=12, color="red" if p_value < 0.05 else "green")
    )

    fig.update_layout(height=500)
    return fig

def create_customer_payment_spending_patterns(df: pd.DataFrame):
    """Advanced spending pattern analysis"""
    spending_patterns = df.groupby(['Customer_Category', 'Payment_Method']).agg({
        'Total_Cost': ['mean', 'std', 'count'],
        'Quantity': ['mean']
    }).round(2)

    spending_patterns.columns = ['Avg_Spending', 'Std_Spending', 'Transaction_Count', 'Avg_Items']
    spending_patterns = spending_patterns.reset_index()

    # Create bubble chart
    fig = px.scatter(
        spending_patterns,
        x='Avg_Spending',
        y='Avg_Items',
        size='Transaction_Count',
        color='Customer_Category',
        symbol='Payment_Method',
        title='Mô hình Chi tiêu: Nhóm KH vs Phương thức TT',
        hover_data=['Std_Spending'],
        size_max=60
    )

    fig.update_layout(
        xaxis_title="Chi tiêu Trung bình (VND)",
        yaxis_title="Số sản phẩm Trung bình",
        height=600
    )
    return fig

def create_customer_payment_loyalty_matrix(df: pd.DataFrame):
    """Matrix showing member vs non-member patterns"""
    loyalty_matrix = df.groupby(['Customer_Category', 'Payment_Method', 'Member']).size().reset_index(name='Count')

    fig = px.sunburst(
        loyalty_matrix,
        path=['Customer_Category', 'Payment_Method', 'Member'],
        values='Count',
        title='Cây Phân tích: Nhóm KH → Phương thức TT → Thành viên'
    )

    fig.update_layout(height=600)
    return fig

def create_customer_payment_seasonal_trends(df: pd.DataFrame):
    """Seasonal trends analysis for customer-payment combinations"""
    seasonal_data = df.groupby(['Season', 'Customer_Category', 'Payment_Method']).size().reset_index(name='Count')

    fig = px.parallel_categories(
        seasonal_data,
        dimensions=['Season', 'Customer_Category', 'Payment_Method'],
        color='Count',
        color_continuous_scale='Viridis',
        title='Xu hướng Theo mùa: Mùa → Nhóm KH → Phương thức TT'
    )

    fig.update_layout(height=600)
    return fig

def create_customer_payment_promotion_response(df: pd.DataFrame):
    """How different customer-payment combinations respond to promotions"""
    promo_response = df.groupby(['Customer_Category', 'Payment_Method', 'Promotion']).agg({
        'Total_Cost': ['mean', 'count']
    }).round(2)

    promo_response.columns = ['Avg_Spending', 'Transaction_Count']
    promo_response = promo_response.reset_index()

    # Filter out None promotions for cleaner visualization
    promo_response = promo_response[promo_response['Promotion'] != 'None']

    fig = px.treemap(
        promo_response,
        path=['Promotion', 'Customer_Category', 'Payment_Method'],
        values='Transaction_Count',
        color='Avg_Spending',
        color_continuous_scale='RdYlGn',
        title='Phản hồi Khuyến mãi: Chương trình → Nhóm KH → Phương thức TT'
    )

    fig.update_layout(height=600)
    return fig

def create_customer_payment_comprehensive_dashboard(df: pd.DataFrame):
    """Comprehensive dashboard combining multiple insights"""

    # Calculate key metrics
    total_customers = len(df)
    avg_spending = df['Total_Cost'].mean()

    # Customer distribution
    customer_dist = df['Customer_Category'].value_counts()
    payment_dist = df['Payment_Method'].value_counts()

    # Cross-tabulation
    cross_tab = pd.crosstab(df['Customer_Category'], df['Payment_Method'], normalize='columns') * 100

    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=[
            'Phân bố Khách hàng',
            'Phân bố Thanh toán',
            'Tỷ lệ KH/Thanh toán (%)',
            'Chi tiêu TB theo Nhóm',
            'Chi tiêu TB theo PT',
            'Tương quan Tổng quát'
        ],
        specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}, {"type": "scatter"}]]
    )

    # Customer distribution pie
    fig.add_trace(
        go.Pie(labels=customer_dist.index, values=customer_dist.values, name="Khách hàng"),
        row=1, col=1
    )

    # Payment distribution pie
    fig.add_trace(
        go.Pie(labels=payment_dist.index, values=payment_dist.values, name="Thanh toán"),
        row=1, col=2
    )

    # Cross-tabulation bar
    for payment in cross_tab.columns:
        fig.add_trace(
            go.Bar(x=cross_tab.index, y=cross_tab[payment], name=payment),
            row=1, col=3
        )

    # Average spending by customer category
    customer_spending = df.groupby('Customer_Category')['Total_Cost'].mean()
    fig.add_trace(
        go.Bar(x=customer_spending.index, y=customer_spending.values, name="Chi tiêu KH"),
        row=2, col=1
    )

    # Average spending by payment method
    payment_spending = df.groupby('Payment_Method')['Total_Cost'].mean()
    fig.add_trace(
        go.Bar(x=payment_spending.index, y=payment_spending.values, name="Chi tiêu PT"),
        row=2, col=2
    )

    # Correlation scatter
    combo_spending = df.groupby(['Customer_Category', 'Payment_Method']).agg({
        'Total_Cost': ['mean', 'count']
    }).reset_index()
    combo_spending.columns = ['Customer_Category', 'Payment_Method', 'Avg_Spending', 'Count']

    fig.add_trace(
        go.Scatter(
            x=combo_spending['Avg_Spending'],
            y=combo_spending['Count'],
            mode='markers+text',
            text=[f"{row['Customer_Category'][:10]}<br>{row['Payment_Method'][:10]}"
                  for _, row in combo_spending.iterrows()],
            textposition='top center',
            marker=dict(size=10, opacity=0.7),
            name="Tương quan"
        ),
        row=2, col=3
    )

    fig.update_layout(
        title=f'Dashboard Tổng quan: {total_customers:,} giao dịch - Chi tiêu TB: {avg_spending:,.0f} VND',
        height=800,
        showlegend=False
    )

    return fig
