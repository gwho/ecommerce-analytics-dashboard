"""
E-Commerce Business Analytics Dashboard
A professional Streamlit dashboard for analyzing e-commerce performance metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import data_loader as dl
import business_metrics as bm

# Page configuration
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        margin: 0;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .trend-positive {
        color: #28a745;
        font-size: 1rem;
        font-weight: bold;
    }
    .trend-negative {
        color: #dc3545;
        font-size: 1rem;
        font-weight: bold;
    }
    .chart-container {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 400px;
    }
    .bottom-card {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
        text-align: center;
    }
    .star-rating {
        color: #ffd700;
        font-size: 1.5rem;
    }
    h1 {
        color: #1f77b4;
        margin-bottom: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    """Load and prepare all datasets"""
    datasets = dl.load_datasets()
    orders = dl.prepare_orders_data(datasets['orders'])
    reviews = dl.prepare_reviews_data(datasets['reviews'])

    return {
        'orders': orders,
        'order_items': datasets['order_items'],
        'products': datasets['products'],
        'customers': datasets['customers'],
        'reviews': reviews
    }

def prepare_sales_data(datasets, start_year, start_month, end_year, end_month):
    """Prepare sales data for a specific period"""
    sales_all = dl.create_sales_dataset(
        datasets['order_items'],
        datasets['orders'],
        status_filter='delivered'
    )

    sales_period = dl.filter_by_date_range(
        sales_all, start_year, start_month, end_year, end_month
    )

    # Enrich data
    sales_period = dl.add_product_categories(sales_period, datasets['products'])
    sales_period = dl.add_customer_geography(sales_period, datasets['orders'], datasets['customers'])
    sales_period = dl.add_review_scores(sales_period, datasets['reviews'])
    sales_period = dl.calculate_delivery_speed(sales_period)
    sales_period['delivery_category'] = sales_period['delivery_speed_days'].apply(dl.categorize_delivery_speed)

    return sales_period

def format_currency(value):
    """Format currency values intelligently"""
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.0f}K"
    else:
        return f"${value:.0f}"

def create_metric_card(label, value, trend_value=None, trend_label="vs previous period"):
    """Create a metric card with optional trend indicator"""
    if trend_value is not None:
        trend_color = "trend-positive" if trend_value >= 0 else "trend-negative"
        trend_arrow = "↑" if trend_value >= 0 else "↓"
        trend_html = f'<div class="{trend_color}">{trend_arrow} {abs(trend_value):.2f}% {trend_label}</div>'
    else:
        trend_html = ""

    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {trend_html}
        </div>
    """, unsafe_allow_html=True)

# Load data
datasets = load_data()

# Get date range from data
min_date = datasets['orders']['order_purchase_timestamp'].min()
max_date = datasets['orders']['order_purchase_timestamp'].max()

# Header
col1, col2 = st.columns([2, 1])
with col1:
    st.title("E-Commerce Analytics Dashboard")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)

    # Year selector - default to 2023
    available_years = sorted(datasets['orders']['year'].unique())
    default_year_index = available_years.index(2023) if 2023 in available_years else len(available_years) - 1

    selected_year = st.selectbox(
        "Select Year",
        available_years,
        index=default_year_index
    )

    # Month range selector
    col_start, col_end = st.columns(2)
    with col_start:
        start_month = st.selectbox("From Month", range(1, 13), index=0, format_func=lambda x: datetime(2000, x, 1).strftime('%B'))
    with col_end:
        end_month = st.selectbox("To Month", range(1, 13), index=11, format_func=lambda x: datetime(2000, x, 1).strftime('%B'))

st.markdown("---")

# Prepare data for current and previous period
current_sales = prepare_sales_data(datasets, selected_year, start_month, selected_year, end_month)
previous_sales = prepare_sales_data(datasets, selected_year - 1, start_month, selected_year - 1, end_month)

# Calculate metrics
comparison_metrics = bm.compare_periods(current_sales, previous_sales)
monthly_revenue = bm.calculate_revenue_by_period(current_sales, period='year-month')
monthly_growth = bm.calculate_mom_growth(monthly_revenue)
avg_mom_growth = monthly_growth['mom_growth'].mean() * 100

# KPI Row - 4 cards
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    create_metric_card(
        "Total Revenue",
        format_currency(comparison_metrics['current_revenue']),
        comparison_metrics['revenue_growth_rate'] * 100
    )

with col2:
    create_metric_card(
        "Monthly Growth",
        f"{avg_mom_growth:+.2f}%",
    )

with col3:
    create_metric_card(
        "Average Order Value",
        f"${comparison_metrics['current_aov']:,.2f}",
        comparison_metrics['aov_growth_rate'] * 100
    )

with col4:
    create_metric_card(
        "Total Orders",
        f"{comparison_metrics['current_orders']:,}",
        comparison_metrics['orders_growth_rate'] * 100
    )

st.markdown("<br>", unsafe_allow_html=True)

# Charts Grid - 2x2 layout
st.subheader("Performance Analytics")

row1_col1, row1_col2 = st.columns(2)

