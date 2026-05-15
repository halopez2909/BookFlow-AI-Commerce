content = """import React from 'react'
import RoutesApp from './routes'

export default function App() {
  return <RoutesApp />
}
"""
with open('frontend-bookflow/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
