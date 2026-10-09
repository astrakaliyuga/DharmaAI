# DharmaAI API Documentation

## 20 Agents

### FileAgent
- `write <file> <content>` | `read <file>` | `list` | `delete <file>`

### ShellAgent
- `run <command>` — Allowed: ls, pwd, echo, cat, date, whoami, df, free, uptime, uname

### CodeAgent
- `python <code>`

### WebAgent
- `search <query>` | `fetch <url>`

### VoiceAgent
- `speak <text>` | `transcribe <file>`

### ImageAgent
- `generate <prompt>`

### VideoAgent
- `create <image> <audio>`

### SystemAgent
- `system info` | `cpu` | `ram` | `disk` | `process`

### NetworkAgent
- `ping <host>` | `dig <domain>` | `whois <domain>`

### DatabaseAgent
- `database <sql>`

### PDFAgent
- `pdf read <file>`

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

### TranslateAgent
- `translate <from> <to> <text>`

### SummarizeAgent
- `summarize <text>`

### SentimentAgent
- `sentiment <text>`
