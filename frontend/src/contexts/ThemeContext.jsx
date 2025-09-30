import React, { createContext, useEffect, useState } from 'react'

export const ThemeContext = createContext({ dark: false, toggle: () => {} })

export function ThemeProvider({ children }) {
  const [dark, setDark] = useState(() => {
    try {
      const raw = localStorage.getItem('uzuri_theme')
      if (raw) return raw === 'dark'
    } catch (e) {}
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
  })

  useEffect(() => {
    if (dark) document.documentElement.classList.add('dark')
    else document.documentElement.classList.remove('dark')
    try { localStorage.setItem('uzuri_theme', dark ? 'dark' : 'light') } catch (e) {}
  }, [dark])

  const toggle = () => setDark((d) => !d)

  return <ThemeContext.Provider value={{ dark, toggle }}>{children}</ThemeContext.Provider>
}
