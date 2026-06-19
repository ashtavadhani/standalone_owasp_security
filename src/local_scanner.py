import os
import requests

def run_simple_scan():
    print("🛡️  Running Ultra-Light Standalone Security Scan...")
    
    target_file = "src/vulnerable_code.py"
    if not os.path.exists(target_file):
        print(f"❌ Missing target file at: {target_file}")
        return

    # FIXED: Added explicit utf-8 encoding and error ignoring to prevent Windows crash
    try:
        with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
            source_code = f.read()
    except Exception as e:
        print(f"❌ Failed to read the target file: {e}")
        return

    # Short, precise prompt to prevent LLM engine memory overload
    prompt = (
        "Find the security flaws in this code. "
        "List them in short bullet points. Be very brief.\n\n"
        f"CODE:\n{source_code}"
    )
    
    payload = {
        "model": "qwen2.5-coder:1.5b",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    
    try:
        # Requesting analysis from your local Ollama engine
        response = requests.post("http://127.0.0.1:11434/api/chat", json=payload, timeout=60)
        
        if response.status_code == 200:
            print("\n📊 AI ANALYSIS RESULTS:")
            print("=" * 40)
            print(response.json()["message"]["content"])
            print("=" * 40)
        else:
            print(f"❌ Local Engine Error (Status {response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error. Is Ollama running? Details: {e}")

if __name__ == "__main__":
    run_simple_scan()