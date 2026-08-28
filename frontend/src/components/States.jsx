import { AlertCircle, Inbox } from 'lucide-react'
export const Loading = () => <div className="state"><div className="spinner"/><span>Loading workspace data…</span></div>
export const ErrorState = ({ message, retry }) => <div className="state error"><AlertCircle size={28}/><strong>Unable to load data</strong><span>{message}</span><button className="button secondary" onClick={retry}>Try again</button></div>
export const EmptyState = ({ label }) => <div className="empty"><Inbox size={28}/><strong>No {label} found</strong><span>Try adjusting your filters or add a new record.</span></div>
