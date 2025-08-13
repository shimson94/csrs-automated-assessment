import React from 'react'

export const Input = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(({ className = '', ...props }, ref) => {
  return (
    <input
      className={`flex h-10 w-full rounded-md border border-slate-200 
        bg-white px-3 py-2 text-sm placeholder:text-slate-500 
        focus:outline-none focus:ring-2 focus:ring-slate-400
        disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
      ref={ref}
      {...props}
    />
  )
})

Input.displayName = 'Input'