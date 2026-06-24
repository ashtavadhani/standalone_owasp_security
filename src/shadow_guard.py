import os
import sys
import json
import requests
import difflib

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "qwen2.5-coder:1.5b"

def show_interactive_diff(original, proposed, filename):
    """Generates a clean, readable visual code comparison in the terminal."""
    print("\n" + "="*60)
    print(f"🔍 PROPOSED SECURITY REMEDIATION PATCH FOR: {filename}")
    print("="*60)
    
    orig_lines = original.splitlines(keepends=True)
    prop_lines = proposed.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        orig_lines, prop_lines, 
        fromfile=f"a/{filename} (CURRENT)", 
        tofile=f"b/{filename} (AI FIXED)"
    )
    
    has_diff = False
    for line in diff:
        has_diff = True
        if line.startswith('+') and not line.startswith('+++'):
            print(f"\033[92m{line.strip()}\033[0m") # Green for additions
        elif line.startswith('-') and not line.startswith('---'):
            print(f"\033[91m{line.strip()}\033[0m") # Red for deletions
        elif line.startswith('@@'):
            print(f"\033[36m{line.strip()}\033[0m") # Cyan for positions
        else:
            print(line.strip())
            
    if not has_diff:
        print("No structural text differences found.")
    print("="*60 + "\n")

def run_interactive_shadow_guard(file_path):
    print(f"🛡️  [ShadowGuard AI] Intercepting file save checkpoint: {file_path}")
    
    if not os.path.exists(file_path):
        print("❌ Error: Target script source file cannot be read.")
        return

    # Rugged file-read with fallback mechanisms
    try:
        absolute_path = os.path.abspath(file_path)
        with open(absolute_path, "r", encoding="utf-8", errors="ignore") as f:
            original_code = f.read()
    except PermissionError:
        print(f"\n❌ Windows Permission Block on: {file_path}")
        return

    # Optimized prompt for ultra-fast local LLM processing
    prompt = (
        "You are an expert automated security engine.\n"
        f"Analyze this code for OWASP flaws. Return data STRICTLY as JSON with these keys:\n"
        f"1. 'vulnerable': true/false\n"
        f"2. 'findings': [list of brief strings]\n"
        f"3. 'fixed_code': 'complete secure code string'\n\n"
        f"CODE TO AUDIT:\n{original_code}"
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.0,      # Stop overthinking, make generation fast
            "num_predict": 1024      # Cap length to prevent infinite loops
        }
    }

    try:
        print("🧠 Local LLM evaluating code security parameters (Streaming Compute)...")
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        
        if response.status_code != 200:
            print(f"❌ Core engine connection failure: {response.text}")
            return

        # Crucial Fix: Parsing happens inside the try block where it belongs!
        result = json.loads(response.json()["message"]["content"])
        
        if result.get("vulnerable") is True:
            print("\n🚨 [ALERT] CRITICAL OWASP SECURITY VULNERABILITIES DETECTED!")
            for issue in result.get("findings", []):
                print(f" ⚠️  - {issue}")
            
            fixed_code = result.get("fixed_code")
            if not fixed_code:
                print("❌ AI failed to generate a structural code patch.")
                return

            # Display interactive diff panel to developer
            show_interactive_diff(original_code, fixed_code, file_path)
            
            # Manual Intervention Prompt Hook
            user_choice = input("👉 Apply AI Security Fix and rewrite file directly? (y/N): ").strip().lower()
            
            if user_choice == 'y':
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(fixed_code)
                print(f"\n✅ [REMEDIATION METRIC] Source file '{file_path}' has been securely rewritten and patched local-side!")
            else:
                print("\n🛑 [REJECTED] Developer declined patch. Leaving vulnerable code untouched but tracking risk logs.")
                sys.exit(1)
        else:
            print("✅ [SECURE] Code passed all autonomous security checks. No vulnerabilities found.")
            
    except requests.exceptions.Timeout:
        print("\n❌ Local engine connection timed out. Ollama took over 5 minutes to generate a response.")
        print("💡 TIP: Make sure your hardware isn't thermal throttling, or switch Ollama to CPU-only mode.")
    except Exception as e:
        print(f"\n❌ Execution sequence interrupted: {e}")

if __name__ == "__main__":
    target = "vulnerable_code.py"
    run_interactive_shadow_guard(target)