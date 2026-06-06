function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 px-6 py-4">
        <h1 className="text-xl font-bold tracking-tight">PPT Reel Converter</h1>
        <p className="text-sm text-gray-400">Landscape PPTX → Instagram Reel (9:16) Scenes</p>
      </header>
      <main className="flex items-center justify-center h-[calc(100vh-80px)]">
        <div className="text-center">
          <div className="border-2 border-dashed border-gray-700 rounded-xl p-12 max-w-md">
            <svg className="mx-auto h-12 w-12 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m6.75 12l-3-3m0 0l-3 3m3-3v3.75M3.375 19.5h9.75m1.125-9.75H15M3.375 19.5c-.621 0-1.125-.504-1.125-1.125V4.125c0-.621.504-1.125 1.125-1.125h6.75c.621 0 1.125.504 1.125 1.125v4.5" />
            </svg>
            <p className="mt-4 text-gray-400">Drop a landscape PPTX file here</p>
            <p className="text-xs text-gray-500 mt-1">or click to browse</p>
          </div>
          <p className="mt-4 text-xs text-gray-600">
            Sequential per-slide processing with 4-gate validation and approval
          </p>
        </div>
      </main>
    </div>
  )
}

export default App