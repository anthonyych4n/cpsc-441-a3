# 🐼 Panda Chat Room - Assignment 3

## 📚 Background
**Objective:** Create a client-server chat application using Python's socket programming with panda-themed interactions.  
**Key Requirements:**
- Server handles multiple clients via threading
- Messages decorated with panda emojis/ASCII art
- Special commands: `@bamboo`, `@grove`, `@leaves`
- Graceful error handling and disconnections
- Creative panda-themed features

### 📁 File Structure
├── server.py

├── client.py

├── README.md

└── panda_server.log

### 📥 Installation & Usage

1.Start Server

```
python server.py
```

2.Connect Clients

```
python client.py
```

- Enter panda name when prompted
- Start chatting or use commands

#### 📝 Logging
Server generates panda_server.log with:
```
[2025-03-05 15:31:02] Message from Joe1: @hug
[2025-03-05 15:31:15] User joined: Joe2
```

### 🎨 Creative Features
Welcome ASCII Art

```
(\_/)  
(•.•)  
/ >🎍 Welcome!
```
Panda Emotes

@hug, @love, @sad trigger ASCII art responses

Random Decorations
Messages broadcast with random emojis: 🐼, 🎍, 🌿
