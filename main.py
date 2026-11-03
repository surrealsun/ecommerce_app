from fastapi import FastAPI

app = FastAPI()

products: dict[int, tuple[str, float, bool]] = {
    5001: ("Organic Whole Milk (1 Gallon)", 4.89, True),
    5002: ("Whole Wheat Bread", 3.29, True),
    5003: ("Fresh Honeycrisp Apples (1 lb)", 2.49, True),
    5004: ("Large Brown Eggs (12 count)", 3.99, True),
    5005: ("Greek Yogurt (32 oz)", 5.49, True)
}
curr_id = 5005

@app.get("/")
def get_home_page():
    return {"content" : "Home Page of E-Commerce app"}

@app.get("/products")
def get_products():
    result = ""
    for id in products.keys():
        print(f"Item ID: {id}, Product Name: {products[id][0]}, Price: {products[id][1]}")
        product_str = f"Item ID: {id}, Product Name: {products[id][0]}, Price: {products[id][1]};   "
        result += product_str 

    return result

@app.get("/items/{item_id}")
def get_item(item_id : int):
    return products.get(item_id)

@app.post("/create")
def add_item(product_name : str, price: float):
    global curr_id
    item_id = curr_id + 1
    products[item_id] = (product_name, price)
    curr_id += 1
    return f"Created with id {item_id}"
    
@app.delete("/delete")
def delete_item(item_id : int):
    products.pop(item_id)    
    return f"Deleted! {item_id}"
    
    
# def main():
    


# if __name__ == "__main__":
#     main()