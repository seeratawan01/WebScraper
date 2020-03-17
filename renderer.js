const { ipcRenderer } = require('electron')
// console.log(ipcRenderer.sendSync('synchronous-message', 'ping')) // prints "pong"

// ipcRenderer.on('asynchronous-reply', (event, arg) => {
//     console.log(arg) // prints "pong"
// })
// ipcRenderer.send('asynchronous-message', 'ping')


document.getElementById("urlform").addEventListener("submit", (e) => {
    e.preventDefault();
    let url = document.getElementById("urlfield").value;

    ipcRenderer.send('url', url)
});

ipcRenderer.on('message', (event, arg) => {
    console.log(arg)
})

