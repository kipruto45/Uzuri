import React from 'react'
import { useQuery } from '@tanstack/react-query'
import apiService from '../../services/apiService'

function fetchStatements(){
  return apiService.payments ? apiService.payments.statements?.() : Promise.resolve([])
}

export default function FeeStatementPage(){
  const { data, isLoading, error } = useQuery(['feeStatements'], fetchStatements)

  if (isLoading) return <div>Loading fee statements...</div>
  if (error) return <div>Error loading: {String(error)}</div>

  const statements = data?.data || []

  return (
    <div>
      <h2>Fee Statements</h2>
      {statements.length === 0 ? (
        <p>No statements available</p>
      ) : (
        <ul>
          {statements.map(s => (
            <li key={s.id}>{s.description || s.period || s.id}</li>
          ))}
        </ul>
      )}
    </div>
  )
}
