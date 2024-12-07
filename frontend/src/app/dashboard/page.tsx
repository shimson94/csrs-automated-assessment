// page.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function Dashboard() {
  const [currentTab, setCurrentTab] = useState('home')

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex">
              {/* Logo/Home */}
              <Link 
                href="/"
                className={`flex items-center px-4 ${
                  currentTab === 'home' ? 'border-b-2 border-blue-500' : ''
                }`}
                onClick={() => setCurrentTab('home')}
              >
                <span className="font-bold text-xl text-blue-800">AutoMarker</span>
              </Link>

              {/* Navigation Links */}
              <div className="hidden md:flex items-center space-x-4">
                <Link
                  href="/submissions"
                  className={`px-3 py-2 rounded-md ${
                    currentTab === 'submissions' ? 'bg-blue-100 text-blue-700' : 'text-gray-700'
                  }`}
                  onClick={() => setCurrentTab('submissions')}
                >
                  Submissions
                </Link>
                <Link
                  href="/assignments"
                  className={`px-3 py-2 rounded-md ${
                    currentTab === 'assignments' ? 'bg-blue-100 text-blue-700' : 'text-gray-700'
                  }`}
                  onClick={() => setCurrentTab('assignments')}
                >
                  Assignments
                </Link>
                <Link
                  href="/marking-suite"
                  className={`px-3 py-2 rounded-md ${
                    currentTab === 'marking-suite' ? 'bg-blue-100 text-blue-700' : 'text-gray-700'
                  }`}
                  onClick={() => setCurrentTab('marking-suite')}
                >
                  Marking Suite
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Dashboard Content */}
      <main className="max-w-7xl mx-auto py-6 px-4">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {/* Placeholder cards - we can update these later */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <h3 className="text-lg font-medium">Recent Submissions</h3>
              <p className="mt-1 text-gray-500">View recent student submissions</p>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <h3 className="text-lg font-medium">Active Assignments</h3>
              <p className="mt-1 text-gray-500">Manage current assignments</p>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <h3 className="text-lg font-medium">Marking Progress</h3>
              <p className="mt-1 text-gray-500">Track grading progress</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}