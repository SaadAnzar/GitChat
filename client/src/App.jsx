import React from 'react'
import { Routes, Route } from 'react-router-dom'
import AskGitHub from './pages/AskGitHub'
import Home from './pages/Home'
import ChatCode from './pages/ChatCode'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chatcode" element={<ChatCode />} />
      <Route path="/ask-github" element={<AskGitHub />} />
    </Routes>
  )
}

export default App
