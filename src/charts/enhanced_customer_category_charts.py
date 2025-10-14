import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_customer_category_donut_chart(df: pd.DataFrame):
    """Enhanced donut chart with better styling and percentages"""
    category_counts = df['Customer_Category'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=category_counts.index,
        values=category_counts.values,
        hole=0.4,
        textinfo='label+percent+value',
        textposition='auto',
        marker=dict(
            colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            line=dict(color='white', width=2)
        )
    )])

    fig.update_layout(
        title={
            'text': 'Phân bố Khách hàng theo Độ tuổi',
            'x': 0.5,
            'font': {'size': 16, 'family': 'Arial Black'}
        },
        showlegend=True,
        height=500,
        annotations=[dict(text=f'Tổng<br>{len(df):,}<br>khách hàng',
                         x=0.5, y=0.5, font_size=14, showarrow=False)]
    )
    return fig

def create_customer_spending_box_plot(df: pd.DataFrame):
    """Box plot showing spending distribution by customer category"""
    fig = px.box(
        df,
        x='Customer_Category',
        y='Total_Cost',
        title='Phân bố Chi tiêu theo Nhóm Khách hàng',
        color='Customer_Category',
        points='outliers'
    )

    fig.update_layout(
        xaxis_title="Nhóm Khách hàng",
        yaxis_title="Tổng Chi tiêu (VND)",
        showlegend=False,
        height=500
    )

    fig.update_traces(marker_size=4)
    return fig

def create_customer_loyalty_analysis(df: pd.DataFrame):
    """Analysis of customer loyalty (Member vs Non-member) by category"""
    loyalty_data = df.groupby(['Customer_Category', 'Member']).size().reset_index(name='Count')
    loyalty_data['Percentage'] = loyalty_data.groupby('Customer_Category')['Count'].transform(lambda x: x / x.sum() * 100)

    fig = px.bar(
        loyalty_data,
        x='Customer_Category',
        y='Count',
        color='Member',
        title='Tỷ lệ Thành viên theo Nhóm Khách hàng',
        text='Percentage',
        color_discrete_map={'Yes': '#2ECC71', 'No': '#E74C3C'}
    )

    fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
    fig.update_layout(
        xaxis_title="Nhóm Khách hàng",
        yaxis_title="Số lượng Giao dịch",
        height=500
    )
    return fig

def create_customer_seasonal_heatmap(df: pd.DataFrame):
    """Heatmap showing customer category preferences by season"""
    heatmap_data = df.groupby(['Customer_Category', 'Season']).size().reset_index(name='Count')
    pivot_data = heatmap_data.pivot(index='Customer_Category', columns='Season', values='Count')

    fig = px.imshow(
        pivot_data.values,
        labels=dict(x="Mùa", y="Nhóm Khách hàng", color="Số giao dịch"),
        x=pivot_data.columns,
        y=pivot_data.index,
        color_continuous_scale='Blues',
        title='Mối quan hệ Nhóm Khách hàng - Mùa vụ'
    )

    fig.update_layout(height=500)
    return fig

def create_customer_average_metrics_radar(df: pd.DataFrame):
    """Radar chart comparing customer categories across multiple metrics"""
    metrics = df.groupby('Customer_Category').agg({
        'Total_Cost': 'mean',
        'Quantity': 'mean',
        'Member': lambda x: (x == 'Yes').mean() * 100  # Membership rate
    }).reset_index()

    # Normalize metrics for radar chart (0-100 scale)
    metrics['Avg_Spending_Norm'] = (metrics['Total_Cost'] / metrics['Total_Cost'].max()) * 100
    metrics['Avg_Items_Norm'] = (metrics['Quantity'] / metrics['Quantity'].max()) * 100
    metrics['Member_Rate'] = metrics['Member']

    fig = go.Figure()

    categories = ['Chi tiêu TB', 'Số SP TB', 'Tỷ lệ TV (%)']

    for _, row in metrics.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row['Avg_Spending_Norm'], row['Avg_Items_Norm'], row['Member_Rate']],
            theta=categories,
            fill='toself',
            name=row['Customer_Category'],
            line=dict(width=2)
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        title='So sánh Đa chiều các Nhóm Khách hàng',
        height=500
    )
    return fig

def create_customer_promotion_response(df: pd.DataFrame):
    """Analysis of how different customer categories respond to promotions"""
    promo_data = df.groupby(['Customer_Category', 'Promotion']).agg({
        'Total_Cost': ['count', 'mean']
    }).round(2)

    promo_data.columns = ['Transaction_Count', 'Avg_Spending']
    promo_data = promo_data.reset_index()

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Số lượng Giao dịch', 'Chi tiêu Trung bình'],
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )

    # Transaction count
    for promo in promo_data['Promotion'].unique():
        if pd.notna(promo):  # Skip NaN values
            data = promo_data[promo_data['Promotion'] == promo]
            fig.add_trace(
                go.Bar(x=data['Customer_Category'], y=data['Transaction_Count'],
                       name=f'{promo} - Count', legendgroup=promo),
                row=1, col=1
            )

    # Average spending
    for promo in promo_data['Promotion'].unique():
        if pd.notna(promo):
            data = promo_data[promo_data['Promotion'] == promo]
            fig.add_trace(
                go.Bar(x=data['Customer_Category'], y=data['Avg_Spending'],
                       name=f'{promo} - Avg', legendgroup=promo, showlegend=False),
                row=1, col=2
            )

    fig.update_layout(
        title='Phản hồi của Khách hàng với các Chương trình Khuyến mãi',
        height=500
    )
    return fig
