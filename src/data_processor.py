import os
from dotenv import load_dotenv
import pandas as pd

def load_files_paths():
    """
    Load file paths from environment variables.
    
    Reads configuration from .env file and returns dictionary of file paths
    for different data tables in the e-commerce system.
    
    Returns:
        dict: Dictionary containing file paths for orders, products, ordered_items,
             product_category, customers, order_reviews, and order_payment tables.
    """
    load_dotenv()
    file_paths = {
        'orders': os.getenv('orders_table_file_path'),
        'products': os.getenv('products_table_file_path'),
        'ordered_items': os.getenv('orderd_items_table_file_path'),
        'product_category': os.getenv('product_category_file_path'),
        'customers': os.getenv('customers_table_file_path'),
        'order_reviews': os.getenv('order_reviews_table_file_path'),
        'order_payment': os.getenv('order_payment_table_file_path')
    }
    return file_paths

def load_table(file_path):
    """
    Load CSV file into a pandas DataFrame.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        pandas.DataFrame: DataFrame containing the data from the CSV file.
    """
    table = pd.read_csv(file_path)
    return table

def load_orders_data(orders_table, this_week_start_date, this_week_last_date, last_week_start_date, last_week_end_date):
    """
    Filter orders data by date range for current and previous week.
    
    Args:
        orders_table (pandas.DataFrame): DataFrame containing order data.
        this_week_start_date (str): Start date for current week analysis.
        this_week_last_date (str): End date for current week analysis.
        last_week_start_date (str): Start date for previous week analysis.
        last_week_end_date (str): End date for previous week analysis.
        
    Returns:
        tuple: Two DataFrames containing:
            - this_week_orders_data: Orders for the current week
            - last_week_orders_data: Orders for the previous week
    """
    orders_table['order_purchase_timestamp'] = pd.to_datetime(orders_table['order_purchase_timestamp'])
    this_week_mask = (orders_table['order_purchase_timestamp'] >= this_week_start_date) & (orders_table['order_purchase_timestamp'] <= this_week_last_date)
    last_week_mask = (orders_table['order_purchase_timestamp'] >= last_week_start_date) & (orders_table['order_purchase_timestamp'] <= last_week_end_date)
    this_week_orders_data = orders_table[this_week_mask]
    last_week_orders_data = orders_table[last_week_mask]
    return this_week_orders_data, last_week_orders_data

def load_revenue_data(this_week_orders_data, last_week_orders_data, order_items_table):
    """
    Merge orders data with order items to generate revenue data for both weeks.
    
    Args:
        this_week_orders_data (pandas.DataFrame): Orders for the current week.
        last_week_orders_data (pandas.DataFrame): Orders for the previous week.
        order_items_table (pandas.DataFrame): Items ordered with prices.
        
    Returns:
        tuple: Two DataFrames containing:
            - this_week_revenue_data: Revenue data for the current week
            - last_week_revenue_data: Revenue data for the previous week
            
    Note:
        Removes unnecessary columns to focus on revenue calculation.
    """
    this_week_revenue_data = this_week_orders_data.merge(order_items_table, on="order_id")
    last_week_revenue_data = last_week_orders_data.merge(order_items_table, on="order_id")
    this_week_revenue_data.drop(columns = ['customer_id', 'order_item_id', 'shipping_limit_date', 'freight_value', 'seller_id', 'order_estimated_delivery_date', 'order_delivered_carrier_date', 'order_approved_at'], inplace=True)
    last_week_revenue_data.drop(columns = ['customer_id', 'order_item_id', 'shipping_limit_date', 'freight_value', 'seller_id', 'order_estimated_delivery_date', 'order_delivered_carrier_date', 'order_approved_at'], inplace=True)
    return this_week_revenue_data, last_week_revenue_data

def clean_product_categories(df, column_name='product_category_name_english'):
    """
    Clean product category names by converting underscores to spaces and capitalizing words.
    
    Args:
        df (pandas.DataFrame): DataFrame containing product categories.
        column_name (str): Name of the column containing categories to clean.
        
    Returns:
        pandas.DataFrame: DataFrame with cleaned category names.
        
    Notes:
        - Fixes specific typos in category names
        - Converts underscores to spaces
        - Capitalizes each word in category names
        - Handles NaN values safely
    """
    # Check if column exists
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in DataFrame.")
        return df
    
    # Fix specific typos first
    typo_corrections = {
        'fashio_female_clothing': 'fashion_female_clothing'
    }
    
    # Apply typo corrections
    df[column_name] = df[column_name].replace(typo_corrections)
    
    # Format all categories
    def format_category(cat_name):
        if pd.isna(cat_name):
            return cat_name
        # Replace underscores with spaces and capitalize each word
        words = str(cat_name).split('_')
        return ' '.join(word.capitalize() for word in words)
    
    # Apply the formatting to the original column
    df[column_name] = df[column_name].apply(format_category)
    
    return df

