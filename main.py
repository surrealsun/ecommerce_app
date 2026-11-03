from fastapi import FastAPI

app = FastAPI()

products: dict[int, tuple[str, float, bool]] = {
    5001: ("Organic Whole Milk (1 Gallon)", 4.89, True),
    5002: ("Whole Wheat Bread", 3.29, True),
    5003: ("Fresh Honeycrisp Apples (1 lb)", 2.49, True),
    5004: ("Large Brown Eggs (12 count)", 3.99, True),
    5005: ("Greek Yogurt (32 oz)", 5.49, False),
}

orders: dict[int, tuple[int, int]] = {1000: (5002, 1)}

curr_item_id = 5005
curr_order_id = 1000


@app.get("/")
def get_home_page():
    return {"content": "Home Page of E-Commerce app"}


@app.get("/products")
def get_products():
    result = ""
    for id in products.keys():
        print(
            f"Item ID: {id}, Product Name: {products[id][0]}, Price: {products[id][1]}, Available : {products[id][2]} "
        )
        product_str = f"Item ID: {id}, Product Name: {products[id][0]}, Price: {products[id][1]}, Available : {products[id][2]};"
        result += product_str

    return result


@app.get("/items/{item_id}")
def get_item(item_id: int):
    return products.get(item_id)


@app.post("/create")
def add_item(product_name: str, price: float):
    global curr_id
    item_id = curr_id + 1
    products[item_id] = (product_name, price)
    curr_id += 1
    return f"Created with id {item_id}"


@app.delete("/delete/{item_id}")
def delete_item(item_id: int):
    products.pop(item_id)
    return f"Deleted! {item_id}"


@app.get("/place_order")
def order_item(item_id: int, quantity: int = 1):
    global curr_order_id
    if products[item_id][2]:
        ord_id = curr_order_id + 1
        orders[ord_id] = (item_id, quantity)
        curr_order_id += 1
        return f"Order Placed with order id {ord_id}"
    else:
        return f"The item {item_id} is not available!"


@app.get("/orders")
def get_orders():
    result = ""
    for id in orders.keys():
        print(
            f"Order ID: {id}, Product ID: {orders[id][0]}, Product Name: {products[orders[id][0]][0]}, Quantity: {orders[id][1]} "
        )
        product_str = f"Order ID: {id}, Product ID: {orders[id][0]}, Product Name: {products[orders[id][0]][0]}, Quantity: {orders[id][1]};"
        result += product_str

    return result


# def main():


# if __name__ == "__main__":
#     main()
