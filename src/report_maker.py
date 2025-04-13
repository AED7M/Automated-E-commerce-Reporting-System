import os
import pandas as pd
from datetime import datetime, timedelta
import shutil
from jinja2 import Environment, FileSystemLoader

# Import modules for data processing, metrics calculation, visualizations, and text generation
from data_processor import (
    load_files_paths,
    load_table,
    load_orders_data,
    load_revenue_data,
    load_products_data,
    load_operational_insights_data,
    prepare_sales_trend_data
)

from metrics import (
    calculate_total_revenue,
    calculate_number_of_orders,
    calculate_average_order_value,
    get_top_category_metrics,
    calculate_average_delivery_time,
    calculate_average_order_rating
)

from visualizations import (
    setup_visualization_style,
    create_sales_trend_chart,
    create_top_categories_chart
)

from text_generator import (
    create_executive_summary,
    generate_sales_insights,
    generate_product_insights,
    generate_operational_insights
)

def generate_ecommerce_report(this_week_start=None, this_week_end=None):
    """
    Process e-commerce data and generate an HTML report with metrics, visualizations and insights.
    
    Args:
        this_week_start: Start date for current week (YYYY-MM-DD)
        this_week_end: End date for current week (YYYY-MM-DD)
        
    Returns:
        str: Path to the generated HTML report
    """
    try:
        # Initialize results container to store all calculated data
        results = {
            'dates': {},      # Date ranges for analysis
            'metrics': {},    # KPIs and calculated metrics
            'insights': {},   # Text insights and analysis
            'visualization_paths': {}  # Paths to generated charts
        }
        
        # Set default date range if not provided
        if not this_week_end:
            today = datetime.now()
            this_week_end = today.strftime('%Y-%m-%d')
            
        if not this_week_start:
            end_date = datetime.strptime(this_week_end, '%Y-%m-%d')
            start_date = end_date - timedelta(days=6)  # 7 day period
            this_week_start = start_date.strftime('%Y-%m-%d')
            
        # Calculate last week's date range for comparison
        this_week_start_dt = datetime.strptime(this_week_start, '%Y-%m-%d')
        last_week_end_dt = this_week_start_dt - timedelta(days=1)
        last_week_start_dt = last_week_end_dt - timedelta(days=6)  # 7 day period
        
        results['dates'] = {
            'this_week_start': this_week_start,
            'this_week_end': this_week_end,
            'last_week_start': last_week_start_dt.strftime('%Y-%m-%d'),
            'last_week_end': last_week_end_dt.strftime('%Y-%m-%d')
        }
        
        print(f"Generating report for period: {this_week_start} to {this_week_end}")
        print(f"Comparison period: {results['dates']['last_week_start']} to {results['dates']['last_week_end']}\n")
        
        # Create directories for outputs
        visualization_dir = 'data/assets/plots'
        reports_dir = 'data/reports'
        os.makedirs(visualization_dir, exist_ok=True)
        os.makedirs(reports_dir, exist_ok=True)
        
        # STEP 1: LOAD DATA
        print("Loading data tables...")
        file_paths = load_files_paths()
        
        # Verify required files exist
        required_files = ['orders', 'ordered_items', 'products', 'product_category', 'order_reviews']
        missing_files = [f for f in required_files if not file_paths.get(f) or not os.path.exists(file_paths[f])]
        
        if missing_files:
            raise FileNotFoundError(f"Missing required files: {', '.join(missing_files)}")
        
        # Load tables and prepare data
        orders_table = load_table(file_paths['orders'])
        order_items_table = load_table(file_paths['ordered_items'])
        products_table = load_table(file_paths['products'])
        product_category_table = load_table(file_paths['product_category'])
        order_reviews_table = load_table(file_paths['order_reviews'])
        
        this_week_orders, last_week_orders = load_orders_data(
            orders_table, 
            this_week_start, 
            this_week_end, 
            results['dates']['last_week_start'], 
            results['dates']['last_week_end']
        )
        
        this_week_revenue, last_week_revenue = load_revenue_data(
            this_week_orders,
            last_week_orders,
            order_items_table
        )
        
        this_week_products, last_week_products = load_products_data(
            this_week_revenue,
            last_week_revenue,
            products_table,
            product_category_table
        )
        
        this_week_ops, last_week_ops = load_operational_insights_data(
            this_week_revenue,
            last_week_revenue,
            order_reviews_table
        )
        
        print("✓ Data loaded successfully\n")
        
        # STEP 2: CALCULATE METRICS
        print("Calculating metrics...")
        
        # Calculate KPIs with week-over-week comparison
        results['metrics']['revenue'] = calculate_total_revenue(this_week_revenue, last_week_revenue)
        results['metrics']['orders'] = calculate_number_of_orders(this_week_revenue, last_week_revenue)
        results['metrics']['aov'] = calculate_average_order_value(this_week_revenue, last_week_revenue)
        results['metrics']['categories'] = get_top_category_metrics(
            this_week_products,
            last_week_products,
            max_categories=5
        )
        results['metrics']['delivery'] = calculate_average_delivery_time(this_week_ops, last_week_ops)
        results['metrics']['satisfaction'] = calculate_average_order_rating(this_week_ops, last_week_ops)
        
        # Prepare data for sales trend visualization
        day_names, revenue_values, order_counts = prepare_sales_trend_data(this_week_revenue)
        results['metrics']['sales_trend'] = (day_names, revenue_values, order_counts)
        
        print("✓ Metrics calculated successfully\n")
        
        # STEP 3: GENERATE TEXT INSIGHTS
        print("Generating insights...")
        
        # Create text insights from calculated metrics
        results['insights']['executive_summary'] = create_executive_summary(
            results['metrics']['revenue'],
            results['metrics']['orders'],
            results['metrics']['aov'],
            results['metrics']['categories']
        )
        
        results['insights']['sales'] = generate_sales_insights(
            results['metrics']['revenue'],
            results['metrics']['orders'],
            results['metrics']['sales_trend']
        )
        
        results['insights']['products'] = generate_product_insights(
            results['metrics']['categories']
        )
        
        results['insights']['operations'] = generate_operational_insights(
            results['metrics']['delivery'],
            results['metrics']['satisfaction']
        )
        
        print("✓ Text insights generated successfully\n")
        
        # STEP 4: CREATE AND SAVE VISUALIZATIONS
        print("Creating visualizations...")
        
        setup_visualization_style()
        
        # Create date-based filenames for consistent naming
        start_date_tag = results['dates']['this_week_start'].replace('-', '')
        end_date_tag = results['dates']['this_week_end'].replace('-', '')
        period_tag = f"{start_date_tag}_{end_date_tag}"
        
        # Generate sales trend chart
        sales_trend_filename = f"sales_trend_{period_tag}.png"
        sales_trend_path = os.path.join(visualization_dir, sales_trend_filename)
        
        create_sales_trend_chart(
            results['metrics']['sales_trend'][0],
            results['metrics']['sales_trend'][1],
            results['metrics']['sales_trend'][2],
            output_path=sales_trend_path
        )
        
        results['visualization_paths']['sales_trend'] = sales_trend_path
        
        # Generate top categories chart
        categories_filename = f"top_categories_{period_tag}.png"
        categories_path = os.path.join(visualization_dir, categories_filename)
        
        create_top_categories_chart(
            results['metrics']['categories'][0],
            results['metrics']['categories'][1],
            results['metrics']['categories'][2],
            results['metrics']['categories'][3],
            results['metrics']['categories'][4],
            results['metrics']['categories'][5],
            results['metrics']['categories'][6],
            max_categories=5,
            output_path=categories_path
        )
        
        results['visualization_paths']['top_categories'] = categories_path
        
        print(f"✓ Visualizations saved to: {visualization_dir}\n")
        
        # STEP 5: GENERATE HTML REPORT
        print("Generating HTML report...")
        
        # Setup Jinja2 template engine
        template_dir = 'templates'
        env = Environment(loader=FileSystemLoader(template_dir))
        env.filters['format_currency'] = lambda value: f"{float(value):,.2f}"
        env.filters['round'] = lambda value, precision: round(float(value), precision)
        
        template = env.get_template('report_template.html')
        
        # Copy CSS file for report styling
        css_source = os.path.join(template_dir, 'report_template.css')
        css_dest = os.path.join(reports_dir, 'report_template.css')
        shutil.copyfile(css_source, css_dest)
        
        # Structure metrics for easier template access
        metrics = {
            'revenue': {
                'this_week': results['metrics']['revenue'][0],
                'last_week': results['metrics']['revenue'][1],
                'percent_change': results['metrics']['revenue'][2],
                'sign': results['metrics']['revenue'][3],
                'trend': results['metrics']['revenue'][4]
            },
            'orders': {
                'this_week': results['metrics']['orders'][0],
                'last_week': results['metrics']['orders'][1],
                'percent_change': results['metrics']['orders'][2],
                'sign': results['metrics']['orders'][3],
                'trend': results['metrics']['orders'][4]
            },
            'aov': {
                'this_week': results['metrics']['aov'][0],
                'last_week': results['metrics']['aov'][1],
                'percent_change': results['metrics']['aov'][2],
                'sign': results['metrics']['aov'][3],
                'trend': results['metrics']['aov'][4]
            },
            'categories': {
                'top_categories': results['metrics']['categories'][0],
                'top_sales': results['metrics']['categories'][1],
                'daily_rates': results['metrics']['categories'][2],
                'last_week_sales': results['metrics']['categories'][3],
                'percent_changes': results['metrics']['categories'][4],
                'signs': results['metrics']['categories'][5],
                'trends': results['metrics']['categories'][6]
            },
            'delivery': {
                'this_week': results['metrics']['delivery'][0],
                'last_week': results['metrics']['delivery'][1],
                'percent_change': results['metrics']['delivery'][2],
                'sign': results['metrics']['delivery'][3],
                'trend': results['metrics']['delivery'][4]
            },
            'satisfaction': {
                'this_week': results['metrics']['satisfaction'][0],
                'difference': results['metrics']['satisfaction'][1],
                'sign': results['metrics']['satisfaction'][2],
                'trend': results['metrics']['satisfaction'][3]
            }
        }
        
        # Pre-calculate values needed for the template
        delivery_time_diff = abs(metrics['delivery']['this_week'] - metrics['delivery']['last_week'])
        
        # Prepare template context
        context = {
            'report_dates': results['dates'],
            'metrics': metrics,
            'delivery_time_diff': delivery_time_diff,
            'executive_summary': results['insights']['executive_summary'],
            'sales_insights': results['insights']['sales'],
            'product_insights': results['insights']['products'],
            'operational_insights': results['insights']['operations'],
            'sales_trend_path': '../assets/plots/' + os.path.basename(sales_trend_path),
            'top_categories_path': '../assets/plots/' + os.path.basename(categories_path),
            'generation_date': datetime.now().strftime('%Y-%m-%d at %H:%M:%S'),
            'range': range,
            'len': len
        }
        
        # Create HTML report with date-based filename
        html_filename = f"report_{period_tag}.html"
        html_path = os.path.join(reports_dir, html_filename)
        
        # Render and save the report
        html_content = template.render(**context)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTML report generated: {html_path}")
        print("\n✅ Report generation completed successfully!")
        
        results['report_path'] = html_path
        return html_path
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    report_path = generate_ecommerce_report('2017-05-01', '2017-05-07')
    print(f"Report saved to: {report_path}")
