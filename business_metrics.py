"""
Business Metrics Calculation Module

This module provides functions for calculating key business metrics
from e-commerce sales data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


def calculate_total_revenue(sales_data: pd.DataFrame) -> float:
    """
    Calculate total revenue from sales data.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'price' column

    Returns
    -------
    float
        Total revenue
    """
    return sales_data['price'].sum()


def calculate_revenue_by_period(sales_data: pd.DataFrame,
                                period: str = 'month') -> pd.DataFrame:
    """
    Calculate revenue grouped by time period.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'price' and period columns ('year', 'month')
    period : str, optional
        Time period to group by: 'month', 'year', or 'year-month'

    Returns
    -------
    pd.DataFrame
        Revenue by period
    """
    if period == 'year':
        revenue = sales_data.groupby('year')['price'].sum().reset_index()
        revenue.columns = ['year', 'revenue']
    elif period == 'month':
        revenue = sales_data.groupby('month')['price'].sum().reset_index()
        revenue.columns = ['month', 'revenue']
    elif period == 'year-month':
        revenue = sales_data.groupby(['year', 'month'])['price'].sum().reset_index()
        revenue.columns = ['year', 'month', 'revenue']
    else:
        raise ValueError(f"Invalid period: {period}. Choose 'year', 'month', or 'year-month'")

    return revenue


def calculate_revenue_growth(current_revenue: float,
                            previous_revenue: float) -> float:
    """
    Calculate revenue growth rate between two periods.

    Parameters
    ----------
    current_revenue : float
        Revenue for current period
    previous_revenue : float
        Revenue for previous period

    Returns
    -------
    float
        Growth rate as decimal (e.g., 0.10 for 10% growth)
    """
    if previous_revenue == 0:
        return 0.0

    growth = (current_revenue - previous_revenue) / previous_revenue
    return growth


def calculate_mom_growth(revenue_by_month: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate month-over-month growth rates.

    Parameters
    ----------
    revenue_by_month : pd.DataFrame
        Revenue by month with 'month' and 'revenue' columns

    Returns
    -------
    pd.DataFrame
        Revenue by month with added 'mom_growth' column
    """
    result = revenue_by_month.copy()
    result['mom_growth'] = result['revenue'].pct_change()
    return result


def calculate_average_order_value(sales_data: pd.DataFrame) -> float:
    """
    Calculate average order value (AOV).

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'order_id' and 'price' columns

    Returns
    -------
    float
        Average order value
    """
    order_totals = sales_data.groupby('order_id')['price'].sum()
    return order_totals.mean()


def calculate_total_orders(sales_data: pd.DataFrame) -> int:
    """
    Calculate total number of unique orders.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'order_id' column

    Returns
    -------
    int
        Total number of unique orders
    """
    return sales_data['order_id'].nunique()


