"use client"

import React, { useState } from 'react'
import Navbar from '@/components/Navbar'
import { Input } from '@/components/MarkingInput'
import { Button } from '@/components/Button'
import { FaSearch, FaSort } from 'react-icons/fa'
import DatePicker from 'react-datepicker/dist/react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import { AssignmentCard } from '@/components/AssignmentCard'

interface Assignment {
  id: string
  title: string
  module: string
  dueDate: Date
  submissions: number
  marked: number
}

const MarkAssignmentsPage = () => {
  const [assignments, setAssignments] = useState<Assignment[]>([
    {
      id: '1',
      title: 'Assignment 1: Haskell Advanced News Classifier',
      module: 'OOP',
      dueDate: new Date('2024-11-01'),
      submissions: 50,
      marked: 30,
    },
    {
      id: '2',
      title: 'Assignment 2: Homeless Shelter Management System for CS students',
      module: 'FP',
      dueDate: new Date('2024-12-15'),
      marked: 20,
      submissions: 60
    },
  ])

  const [searchQuery, setSearchQuery] = useState('')
  const [filterDate, setFilterDate] = useState<Date | null>(null)
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc')

  const filteredAssignments = assignments
    .filter((assignment) => {
      const matchesSearch =
        assignment.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        assignment.module.toLowerCase().includes(searchQuery.toLowerCase())

      const matchesDate = filterDate ? assignment.dueDate <= filterDate : true

      return matchesSearch && matchesDate
    })
    .sort((a, b) => {
      if (sortOrder === 'asc') {
        return a.dueDate.getTime() - b.dueDate.getTime()
      } else {
        return b.dueDate.getTime() - a.dueDate.getTime()
      }
    })

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar currentTab="marking-suite" setCurrentTab={() => {}} />
      <main className="pt-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Page Header */}
        <div className="flex flex-col md:flex-row justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Mark Assignments</h1>
          <div className="flex items-center gap-4 mt-4 md:mt-0">
            {/* Search Input */}
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

            {/* Date Picker */}
            <DatePicker
              selected={filterDate}
              onChange={(date: React.SetStateAction<Date | null>) => setFilterDate(date)}
              placeholderText="Filter by due date"
              dateFormat="dd-MM-yyyy"
              className="h-10 px-3 py-2 text-sm rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            {/* Sort Button */}
            <Button
              variant="outline"
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            >
              <FaSort className="mr-2" />
              {sortOrder === 'asc' ? 'Sort Desc' : 'Sort Asc'}
            </Button>
          </div>
        </div>

        {/* Assignments List */}
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul>
            {filteredAssignments.map((assignment) => (
              <AssignmentCard 
                key={assignment.id}
                assignment={assignment}
                onMark={(id) => {
                  console.log(`Marking assignment ${id}`)
                  // Placeholder for marking logic
                }}
              />
            ))}
          </ul>
        </div>
      </main>
    </div>
  )
}

export default MarkAssignmentsPage
