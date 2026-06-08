import { Link } from 'react-router-dom'
import { useCart } from '../context/CartContext'
import type { Product } from '../types'

export function ProductCard({ product }: { product: Product }) {
  const { addToCart } = useCart()

  return (
    <div className="card">
      <span className="category">{product.category}</span>
      <h2>
        <Link to={`/products/${product.id}`}>{product.name}</Link>
      </h2>
      <p className="desc">
        {product.description.length > 100
          ? product.description.slice(0, 100) + '…'
          : product.description}
      </p>
      <p className="price">${product.price.toFixed(2)}</p>
      <button className="btn btn-primary mt-2" onClick={() => addToCart(product)}>
        Add to Cart
      </button>
    </div>
  )
}
