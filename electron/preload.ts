import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  selectFile: () => ipcRenderer.invoke('select-file'),
  selectOutputDir: () => ipcRenderer.invoke('select-output-dir'),
  startPythonSidecar: (args: {
    filePath: string
    templateStyle: string
    apiKey?: string
    useAi?: boolean
  }) => ipcRenderer.invoke('start-python-sidecar', args),
})
