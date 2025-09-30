import React from 'react'

export default function FeeStatement({ statement }) {
  if (!statement) return null
  return (
    <div className="border p-3 mb-2">
      <div className="font-bold">{statement.term}</div>
      <div>Amount: {statement.amount}</div>
      <div>Balance: {statement.balance}</div>
    </div>
  )
}
