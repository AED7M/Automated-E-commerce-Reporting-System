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

def load_revenue_data(this_week_orders_data,last_week_orders_data,order_items_table):
    this_week_revenue_data = this_week_orders_data.merge(order_items_table, on="order_id")
    last_week_revenue_data = last_week_orders_data.merge(order_items_table, on="order_id")
    this_week_revenue_data.drop(columns = ['customer_id','order_item_id','shipping_limit_date','freight_value','seller_id','order_estimated_delivery_date','order_delivered_carrier_date','order_approved_at'],inplace=True)
    last_week_revenue_data.drop(columns = ['customer_id','order_item_id','shipping_limit_date','freight_value','seller_id','order_estimated_delivery_date','order_delivered_carrier_date','order_approved_at'],inplace=True)
    return this_week_revenue_data, last_week_revenue_data

def load_products_data(this_week_revenue_data,last_week_revenue_data,products_table,products_names_tabel):
    this_week_products_data = this_week_revenue_data.merge(products_table, on="product_id")
    last_week_products_data = last_week_revenue_data.merge(products_table, on="product_id")
    this_week_products_data.drop(columns=['product_width_cm','product_height_cm','product_length_cm','product_weight_g','product_photos_qty','product_description_lenght','product_name_lenght','product_id','order_status','order_id'],inplace=True)
    last_week_products_data.drop(columns=['product_width_cm','product_height_cm','product_length_cm','product_weight_g','product_photos_qty','product_description_lenght','product_name_lenght','product_id','order_status','order_id'],inplace=True)
    this_week_products_data = last_week_products_data.merge(products_names_tabel, on="product_category_name")
    last_week_products_data = last_week_products_data.merge(products_names_tabel, on="product_category_name")
    return this_week_products_data,last_week_products_data


def load_operational_insights_data(this_week_revenue_data,last_week_revenue_data,order_reviews_table):
    this_week_operational_insights_data = this_week_revenue_data.merge(order_reviews_table,on="order_id")
    last_week_operational_insights_data =last_week_revenue_data.merge(order_reviews_table,on="order_id")
    this_week_operational_insights_data.drop(columns=['review_answer_timestamp','review_creation_date','review_comment_message','review_comment_title','review_id','product_id','price','order_id'],inplace=True)
    last_week_operational_insights_data.drop(columns=['review_answer_timestamp','review_creation_date','review_comment_message','review_comment_title','review_id','product_id','price','order_id'],inplace=True)
    return this_week_operational_insights_data,last_week_operational_insights_data
