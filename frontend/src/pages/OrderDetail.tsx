import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getOrder } from '../api/orders'
import type { Order } from '../types'

export function OrderDetail() {
  const { id } = useParams<{ id: string }>()
  const [order, setOrder] = useState<Order | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return
    getOrder(Number(id))
      .then(setOrder)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <p className="loading">Loading order…</p>
  if (!order) return <p className="error">Order not found.</p>

  return (
    <>
      <div className="page-header">
        <h1>Order #{order.id}</h1>
        <span className="order-badge">{order.status}</span>
      </div>
      <div className="order-detail">
        <p style={{ color: '#888', marginBottom: 24 }}>
          Placed on {new Date(order.created_at).toLocaleString()}
        </p>
        <table className="cart-table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Qty</th>
              <th>Unit Price</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {order.items.map(item => (
              <tr key={item.id}>
                <td>{item.product_name}</td>
                <td>{item.quantity}</td>
                <td>${Number(item.unit_price).toFixed(2)}</td>
                <td>${Number(item.subtotal).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="cart-total">Total: ${Number(order.total_amount).toFixed(2)}</p>
        <Link to="/" className="btn btn-primary">
          Continue Shopping
        </Link>
      </div>
    </>
  )
}
