import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter

def setup_colors():
    """
    Set up color palette for visualizations to match report CSS variables.
    
    Returns:
        dict: Dictionary of color codes for various elements
    """
    colors = {
        'primary': '#263A47',
        'secondary': '#445B6A',
        'accent': '#728495',
        'background': '#98A9BE',
        'highlight': '#84C5DB',
        'positive': '#27ae60',
        'negative': '#e74c3c'
    }
    return colors

def setup_visualization_style(colors=None):
    """
    Set up the visualization style to match the report's theme.
    
    Args:
        colors (dict, optional): Dictionary of color codes. If None, will call setup_colors().
    
    Returns:
        dict: The colors dictionary used for styling
    """
    if colors is None:
        colors = setup_colors()
    
    try:
        fm.findfont('Roboto')
        plt.rcParams['font.family'] = 'Roboto'
    except:
        plt.rcParams['font.family'] = 'sans-serif'
    
    custom_palette = [colors['primary'], colors['highlight'], colors['accent'], 
                     colors['secondary'], colors['background']]
    
    sns.set_theme(style="whitegrid", font='sans-serif')
    sns.set_palette(custom_palette)
    
    # Use consistent font sizes 
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 20
    
    # Set a fixed figure size that matches the report width
    # This ensures consistently sized charts that don't look stretched
    plt.rcParams['figure.figsize'] = (10, 6)  # Standard 16:9 aspect ratio
    plt.rcParams['figure.dpi'] = 150
    
    return colors

def create_sales_trend_chart(day_names, 
                           daily_revenue, 
                           order_counts, 
                           output_path='sales_trend_chart.png'):
    """
    Create a combination chart showing sales trends by day of week:
    - Line chart for revenue
    - Bar chart for number of orders
    """
    if not day_names or not daily_revenue or not order_counts or len(day_names) != len(daily_revenue) or len(day_names) != len(order_counts):
        print("Error: Invalid input data for sales trend chart")
        return False
        
    colors = setup_colors()
    
    sales_data = pd.DataFrame({
        'Day': day_names,
        'Revenue': daily_revenue,
        'Orders': order_counts
    })
    
    def currency_formatter(x, pos):
        return f'${x:,.0f}'
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    
    # Adjust bar width for better proportions
    bar_width = 0.6
    bars = ax2.bar(np.arange(len(sales_data)), sales_data['Orders'], 
                  color=colors['highlight'], alpha=0.6, width=bar_width)
    
    # Use thicker lines for better visibility
    line = ax1.plot(np.arange(len(sales_data)), sales_data['Revenue'], 
                   marker='o', linestyle='-', linewidth=2.5, 
                   color=colors['primary'], markerfacecolor='white', 
                   markeredgecolor=colors['primary'], markersize=8)
    
    ax1.set_ylabel('Daily Revenue ($)', color=colors['primary'], fontweight='bold')
    ax1.tick_params(axis='y', colors=colors['primary'])
    ax1.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
    
    ax2.set_ylabel('Number of Orders', color=colors['highlight'], fontweight='bold')
    ax2.tick_params(axis='y', colors=colors['highlight'])
    
    ax1.set_xticks(range(len(sales_data)))
    ax1.set_xticklabels(sales_data['Day'])
    
    # Set y-axis limits with 10% padding for better visualization
    ax1.set_ylim(0, max(daily_revenue) * 1.1)
    ax2.set_ylim(0, max(order_counts) * 1.1)
    
    ax1.set_title('Daily Sales Performance', fontweight='bold', pad=15)
    
    ax1.grid(True, axis='y', alpha=0.2, linestyle='--')
    ax2.grid(False)
    
    # Place legend outside plot area to avoid overlapping with data
    custom_lines = [
        plt.Line2D([0], [0], color=colors['primary'], lw=2.5, marker='o', markerfacecolor='white'),
        plt.Rectangle((0, 0), 1, 1, color=colors['highlight'], alpha=0.6)
    ]
    
    legend = ax1.legend(custom_lines, ['Revenue', 'Number of Orders'], 
              loc='upper center', 
              bbox_to_anchor=(0.5, -0.12),
              frameon=True,
              framealpha=0.9,
              ncol=2)
    
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('none')
    
    # Use tight layout with adjusted padding
    plt.tight_layout(rect=[0.02, 0.05, 0.98, 0.95])
    
    try:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return True
    except Exception as e:
        print(f"Error saving sales trend chart: {e}")
        plt.close()
        return False

def create_top_categories_chart(categories, 
                               sales,
                               daily_rates=None,
                               prev_week_sales=None,
                               percent_changes=None,
                               signs=None,
                               trends=None,
                               max_categories=5,
                               output_path='top_categories_chart.png'):
    """
    Create a vertical column chart showing top product categories by sales.
    """
    if not categories or not sales or len(categories) != len(sales):
        print("Error: Invalid input data for top categories chart")
        return False
        
    colors = setup_colors()
    
    if max_categories < len(categories):
        categories = categories[:max_categories]
        sales = sales[:max_categories]
        if daily_rates:
            daily_rates = daily_rates[:max_categories]
        if prev_week_sales:
            prev_week_sales = prev_week_sales[:max_categories]
        if percent_changes:
            percent_changes = percent_changes[:max_categories]
        if signs:
            signs = signs[:max_categories]
        if trends:
            trends = trends[:max_categories]
    
    category_data = pd.DataFrame({
        'Category': list(categories),
        'Sales': list(sales)
    })
    
    if daily_rates:
        category_data['Daily Orders'] = list(daily_rates)
        
    if prev_week_sales:
        category_data['Prev Sales'] = list(prev_week_sales)
        
    if percent_changes:
        category_data['Change %'] = list(percent_changes)
    
    category_data.sort_values('Sales', ascending=False, inplace=True)
    
    plt.figure(figsize=(10, 6))
    
    # Adjust bar width based on number of categories
    bar_width = 0.65
    if len(category_data) <= 3:
        bar_width = 0.5
    
    bar_plot = sns.barplot(
        x='Category', 
        y='Sales', 
        data=category_data,
        color=colors['primary'],
        width=bar_width
    )
    
    def currency_formatter(x, pos):
        return f'${x:,.0f}'
    bar_plot.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
    
    plt.title('Top Product Categories by Revenue', fontweight='bold', pad=20)
    plt.ylabel('Revenue ($)', fontweight='bold')
    plt.xlabel('')
    
    # Improve readability of category labels
    plt.xticks(rotation=25, ha='right')
    
    # Add 10% padding at the top for better visualization
    plt.ylim(0, max(sales) * 1.1)
    
    plt.grid(axis='y', alpha=0.2, linestyle='--')
    
    # Add value labels on top of each bar for better readability
    for i, v in enumerate(category_data['Sales']):
        bar_plot.text(i, v + (max(sales) * 0.02), f"${v:,.0f}", 
                     color='black', ha='center', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    
    try:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return True
    except Exception as e:
        print(f"Error saving top categories chart: {e}")
        plt.close()
        return False


