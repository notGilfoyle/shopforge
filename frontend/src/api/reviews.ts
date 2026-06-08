import { del, get, post } from './client'
import type { Review } from '../types'

export const getReviews = (productId: string) =>
  get<Review[]>(`/products/${productId}/reviews`)

export const createReview = (
  productId: string,
  data: { user_id: number; rating: number; title: string; body: string }
) => post<Review>(`/products/${productId}/reviews`, data)

export const deleteReview = (reviewId: string) => del(`/reviews/${reviewId}`)
