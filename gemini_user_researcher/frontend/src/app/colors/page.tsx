export default function ColorsPage() {
    return (
      <main className="min-h-screen bg-neutral-50 p-8">
        <div className="max-w-6xl mx-auto space-y-12">
          {/* Core Brand Colors */}
          <section>
            <h2 className="text-2xl font-bold mb-4 text-navy">Core Brand Colors</h2>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              {/* Navy */}
              <div className="space-y-2">
                <div className="h-24 rounded-lg bg-navy flex items-end p-2">
                  <span className="text-neutral-0 text-sm">navy</span>
                </div>
                <div className="h-12 rounded-lg bg-navy-light flex items-center p-2">
                  <span className="text-neutral-0 text-sm">navy-light</span>
                </div>
                <div className="h-12 rounded-lg bg-navy-dark flex items-center p-2">
                  <span className="text-neutral-0 text-sm">navy-dark</span>
                </div>
              </div>
  
              {/* Teal */}
              <div className="space-y-2">
                <div className="h-24 rounded-lg bg-teal flex items-end p-2">
                  <span className="text-neutral-0 text-sm">teal</span>
                </div>
                <div className="h-12 rounded-lg bg-teal-light flex items-center p-2">
                  <span className="text-neutral-0 text-sm">teal-light</span>
                </div>
                <div className="h-12 rounded-lg bg-teal-dark flex items-center p-2">
                  <span className="text-neutral-0 text-sm">teal-dark</span>
                </div>
              </div>
  
              {/* Aqua */}
              <div className="space-y-2">
                <div className="h-24 rounded-lg bg-aqua flex items-end p-2">
                  <span className="text-navy text-sm">aqua</span>
                </div>
                <div className="h-12 rounded-lg bg-aqua-light flex items-center p-2">
                  <span className="text-navy text-sm">aqua-light</span>
                </div>
                <div className="h-12 rounded-lg bg-aqua-dark flex items-center p-2">
                  <span className="text-navy text-sm">aqua-dark</span>
                </div>
              </div>
  
              {/* Sand */}
              <div className="space-y-2">
                <div className="h-24 rounded-lg bg-sand flex items-end p-2">
                  <span className="text-navy text-sm">sand</span>
                </div>
                <div className="h-12 rounded-lg bg-sand-light flex items-center p-2">
                  <span className="text-navy text-sm">sand-light</span>
                </div>
                <div className="h-12 rounded-lg bg-sand-dark flex items-center p-2">
                  <span className="text-navy text-sm">sand-dark</span>
                </div>
              </div>
  
              {/* Sage */}
              <div className="space-y-2">
                <div className="h-24 rounded-lg bg-sage flex items-end p-2">
                  <span className="text-neutral-0 text-sm">sage</span>
                </div>
                <div className="h-12 rounded-lg bg-sage-light flex items-center p-2">
                  <span className="text-neutral-0 text-sm">sage-light</span>
                </div>
                <div className="h-12 rounded-lg bg-sage-dark flex items-center p-2">
                  <span className="text-neutral-0 text-sm">sage-dark</span>
                </div>
              </div>
            </div>
          </section>
  
          {/* Neutral Colors */}
          <section>
            <h2 className="text-2xl font-bold mb-4 text-navy">Neutral Colors</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="space-y-2">
                <div className="h-24 rounded-lg bg-neutral-0 border border-neutral-200 flex items-end p-2">
                  <span className="text-neutral-900 text-sm">neutral-0 (white)</span>
                </div>
                <div className="h-12 rounded-lg bg-neutral-50 border border-neutral-200 flex items-center p-2">
                  <span className="text-neutral-900 text-sm">neutral-50</span>
                </div>
                <div className="h-12 rounded-lg bg-neutral-100 border border-neutral-200 flex items-center p-2">
                  <span className="text-neutral-900 text-sm">neutral-100</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="h-24 rounded-lg bg-neutral-200 flex items-end p-2">
                  <span className="text-neutral-900 text-sm">neutral-200</span>
                </div>
                <div className="h-12 rounded-lg bg-neutral-300 flex items-center p-2">
                  <span className="text-neutral-900 text-sm">neutral-300</span>
                </div>
                <div className="h-12 rounded-lg bg-neutral-400 flex items-center p-2">
                  <span className="text-neutral-900 text-sm">neutral-400</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="h-24 rounded-lg bg-neutral-500 flex items-end p-2">
                  <span className="text-neutral-0 text-sm">neutral-500</span>
                </div>
                <div className="h-12 rounded-lg bg-neutral-600 flex items-center p-2">
                  <span className="text-neutral-0 text-sm">neutral-600</span>
                </div>
                <div className="h-12 rounded-lg bg-neutral-700 flex items-center p-2">
                  <span className="text-neutral-0 text-sm">neutral-700</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="h-24 rounded-lg bg-neutral-800 flex items-end p-2">
                  <span className="text-neutral-0 text-sm">neutral-800</span>
                </div>
                <div className="h-12 rounded-lg bg-neutral-900 flex items-center p-2">
                  <span className="text-neutral-0 text-sm">neutral-900</span>
                </div>
                <div className="h-12 rounded-lg bg-neutral-1000 flex items-center p-2">
                  <span className="text-neutral-0 text-sm">neutral-1000 (black)</span>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>
    );
  }