import React from 'react'
import { render, screen } from '@testing-library/react'
import ClearancePage from '../ClearancePage'

jest.mock('../api', () => ({ listClearanceDocuments: jest.fn(() => ({ results: [] })), uploadClearanceDocument: jest.fn(), deleteClearanceDocument: jest.fn() }))

test('renders clearance header and upload section', () => {
  render(<ClearancePage />)
  expect(screen.getByRole('heading', { name: /clearance documents/i })).toBeInTheDocument()
  expect(screen.getByPlaceholderText(/search documents/i)).toBeInTheDocument()
})
