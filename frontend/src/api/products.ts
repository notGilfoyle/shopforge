import { get } from './client'
import type { Product } from '../types'

export const getProducts = (category?: string) =>
  get<Product[]>(`/products${category ? `?category=${encodeURIComponent(category)}` : ''}`)

export const getProduct = (id: string) => get<Product>(`/products/${id}`)

export const getInventory = (productId: string) =>
  get<{ product_id: string; stock: number }>(`/inventory/${productId}`)
