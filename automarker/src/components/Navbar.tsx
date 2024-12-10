import React, { useState } from 'react';
import Link from 'next/link';


interface NavbarProps {

    currentTab: string;
  
    setCurrentTab: React.Dispatch<React.SetStateAction<string>>;
  
  }
  

  

const Navbar: React.FC<NavbarProps> = () => {
  const [currentTab, setCurrentTab] = useState('home');

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-12">
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
  );
};

export default Navbar;