import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import MarkingSuite from '../../src/app/marking-suite/page'

describe('MarkingSuite', () => {
  it('renders heading', () => {
    render(<MarkingSuite />)
    const heading = screen.getByText('Marking Suite')
    expect(heading).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(<MarkingSuite />)
    expect(screen.getByText('Upload Test Scripts')).toBeInTheDocument()
    expect(screen.getByText('Mark Assignments')).toBeInTheDocument()
  })
})