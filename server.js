const express = require('express');
const http = require('http');
const socketIO = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

const PORT = process.env.PORT || 5003;

let workerSocket = null;

io.on('connection', (socket) => {
    console.log('A user connected');

    socket.on('worker', () => {
        workerSocket = socket;
        console.log('Worker connected');
    });

    socket.on('admin', (command) => {
        if (workerSocket) {
            workerSocket.emit('command', command);
        }
    });

    socket.on('worker-response', (response) => {
        socket.broadcast.emit('admin-response', response);
    });

    socket.on('disconnect', () => {
        console.log('A user disconnected');
        if (socket === workerSocket) {
            workerSocket = null;
        }
    });
});

server.listen(PORT, () => {
    console.log(`Listening on port ${PORT}...`);
});
