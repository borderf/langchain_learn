import axios from 'axios'

const parseBigint = (data) => {
  if (typeof data === 'string') {
    return data.replace(
      /"(id|session_id)":\s*(\d{15,})/g,
      '"$1":"$2"'
    )
  }
  return data
}

const api = axios.create({
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
        } catch (e) {
          return data
        }
      }
      return data
    }
  ]
})

export const sessionApi = {
  create: (title = '新的会话') => 
    api.post('/session/create', { title }),
  
  list: () => 
    api.post('/session/list'),
  
  get: (sessionId) => 
    api.post('/session/get', null, { params: { session_id: sessionId } }),
  
  update: (sessionId, title) => 
    api.post('/session/update', { title }, { params: { session_id: sessionId } }),
  
  delete: (sessionId) => 
    api.post('/session/delete', null, { params: { session_id: sessionId } }),
  
  getMessages: (sessionId) => 
    api.post('/session/messages', null, { params: { session_id: sessionId } })
}

export default api
