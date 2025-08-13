"use client"

import Navbar from '@/components/Navbar'
import React from 'react'
import { useState } from 'react'

const SubmissionsPage = () => {
  const [currentTab, setCurrentTab] = useState('home')
  return (
    <div className="min-h-screen bg-gray-100">
    {/* Navbar */}
    <Navbar currentTab={currentTab} setCurrentTab={setCurrentTab} />
    <main className="max-w-7xl mx-auto py-6 px-4">
      <h1 className="text-3xl font-bold text-gray-900">Submisssions</h1>
    </main>

    </div>
  )
}

export default SubmissionsPage