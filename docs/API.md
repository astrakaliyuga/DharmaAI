# DharmaAI API Documentation

## 17 Agents

### FileAgent
- `write <file> <content>` — Write file
- `read <file>` — Read file
- `list` — List files
- `delete <file>` — Delete file

### ShellAgent
- `run <command>` — Safe command
- Allowed: ls, pwd, echo, cat, date, whoami, df, free, uptime, uname

### CodeAgent
- `python <code>` — Run Python

### WebAgent
- `search <query>` — Web search
- `fetch <url>` — Fetch URL

### VoiceAgent
- `speak <text>` — TTS
- `transcribe <file>` — STT

### ImageAgent
- `generate <prompt>` — Image

### VideoAgent
- `create <image> <audio>` — Video

### SystemAgent
- `system info` | `cpu` | `ram` | `disk` | `process`

### NetworkAgent
- `ping <host>` | `dig <domain>` | `whois <domain>`

### DatabaseAgent
- `database <sql>` — SQLite

### PDFAgent
- `pdf read <file>` — PDF

### BackupAgent
- `backup list` | `backup run`

### EmailAgent
- `email send <to> <subject> <body>`

### SchedulerAgent
- `schedule list` | `schedule add <cron> <cmd>`

### EncryptionAgent
- `encrypt <text>` | `decrypt <base64>` | `hash <text>`

### FileWatcherAgent
- `watch <directory>`

### APIAgent
- `api get <url>` | `api post <url> <data>`

