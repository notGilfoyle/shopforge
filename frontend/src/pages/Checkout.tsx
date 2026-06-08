import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ApiError } from '../api/client'
import { createOrder, createUser } from '../api/orders'
import { useCart } from '../context/CartContext'

export function Checkout() {
  const { items, total, clearCart } = useCart()
  const navigate = useNavigate()

  // After the first checkout, user_id is stored in localStorage so the form
  // isn't shown again on subsequent visits.
  const stored = localStorage.getItem('user_id')
  const [userId, setUserId] = useState<number | null>(stored ? Number(stored) : null)

  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (items.length === 0) {
    return (
      <div className="empty-state">
        <p>Your cart is empty.</p>
      </div>
    )
  }

  const register = async (): Promise<number> => {
    try {
      const user = await createUser(email, name)
      localStorage.setItem('user_id', String(user.id))
      return user.id
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        throw new Error('That email is already registered. Clear browser storage to use a different account.')
      }
      throw err
    }
  }

  const placeOrder = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      let uid = userId
      if (!uid) {
        uid = await register()
        setUserId(uid)
      }
      const order = await createOrder(
        uid,
        items.map(i => ({ product_id: i.product.id, quantity: i.quantity }))
      )
      clearCart()
      navigate(`/orders/${order.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Checkout failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className="page-header">
        <h1>Checkout</h1>
      </div>
      <form
        onSubmit={placeOrder}
        style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}
      >
        <div>
          {!userId ? (
            <div className="card">
              <h2>Your Details</h2>
              <div className="form-group mt-4">
                <label>Email</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Name</label>
                <input
                  required
                  value={name}
                  onChange={e => setName(e.target.value)}
                />
              </div>
            </div>
          ) : (
            <div className="card">
              <p>
                Ordering as user #{userId}.{' '}
                <button
                  type="button"
                  className="btn btn-outline"
                  style={{ padding: '4px 12px', fontSize: '0.85rem' }}
                  onClick={() => {
                    localStorage.removeItem('user_id')
                    setUserId(null)
                  }}
                >
                  Change
                </button>
              </p>
            </div>
          )}
        </div>

        <div className="card">
          <h2>Order Summary</h2>
          {items.map(({ product, quantity }) => (
            <div key={product.id} className="flex justify-between mt-2">
              <span>
                {product.name} × {quantity}
              </span>
              <span>${(product.price * quantity).toFixed(2)}</span>
            </div>
          ))}
          <hr style={{ margin: '16px 0', border: 'none', borderTop: '1px solid #eee' }} />
          <div className="flex justify-between">
            <strong>Total</strong>
            <strong>${total.toFixed(2)}</strong>
          </div>
          {error && <p className="error mt-2">{error}</p>}
          <button
            type="submit"
            className="btn btn-primary mt-4"
            style={{ width: '100%' }}
            disabled={loading || (!userId && (!email || !name))}
          >
            {loading ? 'Placing Order…' : 'Place Order'}
          </button>
        </div>
      </form>
    </>
  )
}
