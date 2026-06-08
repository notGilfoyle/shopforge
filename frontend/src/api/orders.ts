import { get, post } from './client'
import type { Order } from '../types'

export const createUser = (email: string, name: string) =>
  post<{ id: number; email: string; name: string }>('/users', { email, name })

export const getOrder = (id: number) => get<Order>(`/orders/${id}`)

export const createOrder = (
  userId: number,
  items: { product_id: string; quantity: number }[]
) => post<Order>('/orders', { user_id: userId, items })
