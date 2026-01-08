"""
Data Loading and Processing Module

This module provides functions for loading and preparing e-commerce datasets
for analysis. It handles data loading, cleaning, and basic transformations.
"""

import pandas as pd
from typing import Dict


def load_datasets(data_path: str = '') -> Dict[str, pd.DataFrame]:
    """
    Load all e-commerce datasets from CSV files.

    Parameters
    ----------
    data_path : str, optional
        Path to directory containing CSV files (default is current directory)

    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary containing all loaded datasets with keys:
        'orders', 'order_items', 'products', 'customers', 'reviews', 'payments'
    """
    datasets = {}

    # Define file mappings
    files = {
        'orders': 'orders_dataset.csv',
        'order_items': 'order_items_dataset.csv',
        'products': 'products_dataset.csv',
        'customers': 'customers_dataset.csv',
        'reviews': 'order_reviews_dataset.csv',
        'payments': 'order_payments_dataset.csv'
    }

    # Load each dataset
    for key, filename in files.items():
        filepath = f"{data_path}{filename}" if data_path else filename
        datasets[key] = pd.read_csv(filepath)

    return datasets


def prepare_orders_data(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare orders dataset with datetime conversions and derived fields.

    Parameters
    ----------
    orders : pd.DataFrame
        Raw orders dataframe

    Returns
    -------
    pd.DataFrame
        Cleaned orders dataframe with datetime columns and extracted year/month
    """
    orders = orders.copy()

    # Convert timestamp columns to datetime
    timestamp_cols = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]

    for col in timestamp_cols:
        if col in orders.columns:
            orders[col] = pd.to_datetime(orders[col])

    # Extract year and month from purchase timestamp
    orders['year'] = orders['order_purchase_timestamp'].dt.year
    orders['month'] = orders['order_purchase_timestamp'].dt.month

    return orders


def prepare_reviews_data(reviews: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare reviews dataset with datetime conversions.

    Parameters
    ----------
    reviews : pd.DataFrame
        Raw reviews dataframe

    Returns
    -------
    pd.DataFrame
        Cleaned reviews dataframe with datetime columns
    """
    reviews = reviews.copy()

    # Convert timestamp columns to datetime
    reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'])
    reviews['review_answer_timestamp'] = pd.to_datetime(reviews['review_answer_timestamp'])

    return reviews


def create_sales_dataset(order_items: pd.DataFrame,
                        orders: pd.DataFrame,
                        status_filter: str = 'delivered') -> pd.DataFrame:
    """
    Create consolidated sales dataset by merging order items with orders.

    Parameters
    ----------
    order_items : pd.DataFrame
        Order items dataframe
    orders : pd.DataFrame
        Orders dataframe (should be prepared with prepare_orders_data)
    status_filter : str, optional
        Filter to specific order status (default is 'delivered')

    Returns
    -------
    pd.DataFrame
        Merged sales dataset with order and item information
    """
    # Select relevant columns from order items
    items_cols = ['order_id', 'order_item_id', 'product_id', 'price', 'freight_value']

    # Select relevant columns from orders
    orders_cols = [
        'order_id', 'customer_id', 'order_status',
        'order_purchase_timestamp', 'order_delivered_customer_date',
        'year', 'month'
    ]

    # Merge datasets
    sales_data = pd.merge(
        left=order_items[items_cols],
        right=orders[orders_cols],
        on='order_id',
        how='inner'
    )

    # Filter by status if specified
    if status_filter:
        sales_data = sales_data[sales_data['order_status'] == status_filter].copy()

    return sales_data


def add_product_categories(sales_data: pd.DataFrame,
                          products: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich sales data with product category information.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset
    products : pd.DataFrame
        Products dataframe

    Returns
    -------
    pd.DataFrame
        Sales data with product category information
    """
    product_cols = ['product_id', 'product_category_name']

    enriched_data = pd.merge(
        left=sales_data,
        right=products[product_cols],
        on='product_id',
        how='left'
    )

    return enriched_data


def add_customer_geography(sales_data: pd.DataFrame,
                          orders: pd.DataFrame,
                          customers: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich sales data with customer geographic information.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset
    orders : pd.DataFrame
        Orders dataframe
    customers : pd.DataFrame
        Customers dataframe

    Returns
    -------
    pd.DataFrame
        Sales data with customer state information
    """
    # First merge with orders to get customer_id if not already present
    if 'customer_id' not in sales_data.columns:
        sales_with_customer = pd.merge(
            left=sales_data,
            right=orders[['order_id', 'customer_id']],
            on='order_id',
            how='left'
        )
    else:
        sales_with_customer = sales_data.copy()

    # Then merge with customers to get geography
    customer_cols = ['customer_id', 'customer_state', 'customer_city']

    enriched_data = pd.merge(
        left=sales_with_customer,
        right=customers[customer_cols],
        on='customer_id',
        how='left'
    )

    return enriched_data


def add_review_scores(sales_data: pd.DataFrame,
                     reviews: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich sales data with review scores.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset
    reviews : pd.DataFrame
        Reviews dataframe

    Returns
    -------
    pd.DataFrame
        Sales data with review scores
    """
    review_cols = ['order_id', 'review_score']

    enriched_data = pd.merge(
        left=sales_data,
        right=reviews[review_cols],
        on='order_id',
        how='left'
    )

    return enriched_data


def calculate_delivery_speed(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate delivery speed in days for each order.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with order_purchase_timestamp and
        order_delivered_customer_date columns

    Returns
    -------
    pd.DataFrame
        Sales data with delivery_speed_days column
    """
    sales_data = sales_data.copy()

    # Ensure datetime types
    sales_data['order_purchase_timestamp'] = pd.to_datetime(
        sales_data['order_purchase_timestamp']
    )
    sales_data['order_delivered_customer_date'] = pd.to_datetime(
        sales_data['order_delivered_customer_date']
    )

    # Calculate delivery speed in days
    sales_data['delivery_speed_days'] = (
        sales_data['order_delivered_customer_date'] -
        sales_data['order_purchase_timestamp']
    ).dt.days

    return sales_data


def categorize_delivery_speed(days: int) -> str:
    """
    Categorize delivery speed into time buckets.

    Parameters
    ----------
    days : int
        Number of days for delivery

    Returns
    -------
    str
        Delivery category: '1-3 days', '4-7 days', or '8+ days'
    """
    if days <= 3:
        return '1-3 days'
    elif days <= 7:
        return '4-7 days'
    else:
        return '8+ days'


def filter_by_date_range(df: pd.DataFrame,
                        start_year: int,
                        start_month: int,
                        end_year: int,
                        end_month: int,
                        date_column: str = 'order_purchase_timestamp') -> pd.DataFrame:
    """
    Filter dataframe by date range.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to filter
    start_year : int
        Starting year
    start_month : int
        Starting month (1-12)
    end_year : int
        Ending year
    end_month : int
        Ending month (1-12)
    date_column : str, optional
        Name of datetime column to filter on

    Returns
    -------
    pd.DataFrame
        Filtered dataframe
    """
    df = df.copy()

    # Ensure datetime type
    df[date_column] = pd.to_datetime(df[date_column])

    # Create start and end dates
    start_date = pd.Timestamp(year=start_year, month=start_month, day=1)

    # End date is last day of end_month
    if end_month == 12:
        end_date = pd.Timestamp(year=end_year + 1, month=1, day=1) - pd.Timedelta(days=1)
    else:
        end_date = pd.Timestamp(year=end_year, month=end_month + 1, day=1) - pd.Timedelta(days=1)

    # Add time component to make it end of day
    end_date = end_date + pd.Timedelta(hours=23, minutes=59, seconds=59)

    # Filter
    filtered_df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]

    return filtered_df
