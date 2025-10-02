import React from 'react'
import { render, screen, act } from '../../../test-utils'
import userEvent from '@testing-library/user-event'
import AttachmentsPage from '../AttachmentsPage'

jest.mock('../../attachments/api', () => ({
  listAttachments: jest.fn(() => []),
  uploadAttachment: jest.fn(() => ({ id: 1, name: 'file.txt' })),
}))

describe('AttachmentsPage', () => {
  test('renders header and upload area', async () => {
    await act(async () => {
      render(<AttachmentsPage />)
    })
    expect(screen.getByRole('heading', { name: /attachments/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /upload files/i })).toBeInTheDocument()
  })
})
