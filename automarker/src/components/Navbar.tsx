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
    <nav className="fixed top-0 w-full backdrop-blur-sm border-b border-slate-200/20 bg-white/75 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-8">
            {/* Logo/Home */}
            <Link 
              href="/"
              className="flex items-center gap-2 transition-colors"
              onClick={() => setCurrentTab('home')}
            >
              <span className="font-inter font-semibold text-xl bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                AutoMarker
              </span>
            </Link>
  
            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-6">
              {['submissions', 'assignments', 'marking-suite'].map((item) => (
                <Link
                  key={item}
                  href={`/${item}`}
                  className={`
                    font-inter text-sm font-medium px-3 py-2 rounded-md
                    transition-all duration-200 ease-in-out
                    ${currentTab === item 
                      ? 'bg-slate-100 text-slate-900' 
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                    }
                  `}
                  onClick={() => setCurrentTab(item)}
                >
                  {item.charAt(0).toUpperCase() + item.slice(1).replace('-', ' ')}
                </Link>
              ))}
            </div>
          </div>
  
          {/* Mobile Menu Button */}
          <div className="flex md:hidden">
            <button
              type="button"
              className="inline-flex items-center justify-center rounded-md p-2
                         text-slate-600 hover:text-slate-900 hover:bg-slate-100
                         focus:outline-none focus:ring-2 focus:ring-inset focus:ring-slate-500
                         transition-colors"
              onClick={toggleMobileMenu}
            >
              <span className="sr-only">Toggle menu</span>
              {isMobileMenuOpen ? (
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>
  
      {/* Mobile Menu - Updated for more compact design */}
    <div
      className={`
        md:hidden
        transition-all duration-200 ease-in-out
        ${isMobileMenuOpen ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2 pointer-events-none'}
      `}
    >
      <div className="px-2 py-1 space-y-0.5 bg-white/75 backdrop-blur-sm border-t border-slate-200/20">
        {['submissions', 'assignments', 'marking-suite'].map((item) => (
          <Link
            key={item}
            href={`/${item}`}
            className={`
              block font-inter text-xs font-medium px-2.5 py-1.5 rounded-md
              transition-all duration-150 ease-in-out
              ${currentTab === item 
                ? 'bg-slate-100 text-slate-900' 
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }
            `}
            onClick={() => {
              setCurrentTab(item);
              setIsMobileMenuOpen(false);
            }}
          >
            {item.charAt(0).toUpperCase() + item.slice(1).replace('-', ' ')}
          </Link>
        ))}
      </div>
    </div>
    </nav>
  );
};

export default Navbar;