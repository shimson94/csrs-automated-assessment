// pages/recent-activities.tsx
"use client"

import React, { useState } from 'react'
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
  }
];

const RecentActivities = () => {
  const [currentTab, setCurrentTab] = useState('recent-activities');

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <Navbar currentTab={currentTab} setCurrentTab={setCurrentTab} />

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