import axios, { AxiosInstance } from 'axios'
import { Session, Message } from './types'

const parseBigint = (data: string): string => {
  return data.replace(
    /"(id|session_id)":\s*(\d{15,})/g,
    '"$1":"$2"'
  )
}

const api: AxiosInstance = axios.create({
  baseURL: '/api/chat',
  headers: {
    'Content-Type': 'application/json'
  },
  transformResponse: [
    (data) => {
      if (typeof data === 'string') {
        try {
          const parsed = JSON.parse(parseBigint(data))
          return parsed
        } catch {
          return data
        }
      }
      return data
    }
  ]
})

export const sessionApi = {
  create: (title: string = '新的会话') =>
    api.post<Session>('/session/create', { title }),

  list: () =>
    api.post<Session[]>('/session/list'),

  get: (sessionId: string) =>
    api.post<Session>('/session/get', null, { params: { session_id: sessionId } }),

  update: (sessionId: string, title: string) =>
    api.post<Session>('/session/update', { title }, { params: { session_id: sessionId } }),

  delete: (sessionId: string) =>
    api.post<{ message: string }>('/session/delete', null, { params: { session_id: sessionId } }),

  getMessages: (sessionId: string) =>
    api.post<Message[]>('/session/messages', null, { params: { session_id: sessionId } })
}

export default api
