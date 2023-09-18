
import json

f = open('nike_shoes3.json')

data = json.load(f)

def format_product(product):
    age_range = "KIDS"
    if product.get('gender', 'N/A') != age_range:
        age_range = "ADULT"
    formatted_product = f"**{product.get('name', 'N/A')}**\n"
    formatted_product += f"   - Name: {product.get('name', 'N/A')}\n"
    formatted_product += f"   - Brand: {product.get('brand', 'N/A')}\n"
    formatted_product += f"   - age_range: {age_range}\n"
    formatted_product += f"   - Category: {product.get('category', 'N/A')}\n"
    formatted_product += f"   - Price: ${product.get('price', 'N/A')}\n"
    formatted_product += f"   - Availability: {'Available' if product.get('is_in_inventory', False) else 'Out of Stock'}\n"
    formatted_product += f"   - Items Left: {product.get('items_left', 'N/A')}\n"
    formatted_product += f"   - Image: ({product.get('imageURL', 'https://example.com/placeholder.jpg')})\n"
    return formatted_product

def format_names(product):
    formatted_product = f"   - **Name:** {product.get('name', 'N/A')}\n"
    return formatted_product


# Create and open a text file for writing
with open("formatted_catalog.txt", "w") as txt_file:
    # Format and write product details to the file
    for product_id, product_info in data.items():
        formatted_product = format_product(product_info)
        txt_file.write(formatted_product + "\n")

with open("shoes_list.txt", "w") as txt_file:
    # Format and write product details to the file
    for product_id, product_info in data.items():
        formatted_product = format_names(product_info)
        txt_file.write(formatted_product + "\n")