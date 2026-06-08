import { Link, Route, Routes } from 'react-router-dom'
import { useCart } from './context/CartContext'
import { Cart } from './pages/Cart'
import { Checkout } from './pages/Checkout'
import { OrderDetail } from './pages/OrderDetail'
import { ProductDetail } from './pages/ProductDetail'
import { ProductList } from './pages/ProductList'

function Header() {
  const { itemCount } = useCart()
  return (
    <header>
      <div className="container">
        <h1>
          <Link to="/">ShopForge</Link>
        </h1>
        <Link to="/">Products</Link>
        <Link to="/cart">
          Cart{itemCount > 0 ? ` (${itemCount})` : ''}
        </Link>
      </div>
    </header>
  )
}

export default function App() {
  return (
    <>
      <Header />
      <main className="container" style={{ paddingBottom: 48 }}>
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/checkout" element={<Checkout />} />
          <Route path="/orders/:id" element={<OrderDetail />} />
        </Routes>
      </main>
    </>
  )
}
