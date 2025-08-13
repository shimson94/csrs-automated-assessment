"use client"

import React, { useEffect, useState } from 'react'
import Navbar from '@/components/Navbar'
import { Input } from '@/components/MarkingInput'
import { FaSearch } from 'react-icons/fa'
import { AssignmentCard } from '@/components/AssignmentCard'

interface Assignment {
  id: number
  title: string
  module: string
  dueDate: Date
  submissions: number
  marked: number
}

const MarkAssignmentsPage = () => {
  const [assignments, setAssignments] = useState<Assignment[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [sortOrder] = useState<'asc' | 'desc'>('asc')

  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        const response = await fetch('/api/assignments')
        if (!response.ok) throw new Error('Failed to fetch assignments')
        const data = await response.json()
        setAssignments(data.map((assignment: Assignment) => ({
          ...assignment,
          dueDate: new Date(assignment.dueDate)
        })))
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch assignments')
      } finally {
        setIsLoading(false)
      }
    }

    fetchAssignments()
  }, [])

  const filteredAssignments = assignments
    .filter((assignment) => {
      return (
        assignment.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        assignment.module.toLowerCase().includes(searchQuery.toLowerCase())
      )
    })
    .sort((a, b) => {
      if (sortOrder === 'asc') {
        return a.dueDate.getTime() - b.dueDate.getTime()
      } else {
        return b.dueDate.getTime() - a.dueDate.getTime()
      }
    })

  if (isLoading) return <div>Loading assignments...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar currentTab="marking-suite" setCurrentTab={() => {}} />
      <main className="pt-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header section - always visible */}
        <div className="flex flex-col md:flex-row justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Mark Assignments</h1>
          <div className="flex items-center gap-4 mt-4 md:mt-0">
            <div className="relative">
              <Input
                type="text"
                placeholder="Search assignments..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
              <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            </div>
          </div>
        </div>

        {/* Content section with error handling */}
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          {error ? (
            <div className="p-8 text-center">
              <p className="text-lg text-red-600">Error: {error}</p>
            </div>
          ) : (
            <ul>
              {filteredAssignments.map((assignment) => (
                <AssignmentCard 
                  key={assignment.id}
                  assignment={assignment}
                  onMark={(id) => console.log(`Marking assignment ${id}`)}
                />
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  )
}

export default MarkAssignmentsPage
