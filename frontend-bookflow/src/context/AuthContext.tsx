import React, { createContext, useReducer, useRef } from 'react'
import type { ReactNode } from 'react'
import { registerTokenGetter } from '../services/apiClient'

type State = { token: string | null; user?: any; isAuthenticated: boolean }
type Action =
  | { type: 'LOGIN'; payload: { token: string; user?: any } }
  | { type: 'LOGOUT' }

const initial: State = { token: null, user: undefined, isAuthenticated: false }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'LOGIN':
      return { token: action.payload.token, user: action.payload.user, isAuthenticated: true }
    case 'LOGOUT':
      return { token: null, user: undefined, isAuthenticated: false }
    default:
      return state
  }
}

export const AuthContext = createContext<{
  state: State
  dispatch: React.Dispatch<Action>
}>({ state: initial, dispatch: () => null })

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, initial)
  const stateRef = useRef(state)
  stateRef.current = state

  registerTokenGetter(() => stateRef.current.token)

  return <AuthContext.Provider value={{ state, dispatch }}>{children}</AuthContext.Provider>
}
