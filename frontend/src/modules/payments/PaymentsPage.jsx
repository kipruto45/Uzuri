import React, { useEffect, useState } from 'react'
import { listTransactions } from './api'

export default function PaymentsPage() {
  const [txs, setTxs] = useState([])

  useEffect(() => {
    ;(async () => {
      const data = await listTransactions()
      setTxs(data || [])
    })()
  }, [])

  return (
    <div className="p-4">
      <h2>Payments</h2>
      <ul>
        {txs.map((t) => (
          <li key={t.id}>{t.id} - {t.status}</li>
        ))}
      </ul>
    </div>
  )
}

