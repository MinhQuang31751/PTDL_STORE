import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_payment_method_enhanced_pie(df: pd.DataFrame):
    """Enhanced pie chart with custom colors and better formatting"""
    payment_counts = df['Payment_Method'].value_counts()

    colors = {
        'Cash': '#27AE60',
        'Credit Card': '#3498DB',
        'Debit Card': '#E74C3C',
        'Mobile Payment': '#F39C12'
    }

    fig = go.Figure(data=[go.Pie(
        labels=payment_counts.index,
        values=payment_counts.values,
        textinfo='label+percent+value',
        textposition='auto',
        marker=dict(
            colors=[colors.get(method, '#BDC3C7') for method in payment_counts.index],
            line=dict(color='white', width=2)
        ),
        pull=[0.1 if method == payment_counts.index[0] else 0 for method in payment_counts.index]
    )])

    fig.update_layout(
        title={
            'text': 'Phân bố Phương thức Thanh toán',
            'x': 0.5,
            'font': {'size': 16, 'family': 'Arial Black'}
        },
        height=500,
        showlegend=True
    )
    return fig

def create_payment_method_revenue_comparison(df: pd.DataFrame):
    """Enhanced comparison of transaction count vs revenue by payment method"""
    payment_stats = df.groupby('Payment_Method').agg({
        'Total_Cost': ['count', 'sum', 'mean']
    }).round(2)

    payment_stats.columns = ['Transaction_Count', 'Total_Revenue', 'Avg_Transaction']
    payment_stats = payment_stats.reset_index()

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'Số lượng Giao dịch',
            'Tổng Doanh thu',
            'Giao dịch Trung bình',
            'Hiệu suất (Doanh thu/Giao dịch)'
        ],
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )

    colors = ['#27AE60', '#3498DB', '#E74C3C', '#F39C12']

    # Transaction count
    fig.add_trace(
        go.Bar(x=payment_stats['Payment_Method'],
               y=payment_stats['Transaction_Count'],
               marker_color=colors,
               name='Số GD'),
        row=1, col=1
    )

    # Total revenue
    fig.add_trace(
        go.Bar(x=payment_stats['Payment_Method'],
               y=payment_stats['Total_Revenue'],
               marker_color=colors,
               name='Tổng DT'),
        row=1, col=2
    )

    # Average transaction
    fig.add_trace(
        go.Bar(x=payment_stats['Payment_Method'],
               y=payment_stats['Avg_Transaction'],
               marker_color=colors,
               name='GD TB'),
        row=2, col=1
    )

    # Efficiency scatter
    fig.add_trace(
        go.Scatter(
            x=payment_stats['Transaction_Count'],
            y=payment_stats['Total_Revenue'],
            mode='markers+text',
            text=payment_stats['Payment_Method'],
            textposition='top center',
            marker=dict(size=payment_stats['Avg_Transaction']*2,
                       color=colors,
                       opacity=0.7),
            name='Hiệu suất'
        ),
        row=2, col=2
    )

    fig.update_layout(
        title='Phân tích Toàn diện Phương thức Thanh toán',
        height=700,
        showlegend=False
    )
    return fig

def create_payment_method_time_trends(df: pd.DataFrame):
    """Payment method usage trends over time"""
    # Check if we have processed data with date columns
    if 'InvoiceYear' in df.columns and 'InvoiceMonth' in df.columns:
        try:
            # Create YearMonth string first, then convert to datetime
            df_temp = df.copy()
            df_temp['YearMonth'] = df_temp['InvoiceYear'].astype(str) + '-' + df_temp['InvoiceMonth'].astype(str).str.zfill(2) + '-01'
            df_temp['YearMonth'] = pd.to_datetime(df_temp['YearMonth'])

            monthly_payment = df_temp.groupby(['YearMonth', 'Payment_Method']).size().reset_index(name='Count')

            fig = px.line(
                monthly_payment,
                x='YearMonth',
                y='Count',
                color='Payment_Method',
                title='Xu hướng Sử dụng Phương thức Thanh toán theo Thời gian',
                markers=True
            )

            fig.update_layout(
                xaxis_title="Thời gian",
                yaxis_title="Số lượng Giao dịch",
                height=500
            )
        except Exception as e:
            # If datetime conversion fails, fall back to simpler chart
            fig = px.histogram(
                df,
                x='Customer_Category',
                color='Payment_Method',
                title='Phương thức Thanh toán theo Nhóm Khách hàng (Fallback)',
                barmode='group'
            )
            fig.update_layout(height=500)
    else:
        # Fallback: use customer category analysis
        fig = px.histogram(
            df,
            x='Customer_Category',
            color='Payment_Method',
            title='Phương thức Thanh toán theo Nhóm Khách hàng',
            barmode='group'
        )
        fig.update_layout(height=500)

    return fig

