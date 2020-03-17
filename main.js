// Modules to control application life and create native browser window
const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')

// To Run Python Script
let spawn = require('child_process').spawn

function createWindow() {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    title: 'Scraper',
    webPreferences: {
      nodeIntegration: true,
      preload: path.join(__dirname, 'preload.js')
    }
  })

  // and load the index.html of the app.
  mainWindow.loadFile('index.html')

  // Open the DevTools.
  mainWindow.webContents.openDevTools()
}

ipcMain.on('url', (event, url) => {
  letScrap(url, (msg) => {

    console.log(msg)
    event.reply('message', msg)
  })
})



app.whenReady().then(createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', function () {
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})


// Python Communication

const letScrap = (url, cb) => {

  var py = spawn('python', ["scrap.py", url]);

  let dataString = '';

  /*We have to stringify the data first otherwise our python process wont recognize it*/
  // py.stdin.write(url);

  /*Here we are saying that every time our node application receives data from the python process output stream(on 'data'), we want to convert that received data into a string and append it to the overall dataString.*/
  py.stdout.on('data', function (data) {
    dataString += data.toString();
  });

  /*Once the stream is done (on 'end') we want to simply log the received data to the console.*/
  py.stdout.on('end', function () {
    dataString = dataString.trim();
    cb(dataString);
  });

  py.stdin.end();
}

