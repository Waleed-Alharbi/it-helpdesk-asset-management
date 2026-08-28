import { X } from 'lucide-react'
export default function Modal({ title, children, onClose }) { return <div className="modal-backdrop" onMouseDown={onClose}><div className="modal" onMouseDown={event => event.stopPropagation()}><div className="modal-head"><div><h2>{title}</h2><p>Complete the details below and save your changes.</p></div><button className="icon-button" onClick={onClose}><X size={20}/></button></div>{children}</div></div> }
export function Field({ label, children }) { return <label className="field"><span>{label}</span>{children}</label> }
