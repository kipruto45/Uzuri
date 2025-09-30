import reducer, { } from './notificationsSlice'

test('notifications reducer handles initial state', () => {
  const initial = reducer(undefined, { type: '@@INIT' })
  expect(initial).toBeDefined()
  expect(Array.isArray(initial.items)).toBe(true)
})
