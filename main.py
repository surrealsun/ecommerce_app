from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import seriousdb

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


seriousdb.set(5001, ("Organic Whole Milk (1 Gallon)", 4.89, True))  # type: ignore
seriousdb.set(5002, ("Whole Wheat Bread", 3.29, True))  # type: ignore
seriousdb.set(5003, ("Fresh Honeycrisp Apples (1 lb)", 2.49, True))  # type: ignore
seriousdb.set(5004, ("Large Brown Eggs (12 count)", 3.99, True))  # type: ignore
seriousdb.set(5005, ("Greek Yogurt (32 oz)", 5.49, False))  # type: ignore


# products: dict[int, tuple[str, float, bool]] = {
#     5001: ("Organic Whole Milk (1 Gallon)", 4.89, True),
#     5002: ("Whole Wheat Bread", 3.29, True),
#     5003: ("Fresh Honeycrisp Apples (1 lb)", 2.49, True),
#     5004: ("Large Brown Eggs (12 count)", 3.99, True),
#     5005: ("Greek Yogurt (32 oz)", 5.49, False),
# }

orders: dict[int, tuple[int, int]] = {1000: (5002, 1)}

curr_item_id = 5005
curr_order_id = 1000


@app.get("/")
def get_home_page():
    return {"content": "Home Page of E-Commerce app"}


@app.get("/products")
def get_products():
    return [
        {
            "id": item_id,
            "name": seriousdb.get(item_id)[0],
            "price": seriousdb.get(item_id)[1],
            "available": seriousdb.get(item_id)[2],
        }
        for item_id in seriousdb.get_all()
    ]


@app.get("/items/{item_id}")
def get_item(item_id: int):
    return seriousdb.get(item_id)  # type: ignore


@app.post("/create")
def add_item(product_name: str, price: float):
    global curr_item_id
    curr_item_id += 1
    seriousdb.set(curr_item_id, (product_name, price, True))  # type: ignore
    item_id = curr_item_id
    return f"Created with id {item_id}"


@app.delete("/delete/{item_id}")
def delete_item(item_id: int):
    seriousdb.delete(item_id)  # type: ignore
    return f"Deleted! {item_id}"


@app.get("/place_order")
def order_item(item_id: int, quantity: int = 1):
    global curr_order_id
    if seriousdb.get(item_id)[2]:  # type: ignore
        ord_id = curr_order_id + 1
        orders[ord_id] = (item_id, quantity)
        curr_order_id += 1
        return f"Order Placed with order id {ord_id}"
    else:
        return f"The item {item_id} is not available!"


@app.get("/orders")
def get_orders():
    return [
        {
            "id": order_id,
            "product_id": order[0],
            "product_name": seriousdb.get(order[0])[0],  # type: ignore
            "quantity": order[1],
        }
        for order_id, order in orders.items()
    ]


# def main():


# if __name__ == "__main__":
#     main()
