import { useState } from 'react'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Tickets from './pages/Tickets'
import Assets from './pages/Assets'
import Users from './pages/Users'
import Reports from './pages/Reports'
import Settings from './pages/Settings'
const pages = { Dashboard, Tickets, Assets, Users, Reports, Settings }
export default function App() {
  const [page, setPage] = useState('Dashboard'); const [notice, setNotice] = useState('')
  const Page = pages[page]
  return <Layout page={page} setPage={setPage} notice={notice} setNotice={setNotice}><Page notify={setNotice} navigate={setPage} /></Layout>
}