# Chart 1: Revenue Trend (Current vs Previous)
with row1_col1:
    # Prepare current period data
    current_monthly = bm.calculate_revenue_by_period(current_sales, period='year-month')
    previous_monthly = bm.calculate_revenue_by_period(previous_sales, period='year-month')

    fig = go.Figure()

    # Current period - solid line
    fig.add_trace(go.Scatter(
        x=current_monthly['month'],
        y=current_monthly['revenue'],
        mode='lines+markers',
        name=f'{selected_year}',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))

    # Previous period - dashed line
    fig.add_trace(go.Scatter(
        x=previous_monthly['month'],
        y=previous_monthly['revenue'],
        mode='lines+markers',
        name=f'{selected_year - 1}',
        line=dict(color='#ff7f0e', width=2, dash='dash'),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title='Revenue Trend Comparison',
        height=350,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(
            title='Month',
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            showgrid=True,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title='Revenue',
            tickformat='$,.0s',
            showgrid=True,
            gridcolor='lightgray'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

# Chart 2: Top 10 Categories
with row1_col2:
    category_revenue = bm.calculate_revenue_by_category(current_sales).head(10)

    # Create color gradient from light to dark blue
    colors = [f'rgb({int(198 - i*15)}, {int(219 - i*15)}, {int(239 - i*15)})' for i in range(len(category_revenue))]

    fig = go.Figure(go.Bar(
        x=category_revenue['revenue'],
        y=category_revenue['category'],
        orientation='h',
        marker=dict(color=colors),
        text=category_revenue['revenue'].apply(format_currency),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        title='Top 10 Product Categories',
        height=350,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(title='Revenue', tickformat='$,.0s', showgrid=True, gridcolor='lightgray'),
        yaxis=dict(title='', autorange='reversed'),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

# Chart 3: Geographic Distribution
with row2_col1:

    state_revenue = bm.calculate_revenue_by_state(current_sales)

    # Create complete US states list
    all_us_states = pd.DataFrame({
        'state': [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
        ]
    })

    state_revenue_complete = all_us_states.merge(state_revenue, on='state', how='left')
    state_revenue_complete['revenue'] = state_revenue_complete['revenue'].fillna(0)
    state_revenue_complete['revenue_display'] = state_revenue_complete['revenue'].apply(
        lambda x: 'No data' if x == 0 else f'${x:,.2f}'
    )
    state_revenue_complete['revenue_viz'] = state_revenue_complete['revenue'].replace(0, 0.001)

    max_revenue = state_revenue_complete[state_revenue_complete['revenue'] > 0]['revenue'].max() if len(state_revenue_complete[state_revenue_complete['revenue'] > 0]) > 0 else 1000000

    fig = px.choropleth(
        state_revenue_complete,
        locations='state',
        color='revenue_viz',
        locationmode='USA-states',
        scope='usa',
        color_continuous_scale='Blues',
        labels={'revenue_viz': 'Revenue'},
        range_color=[0, max_revenue],
        hover_data={'revenue_viz': False, 'revenue_display': True}
    )

    fig.update_traces(
        marker_line_color='#666666',
        marker_line_width=1,
        hovertemplate='<b>%{location}</b><br>Revenue: %{customdata[0]}<extra></extra>'
    )

    fig.update_layout(
        title='Revenue by State',
        height=350,
        margin=dict(l=0, r=0, t=40, b=0),
        geo=dict(
            projection_type='albers usa',
            showlakes=True,
            lakecolor='#E3F2FD'
        ),
        coloraxis_colorbar=dict(
            title='Revenue',
            tickformat='$,.0s'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# Chart 4: Satisfaction vs Delivery Time
with row2_col2:

    review_by_delivery = bm.calculate_review_by_delivery_speed(current_sales)

    fig = go.Figure(go.Bar(
        x=review_by_delivery['delivery_category'],
        y=review_by_delivery['avg_review_score'],
        marker=dict(color='#1f77b4'),
        text=review_by_delivery['avg_review_score'].apply(lambda x: f'{x:.2f}'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Avg Review: %{y:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title='Average Review Score by Delivery Speed',
        height=350,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(title='Delivery Speed', showgrid=False),
        yaxis=dict(
            title='Average Review Score',
            range=[3.5, 5.0],
            showgrid=True,
            gridcolor='lightgray'
        ),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Bottom Row - 2 cards
st.subheader("Customer Experience Metrics")
bottom_col1, bottom_col2 = st.columns(2)

with bottom_col1:
    avg_delivery_time = bm.calculate_average_delivery_time(current_sales)

    # Calculate previous period for trend
    if len(previous_sales) > 0:
        prev_delivery_time = bm.calculate_average_delivery_time(previous_sales)
        delivery_trend = ((avg_delivery_time - prev_delivery_time) / prev_delivery_time) * 100

        # Note: Lower delivery time is better, so invert the trend color logic
        trend_color = "trend-positive" if delivery_trend < 0 else "trend-negative"
        trend_arrow = "↓" if delivery_trend < 0 else "↑"
        trend_html = f'<div class="{trend_color}">{trend_arrow} {abs(delivery_trend):.2f}% vs previous period</div>'
    else:
        trend_html = ""

    st.markdown(f"""
        <div class="bottom-card">
            <div class="metric-label">Average Delivery Time</div>
            <div class="metric-value">{avg_delivery_time:.1f} days</div>
            {trend_html}
        </div>
    """, unsafe_allow_html=True)

with bottom_col2:
    avg_review_score = bm.calculate_average_review_score(current_sales)

    # Create star rating
    full_stars = int(avg_review_score)
    partial_star = avg_review_score - full_stars
    stars = '★' * full_stars
    if partial_star >= 0.5:
        stars += '½'
    stars += '☆' * (5 - len(stars))

    st.markdown(f"""
        <div class="bottom-card">
            <div class="metric-label">Average Review Score</div>
            <div class="metric-value">{avg_review_score:.2f} / 5.00</div>
            <div class="star-rating">{stars}</div>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>E-Commerce Analytics Dashboard | "
    f"Data Period: {selected_year}-{start_month:02d} to {selected_year}-{end_month:02d}</div>",
    unsafe_allow_html=True
)
