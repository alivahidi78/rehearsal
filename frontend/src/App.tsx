import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Library from './components/Library/Library'
import Session from './components/Session/Session'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Library />} />
        <Route path="/session/:sessionId" element={<Session />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App