def load_products_data(this_week_revenue_data, last_week_revenue_data, products_table, products_names_tabel):
    """
    Merge revenue data with product information and translate category names.
    
    Args:
        this_week_revenue_data (pandas.DataFrame): Revenue data for current week.
        last_week_revenue_data (pandas.DataFrame): Revenue data for previous week.
        products_table (pandas.DataFrame): Product information.
        products_names_tabel (pandas.DataFrame): Product category name translations.
        
    Returns:
        tuple: Two DataFrames containing:
            - this_week_products_data: Enhanced product data for current week
            - last_week_products_data: Enhanced product data for previous week
            
    Note:
        - Removes unnecessary product details
        - Merges product category translations
        - Cleans category names for better readability
    """
    this_week_products_data = this_week_revenue_data.merge(products_table, on="product_id")
    last_week_products_data = last_week_revenue_data.merge(products_table, on="product_id")
    
    this_week_products_data.drop(columns=['product_width_cm', 'product_height_cm', 'product_length_cm', 'product_weight_g', 'product_photos_qty', 'product_description_lenght', 'product_name_lenght', 'product_id', 'order_status', 'order_id'], inplace=True)
    last_week_products_data.drop(columns=['product_width_cm', 'product_height_cm', 'product_length_cm', 'product_weight_g', 'product_photos_qty', 'product_description_lenght', 'product_name_lenght', 'product_id', 'order_status', 'order_id'], inplace=True)
    
    this_week_products_data = this_week_products_data.merge(products_names_tabel, on="product_category_name")
    last_week_products_data = last_week_products_data.merge(products_names_tabel, on="product_category_name")
    
    # Clean and format product categories
    this_week_products_data = clean_product_categories(this_week_products_data)
    last_week_products_data = clean_product_categories(last_week_products_data)
    
    return this_week_products_data, last_week_products_data

def load_operational_insights_data(this_week_revenue_data, last_week_revenue_data, order_reviews_table):
    """
    Generate operational insights by merging revenue data with order reviews.
    
    Args:
        this_week_revenue_data (pandas.DataFrame): Revenue data for current week.
        last_week_revenue_data (pandas.DataFrame): Revenue data for previous week.
        order_reviews_table (pandas.DataFrame): Customer reviews of orders.
        
    Returns:
        tuple: Two DataFrames containing:
            - this_week_operational_insights_data: Operational metrics for current week
            - last_week_operational_insights_data: Operational metrics for previous week
            
    Note:
        Removes unnecessary detail columns to focus on operational metrics.
    """
    this_week_operational_insights_data = this_week_revenue_data.merge(order_reviews_table, on="order_id")
    last_week_operational_insights_data = last_week_revenue_data.merge(order_reviews_table, on="order_id")
    this_week_operational_insights_data.drop(columns=['review_answer_timestamp', 'review_creation_date', 'review_comment_message', 'review_comment_title', 'review_id', 'product_id', 'price', 'order_id'], inplace=True)
    last_week_operational_insights_data.drop(columns=['review_answer_timestamp', 'review_creation_date', 'review_comment_message', 'review_comment_title', 'review_id', 'product_id', 'price', 'order_id'], inplace=True)
    return this_week_operational_insights_data, last_week_operational_insights_data

def prepare_sales_trend_data(revenue_data):
    """
    Prepare daily aggregated sales and order data for trend visualization,
    grouped by day of week.
    
    Args:
        revenue_data (pandas.DataFrame): Revenue data with order_purchase_timestamp and price columns
        
    Returns:
        tuple: Three lists containing:
            - day_names: List of day names (Mon, Tue, etc.)
            - daily_revenue: List of total revenue values for each day
            - order_counts: List of order counts for each day
    """
    # Ensure timestamp is datetime type
    daily_data = revenue_data.copy()
    daily_data['order_purchase_timestamp'] = pd.to_datetime(daily_data['order_purchase_timestamp'])
    
    # Extract day of week information
    daily_data['day_of_week'] = daily_data['order_purchase_timestamp'].dt.dayofweek  # 0=Monday, 6=Sunday
    daily_data['day_name'] = daily_data['order_purchase_timestamp'].dt.day_name()
    daily_data['day_abbr'] = daily_data['order_purchase_timestamp'].dt.strftime('%a')
    
    # Group by day of week to get daily totals
    grouped_revenue = daily_data.groupby('day_of_week').agg({
        'price': 'sum',
        'day_abbr': 'first'  # Get the day abbreviation
    })
    
    # Count unique orders per day of week
    order_counts = daily_data.groupby('day_of_week')['order_id'].nunique()
    
    # Sort by day of week (Monday first)
    grouped_revenue = grouped_revenue.sort_index()
    order_counts = order_counts.sort_index()
    
    # Create lists for visualization function
    day_names = grouped_revenue['day_abbr'].tolist()
    revenue_values = grouped_revenue['price'].tolist()
    count_values = order_counts.tolist()
    
    return day_names, revenue_values, count_values