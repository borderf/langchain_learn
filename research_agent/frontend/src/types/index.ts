export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  session_id: string
  create_at: string
  update_at: string | null
}

export interface Session {
  id: string
  title: string
  create_at: string
  update_at: string | null
  messages: Message[]
}