def create_payment_method_city_analysis(df: pd.DataFrame):
    """Geographic analysis of payment method preferences"""
    city_payment = df.groupby(['City', 'Payment_Method']).size().reset_index(name='Count')

    fig = px.sunburst(
        city_payment,
        path=['City', 'Payment_Method'],
        values='Count',
        title='Phân bố Phương thức Thanh toán theo Thành phố'
    )

    fig.update_layout(height=600)
    return fig

def create_payment_method_basket_analysis(df: pd.DataFrame):
    """Analysis of basket size and value by payment method"""
    basket_stats = df.groupby('Payment_Method').agg({
        'Quantity': ['mean', 'std'],
        'Total_Cost': ['mean', 'std']
    }).round(2)

    basket_stats.columns = ['Avg_Items', 'Std_Items', 'Avg_Cost', 'Std_Cost']
    basket_stats = basket_stats.reset_index()

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Số lượng Sản phẩm Trung bình', 'Giá trị Giỏ hàng Trung bình']
    )

    # Average items
    fig.add_trace(
        go.Bar(
            x=basket_stats['Payment_Method'],
            y=basket_stats['Avg_Items'],
            error_y=dict(type='data', array=basket_stats['Std_Items']),
            name='Số SP TB',
            marker_color='lightblue'
        ),
        row=1, col=1
    )

    # Average cost
    fig.add_trace(
        go.Bar(
            x=basket_stats['Payment_Method'],
            y=basket_stats['Avg_Cost'],
            error_y=dict(type='data', array=basket_stats['Std_Cost']),
            name='Giá trị TB',
            marker_color='lightcoral'
        ),
        row=1, col=2
    )

    fig.update_layout(
        title='Phân tích Giỏ hàng theo Phương thức Thanh toán',
        height=500,
        showlegend=False
    )
    return fig

def create_payment_method_advanced_metrics(df: pd.DataFrame):
    """Advanced metrics dashboard for payment methods"""
    metrics = df.groupby('Payment_Method').agg({
        'Total_Cost': ['count', 'sum', 'mean', 'std'],
        'Quantity': ['mean'],
        'Member': lambda x: (x == 'Yes').mean() * 100
    }).round(2)

    metrics.columns = ['Transactions', 'Revenue', 'Avg_Revenue', 'Std_Revenue', 'Avg_Items', 'Member_Rate']
    metrics = metrics.reset_index()

    # Calculate additional metrics
    metrics['Revenue_Per_Item'] = (metrics['Revenue'] / metrics['Avg_Items']).round(2)
    metrics['Market_Share'] = (metrics['Transactions'] / metrics['Transactions'].sum() * 100).round(1)

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Phương thức', 'Số GD', 'Doanh thu', 'TB/GD', 'TB/SP', 'Thị phần (%)', 'TV (%)'],
            fill_color='paleturquoise',
            align='center',
            font=dict(size=12, color='black')
        ),
        cells=dict(
            values=[
                metrics['Payment_Method'],
                metrics['Transactions'],
                [f'{x:,.0f}' for x in metrics['Revenue']],
                [f'{x:,.0f}' for x in metrics['Avg_Revenue']],
                [f'{x:,.0f}' for x in metrics['Revenue_Per_Item']],
                [f'{x}%' for x in metrics['Market_Share']],
                [f'{x:.1f}%' for x in metrics['Member_Rate']]
            ],
            fill_color='lavender',
            align='center',
            font=dict(size=11)
        )
    )])

    fig.update_layout(
        title='Bảng Thống kê Chi tiết Phương thức Thanh toán',
        height=400
    )
    return fig
