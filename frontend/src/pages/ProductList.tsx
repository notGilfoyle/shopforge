import { useEffect, useState } from 'react'
import { getProducts } from '../api/products'
import { ProductCard } from '../components/ProductCard'
import type { Product } from '../types'

export function ProductList() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getProducts()
      .then(setProducts)
      .catch(err => setError(err instanceof Error ? err.message : 'Failed to load products'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="loading">Loading products…</p>
  if (error) return <p className="error">{error}</p>

  return (
    <>
      <div className="page-header">
        <h1>Products</h1>
      </div>
      {products.length === 0 ? (
        <p className="empty-state">
          No products yet. Run <code>uv run python scripts/seed_products.py</code> in
          the backend to add some.
        </p>
      ) : (
        <div className="product-grid">
          {products.map(p => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      )}
    </>
  )
}
