"""
Generate visualizations from the analysis
"""

# Configuration
CURRENT_START_YEAR = 2023
CURRENT_START_MONTH = 1
CURRENT_END_YEAR = 2023
CURRENT_END_MONTH = 12

DATA_PATH = ''

CHART_COLOR_PRIMARY = '#2E86AB'
FIGURE_SIZE = (12, 6)

# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Import custom modules
import data_loader as dl
import business_metrics as bm

warnings.filterwarnings('ignore')
pd.set_option('display.float_format', '{:.2f}'.format)

print("Generating visualizations...")

# Load and prepare data
datasets = dl.load_datasets(data_path=DATA_PATH)
orders = datasets['orders']
order_items = datasets['order_items']
products = datasets['products']
customers = datasets['customers']
reviews = datasets['reviews']

orders = dl.prepare_orders_data(orders)
sales_all = dl.create_sales_dataset(order_items, orders, status_filter='delivered')

sales_current = dl.filter_by_date_range(
    sales_all, CURRENT_START_YEAR, CURRENT_START_MONTH,
    CURRENT_END_YEAR, CURRENT_END_MONTH
)

sales_current = dl.add_product_categories(sales_current, products)
sales_current = dl.add_customer_geography(sales_current, orders, customers)
sales_current = dl.add_review_scores(sales_current, reviews)
sales_current = dl.calculate_delivery_speed(sales_current)
sales_current['delivery_category'] = sales_current['delivery_speed_days'].apply(dl.categorize_delivery_speed)

# 1. Monthly Revenue Trend
monthly_revenue = bm.calculate_revenue_by_period(sales_current, period='year-month')

plt.figure(figsize=FIGURE_SIZE)
plt.plot(monthly_revenue['month'], monthly_revenue['revenue'],
         marker='o', linewidth=2, markersize=8, color=CHART_COLOR_PRIMARY)
plt.title(f'Monthly Revenue Trend - {CURRENT_START_YEAR}', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue (USD)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
plt.tight_layout()
plt.savefig('monthly_revenue_trend.png', dpi=100)
print("  - Saved monthly_revenue_trend.png")

# 2. Revenue by Product Category
category_revenue = bm.calculate_revenue_by_category(sales_current)

plt.figure(figsize=FIGURE_SIZE)
plt.barh(category_revenue['category'], category_revenue['revenue'], color=CHART_COLOR_PRIMARY)
plt.title(f'Revenue by Product Category - {CURRENT_START_YEAR}', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Revenue (USD)', fontsize=12)
plt.ylabel('Product Category', fontsize=12)
plt.grid(True, alpha=0.3, axis='x')
ax = plt.gca()
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
plt.tight_layout()
plt.savefig('revenue_by_category.png', dpi=100)
print("  - Saved revenue_by_category.png")

# 3. Review Score Distribution
review_distribution = bm.calculate_review_score_distribution(sales_current)

plt.figure(figsize=(10, 6))
plt.barh(review_distribution['review_score'].astype(str),
         review_distribution['percentage'],
         color=CHART_COLOR_PRIMARY)
plt.title(f'Review Score Distribution - {CURRENT_START_YEAR}', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Percentage of Reviews (%)', fontsize=12)
plt.ylabel('Review Score', fontsize=12)
plt.grid(True, alpha=0.3, axis='x')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('review_score_distribution.png', dpi=100)
print("  - Saved review_score_distribution.png")

# 4. Delivery Speed Impact on Reviews
review_by_delivery = bm.calculate_review_by_delivery_speed(sales_current)

plt.figure(figsize=(10, 6))
plt.bar(review_by_delivery['delivery_category'],
        review_by_delivery['avg_review_score'],
        color=CHART_COLOR_PRIMARY)
plt.title(f'Average Review Score by Delivery Speed - {CURRENT_START_YEAR}',
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Delivery Speed', fontsize=12)
plt.ylabel('Average Review Score', fontsize=12)
plt.ylim(3.5, 5.0)
plt.grid(True, alpha=0.3, axis='y')

for i, v in enumerate(review_by_delivery['avg_review_score']):
    plt.text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('delivery_speed_impact.png', dpi=100)
print("  - Saved delivery_speed_impact.png")

print("\nAll visualizations generated successfully!")
