import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import NewRequestModal from '../NewRequestModal'

// Mock the API module
jest.mock('../../api', () => {
  const createLeaveRequest = jest.fn(() => Promise.resolve({ id: 1 }))
  let callCount = 0
  const uploadLeaveDocument = jest.fn((id, fd, onProgress) => {
    callCount += 1
    // first call simulates a failure after some progress, subsequent calls succeed
    return new Promise((res, rej) => {
      let loaded = 0
      const total = 100
      const t = setInterval(() => {
        loaded += 25
        onProgress && onProgress({ loaded, total })
        if (loaded >= total) {
          clearInterval(t)
          if (callCount === 1) {
            rej(new Error('network'))
          } else {
            res({ status: 'ok' })
          }
        }
      }, 5)
    })
  })
  return { createLeaveRequest, uploadLeaveDocument }
})

describe('NewRequestModal', () => {
  beforeEach(() => jest.clearAllMocks())

  test('validates steps and shows combined progress', async () => {
    render(<NewRequestModal isOpen={true} onClose={() => {}} />)

    // Step 0: try to proceed without filling
    const submitBtn = screen.getByRole('button', { name: /Next|Submit/i })
    userEvent.click(submitBtn)

    expect(await screen.findByText(/Select a leave type/i)).toBeInTheDocument()

    // Fill fields
    userEvent.selectOptions(screen.getByRole('combobox'), 'medical')
    const start = screen.getByLabelText(/Start date/i)
    const end = screen.getByLabelText(/End date/i)
    fireEvent.change(start, { target: { value: '2025-10-01' } })
    fireEvent.change(end, { target: { value: '2025-10-05' } })
    userEvent.type(screen.getByLabelText(/Reason/i), 'Need to attend medical appointment')

    userEvent.click(submitBtn)

    // Now on step 1
    expect(await screen.findByText(/Supporting documents/i)).toBeInTheDocument()

    // Add a file via the hidden input
    const input = document.querySelector('input[type=file]')
    const file = new File(['hello'], 'test.pdf', { type: 'application/pdf' })
    fireEvent.change(input, { target: { files: [file] } })

    // Proceed to review
    const nextBtn = screen.getByRole('button', { name: /Next|Submit/i })
    userEvent.click(nextBtn)

    // On review
    expect(await screen.findByText(/Review your request/i)).toBeInTheDocument()

    // Submit and observe combined progress bar appears
    const submitFinal = screen.getByRole('button', { name: /Submit/i })
    userEvent.click(submitFinal)

    // Wait for upload failure to be shown
    await waitFor(() => expect(screen.getByText(/Upload failed|network/i) || screen.getByText(/Upload failed/)))

    // Click retry button for the file
    const retryBtn = await screen.findByRole('button', { name: /Retry/i })
    userEvent.click(retryBtn)

    // After retry the combined progress should be visible
    expect(await screen.findByText(/Uploading documents:/i)).toBeInTheDocument()
    await waitFor(() => expect(screen.getByText(/Uploading documents:/i)).toBeInTheDocument())
  })
})
