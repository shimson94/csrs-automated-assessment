import { Button } from "@/components/Button"
import { FaCheckCircle, FaEye } from "react-icons/fa"

interface Assignment {
  id: number
  title: string
  dueDate: Date
  module: string
  marked: number
  submissions: number
}

interface AssignmentCardProps {
  assignment: Assignment
  onMark: (id: string) => void
}

export function AssignmentCard({ assignment, onMark }: AssignmentCardProps) {
  return (
    <li className="border-b border-gray-200">
      <div className="px-4 py-4 sm:px-6">
        {/* Assignment Header */}
        <div className="flex items-center justify-between">
          <div className="text-sm font-medium text-indigo-600 truncate">
            {assignment.title}
          </div>
          <div className="ml-2 flex-shrink-0 flex">
            <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
              Due {assignment.dueDate.toLocaleDateString()}
            </span>
          </div>
        </div>

        {/* Assignment Details */}
        <div className="mt-2 sm:flex sm:justify-between">
          <div className="sm:flex">
            <p className="flex items-center text-sm text-gray-500">
              Module: {assignment.module}
            </p>
          </div>
          <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
            <FaCheckCircle className="mr-1 text-green-500" />
            {assignment.marked}/{assignment.submissions} Marked
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-4 flex space-x-2">
          <Button variant="default" size="sm">
            <FaEye className="mr-1" />
            View Results
          </Button>
          <Button variant="default" size="sm">
            <FaCheckCircle className="mr-1" />
            Mark All
          </Button>
          <Button
            variant="default"
            size="sm"
            onClick={() => onMark(assignment.id.toString())}
          >
            Mark
          </Button>
        </div>
      </div>
    </li>
  )
}