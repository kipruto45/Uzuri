import React from 'react'
import { render, screen, act } from '../../../test-utils'
import CalendarPage from '../CalendarPage'

jest.mock('../api', () => ({ myEvents: jest.fn(() => []), createEvent: jest.fn(), deleteEvent: jest.fn() }))

test('renders calendar header and new event button', async () => {
  await act(async () => {
    render(<CalendarPage />)
  })
  expect(screen.getByRole('heading', { name: /calendar/i })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /new event/i })).toBeInTheDocument()
})
