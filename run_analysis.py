"""
Run the E-Commerce Analysis
This script executes the same analysis as the refactored notebook
"""

# Configuration
CURRENT_START_YEAR = 2023
CURRENT_START_MONTH = 1
CURRENT_END_YEAR = 2023
CURRENT_END_MONTH = 12

COMPARISON_START_YEAR = 2022
COMPARISON_START_MONTH = 1
COMPARISON_END_YEAR = 2022
COMPARISON_END_MONTH = 12

DATA_PATH = ''

CHART_COLOR_PRIMARY = '#2E86AB'
CHART_COLOR_SECONDARY = '#A23B72'
CHART_COLOR_ACCENT = '#F18F01'
FIGURE_SIZE = (12, 6)

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

# Import custom modules
import data_loader as dl
import business_metrics as bm

# Configuration
warnings.filterwarnings('ignore')
pd.set_option('display.float_format', '{:.2f}'.format)

print("="*70)
print("E-COMMERCE BUSINESS ANALYTICS")
print("="*70)
print("\n1. Loading datasets...")

# Load all datasets
datasets = dl.load_datasets(data_path=DATA_PATH)

# Extract individual datasets
orders = datasets['orders']
order_items = datasets['order_items']
products = datasets['products']
customers = datasets['customers']
reviews = datasets['reviews']

print(f"   - Loaded {len(orders):,} orders")
print(f"   - Loaded {len(order_items):,} order items")
print(f"   - Loaded {len(products):,} products")
print(f"   - Loaded {len(customers):,} customers")
print(f"   - Loaded {len(reviews):,} reviews")

print("\n2. Preparing datasets...")
orders = dl.prepare_orders_data(orders)
reviews = dl.prepare_reviews_data(reviews)
print(f"   - Date range: {orders['order_purchase_timestamp'].min().date()} to {orders['order_purchase_timestamp'].max().date()}")

print(f"\n3. Creating sales dataset for analysis period...")
sales_all = dl.create_sales_dataset(order_items, orders, status_filter='delivered')

# Filter to current period
sales_current = dl.filter_by_date_range(
    sales_all,
    start_year=CURRENT_START_YEAR,
    start_month=CURRENT_START_MONTH,
    end_year=CURRENT_END_YEAR,
    end_month=CURRENT_END_MONTH
)

# Filter to comparison period
sales_comparison = dl.filter_by_date_range(
    sales_all,
    start_year=COMPARISON_START_YEAR,
    start_month=COMPARISON_START_MONTH,
    end_year=COMPARISON_END_YEAR,
    end_month=COMPARISON_END_MONTH
)

print(f"   - Current period ({CURRENT_START_YEAR}): {len(sales_current):,} delivered order items")
print(f"   - Comparison period ({COMPARISON_START_YEAR}): {len(sales_comparison):,} delivered order items")

print("\n4. Enriching data...")
sales_current = dl.add_product_categories(sales_current, products)
sales_comparison = dl.add_product_categories(sales_comparison, products)

sales_current = dl.add_customer_geography(sales_current, orders, customers)
sales_comparison = dl.add_customer_geography(sales_comparison, orders, customers)

sales_current = dl.add_review_scores(sales_current, reviews)
sales_comparison = dl.add_review_scores(sales_comparison, reviews)

sales_current = dl.calculate_delivery_speed(sales_current)
sales_comparison = dl.calculate_delivery_speed(sales_comparison)

sales_current['delivery_category'] = sales_current['delivery_speed_days'].apply(dl.categorize_delivery_speed)
sales_comparison['delivery_category'] = sales_comparison['delivery_speed_days'].apply(dl.categorize_delivery_speed)

print("   - Data enrichment complete")

# Calculate period comparison metrics
print("\n5. Calculating business metrics...")
comparison_metrics = bm.compare_periods(sales_current, sales_comparison)

# Display results
print("\n" + "="*70)
print("REVENUE COMPARISON")
print("="*70)
print(f"\nCurrent Period ({CURRENT_START_YEAR})")
print(f"  Total Revenue: ${comparison_metrics['current_revenue']:,.2f}")
print(f"  Total Orders: {comparison_metrics['current_orders']:,.0f}")
print(f"  Average Order Value: ${comparison_metrics['current_aov']:,.2f}")

