import React from 'react'

// Simple sparkline SVG component — dependency-free and responsive
export default function Sparkline({ data = [], width = 120, height = 28, stroke = '#4f46e5' }) {
  if (!data || data.length === 0) return null
  const max = Math.max(...data)
  const min = Math.min(...data)
  const range = max - min || 1
  const step = width / (data.length - 1)
  const points = data.map((d, i) => `${i * step},${height - ((d - min) / range) * height}`).join(' ')
  const last = data[data.length - 1]
  const lastY = height - ((last - min) / range) * height
  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none" aria-hidden>
      <polyline fill="none" stroke={stroke} strokeWidth="1.6" points={points} strokeLinecap="round" strokeLinejoin="round" />
      <circle cx={width - step} cy={lastY} r="2.2" fill={stroke} />
    </svg>
  )
}
