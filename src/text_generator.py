def create_executive_summary(
    total_revenue_data,
    order_count_data,
    avg_order_value_data,
    top_category_data):
    """
    Generate a comprehensive executive summary with key insights.
    
    Returns:
        str: A formatted executive summary in paragraphs
    """
    this_week_revenue, last_week_revenue, revenue_change, revenue_sign, revenue_trend = total_revenue_data
    this_week_orders, last_week_orders, order_change, order_sign, order_trend = order_count_data
    this_week_aov, last_week_aov, aov_change, aov_sign, aov_trend = avg_order_value_data
    
    categories, sales, daily_rates, prev_sales, percent_changes, signs, trends = top_category_data
    top_category = categories[0]
    top_category_change = percent_changes[0]
    top_category_sign = signs[0]
    
    executive_summary = f"This week's e-commerce performance "
    
    if revenue_trend == 'positive':
        executive_summary += "showed growth "
    elif revenue_trend == 'neutral':
        executive_summary += "remained stable "
    else:
        executive_summary += "faced some challenges "
    
    executive_summary += f"with a {revenue_sign}{revenue_change}% {revenue_trend} trend in total revenue"
    executive_summary += f" and a {order_sign}{order_change}% {order_trend} trend in total orders. "
    
    if aov_trend == 'positive':
        executive_summary += f"Customers spent more per order with average order value increasing by {aov_change}%. "
    elif aov_trend == 'negative':
        executive_summary += f"Average order value decreased by {aov_change}%, suggesting a shift toward lower-priced items. "
    else:
        executive_summary += f"Average order value remained consistent at ${this_week_aov:.2f}. "
    
    executive_summary += f"Our top-performing product category was {top_category}, "
    if top_category_sign == '+':
        executive_summary += f"which saw a {top_category_change}% increase in sales compared to last week "
    elif top_category_sign == '-':
        executive_summary += f"which experienced a {top_category_change}% decrease in sales compared to last week "
    else:
        executive_summary += f"which maintained stable sales compared to last week "
    
    executive_summary += f"with an average of {daily_rates[0]} daily orders. "
    
    return executive_summary

def generate_sales_insights(
    total_revenue_data, 
    order_count_data, 
    daily_sales_data, 
    peak_day_index=None):
    """
    Generate sales performance insights as individual bullet points.
    
    Returns:
        tuple: (weekly_comparison, peak_day_insight, day_distribution)
    """
    _, _, revenue_change, revenue_sign, revenue_trend = total_revenue_data
    this_week_orders, last_week_orders, order_change, order_sign, order_trend = order_count_data
    day_names, daily_revenue, daily_orders = daily_sales_data
    
    if peak_day_index is None:
        peak_day_index = daily_revenue.index(max(daily_revenue))
    
    peak_day = day_names[peak_day_index]
    
    weekly_comparison = f"This week's sales were {revenue_sign}{revenue_change}% "
    weekly_comparison += "higher than last week's." if revenue_sign == '+' else "lower than last week's."
    
    peak_day_insight = f"Peak sales day was {peak_day}, with "
    peak_day_insight += f"revenue of ${daily_revenue[peak_day_index]:,.2f} and {daily_orders[peak_day_index]} orders."
    
    weekend_indices = [i for i, day in enumerate(day_names) if day in ['Sat', 'Sun']]
    if weekend_indices:
        weekend_revenue = sum(daily_revenue[i] for i in weekend_indices)
        weekend_percent = (weekend_revenue / sum(daily_revenue)) * 100
        day_distribution = f"Weekend sales represented {weekend_percent:.1f}% of total weekly revenue, "
        if weekend_percent > 30:
            day_distribution += "showing strong weekend performance."
        elif weekend_percent > 20:
            day_distribution += "with balanced weekday-weekend distribution."
        else:
            day_distribution += "indicating stronger weekday performance."
    else:
        day_distribution = f"Order volume {order_trend}d by {order_sign}{order_change}%, "
        day_distribution += "showing increased customer engagement." if order_trend == 'positive' else \
                          "suggesting a need to evaluate customer acquisition channels." if order_trend == 'negative' else \
                          "maintaining consistent customer activity."
    
    return weekly_comparison, peak_day_insight, day_distribution

def generate_product_insights(top_category_data):
    """
    Generate product performance insights for top 3 categories.
    
    Returns:
        tuple: (top_category_insight, second_category_insight, third_category_insight)
    """
    categories, sales, daily_rates, prev_sales, percent_changes, signs, trends = top_category_data
    
    category_insights = []
    
    for i in range(3):
        insight = f"{categories[i]} "
        
        if trends[i] == 'positive':
            if percent_changes[i] > 10:
                insight += f"continues to be a top-performing category, with a significant {percent_changes[i]}% growth."
            else:
                insight += f"saw a healthy {percent_changes[i]}% increase in sales."
        elif trends[i] == 'negative':
            if percent_changes[i] > 10:
                insight += f"experienced a notable decline of {percent_changes[i]}% in sales."
            else:
                insight += f"showed a slight decrease of {percent_changes[i]}% in sales."
        else:
            insight += f"showed steady performance with consistent sales levels."
        
        category_insights.append(insight)
    
    return category_insights[0], category_insights[1], category_insights[2]

def generate_operational_insights(delivery_time_data, satisfaction_data):
    """
    Generate insights about operational metrics like delivery time and customer satisfaction.
    
    Args:
        delivery_time_data (tuple): Current and previous delivery time metrics
        satisfaction_data (tuple): Current and previous satisfaction metrics
        
    Returns:
        list: List of insight statements about operational metrics
    """
    this_week_delivery_time, last_week_delivery_time, percent_change, sign, trend = delivery_time_data
    
    # Create delivery time insight
    if trend == 'positive':
        delivery_message = f"Average delivery time improved to {this_week_delivery_time:.1f} days, {sign}{percent_change}% faster than last week's {last_week_delivery_time:.1f} days."
    elif trend == 'negative':
        delivery_message = f"Average delivery time increased to {this_week_delivery_time:.1f} days, {sign}{percent_change}% slower than last week's {last_week_delivery_time:.1f} days."
    else:
        delivery_message = f"Average delivery time remained stable at {this_week_delivery_time:.1f} days."
    
    this_week_rating, difference, sign, trend = satisfaction_data
    
    # Create satisfaction insight
    if trend == 'positive':
        satisfaction_message = f"Customer satisfaction improved to {this_week_rating:.1f}/5.0"
        if difference > 0:
            satisfaction_message += f" (↑ {difference} points)"
        satisfaction_message += ", reflecting substantial service enhancements." if difference >= 0.3 else \
                              ", showing positive customer reception."
    elif trend == 'negative':
        satisfaction_message = f"Customer satisfaction declined to {this_week_rating:.1f}/5.0"
        if difference > 0:
            satisfaction_message += f" (↓ {difference} points)"
        satisfaction_message += ", requiring immediate attention." if difference >= 0.3 else \
                              ", suggesting opportunities for improvement."
    else:
        satisfaction_message = f"Customer satisfaction remained steady at {this_week_rating:.1f}/5.0, maintaining consistent service standards."
    
    return [delivery_message, satisfaction_message]
