import { Link, useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'

export function Cart() {
  const { items, removeFromCart, updateQuantity, total } = useCart()
  const navigate = useNavigate()

  if (items.length === 0) {
    return (
      <div className="empty-state">
        <p>Your cart is empty.</p>
        <Link to="/" className="btn btn-primary mt-4">
          Browse Products
        </Link>
      </div>
    )
  }

  return (
    <>
      <div className="page-header">
        <h1>Your Cart</h1>
      </div>
      <table className="cart-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Subtotal</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {items.map(({ product, quantity }) => (
            <tr key={product.id}>
              <td>
                <Link to={`/products/${product.id}`}>{product.name}</Link>
              </td>
              <td>${product.price.toFixed(2)}</td>
              <td>
                <input
                  type="number"
                  min={1}
                  value={quantity}
                  onChange={e => updateQuantity(product.id, Number(e.target.value))}
                  style={{ width: 60 }}
                />
              </td>
              <td>${(product.price * quantity).toFixed(2)}</td>
              <td>
                <button
                  className="btn btn-danger"
                  onClick={() => removeFromCart(product.id)}
                >
                  Remove
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="cart-total">Total: ${total.toFixed(2)}</p>
      <div className="flex gap-2 justify-between">
        <Link to="/" className="btn btn-outline">
          ← Continue Shopping
        </Link>
        <button className="btn btn-primary" onClick={() => navigate('/checkout')}>
          Checkout →
        </button>
      </div>
    </>
  )
}