print(f"\nComparison Period ({COMPARISON_START_YEAR})")
print(f"  Total Revenue: ${comparison_metrics['previous_revenue']:,.2f}")
print(f"  Total Orders: {comparison_metrics['previous_orders']:,.0f}")
print(f"  Average Order Value: ${comparison_metrics['previous_aov']:,.2f}")

print(f"\nYear-over-Year Growth")
print(f"  Revenue Growth: {comparison_metrics['revenue_growth_rate']*100:+.2f}%")
print(f"  Orders Growth: {comparison_metrics['orders_growth_rate']*100:+.2f}%")
print(f"  AOV Growth: {comparison_metrics['aov_growth_rate']*100:+.2f}%")

# Calculate monthly metrics
print("\n" + "="*70)
print("MONTHLY PERFORMANCE")
print("="*70)
monthly_revenue = bm.calculate_revenue_by_period(sales_current, period='year-month')
monthly_growth = bm.calculate_mom_growth(monthly_revenue)

print(f"\nMonth-over-Month Growth - {CURRENT_START_YEAR}")
print("-"*50)
for idx, row in monthly_growth.iterrows():
    month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(row['month'])-1]
    growth_str = f"{row['mom_growth']*100:+.2f}%" if pd.notna(row['mom_growth']) else "N/A"
    print(f"  {month_name}: ${row['revenue']:,.2f} ({growth_str})")

avg_mom_growth = monthly_growth['mom_growth'].mean()
print("-"*50)
print(f"  Average MoM Growth: {avg_mom_growth*100:+.2f}%")

# Product performance
print("\n" + "="*70)
print("PRODUCT PERFORMANCE")
print("="*70)
category_revenue = bm.calculate_revenue_by_category(sales_current)
print(f"\nTop 5 Product Categories by Revenue - {CURRENT_START_YEAR}")
print("-"*60)
for idx, row in category_revenue.head(5).iterrows():
    percentage = (row['revenue'] / category_revenue['revenue'].sum() * 100)
    print(f"  {row['category']:30s} ${row['revenue']:>12,.2f} ({percentage:>5.1f}%)")

# Geographic analysis
print("\n" + "="*70)
print("GEOGRAPHIC PERFORMANCE")
print("="*70)
state_revenue = bm.calculate_revenue_by_state(sales_current)
print(f"\nTop 5 States by Revenue - {CURRENT_START_YEAR}")
print("-"*50)
for idx, row in state_revenue.head(5).iterrows():
    percentage = (row['revenue'] / state_revenue['revenue'].sum() * 100)
    print(f"  {row['state']}: ${row['revenue']:,.2f} ({percentage:.1f}%)")

# Customer experience
print("\n" + "="*70)
print("CUSTOMER EXPERIENCE")
print("="*70)

# Filter orders for current period
orders_current = dl.filter_by_date_range(
    orders,
    start_year=CURRENT_START_YEAR,
    start_month=CURRENT_START_MONTH,
    end_year=CURRENT_END_YEAR,
    end_month=CURRENT_END_MONTH
)

status_dist = bm.calculate_order_status_distribution(orders_current)
print(f"\nOrder Status Distribution - {CURRENT_START_YEAR}")
print("-"*50)
for idx, row in status_dist.iterrows():
    print(f"  {row['order_status']:12s}: {row['count']:>5,} ({row['percentage']:>5.1f}%)")

avg_review_score = bm.calculate_average_review_score(sales_current)
review_distribution = bm.calculate_review_score_distribution(sales_current)

print(f"\nCustomer Review Analysis - {CURRENT_START_YEAR}")
print("-"*50)
print(f"  Average Review Score: {avg_review_score:.2f}/5.00")
print("\n  Review Score Distribution:")
for idx, row in review_distribution.iterrows():
    print(f"    {int(row['review_score'])} stars: {row['count']:>4,} reviews ({row['percentage']:>5.1f}%)")

