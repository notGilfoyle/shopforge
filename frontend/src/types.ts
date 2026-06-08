export interface Product {
  id: string
  name: string
  description: string
  price: number
  category: string
  images?: string[]
  attributes?: Record<string, unknown>
  created_at: string
  updated_at: string
}

export interface Review {
  id: string
  product_id: string
  user_id: number
  rating: number
  title: string
  body: string
  created_at: string
}

export interface OrderItem {
  id: number
  product_id: string
  product_name: string
  quantity: number
  unit_price: string
  subtotal: string
}

export interface Order {
  id: number
  user_id: number
  status: string
  total_amount: string
  items: OrderItem[]
  created_at: string
}

export interface CartItem {
  product: Product
  quantity: number
}
