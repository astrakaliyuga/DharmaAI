from brain.llm import LLMBrain
from brain.rag import RAGBrain
from brain.rag_integration import RAGIntegration
from agents.manager import AgentManager

def main():
    print("=" * 60)
    print("DharmaAI - Full AI Assistant (12 Agents)")
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
    print("  --- Exit ---")
    print("  /quit               - exit")
    print("=" * 60)
    print("Examples:")
    print("  /agent write hello.txt Hello DharmaAI")
    print("  /web search Python programming")
    print("  /speak Hello from DharmaAI")
    print("  /image a beautiful sunset")
    print("  /system")
    print("  /ping google.com")
    print("  /db CREATE TABLE users (id INTEGER, name TEXT)")
    print("  /backup list")
    print("=" * 60)
    
    brain = LLMBrain()
    rag = RAGBrain()
    rag_int = RAGIntegration()
    manager = AgentManager()
    telugu_mode = False
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            cmd = user_input.lower()
            
            # ==================== EXIT ====================
            if cmd in ["/quit", "/exit", "/bye", "quit", "exit", "bye", "q"]:
                brain.save_memory()
                print("Memory saved. Goodbye!")
                break
            
            # ==================== CHAT ====================
            elif cmd == "/reset":
                brain.reset()
                print("Conversation reset.")
                continue
            
            elif cmd == "/memory":
                print("\n--- Recent Memory ---")
                for m in brain.recall(10):
                    print(f"  [{m['metadata']['type']}] {m['content'][:80]}")
                continue
            
            elif cmd == "/save":
                path = brain.save_memory()
                print(f"Saved to {path}")
                continue
            
            elif cmd.startswith("/remember "):
                content = user_input[10:].strip()
                brain.remember(content)
                print(f"Remembered: {content}")
                continue
            
            elif cmd.startswith("/search "):
                query = user_input[8:].strip()
                results = brain.search_memory(query)
                print(f"\n--- Search Results for: {query} ---")
                if results['documents'] and results['documents'][0]:
                    for doc in results['documents'][0]:
                        print(f"  - {doc}")
                else:
                    print("  No results found.")
                continue
            
            # ==================== RAG ====================
            elif cmd.startswith("/rag "):
                question = user_input[5:].strip()
                answer = rag.query(question)
                print(f"\nRAG: {answer}")
                continue
            
            elif cmd.startswith("/load "):
                filepath = user_input[6:].strip()
                result = rag_int.load_text_file(filepath)
                print(f"\nRAG: {result}")
                continue
            
            # ==================== AGENTS ====================
            elif cmd == "/agents":
                print("\n--- Available Agents ---")
                for name, desc in manager.list_agents():
                    print(f"  {name}: {desc}")
                continue
            
            elif cmd.startswith("/agent "):
                task = user_input[7:].strip()
                print(f"\n[Routing task: {task}]")
                result = manager.run(task)
                print(f"\nAgent: {result}")
                continue
            
            # ==================== WEB ====================
            elif cmd.startswith("/web "):
                task = user_input[5:].strip()
                print(f"\n[Web: {task}]")
                result = manager.run(task)
                print(f"\nWeb: {result}")
                continue
            
            # ==================== VOICE ====================
            elif cmd.startswith("/speak "):
                text = user_input[7:].strip()
                print(f"\n[Speaking: {text}]")
                result = manager.run(f"speak {text}")
                print(f"\nVoice: {result}")
                continue
            
            elif cmd.startswith("/transcribe "):
                audio = user_input[12:].strip()
                print(f"\n[Transcribing: {audio}]")
                result = manager.run(f"transcribe {audio}")
                print(f"\nTranscription: {result}")
                continue
            
            # ==================== IMAGE ====================
            elif cmd.startswith("/image "):
                prompt = user_input[7:].strip()
                print(f"\n[Generating image: {prompt}]")
                print("(CPU lo 4-5 min padutundi...)")
                result = manager.run(f"generate {prompt}")
                print(f"\nImage: {result}")
                continue
            
            # ==================== VIDEO ====================
            elif cmd.startswith("/video "):
                args = user_input[7:].strip()
                print(f"\n[Creating video: {args}]")
                result = manager.run(f"create {args}")
                print(f"\nVideo: {result}")
                continue
            
            # ==================== SYSTEM ====================
            elif cmd == "/system":
                result = manager.run("system info")
                print(f"\nSystem: {result}")
                continue
            
            elif cmd == "/cpu":
                result = manager.run("cpu")
                print(f"\nCPU: {result}")
                continue
            
            elif cmd == "/ram":
                result = manager.run("ram")
                print(f"\nRAM: {result}")
                continue
            
            elif cmd == "/disk":
                result = manager.run("disk")
                print(f"\nDisk: {result}")
                continue
            
            elif cmd == "/process":
                result = manager.run("process")
                print(f"\nProcess: {result}")
                continue
            
            # ==================== NETWORK ====================
            elif cmd.startswith("/ping "):
                host = user_input[6:].strip()
                result = manager.run(f"ping -c 3 {host}")
                print(f"\nPing: {result}")
                continue
            
            elif cmd.startswith("/dig "):
                domain = user_input[5:].strip()
                result = manager.run(f"dig {domain}")
                print(f"\nDig: {result}")
                continue
            
            elif cmd.startswith("/whois "):
                domain = user_input[7:].strip()
                result = manager.run(f"whois {domain}")
                print(f"\nWhois: {result}")
                continue
            
            # ==================== DATABASE ====================
            elif cmd.startswith("/db "):
                query = user_input[4:].strip()
                result = manager.run(f"database {query}")
                print(f"\nDB: {result}")
                continue
            
            # ==================== PDF ====================
            elif cmd.startswith("/pdf "):
                filepath = user_input[5:].strip()
                result = manager.run(f"pdf read {filepath}")
                print(f"\nPDF: {result}")
                continue
            
            # ==================== BACKUP ====================
            elif cmd == "/backup list":
                result = manager.run("backup list")
                print(f"\nBackup: {result}")
                continue
            
            elif cmd == "/backup run":
                result = manager.run("backup run")
                print(f"\nBackup: {result}")
                continue
            
            # ==================== NORMAL CHAT ====================
            else:
                reply = brain.think(user_input, telugu_mode=telugu_mode)
                print(f"\nDharmaAI: {reply}")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Saving memory...")
            brain.save_memory()
            break

if __name__ == "__main__":
    main()
