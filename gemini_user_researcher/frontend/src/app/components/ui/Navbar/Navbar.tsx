export const Navbar = () => {
    return (
      <nav className="bg-navy border-b border-navy-light">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo/Brand */}
            <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-neutral-50 hover:text-sand transition-colors">UI Insight</h1>
            </div>
  
          </div>
        </div>
      </nav>
    );
  };