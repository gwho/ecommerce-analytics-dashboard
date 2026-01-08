# E-Commerce Business Analytics

A comprehensive, configurable analysis framework for e-commerce business performance metrics including revenue trends, customer behavior, product performance, and operational efficiency.

## Overview

This project provides a refactored and modular approach to analyzing e-commerce data. The analysis can be configured for any date range, making it reusable for ongoing business intelligence needs.

## Project Structure

```
DATA_ANALYSIS/
├── dashboard.py                   # Streamlit dashboard application
├── EDA_Refactored.ipynb          # Main analysis notebook
├── data_loader.py                 # Data loading and preparation functions
├── business_metrics.py            # Business metric calculations
├── requirements.txt               # Python dependencies
├── CLAUDE.md                      # Claude Code guidance
├── *.csv                          # Data files
└── README.md                      # This file
```

## Files Description

### dashboard.py
Professional Streamlit dashboard featuring:
- **Header**: Title with year and month range filters
- **KPI Row**: 4 metric cards (Total Revenue, Monthly Growth, AOV, Total Orders) with trend indicators
- **Charts Grid**: 2x2 layout with:
  - Revenue trend comparison (current vs previous year)
  - Top 10 product categories bar chart
  - US choropleth map showing revenue by state
  - Customer satisfaction vs delivery speed
- **Bottom Row**: Average delivery time and review score cards
- Real-time updates based on date range selection
- Professional styling with consistent color scheme

### EDA_Refactored.ipynb
The main Jupyter notebook containing:
- Comprehensive business metrics analysis
- Interactive visualizations
- Configurable date range filtering
- Period-over-period comparisons
- Well-documented sections with markdown explanations

### data_loader.py
Module for data loading and preparation:
- `load_datasets()`: Load all CSV files
- `prepare_orders_data()`: Process orders with datetime conversions
- `create_sales_dataset()`: Merge orders and items
- `add_product_categories()`: Enrich with product information
- `add_customer_geography()`: Add geographic dimensions
- `calculate_delivery_speed()`: Compute delivery metrics
- `filter_by_date_range()`: Filter data by configurable periods

### business_metrics.py
Module for business metric calculations:
- Revenue analysis (total, by period, growth rates)
- Order metrics (AOV, total orders, items per order)
- Product performance (revenue by category)
- Geographic analysis (revenue by state)
- Customer experience (review scores, delivery performance)
- Period comparison functions

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure all CSV data files are in the same directory as the notebook:
   - customers_dataset.csv
   - orders_dataset.csv
   - order_items_dataset.csv
   - order_reviews_dataset.csv
   - order_payments_dataset.csv
   - products_dataset.csv

## Usage

### Running the Dashboard

The quickest way to explore the data is through the interactive Streamlit dashboard:

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser with:
- Interactive date range filters
- Real-time KPI cards with trend indicators
- Professional charts and visualizations
- US choropleth map
- Customer experience metrics

### Running the Analysis Notebook

1. Open the refactored notebook:
```bash
jupyter notebook EDA_Refactored.ipynb
```

2. Configure the analysis parameters in Section 3:

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
```

3. Run all cells to generate the complete analysis

### Customizing the Analysis

#### Analyze a Different Time Period

To analyze Q1 2023 compared to Q1 2022:

```python
CURRENT_START_YEAR = 2023
CURRENT_START_MONTH = 1
CURRENT_END_YEAR = 2023
CURRENT_END_MONTH = 3

COMPARISON_START_YEAR = 2022
COMPARISON_START_MONTH = 1
COMPARISON_END_YEAR = 2022
COMPARISON_END_MONTH = 3
```

#### Change Visualization Colors

```python
CHART_COLOR_PRIMARY = '#2E86AB'      # Primary chart color
CHART_COLOR_SECONDARY = '#A23B72'    # Secondary color
CHART_COLOR_ACCENT = '#F18F01'       # Accent color
FIGURE_SIZE = (12, 6)                # Default figure size
```

#### Specify Data Path

If your CSV files are in a subdirectory:

```python
DATA_PATH = 'ecommerce_data/'
```

### Using the Modules Independently

The data_loader and business_metrics modules can be used independently in other scripts or notebooks:

```python
import data_loader as dl
import business_metrics as bm

