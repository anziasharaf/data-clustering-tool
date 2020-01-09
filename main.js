const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')

/*************************** py process *********************************/

const PY_DIST_FOLDER = 'appdist' 
const PY_FOLDER = 'app'
const PY_MODULE = 'api' // without .py suffix

let pyProc = null
let pyPort = null

const guessPackaged = () => {
  const fullPath = path.join(__dirname, PY_DIST_FOLDER)
  return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
  if (!guessPackaged()) {
    return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
  }
  if (process.platform === 'win32') {
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
  }
  return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
}

const selectPort = () => {
  pyPort = 4242
  return pyPort
}
c = "/home/icfoss5/Desktop/Projects/scstproj/codes/Test1.csv"
const createPyProc = () => {
  let script = getScriptPath()
  let port = '' + selectPort()

  if (true){//(guessPackaged()) {
    pyProc = require('child_process').execFile(script, [port])
  } else {
    pyProc = require('child_process').spawn('/home/user/my_env/bin/python', [script, port])
    console.log(pyProc)
  }
 
  if (pyProc != null) {
    //console.log(pyProc)
    console.log('child process success on port ' + port)
  }
}

const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
  pyPort = null
}

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)

/************************* window management ****************************/

let mainWindow = null

const createWindow = () => {
  mainWindow = new BrowserWindow({icon:'favicon.png'})
  mainWindow.maximize()
  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))
  //mainWindow.webContents.openDevTools()

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})
