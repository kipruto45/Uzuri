import React from 'react'

export default function MiniBarChart({ data = [], width = 120, height = 28, color = '#10b981' }) {
  if (!data || data.length === 0) return null
  const max = Math.max(...data)
  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} aria-hidden>
      {data.map((d, i) => {
        const w = width / data.length
        const h = (d / max) * height
        const x = i * w
        return <rect key={i} x={x + 1} y={height - h} width={w - 2} height={h} fill={color} rx={2} />
      })}
    </svg>
  )
}
