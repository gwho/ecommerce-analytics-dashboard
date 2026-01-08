# E-Commerce Analytics Dashboard Guide

## Overview

The Streamlit dashboard provides an interactive, professional interface for exploring e-commerce business metrics. It features real-time filtering, trend indicators, and comprehensive visualizations.

## Quick Start

### Option 1: Using the Launch Script
```bash
./run_dashboard.sh
```

### Option 2: Direct Command
```bash
streamlit run dashboard.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

## Dashboard Layout

### Header Section
- **Title**: E-Commerce Analytics Dashboard (left-aligned)
- **Date Range Filter**: Year and month range selectors (right-aligned)
  - Select analysis year from dropdown
  - Choose start month (From Month)
  - Choose end month (To Month)
  - Filters apply to all metrics and charts

### KPI Row (4 Cards)

All KPI cards display:
- Metric name
- Current value (formatted)
- Trend indicator (vs previous period)
  - Green arrow up (↑) for positive trends
  - Red arrow down (↓) for negative trends
  - Two decimal places for percentage changes

**Cards:**
1. **Total Revenue**: Current period revenue with YoY growth %
2. **Monthly Growth**: Average month-over-month growth rate
3. **Average Order Value**: AOV with YoY change %
4. **Total Orders**: Order count with YoY growth %

### Charts Grid (2x2 Layout)

#### Row 1

**Chart 1: Revenue Trend Comparison**
- Line chart comparing current year vs previous year
- Solid line: Current period
- Dashed line: Previous period
- Grid lines for easier reading
- Y-axis: Revenue formatted as $300K, $2M, etc.
- X-axis: Months (Jan-Dec)
- Hover to see exact values
- Interactive legend

**Chart 2: Top 10 Product Categories**
- Horizontal bar chart sorted by revenue (descending)
- Blue gradient: Lighter for lower values, darker for higher values
- Values displayed on bars formatted as $300K, $2M
- Hover to see exact revenue
- Automatically shows top 10 categories

#### Row 2

**Chart 3: Revenue by State (US Choropleth Map)**
- Interactive US map color-coded by revenue
- Blue gradient: Lighter = lower revenue, darker = higher revenue
- All 51 states/territories visible (including those with no data)
- States without data appear in light gray
- Hover over any state to see:
  - State abbreviation
  - Revenue amount or "No data"
- Click and drag to zoom
- Double-click to reset

**Chart 4: Customer Satisfaction vs Delivery Speed**
- Bar chart showing average review score by delivery speed
- X-axis: Delivery time buckets (1-3 days, 4-7 days, 8+ days)
- Y-axis: Average review score (3.5 to 5.0 scale)
- Blue bars with values displayed on top
- Shows how faster delivery correlates with satisfaction

### Bottom Row (2 Cards)

**Card 1: Average Delivery Time**
- Large number showing average days
- Trend indicator vs previous period
  - Green/down arrow = Improvement (fewer days)
  - Red/up arrow = Decline (more days)
- Note: Lower is better for delivery time

**Card 2: Average Review Score**
- Large number showing average rating (X.XX / 5.00)
- Star rating visualization (★★★★☆)
- Subtitle: "Average Review Score"
- Full stars, half stars, and empty stars based on score

## Features

### Interactive Filtering
- All charts and metrics update in real-time when you change:
  - Year selection
  - Start month
  - End month
- Previous period automatically calculated (prior year, same months)
- Comparison metrics recalculate automatically

### Data Caching
- Dashboard uses Streamlit's caching for fast performance
- Initial load may take a few seconds
- Subsequent interactions are instant
- Data reloads only when source files change

### Responsive Design
- Professional styling with card-based layout
- Consistent heights for each row
- White cards with subtle shadows
- Grid lines on charts for readability
- Proper spacing and alignment

### Color Scheme
- **Primary Blue**: #1f77b4 (titles, main metrics)
- **Green**: #28a745 (positive trends)
- **Red**: #dc3545 (negative trends)
- **Gray Borders**: #e0e0e0 (card borders)
- **Blue Gradients**: Charts use light to dark blue scales

## Usage Examples

### Analyzing Full Year Performance
1. Select year: 2023
2. From Month: January
3. To Month: December
4. View full year metrics compared to 2022

### Analyzing Q1 Performance
1. Select year: 2023
2. From Month: January
3. To Month: March
4. View Q1 2023 metrics compared to Q1 2022

### Analyzing Specific Period
1. Select year: 2023
2. From Month: June
3. To Month: August
4. View summer season performance

### Understanding Trends
- **Revenue Trend Chart**: See monthly fluctuations, identify seasonality
- **Category Performance**: Identify best-selling categories
- **Geographic Patterns**: See which states drive most revenue
- **Delivery Impact**: Understand correlation between speed and satisfaction

## Technical Details

### Dependencies
- streamlit>=1.28.0
- pandas>=1.3.0
- plotly>=5.0.0
- Custom modules: data_loader.py, business_metrics.py

### Data Requirements
All CSV files must be in the same directory as dashboard.py:
- customers_dataset.csv
- orders_dataset.csv
- order_items_dataset.csv
- products_dataset.csv
- order_reviews_dataset.csv
- order_payments_dataset.csv

### Performance
- Caching enabled for data loading
- Fast chart rendering with Plotly
- Efficient data transformations
- Suitable for datasets up to millions of rows

## Troubleshooting

### Dashboard won't start
```bash
# Check if streamlit is installed
pip list | grep streamlit

# Reinstall if needed
pip install -r requirements.txt
```

### Port already in use
```bash
# Use a different port
streamlit run dashboard.py --server.port 8502
```

### Charts not displaying
- Check that all CSV files are present
- Verify data has records for selected date range
- Check browser console for JavaScript errors

### Slow performance
- Reduce date range (analyze shorter periods)
- Check available system memory
- Clear browser cache

## Customization

### Changing Colors
Edit the color values in `dashboard.py`:
- Line ~40: CSS styles for metric cards
- Line ~320: Chart colors (e.g., `color='#1f77b4'`)

### Modifying Layout
- Card heights: Adjust CSS `height` values
- Column widths: Modify `st.columns()` ratios
- Chart heights: Update `fig.update_layout(height=350)`

### Adding New Metrics
1. Calculate metric using business_metrics.py functions
2. Add new card with `create_metric_card()`
3. Update layout columns as needed

## Best Practices

1. **Start with full year** to see overall trends
2. **Compare to previous year** for context
3. **Drill down to quarters/months** for details
4. **Use hover tooltips** to see exact values
5. **Export charts** by clicking camera icon in Plotly toolbar

## Support

For issues or questions:
- Check this guide first
- Review README.md for setup instructions
- Verify all dependencies are installed
- Ensure CSV files are present and valid
