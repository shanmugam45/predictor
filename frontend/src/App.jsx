import { Routes, Route } from 'react-router-dom'
import Layout from './components/common/Layout'
import Predict from './pages/Predict'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Predict />} />
        <Route path="predict" element={<Predict />} />
      </Route>
    </Routes>
  )
}
