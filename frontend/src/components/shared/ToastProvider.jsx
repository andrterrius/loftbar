'use client'

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AlertCircle, X } from 'lucide-react'

const ToastContext = createContext(null)

const AUTO_HIDE_MS = 3000

export function ToastProvider({ children }) {
  const [toast, setToast] = useState(null)
  const timerRef = useRef(null)

  const dismiss = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current)
      timerRef.current = null
    }
    setToast(null)
  }, [])

  const showError = useCallback((message) => {
    const text = message == null ? 'Произошла ошибка' : String(message)
    if (timerRef.current) clearTimeout(timerRef.current)
    setToast({ id: Date.now(), message: text })
    timerRef.current = setTimeout(() => {
      setToast(null)
      timerRef.current = null
    }, AUTO_HIDE_MS)
  }, [])

  useEffect(
    () => () => {
      if (timerRef.current) clearTimeout(timerRef.current)
    },
    []
  )

  return (
    <ToastContext.Provider value={{ showError, dismiss }}>
      {children}
      <AnimatePresence mode="wait">
        {toast ? (
          <motion.div
            key={toast.id}
            role="alert"
            initial={{ opacity: 0, y: -16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ type: 'spring', stiffness: 380, damping: 28 }}
            className="fixed z-[55] top-14 left-3 right-3 md:top-20 md:left-auto md:right-5 md:max-w-md md:w-[min(100%,28rem)] pointer-events-none"
          >
            <div className="pointer-events-auto flex gap-3 rounded-2xl border border-purple-500/30 bg-neutral-950/95 px-4 py-3.5 shadow-[inset_0_0_0_1px_rgba(168,85,247,0.08),0_0_32px_rgba(147,51,234,0.14),0_12px_40px_rgba(0,0,0,0.5)] backdrop-blur-md">
              <span className="mt-0.5 shrink-0 rounded-lg bg-gradient-to-br from-fuchsia-500/20 to-purple-600/20 p-2 text-fuchsia-300">
                <AlertCircle className="h-5 w-5" strokeWidth={2} aria-hidden />
              </span>
              <p className="min-w-0 flex-1 pt-0.5 text-sm font-medium leading-snug text-neutral-100">
                {toast.message}
              </p>
              <button
                type="button"
                onClick={dismiss}
                className="shrink-0 rounded-lg p-1.5 text-neutral-500 transition-colors hover:bg-white/10 hover:text-white"
                aria-label="Закрыть"
              >
                <X className="h-5 w-5" strokeWidth={1.75} />
              </button>
            </div>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) {
    throw new Error('useToast must be used within ToastProvider')
  }
  return ctx
}
