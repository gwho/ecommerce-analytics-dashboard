# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an e-commerce data analysis project using Jupyter notebooks to analyze sales, customer, and product data. The analysis focuses on revenue trends, customer behavior, product performance, and operational metrics.

## Data Structure

The project uses six CSV datasets representing an e-commerce platform:

- **customers_dataset.csv**: Customer information (customer_id, customer_unique_id, zip code, city, state)
- **orders_dataset.csv**: Order lifecycle data (order_id, customer_id, status, timestamps for purchase/approval/delivery)
- **order_items_dataset.csv**: Line items for each order (product_id, seller_id, price, freight_value, shipping limits)
- **order_reviews_dataset.csv**: Customer reviews (review_id, order_id, review_score 1-5, comments, timestamps)
- **order_payments_dataset.csv**: Payment information
- **products_dataset.csv**: Product catalog (product_id, category_name, dimensions, weight, photos)

**Note**: The CSV files reference a path `ecommerce_data/` in the notebook, but the actual files are stored in the root directory. When reading CSVs, the notebook uses the incorrect path.

## Key Data Relationships

- Orders link to customers via `customer_id`
- Order items link to orders via `order_id`, to products via `product_id`, and to sellers via `seller_id`
- Reviews link to orders via `order_id`
- Products have 13 categories: books_media, grocery_gourmet_food, electronics, sports_outdoors, home_garden, pet_supplies, automotive, health_personal_care, toys_games, beauty_personal_care, clothing_shoes_jewelry, tools_home_improvement, baby_products

## Analysis Notebook (EDA.ipynb)

The notebook performs the following analyses:

1. **Revenue Analysis**: Year-over-year comparison (2022 vs 2023), monthly growth trends
2. **Order Metrics**: Average order value, total order counts, order status distribution
3. **Product Performance**: Revenue by product category
4. **Geographic Analysis**: Sales by US state (with choropleth visualization using Plotly)
5. **Delivery & Reviews**: Correlation between delivery speed and review scores, average delivery time

### Key Findings from Current Analysis

- 2023 revenue: $3,360,294.74 (declined 2.46% vs 2022)
- Average monthly growth in 2023: -0.39%
- Average order value 2023: $724.98 (essentially flat vs 2022)
- Total orders 2023: 4,635 (down 2.4% vs 2022)
- Order status distribution 2023: 93.6% delivered, 3.2% shipped, 1.3% canceled
- Average delivery time: 8 days
- Average review score 2023: 4.10/5.00
- Delivery speed impact: 1-3 day deliveries get 4.19 avg review, 4-7 days get 4.08, 8+ days get 4.11

## Working with the Notebook

### Running Cells

Use the `mcp__ide__executeCode` tool to run Python code in the Jupyter kernel. All code executes in a persistent kernel, so variables and imports persist across executions.

### Common Data Operations

**Filtering for delivered orders only**:
```python
sales_delivered = sales_data[sales_data['order_status'] == 'delivered']
```

**Extracting year/month from timestamps**:
```python
df['timestamp_col'] = pd.to_datetime(df['timestamp_col'])
df['year'] = df['timestamp_col'].apply(lambda t: t.year)
df['month'] = df['timestamp_col'].apply(lambda t: t.month)
```

**Merging datasets** (common patterns in notebook):
```python
# Orders + Order Items + Products
sales_data = pd.merge(order_items[cols], orders[cols], on='order_id')
sales_categories = pd.merge(products[cols], sales_data[cols], on='product_id')

# Orders + Customers (via customer_id)
sales_customers = pd.merge(sales_data, orders[['order_id', 'customer_id']], on='order_id')
sales_states = pd.merge(sales_customers, customers[['customer_id', 'customer_state']], on='customer_id')
```

## Known Issues

### SettingWithCopyWarning

The notebook generates multiple `SettingWithCopyWarning` messages when modifying filtered dataframes. To fix these, use `.copy()` when creating filtered dataframes:

```python
# Instead of:
sales_delivered = sales_data[sales_data['order_status'] == 'delivered']

# Use:
sales_delivered = sales_data[sales_data['order_status'] == 'delivered'].copy()
```

### File Path Discrepancy

The notebook reads from `ecommerce_data/` subdirectory, but CSV files are in the root directory. Update CSV read paths or move files to match.

## Visualization Libraries

- **matplotlib**: Basic plotting (bar charts, line plots via pandas `.plot()`)
- **plotly.express**: Interactive choropleth maps for geographic visualization (`px.choropleth`)

## Refactored Analysis (EDA_Refactored.ipynb)

A production-ready version of the analysis with improved structure and modularity.

### Module Architecture

**data_loader.py**: Data loading and preparation functions
- `load_datasets()`: Load all CSV files into a dictionary
- `prepare_orders_data()`: Convert timestamps and extract year/month
- `create_sales_dataset()`: Merge order items with orders, filter by status
- `add_product_categories()`: Enrich with product information
- `add_customer_geography()`: Add state and city information
- `add_review_scores()`: Merge review data
- `calculate_delivery_speed()`: Compute days between purchase and delivery
- `filter_by_date_range()`: Filter dataframes by configurable start/end year-month

**business_metrics.py**: Business metric calculation functions
- Revenue metrics: `calculate_total_revenue()`, `calculate_revenue_by_period()`, `calculate_revenue_growth()`
- Order metrics: `calculate_average_order_value()`, `calculate_total_orders()`, `calculate_items_per_order()`
- Product metrics: `calculate_revenue_by_category()`
- Geographic metrics: `calculate_revenue_by_state()`
- Customer experience: `calculate_average_review_score()`, `calculate_average_delivery_time()`, `calculate_review_by_delivery_speed()`
- Comparisons: `compare_periods()`, `generate_summary_statistics()`

### Configuration System

The refactored notebook uses configuration variables to enable flexible analysis:

```python
# Current period
CURRENT_START_YEAR = 2023
CURRENT_START_MONTH = 1
CURRENT_END_YEAR = 2023
CURRENT_END_MONTH = 12

# Comparison period
COMPARISON_START_YEAR = 2022
COMPARISON_START_MONTH = 1
COMPARISON_END_YEAR = 2022
COMPARISON_END_MONTH = 12

# Paths and styling
DATA_PATH = ''  # Leave empty for current directory
CHART_COLOR_PRIMARY = '#2E86AB'
```

### Key Improvements

1. **Modular design**: Reusable functions in separate Python modules
2. **Configurable date ranges**: Analyze any time period without code changes
3. **No pandas warnings**: Proper use of `.copy()` to avoid SettingWithCopyWarning
4. **Professional visualizations**: Consistent styling, proper labels, titles with date ranges
5. **Comprehensive documentation**: Markdown cells, docstrings, data dictionary, table of contents
6. **Automated insights**: Summary statistics and key observations generation

### Usage Pattern

```python
import data_loader as dl
import business_metrics as bm

# Load and prepare data
datasets = dl.load_datasets()
orders = dl.prepare_orders_data(datasets['orders'])

# Create sales dataset for specific period
sales_all = dl.create_sales_dataset(datasets['order_items'], orders)
sales_2023 = dl.filter_by_date_range(sales_all, 2023, 1, 2023, 12)

# Calculate metrics
revenue = bm.calculate_total_revenue(sales_2023)
aov = bm.calculate_average_order_value(sales_2023)
```
