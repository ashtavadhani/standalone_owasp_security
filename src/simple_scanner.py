import os
import subprocess

file_path = "vulnerable_code.py"
print(f"🔍 Reading target file: {file_path}...")

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    current_code = f.read()

# Prompt forcing the AI to output clean code only
prompt = (
    "Review this Python code for OWASP security flaws. "
    "Rewrite the code to fix them securely using best practices. "
    "Output ONLY the clean, fixed Python code. Do not write explanations.\n\n"
    f"CODE:\n{current_code}"
)

print("🧠 Asking local Ollama for the secure code fix...")
try:
    # Query Ollama via direct command-line execution
    result = subprocess.run(
        ["ollama", "run", "qwen2.5-coder:1.5b", prompt],
        capture_output=True, text=True, encoding="utf-8"
    )
    fixed_code = result.stdout.strip()
    
    # Strip away any markdown formatting if the LLM wraps the code block
    if fixed_code.startswith("```python"):
        fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
    elif fixed_code.startswith("```"):
        fixed_code = fixed_code.split("```")[1].split("```")[0].strip()

    print("\n--- PROPOSED FIX FROM AI ---")
    print(fixed_code)
    print("----------------------------\n")

    # Human-In-The-Loop Confirmation
    choice = input("👉 Apply fix? This will create a separate '_fixed' file. (y/n): ").strip().lower()

    if choice == 'y':
        # Generate the new distinct filename
        new_file_path = file_path.replace(".py", "_fixed.py")
        
        with open(new_file_path, "w", encoding="utf-8") as f:
            f.write(fixed_code)
            
        print(f"✅ Original file kept safe!")
        print(f"💾 Secure version saved separately to: {new_file_path}")
    else:
        print("🛑 Patch rejected. No files were created or changed.")

except Exception as e:
    print(f"❌ Something went wrong: {e}")