import pandas as pd
import math

def calculate_percent_change(current, previous, inverse_trend=False):
    """
    Calculate percentage change and determine trend.
    
    Args:
        current: Current period value
        previous: Previous period value
        inverse_trend: If True, a negative change is considered positive (e.g., for delivery times)
    
    Returns:
        tuple: (percent_change, sign, trend)
    """
    if previous != 0:
        percent_change = ((current - previous) / previous) * 100
        if percent_change == 0:
            sign = ''
            trend = 'neutral'
        else:
            if inverse_trend:
                sign = '+' if percent_change < 0 else '-'
                trend = 'positive' if percent_change < 0 else 'negative'
            else:
                sign = '+' if percent_change > 0 else '-'
                trend = 'positive' if percent_change > 0 else 'negative'
    else:
        percent_change = 0
        sign = ''
        trend = 'neutral'
    
    return round(abs(percent_change), 1), sign, trend

def calculate_total_revenue(this_week_revenue_data, last_week_revenue_data):
    """
    Calculate total revenue metrics comparing current week to previous week.
    
    Args:
        this_week_revenue_data (DataFrame): Current week's revenue data with 'price' column
        last_week_revenue_data (DataFrame): Previous week's revenue data with 'price' column
    
    Returns:
        tuple: (this_week_total_revenue, last_week_total_revenue, percent_change, sign, trend)
            - this_week_total_revenue: Total revenue for current week
            - last_week_total_revenue: Total revenue for previous week
            - percent_change: Absolute percentage change (rounded to 1 decimal place)
            - sign: '+', '-', or '' (empty for no change)
            - trend: 'positive', 'negative', or 'neutral'
    """
    this_week_total_revenue = this_week_revenue_data['price'].sum()
    last_week_total_revenue = last_week_revenue_data['price'].sum()
    
    percent_change, sign, trend = calculate_percent_change(this_week_total_revenue, last_week_total_revenue)
    
    return this_week_total_revenue, last_week_total_revenue, percent_change, sign, trend

def calculate_number_of_orders(this_week_revenue_data, last_week_revenue_data):
    """
    Calculate order count metrics comparing current week to previous week.
    
    Args:
        this_week_revenue_data (DataFrame): Current week's revenue data
        last_week_revenue_data (DataFrame): Previous week's revenue data
    
    Returns:
        tuple: (this_week_number_of_order, last_week_number_of_order, percent_change, sign, trend)
            - this_week_number_of_order: Number of orders in current week
            - last_week_number_of_order: Number of orders in previous week
            - percent_change: Absolute percentage change (rounded to 1 decimal place)
            - sign: '+', '-', or '' (empty for no change)
            - trend: 'positive', 'negative', or 'neutral'
    """
    this_week_number_of_order = len(this_week_revenue_data)
    last_week_number_of_order = len(last_week_revenue_data)
    
    percent_change, sign, trend = calculate_percent_change(this_week_number_of_order, last_week_number_of_order)
    
    return this_week_number_of_order, last_week_number_of_order, percent_change, sign, trend

def calculate_average_order_value(this_week_revenue_data, last_week_revenue_data):
    """
    Calculate average order value metrics comparing current week to previous week.
    
    Args:
        this_week_revenue_data (DataFrame): Current week's revenue data with 'price' column
        last_week_revenue_data (DataFrame): Previous week's revenue data with 'price' column
    
    Returns:
        tuple: (this_week_average_order_value, last_week_average_order_value, percent_change, sign, trend)
            - this_week_average_order_value: Average order value for current week
            - last_week_average_order_value: Average order value for previous week
            - percent_change: Absolute percentage change (rounded to 1 decimal place)
            - sign: '+', '-', or '' (empty for no change)
            - trend: 'positive', 'negative', or 'neutral'
    """
    this_week_average_order_value = this_week_revenue_data['price'].mean()
    last_week_average_order_value = last_week_revenue_data['price'].mean()
    
    percent_change, sign, trend = calculate_percent_change(this_week_average_order_value, last_week_average_order_value)
    
    return this_week_average_order_value, last_week_average_order_value, percent_change, sign, trend

def get_top_category_metrics(this_week_products_data, last_week_products_data, max_categories=3):
    """
    Identify top product categories by sales and calculate related metrics.
    
    Args:
        this_week_products_data (DataFrame): Current week's product data with columns:
                                           'product_category_name_english' and 'price'
        last_week_products_data (DataFrame): Previous week's product data with same columns
        max_categories (int, optional): Maximum number of top categories to return (default: 3)
    
    Returns:
        tuple: Multiple tuples containing:
            - this_week_top_categories: Top categories by sales for current week
            - this_week_top_products_sales: Sales amount for top categories
            - daily_order_rates: Average daily orders for top categories (rounded up)
            - last_week_sales: Sales amount for the same categories in previous week
            - percent_changes: Percentage changes between weeks for each category
            - signs: '+', '-', or '' for each category
            - trends: 'positive', 'negative', or 'neutral' for each category
    """
    # Get this week's top categories and their sales
    this_week_data = this_week_products_data.groupby('product_category_name_english')['price'].sum().nlargest(max_categories)
    this_week_top_categories = tuple(this_week_data.index)
    this_week_top_products_sales = tuple(this_week_data.values)
    
    # Count orders for each of the top categories and calculate daily average
    daily_order_rates = []
    for category in this_week_top_categories:
        # Count occurrences of this category in the dataset
        count = (this_week_products_data['product_category_name_english'] == category).sum()
        
        # Calculate daily average by dividing by 7 and rounding up
        daily_rate = math.ceil(count / 7)  # Use ceil to round up
        daily_order_rates.append(daily_rate)

    # Convert to tuples
    daily_order_rates = tuple(daily_order_rates)
    
    # Calculate sales for these same categories in the last week
    last_week_sales = []
    percent_changes = []
    signs = []
    trends = []
    
    for category in this_week_top_categories:
        # Get last week's sales for this category
        last_week_category_sales = last_week_products_data[
            last_week_products_data['product_category_name_english'] == category
        ]['price'].sum()
        
        last_week_sales.append(last_week_category_sales)
        
        # Calculate percentage change
        percent_change, sign, trend = calculate_percent_change(this_week_data[category], last_week_category_sales)
        
        percent_changes.append(percent_change)
        signs.append(sign)
        trends.append(trend)
    
    # Convert lists to tuples
    last_week_sales = tuple(last_week_sales)
    percent_changes = tuple(percent_changes)
    signs = tuple(signs)
    trends = tuple(trends)
    
    return this_week_top_categories, this_week_top_products_sales, daily_order_rates, last_week_sales, percent_changes, signs, trends

