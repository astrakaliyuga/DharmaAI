from brain.llm import LLMBrain
from brain.rag import RAGBrain
from brain.rag_integration import RAGIntegration
from agents.manager import AgentManager

def process_single_command(user_input, brain, rag, rag_int, manager):
    """Single command process chey"""
    cmd = user_input.lower().strip()
    
    if cmd in ["/quit", "/exit", "/bye", "quit", "exit", "bye", "q"]:
        brain.save_memory()
        return "EXIT"
    
    elif cmd == "/reset":
        brain.reset()
        return "Conversation reset."
    
    elif cmd == "/memory":
        result = "\n--- Recent Memory ---\n"
        for m in brain.recall(10):
            result += f"  [{m['metadata']['type']}] {m['content'][:80]}\n"
        return result
    
    elif cmd == "/save":
        path = brain.save_memory()
        return f"Saved to {path}"
    
    elif cmd.startswith("/remember "):
        content = user_input[10:].strip()
        brain.remember(content)
        return f"Remembered: {content}"
    
    elif cmd.startswith("/search "):
        query = user_input[8:].strip()
        results = brain.search_memory(query)
        result = f"\n--- Search Results for: {query} ---\n"
        if results['documents'] and results['documents'][0]:
            for doc in results['documents'][0]:
                result += f"  - {doc}\n"
        else:
            result += "  No results found.\n"
        return result
    
    elif cmd.startswith("/rag "):
        question = user_input[5:].strip()
        return f"RAG: {rag.query(question)}"
    
    elif cmd.startswith("/load "):
        filepath = user_input[6:].strip()
        return f"RAG: {rag_int.load_text_file(filepath)}"
    
    elif cmd == "/agents":
        result = "\n--- Available Agents ---\n"
        for name, desc in manager.list_agents():
            result += f"  {name}: {desc}\n"
        return result
    
    elif cmd.startswith("/agent "):
        task = user_input[7:].strip()
        return f"Agent: {manager.run(task)}"
    
    elif cmd.startswith("/web "):
        task = user_input[5:].strip()
        return f"Web: {manager.run(task)}"
    
    elif cmd.startswith("/speak "):
        text = user_input[7:].strip()
        return f"Voice: {manager.run(f'speak {text}')}"
    
    elif cmd.startswith("/transcribe "):
        audio = user_input[12:].strip()
        return f"Transcription: {manager.run(f'transcribe {audio}')}"
    
    elif cmd.startswith("/image "):
        prompt = user_input[7:].strip()
        return f"Image: {manager.run(f'generate {prompt}')}"
    
    elif cmd.startswith("/video "):
        args = user_input[7:].strip()
        return f"Video: {manager.run(f'create {args}')}"
    
    elif cmd == "/system":
        return f"System: {manager.run('system info')}"
    
    elif cmd == "/cpu":
        return f"CPU: {manager.run('cpu')}"
    
    elif cmd == "/ram":
        return f"RAM: {manager.run('ram')}"
    
    elif cmd == "/disk":
        return f"Disk: {manager.run('disk')}"
    
    elif cmd == "/process":
        return f"Process: {manager.run('process')}"
    
    elif cmd.startswith("/ping "):
        host = user_input[6:].strip()
        return f"Ping: {manager.run(f'ping -c 3 {host}')}"
    
    elif cmd.startswith("/dig "):
        domain = user_input[5:].strip()
        return f"Dig: {manager.run(f'dig {domain}')}"
    
    elif cmd.startswith("/whois "):
        domain = user_input[7:].strip()
        return f"Whois: {manager.run(f'whois {domain}')}"
    
    elif cmd.startswith("/db "):
        query = user_input[4:].strip()
        return f"DB: {manager.run(f'database {query}')}"
    
    elif cmd.startswith("/pdf "):
        filepath = user_input[5:].strip()
        return f"PDF: {manager.run(f'pdf read {filepath}')}"
    
    elif cmd == "/backup list":
        return f"Backup: {manager.run('backup list')}"
    
    elif cmd == "/backup run":
        return f"Backup: {manager.run('backup run')}"
    
    elif cmd.startswith("/translate "):
        args = user_input[11:].strip()
        return f"Translate: {manager.run(f'translate {args}')}"
    
    elif cmd.startswith("/summarize "):
        text = user_input[11:].strip()
        return f"Summarize: {manager.run(f'summarize {text}')}"
    
    elif cmd.startswith("/sentiment "):
        text = user_input[11:].strip()
        return f"Sentiment: {manager.run(f'sentiment {text}')}"
    
    else:
        return f"DharmaAI: {brain.think(user_input)}"