avg_delivery_time = bm.calculate_average_delivery_time(sales_current)
review_by_delivery = bm.calculate_review_by_delivery_speed(sales_current)

print(f"\nDelivery Performance - {CURRENT_START_YEAR}")
print("-"*50)
print(f"  Average Delivery Time: {avg_delivery_time:.1f} days")
print("\n  Review Score by Delivery Speed:")
for idx, row in review_by_delivery.iterrows():
    print(f"    {row['delivery_category']:10s}: {row['avg_review_score']:.2f}/5.00")

# Generate comprehensive summary
summary_current = bm.generate_summary_statistics(sales_current, orders_current)

print("\n" + "="*70)
print("EXECUTIVE SUMMARY")
print("="*70)
print(f"\nAnalysis Period: {CURRENT_START_YEAR}-{CURRENT_START_MONTH:02d} to {CURRENT_END_YEAR}-{CURRENT_END_MONTH:02d}")
print(f"Comparison Period: {COMPARISON_START_YEAR}-{COMPARISON_START_MONTH:02d} to {COMPARISON_END_YEAR}-{COMPARISON_END_MONTH:02d}")

print("\n" + "-"*70)
print("KEY METRICS")
print("-"*70)
print(f"  Total Revenue: ${summary_current['total_revenue']:,.2f}")
print(f"  Total Orders: {summary_current['total_orders']:,}")
print(f"  Average Order Value: ${summary_current['average_order_value']:,.2f}")
print(f"  Average Items per Order: {summary_current['average_items_per_order']:.2f}")
print(f"  Average Review Score: {summary_current['average_review_score']:.2f}/5.00")
print(f"  Average Delivery Time: {summary_current['average_delivery_days']:.1f} days")

print("\n" + "-"*70)
print("PERIOD-OVER-PERIOD COMPARISON")
print("-"*70)
print(f"  Revenue Change: {comparison_metrics['revenue_growth_rate']*100:+.2f}%")
print(f"  Orders Change: {comparison_metrics['orders_growth_rate']*100:+.2f}%")
print(f"  AOV Change: {comparison_metrics['aov_growth_rate']*100:+.2f}%")

print("\n" + "-"*70)
print("TOP PERFORMERS")
print("-"*70)
print(f"  Top Category: {category_revenue.iloc[0]['category']} (${category_revenue.iloc[0]['revenue']:,.2f})")
print(f"  Top State: {state_revenue.iloc[0]['state']} (${state_revenue.iloc[0]['revenue']:,.2f})")

print("\n" + "-"*70)
print("KEY OBSERVATIONS")
print("-"*70)

print("\n1. Revenue Performance:")
if comparison_metrics['revenue_growth_rate'] > 0:
    print(f"   - Revenue increased by {comparison_metrics['revenue_growth_rate']*100:.2f}% vs prior period")
else:
    print(f"   - Revenue declined by {abs(comparison_metrics['revenue_growth_rate'])*100:.2f}% vs prior period")
print(f"   - Average month-over-month growth: {avg_mom_growth*100:+.2f}%")

print("\n2. Customer Experience:")
print(f"   - Customer satisfaction: {summary_current['average_review_score']:.2f}/5.00")
print(f"   - Delivery performance: {summary_current['average_delivery_days']:.1f} days average")
fastest_delivery = review_by_delivery.iloc[0]
print(f"   - {fastest_delivery['delivery_category']} achieve highest satisfaction ({fastest_delivery['avg_review_score']:.2f}/5.00)")

print("\n3. Product Performance:")
top_3_categories = category_revenue.head(3)
top_3_pct = (top_3_categories['revenue'].sum() / category_revenue['revenue'].sum()) * 100
print(f"   - Top 3 categories account for {top_3_pct:.1f}% of revenue")
for idx, row in top_3_categories.iterrows():
    pct = (row['revenue'] / category_revenue['revenue'].sum()) * 100
    print(f"   - {row['category']}: {pct:.1f}%")

print("\n" + "="*70)
print("Analysis complete!")
print("="*70)
