import { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [quantities, setQuantities] = useState({});
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadData() {
    setLoading(true);
    try {
      const [productsResponse, ordersResponse] = await Promise.all([
        fetch(`${API_URL}/products`),
        fetch(`${API_URL}/orders`),
      ]);
      if (!productsResponse.ok || !ordersResponse.ok) throw new Error("Could not load shop data.");
      setProducts(await productsResponse.json());
      setOrders(await ordersResponse.json());
    } catch (error) {
      setMessage(`${error.message} Start FastAPI on port 8000 and try again.`);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadData(); }, []);

  async function placeOrder(itemId) {
    const quantity = Number(quantities[itemId] || 1);
    const response = await fetch(`${API_URL}/place_order?item_id=${itemId}&quantity=${quantity}`);
    const result = await response.text();
    setMessage(result);
    if (response.ok) await loadData();
  }

  return (
    <main className="container">
      <header>
        <h1>Simple Shop</h1>
        <p>Choose a product and place an order.</p>
      </header>

      {message && <div className="message">{message}</div>}

      <section>
        <h2>Products</h2>
        {loading ? <p>Loading...</p> : (
          <div className="products">
            {products.map((product) => (
              <article className="product" key={product.id}>
                <div>
                  <h3>{product.name}</h3>
                  <p>${product.price.toFixed(2)}</p>
                  <small className={product.available ? "available" : "unavailable"}>
                    {product.available ? "Available" : "Not available"}
                  </small>
                </div>
                {product.available && (
                  <div className="order-controls">
                    <input
                      aria-label={`Quantity for ${product.name}`}
                      type="number"
                      min="1"
                      value={quantities[product.id] || 1}
                      onChange={(event) => setQuantities({ ...quantities, [product.id]: event.target.value })}
                    />
                    <button onClick={() => placeOrder(product.id)}>Order</button>
                  </div>
                )}
              </article>
            ))}
          </div>
        )}
      </section>

      <section>
        <h2>Orders</h2>
        {orders.length === 0 ? <p>No orders yet.</p> : (
          <div className="orders">
            {orders.map((order) => (
              <p key={order.id}>Order #{order.id}: {order.product_name} × {order.quantity}</p>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<StrictMode><App /></StrictMode>);
