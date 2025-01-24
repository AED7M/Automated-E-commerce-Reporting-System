import os
from dotenv import load_dotenv
import pandas as pd

def load_files_paths():
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
    table = pd.read_csv(file_path)
    return table

def load_orders_data(orders_table, this_week_start_date, this_week_last_date, last_week_start_date, last_week_end_date):
    orders_table['order_purchase_timestamp'] = pd.to_datetime(orders_table['order_purchase_timestamp'])
    this_week_mask = (orders_table['order_purchase_timestamp'] >= this_week_start_date) & (orders_table['order_purchase_timestamp'] <= this_week_last_date)
    last_week_mask = (orders_table['order_purchase_timestamp'] >= last_week_start_date) & (orders_table['order_purchase_timestamp'] <= last_week_end_date)
    this_week_orders_data = orders_table[this_week_mask]
    last_week_orders_data = orders_table[last_week_mask]
    return this_week_orders_data,last_week_orders_data

def load_revenue_data(orders_table, this_week_orders_data,last_week_orders_data,order_payment_table):
    this_week_revenue_data = this_week_orders_data.merge(order_payment_table, on="order_id")
    last_week_revenue_data = last_week_orders_data.merge(order_payment_table, on="order_id")
    return this_week_revenue_data, last_week_revenue_data








