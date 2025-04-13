# Automated E-commerce Reporting System

A Python-based system for generating beautiful, comprehensive reports from e-commerce data. This tool automatically processes transaction data, calculates key metrics, generates insights, creates visualizations, and packages everything in an HTML report.

<<<<<<< HEAD
![Example Report](/Example%20Report.png)

=======
>>>>>>> 06c576efa6c3ecf3abe6d24829885100fcdecea2
## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Report Contents](#report-contents)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Customizing](#customizing)
- [Troubleshooting](#troubleshooting)

## Features

- **Data Processing**: Automatically loads and processes e-commerce transaction data
- **Week-over-Week Analysis**: Compares current week metrics with previous week
- **Key Metric Calculation**: Revenue, order count, average order value, and more
- **Top Categories Analysis**: Identifies and analyzes top-performing product categories
- **Operational Metrics**: Monitors delivery time and customer satisfaction
- **Visualization Generation**: Creates beautiful charts for sales trends and top categories
- **Insight Generation**: Produces natural language insights about business performance
- **HTML Report Generation**: Packages all data, insights, and visuals into a professional HTML report

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Automated-E-commerce-Reporting-System.git
cd Automated-E-commerce-Reporting-System
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root with your data file paths:
```
orders_table_file_path=data/raw/orders.csv
products_table_file_path=data/raw/products.csv
orderd_items_table_file_path=data/raw/order_items.csv
product_category_file_path=data/raw/product_category_name_translation.csv
customers_table_file_path=data/raw/customers.csv
order_reviews_table_file_path=data/raw/order_reviews.csv
order_payment_table_file_path=data/raw/order_payments.csv
```

2. Ensure your data directory structure matches:
```
data/
├── raw/          # Raw CSV files
├── assets/plots/ # Generated visualizations go here
└── reports/      # Output reports are saved here
```

## Usage

### Generate a report for a specific date range:

```bash
python src/report_maker.py '2017-05-01' '2017-05-07'
```

The script accepts two date parameters:
- First parameter: Start date (YYYY-MM-DD)
- Second parameter: End date (YYYY-MM-DD)

### Generate a report for the most recent week:

```bash
python src/report_maker.py
```

When run without parameters, the system will generate a report for the 7 days leading up to today.

## Report Contents

The generated report includes:

- **Executive Summary**: Overall business performance at a glance
- **Key Performance Indicators**: Revenue, orders, and average order value with week-over-week comparison
- **Sales Performance**: Daily sales trend chart and key insights
- **Product Performance**: Top product categories, comparison table, and insights
- **Operational Insights**: Delivery time and customer satisfaction metrics

## Project Structure

```
Automated-E-commerce-Reporting-System/
├── data/                     # Data directories
│   ├── raw/                  # Raw input CSV files
│   ├── assets/plots/         # Generated visualization images
│   └── reports/              # Output report files
├── src/                      # Source code
│   ├── data_processor.py     # Data loading and processing functions
│   ├── metrics.py            # Business metrics calculations
│   ├── visualizations.py     # Chart generation functions
│   ├── text_generator.py     # Insight generation functions
│   └── report_maker.py       # Main report generation script
├── templates/                # Report templates
│   ├── report_template.html  # HTML template for the report
│   └── report_template.css   # CSS styling for the report
├── .env                      # Environment variables for file paths
└── requirements.txt          # Python dependencies
```

## How It Works

The system works in 5 main steps:

1. **Data Loading**: 
   - Reads CSV files specified in the .env file
   - Filters data for the specified time periods (current week and previous week)

2. **Metric Calculation**:
   - Revenue, order counts, and average order values
   - Top-selling product categories
   - Operational metrics like delivery time and customer satisfaction
   - Week-over-week performance changes

3. **Text Insight Generation**:
   - Creates natural language insights from calculated metrics
   - Highlights important trends and changes
   - Generates an executive summary

4. **Visualization Creation**:
   - Sales trend chart showing daily revenue and order counts
   - Top product categories chart

5. **Report Generation**:
   - Combines all elements using the HTML template
   - Applies CSS styling for a professional look
   - Outputs the final report to the data/reports directory

## Customizing

### HTML Template

Modify `templates/report_template.html` to change the report structure.

### CSS Styling

Edit `templates/report_template.css` to customize colors, fonts, and layout.

### Adding New Metrics

1. Add calculation functions in `src/metrics.py`
2. Update `src/report_maker.py` to include your new metrics
3. Modify the HTML template to display them

## Troubleshooting

### Missing Dependencies

If you see dependency errors:
```bash
pip install -r requirements.txt
```

### Data File Not Found

Ensure your `.env` file has the correct paths and the data files exist.

### Visualization Errors

Make sure matplotlib and seaborn are installed and working correctly:
```bash
pip install --upgrade matplotlib seaborn
```

### Report Not Generated

Check the console output for error messages. Common issues include:
- Missing data files
- Invalid date formats
- Insufficient data for the specified period
