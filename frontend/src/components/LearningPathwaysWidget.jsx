import React from 'react'
import { Card, CardContent } from '../components/ui/Card'
import { useLearningPathways } from '../hooks/useLearningPathways'

export default function LearningPathwaysWidget() {
  const { data: paths = [], isLoading } = useLearningPathways()
  if (isLoading) return <div className="p-4">Loading pathways…</div>
  return (
    <Card>
      <CardContent>
        <h3 className="font-semibold">Suggested pathways</h3>
        <ul className="mt-2 text-sm">
          {paths.slice(0, 5).map((p) => (
            <li key={p.id}>{p.title}</li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}
