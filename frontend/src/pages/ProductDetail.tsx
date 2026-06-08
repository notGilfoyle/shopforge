import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getInventory, getProduct } from '../api/products'
import { getReviews } from '../api/reviews'
import { ReviewForm } from '../components/ReviewForm'
import { StarRating } from '../components/StarRating'
import { useCart } from '../context/CartContext'
import type { Product, Review } from '../types'

export function ProductDetail() {
  const { id } = useParams<{ id: string }>()
  const [product, setProduct] = useState<Product | null>(null)
  const [reviews, setReviews] = useState<Review[]>([])
  const [stock, setStock] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [added, setAdded] = useState(false)
  const { addToCart } = useCart()

  // user_id is stored in localStorage after the first checkout
  const userId = Number(localStorage.getItem('user_id')) || null

  useEffect(() => {
    if (!id) return
    Promise.all([
      getProduct(id),
      getReviews(id),
      getInventory(id).catch(() => null), // graceful if no inventory record yet
    ])
      .then(([p, r, inv]) => {
        setProduct(p)
        setReviews(r)
        setStock(inv?.stock ?? null)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <p className="loading">Loading…</p>
  if (!product) return <p className="error">Product not found.</p>

  const handleAddToCart = () => {
    addToCart(product)
    setAdded(true)
    setTimeout(() => setAdded(false), 2000)
  }

  const avgRating =
    reviews.length > 0
      ? (reviews.reduce((s, r) => s + r.rating, 0) / reviews.length).toFixed(1)
      : null

  return (
    <>
      <div className="product-detail">
        <span className="category">{product.category}</span>
        <h1>{product.name}</h1>
        <div className="meta">
          {avgRating && (
            <>
              <StarRating rating={Math.round(Number(avgRating))} />
              <span>
                {avgRating} ({reviews.length} review{reviews.length !== 1 ? 's' : ''})
              </span>
            </>
          )}
          {stock !== null && (
            <span style={{ color: stock === 0 ? '#dc3545' : '#888' }}>
              {stock === 0 ? 'Out of stock' : `${stock} in stock`}
            </span>
          )}
        </div>
        <p style={{ marginBottom: 24, color: '#555' }}>{product.description}</p>
        <div className="flex items-center gap-4">
          <span className="big-price">${product.price.toFixed(2)}</span>
          <button
            className="btn btn-primary"
            onClick={handleAddToCart}
            disabled={stock === 0}
          >
            {added ? '✓ Added!' : 'Add to Cart'}
          </button>
        </div>
      </div>

      <div className="reviews">
        <h2>Reviews ({reviews.length})</h2>
        {reviews.length === 0 && (
          <p className="empty-state" style={{ padding: '20px 0' }}>
            No reviews yet. Be the first!
          </p>
        )}
        {reviews.map(r => (
          <div key={r.id} className="review">
            <div className="review-header">
              <StarRating rating={r.rating} />
              <h4>{r.title}</h4>
              <span className="review-meta">
                {new Date(r.created_at).toLocaleDateString()}
              </span>
            </div>
            <p className="review-body">{r.body}</p>
          </div>
        ))}
        <ReviewForm
          productId={product.id}
          userId={userId}
          onCreated={r => setReviews(prev => [r, ...prev])}
        />
      </div>
    </>
  )
}
