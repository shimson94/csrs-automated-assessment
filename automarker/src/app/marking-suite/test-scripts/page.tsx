"use client"
import React, { useState } from 'react'
import { Input } from '@/components/MarkingInput'
import { Button } from '@/components/Button'
import { Dialog } from '@/components/MarkingDialog'
import { FaSearch, FaPlus, FaTrash, FaTimes } from 'react-icons/fa'
import Navbar from '@/components/Navbar'

interface TestScript {
  id: string
  name: string
  dateUploaded: string
  size: string
  language: string
}

interface Assignment {
  id: string
  title: string
  course: string
  dueDate: string
}

const TestScriptsPage = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [selectedScript, setSelectedScript] = useState<TestScript | null>(null)
  const [scripts, setScripts] = useState<TestScript[]>([
    {
      id: '1',
      name: 'test_assignment1.py',
      dateUploaded: '2024-03-20',
      size: '2.4 KB',
      language: 'Python'
    }
  ])

  const assignments: Assignment[] = [
    { id: '1', title: 'Assignment 1', course: 'CS101', dueDate: '2024-04-01' },
    { id: '2', title: 'Assignment 2', course: 'CS101', dueDate: '2024-04-15' }
  ]

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const newScript: TestScript = {
        id: Date.now().toString(),
        name: file.name,
        dateUploaded: new Date().toLocaleDateString(),
        size: `${(file.size / 1024).toFixed(2)} KB`,
        language: file.name.split('.').pop()?.toUpperCase() || 'Unknown'
      }
      setScripts([...scripts, newScript])
    }
  }

  const deleteScript = (id: string) => {
    setScripts(scripts.filter(script => script.id !== id))
  }

  const filteredScripts = scripts.filter(script =>
    script.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar currentTab="marking-suite" setCurrentTab={() => {}} />
      <main className="pt-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Test Scripts</h1>
          
          <div className="flex items-center gap-4">
            <div className="relative">
              <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                type="text"
                placeholder="Search scripts..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Button variant="outline" onClick={() => document.getElementById('file-upload')?.click()}>
              <FaPlus className="h-4 w-4 mr-2" />
              Add Script
            </Button>
            <input
              id="file-upload"
              type="file"
              accept=".py,.js,.ts"
              className="hidden"
              onChange={handleFileUpload}
            />
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filteredScripts.map((script) => (
            <div
              key={script.id}
              className="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-medium text-gray-900">{script.name}</h3>
                  <p className="text-sm text-gray-500">Uploaded: {script.dateUploaded}</p>
                </div>
                <button
                  onClick={() => deleteScript(script.id)}
                  className="text-gray-400 hover:text-red-500 transition-colors"
                >
                  <FaTrash className="h-4 w-4" />
                </button>
              </div>
              
              <div className="flex items-center justify-between mt-4">
                <span className="text-xs bg-slate-100 text-slate-700 px-2 py-1 rounded">
                  {script.language}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setSelectedScript(script)
                    setIsDialogOpen(true)
                  }}
                >
                  Apply to Assignment
                </Button>
              </div>
            </div>
          ))}
        </div>
      </main>

        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md mx-4">
            <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold">Select Assignment</h2>
            <button
                onClick={() => setIsDialogOpen(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
            >
                <FaTimes className="h-5 w-5" />
            </button>
            </div>
            
            <Input
            type="text"
            placeholder="Search assignments..."
            className="mb-4"
            />
            
            <div className="space-y-2 max-h-64 overflow-y-auto">
            {assignments.map((assignment) => (
                <button
                key={assignment.id}
                className="w-full p-3 text-left hover:bg-gray-50 rounded-md"
                onClick={() => {
                    console.log(`Applying ${selectedScript?.name} to ${assignment.title}`)
                    setIsDialogOpen(false)
                }}
                >
                <h3 className="font-medium">{assignment.title}</h3>
                <p className="text-sm text-gray-500">{assignment.course}</p>
                </button>
            ))}
            </div>
        </div>
        </Dialog>
    </div>
  )
}

export default TestScriptsPage