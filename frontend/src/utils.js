export const initials = name => name?.split(' ').map(part => part[0]).slice(0, 2).join('') || '—'
export const formatDate = value => value ? new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(value)) : '—'
export const ticketBadge = value => `badge ${value?.toLowerCase().replaceAll(' ', '-')}`
export const assetBadge = value => `badge ${value?.toLowerCase().replaceAll(' ', '-')}`
