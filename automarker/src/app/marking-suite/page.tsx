"use client"

import Navbar from '@/components/Navbar'
import React from 'react'
import Link from 'next/link'
import {FaCheckCircle} from 'react-icons/fa'
import {FaUpload} from 'react-icons/fa'

interface TestScript {
  id: string
  name: string
  dateUploaded: string
  size: string
}

interface Assignment {
  id: string
  title: string
  course: string
  dueDate: string
}

const MarkingSuite = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar currentTab="marking-suite" setCurrentTab={function (value: React.SetStateAction<string>): void {
        throw new Error('Function not implemented.')
      } } />
      <main className="pt-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Marking Suite</h1>
        <div className="grid gap-6 md:grid-cols-2">
          <Link 
            href="/marking-suite/test-scripts"
            className="group block p-6 bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200"
          >
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="p-4 bg-purple-100 rounded-full group-hover:bg-purple-200 transition-colors">
                <FaUpload className="w-8 h-8 text-purple-600" />
              </div>
              <h2 className="text-xl font-semibold text-gray-900">Upload Test Scripts</h2>
              <p className="text-sm text-gray-500">
                Manage your test scripts for automated marking
              </p>
            </div>
          </Link>

          <Link 
            href="/marking-suite/assignments"
            className="group block p-6 bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200"
          >
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="p-4 bg-emerald-100 rounded-full group-hover:bg-emerald-200 transition-colors">
                <FaCheckCircle className="w-8 h-8 text-emerald-600" />
              </div>
              <h2 className="text-xl font-semibold text-gray-900">Mark Assignments</h2>
              <p className="text-sm text-gray-500">
                View and grade student submissions
              </p>
            </div>
          </Link>
        </div>
      </main>
    </div>
  )
}

export default MarkingSuite