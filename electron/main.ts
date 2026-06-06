import { app, BrowserWindow, ipcMain, dialog } from 'electron'
import path from 'path'
import { fileURLToPath } from 'url'
import { spawn } from 'child_process'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

let mainWindow: BrowserWindow | null = null
let pythonProcess: ReturnType<typeof spawn> | null = null

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  })

  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadFile(path.join(__dirname, '../index.html'))
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../index.html'))
  }
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
  if (pythonProcess) {
    pythonProcess.kill()
  }
})

// IPC handlers
ipcMain.handle('select-file', async () => {
  const result = await dialog.showOpenDialog(mainWindow!, {
    properties: ['openFile'],
    filters: [{ name: 'PowerPoint', extensions: ['pptx'] }],
  })
  return result.filePaths[0] || null
})

ipcMain.handle('select-output-dir', async () => {
  const result = await dialog.showOpenDialog(mainWindow!, {
    properties: ['openDirectory'],
  })
  return result.filePaths[0] || null
})

ipcMain.handle('start-python-sidecar', async (_, args: {
  filePath: string
  templateStyle: string
  apiKey?: string
  useAi?: boolean
}) => {
  return new Promise((resolve, reject) => {
    const pythonPath = path.join(__dirname, '../../python/reel_converter/cli.py')
    const pythonExe = process.platform === 'win32' ? 'python' : 'python3'
    
    const env = { ...process.env }
    if (args.apiKey) {
      env.OPENCODE_GO_API_KEY = args.apiKey
    }

    pythonProcess = spawn(pythonExe, [
      pythonPath,
      args.filePath,
      '--template', args.templateStyle,
      '--auto-approve',
    ], { env, cwd: path.join(__dirname, '../..') })

    let output = ''
    let error = ''

    pythonProcess.stdout?.on('data', (data) => {
      output += data.toString()
    })

    pythonProcess.stderr?.on('data', (data) => {
      error += data.toString()
    })

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        resolve({ success: true, output })
      } else {
        reject(new Error(`Python process exited with code ${code}: ${error}`))
      }
    })
  })
})
