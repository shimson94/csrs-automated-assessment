import React, { useState } from 'react';
import Link from 'next/link';


interface NavbarProps {

    currentTab: string;
  
    setCurrentTab: React.Dispatch<React.SetStateAction<string>>;
  
  }
  

  

const Navbar: React.FC<NavbarProps> = () => {
  const [currentTab, setCurrentTab] = useState('home');

  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
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

          {/* Mobile Menu Button */}
          <div className="flex items-center md:hidden">
            <button
              type="button"
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              aria-controls="mobile-menu"
              aria-expanded={isMobileMenuOpen}
              onClick={toggleMobileMenu}
            >
              <span className="sr-only">Open main menu</span>
              {/* Icon when menu is closed. */}
              <svg className={`${isMobileMenuOpen ? 'hidden' : 'block'} h-6 w-6`} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7" />
              </svg>
              {/* Icon when menu is open. */}
              <svg className={`${isMobileMenuOpen ? 'block' : 'hidden'} h-6 w-6`} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <div className={`md:hidden ${isMobileMenuOpen ? 'block' : 'hidden'}`} id="mobile-menu">
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <Link
            href="/submissions"
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              currentTab === 'submissions' ? 'bg-blue-100 text-blue-700' : 'text-gray-700'
            }`}
            onClick={() => {
              setCurrentTab('submissions');
              setIsMobileMenuOpen(false);
            }}
          >
            Submissions
          </Link>
          <Link
            href="/assignments"
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              currentTab === 'assignments' ? 'bg-blue-100 text-blue-700' : 'text-gray-700'
            }`}
            onClick={() => {
              setCurrentTab('assignments');
              setIsMobileMenuOpen(false);
            }}
          >
            Assignments
          </Link>
          <Link
            href="/marking-suite"
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              currentTab === 'marking-suite' ? 'bg-blue-100 text-blue-700' : 'text-gray-700'
            }`}
            onClick={() => {
              setCurrentTab('marking-suite');
              setIsMobileMenuOpen(false);
            }}
          >
            Marking Suite
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;