def calculate_revenue_by_category(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate revenue by product category.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'product_category_name' and 'price' columns

    Returns
    -------
    pd.DataFrame
        Revenue by category, sorted in descending order
    """
    category_revenue = (
        sales_data.groupby('product_category_name')['price']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    category_revenue.columns = ['category', 'revenue']

    return category_revenue


def calculate_revenue_by_state(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate revenue by customer state.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'customer_state' and 'price' columns

    Returns
    -------
    pd.DataFrame
        Revenue by state, sorted in descending order
    """
    state_revenue = (
        sales_data.groupby('customer_state')['price']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    state_revenue.columns = ['state', 'revenue']

    return state_revenue


def calculate_average_review_score(sales_data: pd.DataFrame) -> float:
    """
    Calculate average review score.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'review_score' column

    Returns
    -------
    float
        Average review score
    """
    return sales_data['review_score'].mean()


def calculate_review_score_distribution(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate distribution of review scores.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'review_score' column

    Returns
    -------
    pd.DataFrame
        Count and percentage for each review score
    """
    # Get unique orders with their review scores
    review_data = sales_data[['order_id', 'review_score']].drop_duplicates()

    distribution = review_data['review_score'].value_counts().sort_index()
    percentage = review_data['review_score'].value_counts(normalize=True).sort_index() * 100

    result = pd.DataFrame({
        'review_score': distribution.index,
        'count': distribution.values,
        'percentage': percentage.values
    })

    return result


def calculate_average_delivery_time(sales_data: pd.DataFrame) -> float:
    """
    Calculate average delivery time in days.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'delivery_speed_days' column

    Returns
    -------
    float
        Average delivery time in days
    """
    # Get unique orders with delivery times
    delivery_data = sales_data[['order_id', 'delivery_speed_days']].drop_duplicates()

    return delivery_data['delivery_speed_days'].mean()


def calculate_review_by_delivery_speed(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average review score by delivery speed category.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'delivery_category' and 'review_score' columns

    Returns
    -------
    pd.DataFrame
        Average review score by delivery category
    """
    # Get unique orders
    review_delivery = sales_data[
        ['order_id', 'delivery_category', 'review_score']
    ].drop_duplicates()

    result = (
        review_delivery.groupby('delivery_category')['review_score']
        .mean()
        .reset_index()
    )
    result.columns = ['delivery_category', 'avg_review_score']

    # Sort by delivery speed
    category_order = ['1-3 days', '4-7 days', '8+ days']
    result['delivery_category'] = pd.Categorical(
        result['delivery_category'],
        categories=category_order,
        ordered=True
    )
    result = result.sort_values('delivery_category')

    return result


def calculate_order_status_distribution(orders_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate distribution of order statuses.

    Parameters
    ----------
    orders_data : pd.DataFrame
        Orders dataset with 'order_status' column

    Returns
    -------
    pd.DataFrame
        Count and percentage for each order status
    """
    distribution = orders_data['order_status'].value_counts()
    percentage = orders_data['order_status'].value_counts(normalize=True) * 100

    result = pd.DataFrame({
        'order_status': distribution.index,
        'count': distribution.values,
        'percentage': percentage.values
    })

    return result


def calculate_items_per_order(sales_data: pd.DataFrame) -> float:
    """
    Calculate average number of items per order.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'order_id' column

    Returns
    -------
    float
        Average items per order
    """
    items_per_order = sales_data.groupby('order_id').size()
    return items_per_order.mean()


def compare_periods(current_period_data: pd.DataFrame,
                   previous_period_data: pd.DataFrame,
                   metric_name: str = 'revenue') -> Dict[str, float]:
    """
    Compare key metrics between two time periods.

    Parameters
    ----------
    current_period_data : pd.DataFrame
        Sales data for current period
    previous_period_data : pd.DataFrame
        Sales data for previous period
    metric_name : str, optional
        Name of metric being compared

    Returns
    -------
    Dict[str, float]
        Dictionary with current value, previous value, change, and growth rate
    """
    # Calculate totals
    current_revenue = calculate_total_revenue(current_period_data)
    previous_revenue = calculate_total_revenue(previous_period_data)

    # Calculate growth
    growth_rate = calculate_revenue_growth(current_revenue, previous_revenue)
    absolute_change = current_revenue - previous_revenue

    # Calculate other key metrics
    current_aov = calculate_average_order_value(current_period_data)
    previous_aov = calculate_average_order_value(previous_period_data)
    aov_growth = calculate_revenue_growth(current_aov, previous_aov)

    current_orders = calculate_total_orders(current_period_data)
    previous_orders = calculate_total_orders(previous_period_data)
    orders_growth = calculate_revenue_growth(current_orders, previous_orders)

    return {
        'current_revenue': current_revenue,
        'previous_revenue': previous_revenue,
        'revenue_change': absolute_change,
        'revenue_growth_rate': growth_rate,
        'current_aov': current_aov,
        'previous_aov': previous_aov,
        'aov_growth_rate': aov_growth,
        'current_orders': current_orders,
        'previous_orders': previous_orders,
        'orders_growth_rate': orders_growth
    }


def generate_summary_statistics(sales_data: pd.DataFrame,
                                orders_data: pd.DataFrame) -> Dict[str, any]:
    """
    Generate comprehensive summary statistics for a period.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with all relevant columns
    orders_data : pd.DataFrame
        Orders dataset for status analysis

    Returns
    -------
    Dict[str, any]
        Dictionary containing all key metrics
    """
    summary = {
        'total_revenue': calculate_total_revenue(sales_data),
        'total_orders': calculate_total_orders(sales_data),
        'average_order_value': calculate_average_order_value(sales_data),
        'average_items_per_order': calculate_items_per_order(sales_data),
    }

    # Add review metrics if available
    if 'review_score' in sales_data.columns:
        summary['average_review_score'] = calculate_average_review_score(sales_data)

    # Add delivery metrics if available
    if 'delivery_speed_days' in sales_data.columns:
        summary['average_delivery_days'] = calculate_average_delivery_time(sales_data)

    return summary