# Load data
datasets = dl.load_datasets()
orders = dl.prepare_orders_data(datasets['orders'])

# Create sales dataset
sales = dl.create_sales_dataset(
    datasets['order_items'],
    orders,
    status_filter='delivered'
)

# Calculate metrics
total_revenue = bm.calculate_total_revenue(sales)
aov = bm.calculate_average_order_value(sales)
```

## Analysis Sections

The refactored notebook includes the following sections:

### 1. Introduction and Business Objectives
Overview of the analysis goals and key business questions

### 2. Data Dictionary
Comprehensive documentation of datasets, columns, and business term definitions

### 3. Configuration
Configurable parameters for date ranges and visualization settings

### 4. Data Loading and Preparation
Automated data loading, cleaning, and enrichment

### 5. Business Metrics Analysis
- **Revenue Analysis**: Total revenue, growth rates, monthly trends
- **Product Performance**: Revenue by category, top performers
- **Geographic Analysis**: Sales by state with choropleth visualization
- **Customer Experience**: Review scores, delivery performance, order status

### 6. Summary and Key Observations
Automated summary with key findings and insights

## Key Features

### Improvements Over Original Notebook

1. **Modular Code Structure**
   - Reusable functions in separate modules
   - Clean separation of data loading and business logic
   - Easy to maintain and extend

2. **Configurable Analysis**
   - Flexible date range selection
   - Works for any time period in the dataset
   - Easy period-over-period comparisons

3. **Enhanced Documentation**
   - Clear section headers with markdown explanations
   - Table of contents for easy navigation
   - Comprehensive data dictionary
   - Inline comments and docstrings

4. **Improved Visualizations**
   - Professional styling with consistent colors
   - Descriptive titles with date ranges
   - Proper axis labels and legends
   - Interactive Plotly maps

5. **Code Quality**
   - Eliminates SettingWithCopyWarning issues
   - Consistent naming conventions
   - Type hints in function signatures
   - Comprehensive docstrings

6. **Business Insights**
   - Automated summary generation
   - Clear key observations
   - Period comparison metrics
   - Top performer identification

## Data Requirements

The analysis expects the following CSV files:

- **customers_dataset.csv**: Customer information (ID, location)
- **orders_dataset.csv**: Order details (ID, status, timestamps)
- **order_items_dataset.csv**: Line items (product, price, freight)
- **order_reviews_dataset.csv**: Customer reviews and ratings
- **order_payments_dataset.csv**: Payment information
- **products_dataset.csv**: Product catalog (ID, category)

## Metrics Calculated

### Revenue Metrics
- Total revenue
- Revenue by month/year
- Month-over-month growth
- Year-over-year growth
- Revenue by product category
- Revenue by geographic region

### Order Metrics
- Total orders
- Average order value (AOV)
- Average items per order
- Order status distribution

### Customer Experience Metrics
- Average review score
- Review score distribution
- Average delivery time
- Review score by delivery speed

## Tips for Analysts

1. **Run the entire notebook** to ensure all dependencies are loaded
2. **Modify only the configuration section** for different analyses
3. **Export visualizations** using the notebook's save features
4. **Add custom analyses** by importing the modules and creating new cells
5. **Document changes** in markdown cells when extending the analysis

## Troubleshooting

### Common Issues

**Module not found error**
```bash
pip install -r requirements.txt
```

**CSV file not found**
- Ensure CSV files are in the correct directory
- Update DATA_PATH in configuration if files are in a subdirectory

**Date range returns no data**
- Verify the date range exists in your dataset
- Check the dataset date range printed in Section 4

**Plotly map not displaying**
- Ensure plotly is installed: `pip install plotly`
- Try running the cell again

## Extending the Analysis

To add new analyses:

1. **Add functions to modules**
   - Data transformations go in data_loader.py
   - Metric calculations go in business_metrics.py

2. **Create new notebook sections**
   - Add markdown cells explaining the analysis
   - Call module functions to perform calculations
   - Create visualizations to display results

3. **Update configuration**
   - Add new parameters to the configuration section if needed

## Contributing

When making changes:
1. Follow existing code style and naming conventions
2. Add docstrings to all new functions
3. Update README if adding new features
4. Test with different date ranges

## License

This analysis framework is provided as-is for business intelligence purposes.
