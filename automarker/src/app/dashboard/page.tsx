// page.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'
import ActivityCard, { Activity } from '@/components/ActivityCard'
import Navbar from '@/components/Navbar'

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
  },
  {
    id: 4,
    type: 'assignment',
    time: '1 hour ago',
    title: 'New assignment published',
    description: 'Assignment 3: Data Structures'
  },
  {
    id: 5,
    type: 'assignment',
    time: '1 hour ago',
    title: 'New assignment published',
    description: 'Assignment 3: Data Structures'
  },
  {
    id: 6,
    type: 'assignment',
    time: '1 hour ago',
    title: 'New assignment published',
    description: 'Assignment 3: Data Structures'
  }
];

export default function Dashboard() {
  const [currentTab, setCurrentTab] = useState('home')

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar currentTab={currentTab} setCurrentTab={setCurrentTab} />

      <main className="pt-16 max-w-7xl mx-auto py-6 px-4">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        
        {/* Quick Stats Row */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-blue-600">Pending Reviews</p>
            <p className="text-2xl font-bold">23</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-sm text-green-600">Graded Today</p>
            <p className="text-2xl font-bold">45</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg">
            <p className="text-sm text-yellow-600">Active Assignments</p>
            <p className="text-2xl font-bold">3</p>
          </div>
        </div>

        
      
        <div className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Activities */}
            <div className="lg:col-span-2 bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium mb-4 flex justify-between items-center">
            Recent Activities
            <Link href="/dashboard/recents" className="text-blue-600 hover:underline text-sm">
              View all
            </Link>
            </h2>
            <div className="space-y-4">
            {recentActivities.slice(0, 5).map((activity) => (
              <ActivityCard key={activity.id} activity={activity} />
            ))}
            </div>
          </div>
      
          {/* Priority Tasks */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium mb-4">Priority Tasks</h2>
            <div className="space-y-3">
              <div className="flex items-center p-2 bg-red-50 rounded">
                <div className="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                <p className="text-sm">5 submissions need manual review</p>
              </div>
              <div className="flex items-center p-2 bg-yellow-50 rounded">
                <div className="w-2 h-2 bg-yellow-500 rounded-full mr-2"></div>
                <p className="text-sm">Assignment 2 deadline in 2 hours</p>
              </div>
              <div className="flex items-center p-2 bg-blue-50 rounded">
                <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                <p className="text-sm">Update test cases for Lab 3</p>
              </div>
            </div>
      
            {/* System Status */}
            <div className="mt-6">
              <h3 className="text-sm font-medium mb-2">System Status</h3>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-600">All systems operational</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}