def main():
    print("=" * 60)
    print("DharmaAI - Full AI Assistant (20 Agents)")
    print("=" * 60)
    print("Commands:")
    print("  --- Chat ---")
    print("  /reset              - conversation reset")
    print("  /memory             - short-term memory chudu")
    print("  /save               - memory save chey")
    print("  /remember <text>    - long-term memory lo save chey")
    print("  /search <query>     - long-term memory lo search chey")
    print("  --- RAG ---")
    print("  /rag <question>     - RAG query chey")
    print("  /load <file>        - load document to RAG")
    print("  --- Agents ---")
    print("  /agents             - available agents chudu")
    print("  /agent <task>       - agent tho task run chey")
    print("  --- Web ---")
    print("  /web search <query> - web search")
    print("  /web fetch <url>    - fetch URL content")
    print("  --- Voice ---")
    print("  /speak <text>       - text to speech")
    print("  /transcribe <file>  - speech to text")
    print("  --- Image ---")
    print("  /image <prompt>     - generate image")
    print("  --- Video ---")
    print("  /video <img> <aud>  - create video")
    print("  --- System ---")
    print("  /system             - system info")
    print("  /cpu                - CPU info")
    print("  /ram                - RAM info")
    print("  /disk               - Disk info")
    print("  /process            - Process info")
    print("  --- Network ---")
    print("  /ping <host>        - ping")
    print("  /dig <domain>       - dig")
    print("  /whois <domain>     - whois")
    print("  --- Database ---")
    print("  /db <sql>           - SQLite query")
    print("  --- PDF ---")
    print("  /pdf <file>         - PDF read")
    print("  --- Backup ---")
    print("  /backup list        - list backups")
    print("  /backup run         - run backup")
    print("  --- Translate ---")
    print("  /translate <from> <to> <text> - translate")
    print("  --- Summarize ---")
    print("  /summarize <text>   - summarize")
    print("  --- Sentiment ---")
    print("  /sentiment <text>   - sentiment")
    print("  --- Exit ---")
    print("  /quit               - exit")
    print("=" * 60)
    print("💡 MULTI-COMMAND: Use ',' to separate commands")
    print("   Example: /system, /cpu, /ram, /agents, /quit")
    print("=" * 60)
    
    brain = LLMBrain()
    rag = RAGBrain()
    rag_int = RAGIntegration()
    manager = AgentManager()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Multi-command split — "," tho separate chey
            if "," in user_input:
                parts = [p.strip() for p in user_input.split(",") if p.strip()]
                
                for i, part in enumerate(parts, 1):
                    print(f"\n{'='*60}")
                    print(f">>> [{i}/{len(parts)}] {part}")
                    print('='*60)
                    
                    result = process_single_command(part, brain, rag, rag_int, manager)
                    
                    if result == "EXIT":
                        print("Memory saved. Goodbye!")
                        return
                    
                    print(result)
                
                print(f"\n{'='*60}")
                print(f"✅ All {len(parts)} commands completed!")
                print('='*60)
                continue
            
            # Single command
            result = process_single_command(user_input, brain, rag, rag_int, manager)
            
            if result == "EXIT":
                print("Memory saved. Goodbye!")
                break
            
            print(f"\n{result}")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Saving memory...")
            brain.save_memory()
            break

if __name__ == "__main__":
    main()
