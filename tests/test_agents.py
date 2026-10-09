import sys
sys.path.insert(0, '/mnt/kaliyuga/DharmaAI')

from agents.manager import AgentManager

def test_agents():
    manager = AgentManager()
    agents = manager.list_agents()
    assert len(agents) == 20, f"Expected 20 agents, got {len(agents)}"
    print(f"✅ {len(agents)} agents loaded")
    for name, desc in agents:
        print(f"   - {name}: {desc}")

def test_file_agent():
    manager = AgentManager()
    result = manager.run("write test_unit.txt Hello Unit Test")
    assert "Written" in result, f"Write failed: {result}"
    
    result = manager.run("read test_unit.txt")
    assert "Hello Unit Test" in result, f"Read failed: {result}"
    
    result = manager.run("delete test_unit.txt")
    assert "Deleted" in result, f"Delete failed: {result}"
    print("✅ FileAgent working")

def test_shell_agent():
    manager = AgentManager()
    result = manager.run("run whoami")
    assert result and "not allowed" not in result, f"Shell failed: {result}"
    print(f"✅ ShellAgent working (whoami: {result})")

def test_code_agent():
    manager = AgentManager()
    result = manager.run("python print(2+2)")
    assert "4" in result, f"Code failed: {result}"
    print(f"✅ CodeAgent working (2+2={result})")

if __name__ == "__main__":
    print("=" * 60)
    print("DharmaAI Agent Tests")
    print("=" * 60)
    
    test_agents()
    test_file_agent()
    test_shell_agent()
    test_code_agent()
    
    print()
    print("=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
