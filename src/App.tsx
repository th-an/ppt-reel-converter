import { useState, useCallback } from 'react'
import type {
  AppState,
} from './types'

function App() {
  const [appState, setAppState] = useState<AppState>({
    phase: 'upload',
    fingerprints: [],
    currentSlideIndex: 0,
    totalSlides: 0,
    currentResult: null,
    approvedSlides: new Set(),
    skippedSlides: new Set(),
    selectedTemplate: 'reel_clean',
    error: null,
  })

  const handleFileSelect = useCallback(async () => {
    try {
      const path = await (window as any).electronAPI.selectFile()
      if (path) {
        setAppState(prev => ({ ...prev, phase: 'scanning' }))
        
        const response = await (window as any).electronAPI.startPythonSidecar({
          filePath: path,
          templateStyle: appState.selectedTemplate,
        })
        
        console.log('Processing complete:', response)
        setAppState(prev => ({
          ...prev,
          phase: 'complete',
          totalSlides: prev.fingerprints.length,
        }))
      }
    } catch (error) {
      console.error('Error:', error)
      setAppState(prev => ({ ...prev, error: String(error), phase: 'upload' }))
    }
  }, [appState.selectedTemplate])

  const handleApprove = (slideNumber: number) => {
    setAppState(prev => {
      const approved = new Set(prev.approvedSlides)
      approved.add(slideNumber)
      return { ...prev, approvedSlides: approved }
    })
  }

  const handleSkip = (slideNumber: number) => {
    setAppState(prev => {
      const skipped = new Set(prev.skippedSlides)
      skipped.add(slideNumber)
      return { ...prev, skippedSlides: skipped }
    })
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex flex-col">
      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold tracking-tight">PPT Reel Converter</h1>
          <p className="text-sm text-gray-400">Landscape → Instagram Reel (9:16)</p>
        </div>
        <div className="text-sm text-gray-500">
          {appState.phase === 'upload' && 'Ready'}
          {appState.phase === 'scanning' && 'Scanning...'}
          {appState.phase === 'processing' && 'Processing...'}
          {appState.phase === 'complete' && 'Complete'}
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center p-6">
        {appState.phase === 'upload' && (
          <div className="w-full max-w-2xl">
            <div
              className="border-2 border-dashed border-gray-700 rounded-xl p-12 text-center hover:border-gray-500 transition-colors cursor-pointer"
              onClick={handleFileSelect}
            >
              <svg className="mx-auto h-16 w-16 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m6.75 12l-3-3m0 0l-3 3m3-3v3.75M3.375 19.5h9.75m1.125-9.75H15M3.375 19.5c-.621 0-1.125-.504-1.125-1.125V4.125c0-.621.504-1.125 1.125-1.125h6.75c.621 0 1.125.504 1.125 1.125v4.5" />
              </svg>
              <p className="mt-6 text-lg text-gray-300">Click to select a landscape PPTX file</p>
              <p className="mt-2 text-sm text-gray-500">The file will be processed slide by slide</p>
              <div className="mt-6 flex justify-center gap-2">
                {['reel_clean', 'reel_modern', 'reel_bold', 'reel_minimal', 'reel_corporate'].map((style) => (
                  <button
                    key={style}
                    onClick={(e) => {
                      e.stopPropagation()
                      setAppState(prev => ({ ...prev, selectedTemplate: style }))
                    }}
                    className={`px-3 py-1 rounded-full text-xs ${
                      appState.selectedTemplate === style
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                    }`}
                  >
                    {style.replace('reel_', '')}
                  </button>
                ))}
              </div>
            </div>
            
            <div className="mt-8 text-center text-sm text-gray-600">
              <p>4-Gate Pipeline: Scan → Plan → Render → Verify</p>
              <p className="mt-1">Sequential approval: Slide N+1 waits for Slide N approval</p>
            </div>
          </div>
        )}

        {appState.phase === 'scanning' && (
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-4 text-gray-400">Scanning PPTX file...</p>
            <p className="text-sm text-gray-600">Extracting text, images, charts, and theme</p>
          </div>
        )}

        {appState.phase === 'processing' && (
          <div className="w-full max-w-4xl">
            <div className="flex items-center gap-4 mb-6">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              <div>
                <p className="text-gray-300">Processing slide {appState.currentSlideIndex + 1} of {appState.totalSlides}</p>
                <p className="text-sm text-gray-500">Slide N+1 locked until approval</p>
              </div>
            </div>

            {/* Progress bar */}
            <div className="w-full bg-gray-800 rounded-full h-2 mb-8">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${appState.totalSlides > 0 ? ((appState.currentSlideIndex + 1) / appState.totalSlides) * 100 : 0}%` }}
              ></div>
            </div>

            {/* Slide thumbnails */}
            <div className="flex gap-2 mb-8 overflow-x-auto">
              {appState.fingerprints.map((fp, idx) => (
                <div
                  key={idx}
                  className={`flex-shrink-0 w-24 h-16 rounded-lg border-2 flex items-center justify-center text-xs ${
                    appState.approvedSlides.has(idx + 1)
                      ? 'border-green-500 bg-green-900/20 text-green-400'
                      : appState.skippedSlides.has(idx + 1)
                      ? 'border-gray-600 bg-gray-800 text-gray-500'
                      : idx === appState.currentSlideIndex
                      ? 'border-blue-500 bg-blue-900/20 text-blue-400'
                      : 'border-gray-700 bg-gray-800 text-gray-400'
                  }`}
                >
                  {fp.slide_number}
                </div>
              ))}
            </div>

            {/* Current slide result */}
            {appState.currentResult && (
              <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
                <div className="grid grid-cols-2 gap-6">
                  {/* Original */}
                  <div>
                    <h3 className="text-sm font-semibold text-gray-400 mb-3">Original Landscape</h3>
                    <div className="aspect-video bg-gray-800 rounded-lg p-4 flex items-center justify-center">
                      <div className="text-center">
                        <p className="text-lg font-bold">{appState.fingerprints[appState.currentSlideIndex]?.title_text || 'No Title'}</p>
                        <p className="text-sm text-gray-500 mt-2">
                          {appState.fingerprints[appState.currentSlideIndex]?.bullet_items.length || 0} bullets
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Result */}
                  <div>
                    <h3 className="text-sm font-semibold text-gray-400 mb-3">Portrait Preview</h3>
                    <div className="aspect-[9/16] bg-gray-800 rounded-lg p-4 flex items-center justify-center max-h-64">
                      <div className="text-center">
                        <p className="text-lg font-bold text-blue-400">
                          {appState.currentResult.scenes[0]?.placeholders_filled?.title || 'No Title'}
                        </p>
                        <div className="text-xs text-gray-400 mt-2 space-y-1">
                          {appState.currentResult.scenes.map((scene, i: number) => (
                            <p key={i}>Scene {i + 1}: {scene.layout_used}</p>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Gate scores */}
                <div className="mt-6 grid grid-cols-4 gap-3">
                  <div className="bg-gray-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-gray-500">Gate 1</p>
                    <p className="text-green-400 font-semibold">PASS</p>
                    <p className="text-xs text-gray-600">Scan</p>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-gray-500">Gate 2</p>
                    <p className={`font-semibold ${appState.currentResult.gate2.status === 'PASS' ? 'text-green-400' : 'text-yellow-400'}`}>
                      {appState.currentResult.gate2.status}
                    </p>
                    <p className="text-xs text-gray-600">Plan</p>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-gray-500">Gate 3</p>
                    <p className={`font-semibold ${appState.currentResult.gate3.status === 'PASS' ? 'text-green-400' : 'text-yellow-400'}`}>
                      {appState.currentResult.gate3.status}
                    </p>
                    <p className="text-xs text-gray-600">Render</p>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-gray-500">Gate 4</p>
                    <p className={`font-semibold ${appState.currentResult.gate4.status === 'PASS' ? 'text-green-400' : 'text-yellow-400'}`}>
                      {appState.currentResult.gate4.score}/100
                    </p>
                    <p className="text-xs text-gray-600">Verify</p>
                  </div>
                </div>

                {/* Approval controls */}
                <div className="mt-6 flex justify-center gap-3">
                  <button
                    onClick={() => handleApprove(appState.currentSlideIndex + 1)}
                    className="px-6 py-2 bg-green-600 hover:bg-green-500 rounded-lg font-semibold text-white transition-colors"
                  >
                    ✓ Approve Slide
                  </button>
                  <button
                    onClick={() => handleSkip(appState.currentSlideIndex + 1)}
                    className="px-6 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold text-white transition-colors"
                  >
                    ⊘ Skip
                  </button>
                  <button
                    className="px-6 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg font-semibold text-white transition-colors"
                  >
                    ↻ Retry
                  </button>
                </div>

                {/* Validation details */}
                {appState.currentResult.gate4.details.flags.length > 0 && (
                  <div className="mt-4 bg-yellow-900/20 border border-yellow-700/50 rounded-lg p-3">
                    <p className="text-sm font-semibold text-yellow-400 mb-2">Validation Flags</p>
                    <ul className="text-sm text-yellow-300/80 space-y-1">
                      {appState.currentResult.gate4.details.flags.map((flag: string, i: number) => (
                        <li key={i}>• {flag}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {appState.phase === 'complete' && (
          <div className="text-center">
            <div className="text-green-400 text-6xl mb-4">✓</div>
            <h2 className="text-2xl font-bold text-white mb-2">Conversion Complete</h2>
            <p className="text-gray-400 mb-6">
              {appState.approvedSlides.size} slides approved, {appState.skippedSlides.size} skipped
            </p>
            <button
              onClick={() => setAppState({
                phase: 'upload',
                fingerprints: [],
                currentSlideIndex: 0,
                totalSlides: 0,
                currentResult: null,
                approvedSlides: new Set(),
                skippedSlides: new Set(),
                selectedTemplate: 'reel_clean',
                error: null,
              })}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg font-semibold text-white transition-colors"
            >
              Convert Another File
            </button>
          </div>
        )}

        {appState.error && (
          <div className="mt-4 bg-red-900/20 border border-red-700/50 rounded-lg p-4 max-w-2xl">
            <p className="text-red-400 font-semibold">Error</p>
            <p className="text-red-300/80 text-sm mt-1">{appState.error}</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
