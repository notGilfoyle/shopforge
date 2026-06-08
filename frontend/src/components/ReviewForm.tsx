import { useState } from 'react'
import { createReview } from '../api/reviews'
import type { Review } from '../types'

interface Props {
  productId: string
  userId: number | null
  onCreated: (review: Review) => void
}

export function ReviewForm({ productId, userId, onCreated }: Props) {
  const [rating, setRating] = useState(5)
  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (!userId) {
    return (
      <p className="error mt-4">
        <Link to="/checkout">Complete a purchase</Link> to leave a review.
      </p>
    )
  }

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const review = await createReview(productId, { user_id: userId, rating, title, body })
      onCreated(review)
      setTitle('')
      setBody('')
      setRating(5)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit review')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={submit} className="card mt-4">
      <h3>Write a Review</h3>
      <div className="form-group mt-4">
        <label>Rating</label>
        <select value={rating} onChange={e => setRating(Number(e.target.value))}>
          {[5, 4, 3, 2, 1].map(n => (
            <option key={n} value={n}>
              {'★'.repeat(n)} ({n}/5)
            </option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label>Title</label>
        <input
          required
          maxLength={200}
          value={title}
          onChange={e => setTitle(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label>Review</label>
        <textarea required rows={4} value={body} onChange={e => setBody(e.target.value)} />
      </div>
      {error && <p className="error">{error}</p>}
      <button className="btn btn-primary" type="submit" disabled={loading}>
        {loading ? 'Submitting…' : 'Submit Review'}
      </button>
    </form>
  )
}

// Inline to avoid a circular import through react-router-dom in a component file
function Link({ to, children }: { to: string; children: React.ReactNode }) {
  return <a href={to}>{children}</a>
}
