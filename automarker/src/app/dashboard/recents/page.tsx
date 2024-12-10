// pages/recent-activities.tsx
import React from 'react'
import Link from 'next/link'
import ActivityCard, { Activity } from '@/components/ActivityCard'

const recentActivities: Activity[] = [
  {
    id: 1,
    type: 'submission',
    time: '2 minutes ago',
    title: 'New submission: Assignment 2',
    description: 'by John Smith'
  },
  {
    id: 2,
    type: 'grading',
    time: '15 minutes ago',
    title: 'Grading completed: Lab 1',
    description: '25 submissions processed'
  },
  {
    id: 3,
    type: 'assignment',
    time: '1 hour ago',
    title: 'New assignment published',
    description: 'Assignment 3: Data Structures'
  }
];

const RecentActivities = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-12">
            <div className="flex">
              {/* Logo/Home */}
              <Link 
                href="/"
                className="flex items-center px-4 hover:text-blue-600 transition-colors"
              >
                <span className="font-bold text-xl text-blue-800">AutoMarker</span>
              </Link>

              {/* Navigation Links */}
              <div className="hidden md:flex items-center space-x-4">
                <Link
                  href="/submissions"
                  className="px-3 py-2 rounded-md text-gray-700 hover:text-blue-600 transition-colors"
                >
                  Submissions
                </Link>
                <Link
                  href="/assignments"
                  className="px-3 py-2 rounded-md text-gray-700 hover:text-blue-600 transition-colors"
                >
                  Assignments
                </Link>
                <Link
                  href="/marking-suite"
                  className="px-3 py-2 rounded-md text-gray-700 hover:text-blue-600 transition-colors"
                >
                  Marking Suite
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Recent Activities</h1>
        <div className="space-y-4">
          {recentActivities.map((activity) => (
            <ActivityCard key={activity.id} activity={activity} />
          ))}
        </div>
      </main>
    </div>
  )
}

export default RecentActivities