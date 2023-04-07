# IMPORTS
from datetime import datetime
import statistics as stat

# READING DATASET
with open('sales-data.txt', 'r') as file:
    file_data = file.read()
data = file_data.split('\n')

# FILTERING
data.pop(0)
data = [item for item in data if item != '']

print('-------------------------\n\tANSWERS\n-------------------------')

# QUESTION 1: Total sales of the store.
total_sales = 0
for item in data:
    total_sales += int(item.split(',')[4])
print(f'\nQ1. Total sales of the store:$ {total_sales}' )

# SORTING SALES DATA PER MONTH
monthly_data = {}
for items in data:
    item_list = items.split(',')
    month = datetime.strptime(item_list[0], '%Y-%m-%d').strftime("%B")
    date, product, price, quantity, total = item_list[0], item_list[1], item_list[2], item_list[3], item_list[4]
    item_dict = {
        'month': month,
        'product': product,
        'quantity': quantity,
        'price': price,
        'total': total
    }
    if month not in monthly_data:
        monthly_data[month] = [item_dict]
    else:
        monthly_data[month].append(item_dict)

# CUMULATING PRODUCTS RECORDSET FOR MONTHLY SALE RECORDS :
sorted_monthly_data = {}
for months, items in monthly_data.items():
    monthly_products = {}
    for item in items:
        product = item['product']
        price, quantity, total = int(item['price']), int(item['quantity']), int(item['total'])
        if product not in monthly_products:
            monthly_products[product] = {
                'month': item['month'],
                'product': product,
                'quantity': quantity,
                'price': price,
                'total': total
            }
        else:
            monthly_products[product]['product'] = product
            monthly_products[product]['quantity'] += quantity
            monthly_products[product]['price'] = price
            monthly_products[product]['total'] += total
        sorted_monthly_data[months] = list(monthly_products.values())
# print(sorted_monthly_data)

print('\nQ2.Month wise sales totals.\n----------------------------')
monthly_sales_totals = {}
for keys, values in sorted_monthly_data.items():
    # print(keys)
    total_sales = 0
    for val in values:
        total_sales += val['total']
    monthly_sales_totals[keys] = total_sales
    print(f'Total sales of {keys} is $ {monthly_sales_totals[keys]}')

# QUESTION 3: Most popular item (most quantity sold) in each month.
print('\nQ3.Most popular item (most quantity sold) in each '
      'month.\n--------------------------------------------------------')
monthly_max_sold_items = {}  # FOR Q.3
monthly_most_profit_item = {}  # FOR Q.4
for month, values in sorted_monthly_data.items():
    max_quantity = 0
    max_sold_product = ""
    max_profit = 0
    # FOR QUESTION NO:4:
    most_revenue_product = ""
    most_revenue_quantity = 0
    most_profit_generated = 0
    # FOR QUESTION NO:3
    for item in values:
        # print(item)
        if item['quantity'] > max_quantity:
            max_sold_product = item['product']
            max_quantity = item['quantity']
            max_price = item['price']
            max_profit = item['total']
        # FOR QUESTION NO:4
        if item['total'] > most_profit_generated:
            most_revenue_product = item["product"]
            most_revenue_quantity = item["quantity"]
            most_profit_generated = item["total"]
    monthly_max_sold_items[month] = {
        'product': max_sold_product,
        'quantity': max_quantity,
        'price': max_price,
        'profit': max_profit,
    }
    monthly_most_profit_item[month] = {
        "product": most_revenue_product,
        "quantity": most_revenue_quantity,
        "profit": most_profit_generated
    }
    print(
        f'Most Popular item of {month} is {monthly_max_sold_items[month]["product"]} with a total of {monthly_max_sold_items[month]["quantity"]} items sold')

# QUESTION 4: Items generating most revenue in each month.
print('\nQ4.Items generating most revenue in each '
      'month.\n-----------------------------------------------')
for month, values in monthly_most_profit_item.items():
    print(f'most revenue generating item of {month} is '
          f'{monthly_most_profit_item[month]["product"]} with '
          f'{monthly_most_profit_item[month]["quantity"]} quantities sold, generating'
          f' total revenue of {monthly_most_profit_item[month]["profit"]} Dollars.')

# QUESTION 5: Maximum,Minimum and Average Orders for the
# popular item in each month.
print('\nQ5.Min, Max and Average Orders for the popular item in each month.'
      '\n------------------------------------------------------------------')

# SALES DATA PER DATE
daily_data = {}
for item in data:
    item_list = item.split(',')
    date, product, price, quantity, total = item_list[0], item_list[1], item_list[2], item_list[3], item_list[4]
    month = datetime.strptime(item_list[0], '%Y-%m-%d').strftime("%B")
    item_dict = {
        'date': date,
        'month': month,
        'product': product,
        'price': price,
        'quantity': quantity,
        'total': total
    }
    if date not in daily_data:
        daily_data[date] = [item_dict]
    else:
        daily_data[date].append(item_dict)

# CUMULATING PRODUCT SALE RECORDS TOGETHER:
sorted_daily_data = {}
for date, items in daily_data.items():
    products_data = {}
    for item in items:
        product, date, price, quantity, total = item['product'], item['date'], int(item['price']), int(
            item['quantity']), int(item['total'])
        month = datetime.strptime(item['date'], '%Y-%m-%d').strftime("%B")
        if product not in products_data:
            products_data[product] = {
                'product': product,
                'quantity': quantity,
                'price': price,
                'total': total,
                'date': date,
                'month': month
            }
        else:
            products_data[product]['product'] = product
            products_data[product]['quantity'] += quantity
            products_data[product]['price'] = price
            products_data[product]['total'] += total
            products_data[product]['date'] = date
    sorted_daily_data[date] = list(products_data.values())
# print(sorted_daily_data)
popular_item_detailed = {}
min_max_avg_orders = {}
for months, items in monthly_max_sold_items.items():
    # print(months)
    # print(items, '\n\n')
    for keys, values in sorted_daily_data.items():
        for value in values:
            # print(value)
            if value['product'] == items['product'] and value['month'] == months:
                if months not in popular_item_detailed:
                    popular_item_detailed[months] = [value]
                else:
                    popular_item_detailed[months].append(value)
# print(popular_item_detailed, "\npopular")
most_sold_orders = {}
for key, vals in popular_item_detailed.items():
    # print(vals,'\n\n')
    most_sold_order = max(vals, key=lambda x: x['quantity'])
    min_sold_order = min(vals, key=lambda x: x['quantity'])
    avg_sold_order = stat.mean(val['quantity'] for val in vals)
    most_sold_orders[key] = {
        'product': most_sold_order['product'],
        'maximum_sale': most_sold_order,
        'minimum_sale': min_sold_order,
        'average_sale': avg_sold_order
    }
# print(most_sold_orders)
# PRINTING ANSWER
for key, vals in most_sold_orders.items():
    product = vals['product']
    max_sold = vals['maximum_sale']['quantity']
    min_sold = vals['minimum_sale']['quantity']
    avg_sold = vals['average_sale']
    # print(vals)
    print(
        f"#{key}\n********\nMost Popular product: {product}\nmaximum sold:{max_sold}\n"
        f"minimum sold:{min_sold}\naverage sold:{avg_sold}\n")
