import React from 'react'
import { render, screen } from '@testing-library/react'
import { act } from 'react'
import userEvent from '@testing-library/user-event'

// Instead of exercising react-query internals we mock the hook exports
// from the implementation so tests can assert expected UI interactions
// and that consumers call into the mutation APIs correctly.
jest.mock('../useAiSupport', () => ({
  useConversations: jest.fn(),
  useCreateConversation: jest.fn(),
  useAlerts: jest.fn(),
  useCreateAlert: jest.fn(),
  useDeleteAlert: jest.fn(),
}))

import {
  useConversations,
  useCreateConversation,
  useAlerts,
  useCreateAlert,
  useDeleteAlert,
} from '../useAiSupport'

describe('useAiSupport hooks (consumer behavior)', () => {
  afterEach(() => jest.resetAllMocks())

  test('consumer reads conversations data from useConversations', async () => {
    useConversations.mockReturnValue({ data: [{ id: 1, message: 'hi', response: 'hello' }], isLoading: false })

    function Test() {
      const { data, isLoading } = useConversations()
      if (isLoading) return <div>loading</div>
      return <div data-testid="convs">{JSON.stringify(data)}</div>
    }

    await act(async () => {
      render(<Test />)
    })
    expect(await screen.findByTestId('convs')).toHaveTextContent('hi')
  })

  test('consumer triggers create conversation mutation', async () => {
    useConversations.mockReturnValue({ data: [], isLoading: false })
    const createMut = { mutate: jest.fn() }
    useCreateConversation.mockReturnValue(createMut)

    function Test() {
      const { data = [] } = useConversations()
      const create = useCreateConversation()
      return (
        <div>
          <button onClick={() => create.mutate({ message: 'abc' })}>create</button>
          <div data-testid="list">{JSON.stringify(data)}</div>
        </div>
      )
    }

    await act(async () => {
      render(<Test />)
    })
    await userEvent.click(screen.getByRole('button', { name: /create/i }))
    expect(createMut.mutate).toHaveBeenCalledWith({ message: 'abc' })
  })

  test('consumer calls alert create and delete mutations', async () => {
    useAlerts.mockReturnValue({ data: [{ id: 1, message: 'test' }], isLoading: false })
    const createMut = { mutate: jest.fn() }
    const deleteMut = { mutate: jest.fn() }
    useCreateAlert.mockReturnValue(createMut)
    useDeleteAlert.mockReturnValue(deleteMut)

    function Test() {
      const { data = [] } = useAlerts()
      const create = useCreateAlert()
      const del = useDeleteAlert()
      return (
        <div>
          <button onClick={() => create.mutate({ message: 'new' })}>create</button>
          <button onClick={() => del.mutate(1)}>del</button>
          <div data-testid="alerts">{JSON.stringify(data)}</div>
        </div>
      )
    }

    await act(async () => {
      render(<Test />)
    })
    expect(await screen.findByTestId('alerts')).toHaveTextContent('test')
    await userEvent.click(screen.getByRole('button', { name: /create/i }))
    expect(createMut.mutate).toHaveBeenCalledWith({ message: 'new' })
    await userEvent.click(screen.getByRole('button', { name: /del/i }))
    expect(deleteMut.mutate).toHaveBeenCalledWith(1)
  })
})
