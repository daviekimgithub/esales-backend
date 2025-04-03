import requests

# Your Django backend URL
BASE_URL = "http://127.0.0.1:8000/products/"

# Fetch categories from dummyjson
CATEGORY_URL = "https://dummyjson.com/products/categories"
PRODUCTS_URL = "https://dummyjson.com/products?limit=200"

def fetch_categories():
    response = requests.get(CATEGORY_URL)
    if response.status_code == 200:
        return response.json()  # This should be a list of category dictionaries
    return []

def fetch_products():
    response = requests.get(PRODUCTS_URL)
    if response.status_code == 200:
        return response.json().get("products", [])
    return []

def post_category(category):
    data = {
        "slug": category["slug"],  # Extracting the correct fields
        "name": category["name"],
        "url": category["url"]
    }
    response = requests.post(BASE_URL + "categories/", json=data)
    if response.status_code in [200, 201]:
        print(f"Category {category['name']} added successfully.")
    else:
        print(f"Failed to add category {category['name']}: {response.text}")

def post_product(product):
    data = {
        "category": product["category"],
        "title": product["title"],
        "description": product["description"],
        "price": product["price"],
        "discount_percentage": product["discountPercentage"],
        "rating": product["rating"],
        "stock": product["stock"],
        "thumbnail": product["thumbnail"]
    }
    response = requests.post(BASE_URL, json=data)
    if response.status_code in [200, 201]:
        product_id = response.json().get("id")
        print(f"Product {product['title']} added successfully.")
        
        # Add product images
        for image_url in product.get("images", []):
            post_product_image(product_id, image_url)
    else:
        print(f"Failed to add product {product['title']}: {response.text}")

def post_product_image(product_id, url):
    data = {
        "product": product_id,
        "url": url
    }
    response = requests.post(BASE_URL + "images/", json=data)
    if response.status_code in [200, 201]:
        print(f"Image {url} added successfully.")
    else:
        print(f"Failed to add image {url}: {response.text}")

def main():
    categories = fetch_categories()
    for category in categories:
        post_category(category)  # category is now a dictionary

    products = fetch_products()
    for product in products:
        post_product(product)

if __name__ == "__main__":
    main()
