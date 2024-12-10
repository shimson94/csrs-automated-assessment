"use client"

import Navbar from '@/components/Navbar'
import React from 'react'
import { useState } from 'react'

const AssessmentsPage = () => {
  const [currentTab, setCurrentTab] = useState('home')
  return (
    <div className="min-h-screen bg-gray-100">
    {/* Navbar */}
    <Navbar currentTab={currentTab} setCurrentTab={setCurrentTab} />

    </div>
  )
}

export default AssessmentsPage