def get_mean_delivery_time(operational_insights_data):
    """
    Calculate the mean delivery time from order purchase to customer delivery.
    
    Filters out outliers by excluding delivery times over 50 days.
    
    Args:
        operational_insights_data (DataFrame): Operations data with columns:
                                             'order_status', 'order_delivered_customer_date',
                                             and 'order_purchase_timestamp'
    
    Returns:
        float: Mean delivery time in days for delivered orders
    """
    # Make sure the timestamp columns are datetime type
    operational_insights_data['order_delivered_customer_date'] = pd.to_datetime(operational_insights_data['order_delivered_customer_date'])
    operational_insights_data['order_purchase_timestamp'] = pd.to_datetime(operational_insights_data['order_purchase_timestamp'])

    # Filter for delivered orders
    delivered_orders = operational_insights_data[operational_insights_data['order_status'] == 'delivered']

    # Calculate delivery times
    delivery_times = delivered_orders['order_delivered_customer_date'] - delivered_orders['order_purchase_timestamp']

    # Convert to days
    delivery_days = delivery_times.dt.total_seconds() / (86400)  # 86400 seconds in a day

    # Filter for delivery times less than 50 days
    filtered_delivery_days = delivery_days[delivery_days < 50]

    # Calculate the mean
    return filtered_delivery_days.mean()

def calculate_average_delivery_time(this_week_operational_insights_data, last_week_operational_insights_data):
    """
    Calculate average delivery time metrics comparing current week to previous week.
    
    Note: For delivery time, a reduction (negative change) is considered positive.
    
    Args:
        this_week_operational_insights_data (DataFrame): Current week's operational data
        last_week_operational_insights_data (DataFrame): Previous week's operational data
        
    Returns:
        tuple: (this_week_mean_delivery_time, last_week_mean_delivery_time, percent_change, sign, trend)
            - this_week_mean_delivery_time: Average delivery time for current week (in days)
            - last_week_mean_delivery_time: Average delivery time for previous week (in days)
            - percent_change: Absolute percentage change (rounded to 1 decimal place)
            - sign: '+' (for faster delivery), '-' (for slower delivery), or '' (no change)
            - trend: 'positive' (for faster delivery), 'negative' (for slower delivery), or 'neutral'
    """
    this_week_mean_delivery_time = get_mean_delivery_time(this_week_operational_insights_data)
    last_week_mean_delivery_time = get_mean_delivery_time(last_week_operational_insights_data)
    
    # For delivery time, a reduction is positive, so we use inverse_trend=True
    percent_change, sign, trend = calculate_percent_change(
        this_week_mean_delivery_time, 
        last_week_mean_delivery_time, 
        inverse_trend=True
    )
    
    return this_week_mean_delivery_time, last_week_mean_delivery_time, percent_change, sign, trend

def calculate_average_order_rating(this_week_operational_insights_data, last_week_operational_insights_data):
    """
    Calculate average order rating metrics comparing current week to previous week.
    
    Args:
        this_week_operational_insights_data (DataFrame): Current week's operational data with 'review_score' column
        last_week_operational_insights_data (DataFrame): Previous week's operational data with 'review_score' column
        
    Returns:
        tuple: (this_week_average_order_rating, difference, sign, trend)
            - this_week_average_order_rating: Average review score for current week
            - difference: Absolute difference between current and previous week's ratings
            - sign: '+' (for higher rating), '-' (for lower rating), or '' (no change)
            - trend: 'positive' (for higher rating), 'negative' (for lower rating), or 'neutral'
    """
    this_week_average_order_rating = this_week_operational_insights_data['review_score'].mean()
    last_week_average_order_rating = last_week_operational_insights_data['review_score'].mean()
    
    # Calculate the difference (not percentage)
    raw_difference = this_week_average_order_rating - last_week_average_order_rating
    
    # Determine sign and trend with proper threshold to avoid tiny differences
    if abs(raw_difference) < 0.05: 
        difference = 0.0
        sign = ''
        trend = 'neutral'
    else:
        difference = round(abs(raw_difference), 1)
        sign = '+' if raw_difference > 0 else '-'
        trend = 'positive' if raw_difference > 0 else 'negative'
    
    return this_week_average_order_rating, difference, sign, trend