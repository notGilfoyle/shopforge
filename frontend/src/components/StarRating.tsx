export function StarRating({ rating, max = 5 }: { rating: number; max?: number }) {
  return (
    <span className="stars" aria-label={`${rating} out of ${max} stars`}>
      {Array.from({ length: max }, (_, i) => (i < rating ? '★' : '☆')).join('')}
    </span>
  )
}
