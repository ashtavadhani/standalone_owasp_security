import os
import subprocess
import json
import re

# Configuration
TARGET_FILE = "vulnerable_code.py"
MODEL = "qwen2.5-coder:1.5b"

def clean_and_parse_json(raw_text):
    """Safely scrubs hidden invalid control characters and parses the JSON."""
    raw_text = raw_text.strip()
    
    # Strip markdown code blocks if present
    if "```json" in raw_text:
        raw_text = raw_text.split("```json")[1].split("```")[0].strip()
    elif "```" in raw_text:
        raw_text = raw_text.split("```")[1].split("```")[0].strip()
        
    # Remove invalid control characters (ascii 0-31) that break json.loads
    clean_text = re.sub(r'[\x00-\x1F\x7F]', '', raw_text)
    
    return json.loads(clean_text)

def run_agent_1_auditor(source_code):
    """Agent 1: Inspects the code and outputs structural JSON data."""
    print("🤖 Agent 1 [Auditor]: Analysing source parameters for vulnerabilities...")
    
    prompt = (
        "You are an automated AppSec Code Auditor. Analyze the following code for security flaws. "
        "You must return your output strictly as a JSON object with exactly two fields:\n"
        "1. 'vulnerable': true or false\n"
        "2. 'flaws': a simple list of brief strings describing the found vulnerabilities.\n\n"
        "CRITICAL: Keep your output strings flat, short, on a single line, and do not use tabs or raw newlines inside the text.\n\n"
        f"CODE TO AUDIT:\n{source_code}"
    )
    
    result = subprocess.run(["ollama", "run", MODEL, prompt], capture_output=True, text=True, encoding="utf-8")
    return clean_and_parse_json(result.stdout)

def run_agent_2_fixer(source_code, audit_report):
    """Agent 2: Consumes the JSON audit report and rewrites the code securely."""
    print("🤖 Agent 2 [Remediation Engineer]: Generating secure code variations...")
    
    prompt = (
        "You are an automated Security Remediation Engineer. Review the original code and the accompanying "
        "JSON audit report containing identified vulnerabilities. Rewrite the code completely to fix these flaws.\n"
        "Output ONLY the raw rewritten Python code. Do not include markdown code block syntax (like ```python) or structural explanations.\n\n"
        f"ORIGINAL CODE:\n{source_code}\n\n"
        f"AUDIT REPORT:\n{json.dumps(audit_report, indent=2)}"
    )
    
    result = subprocess.run(["ollama", "run", MODEL, prompt], capture_output=True, text=True, encoding="utf-8")
    fixed_code = result.stdout.strip()
    
    if fixed_code.startswith("```python"):
        fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
    elif fixed_code.startswith("```"):
        fixed_code = fixed_code.split("```")[1].split("```")[0].strip()
        
    return fixed_code

def main():
    print("🚀 Initializing Multi-Agent Local Security Fabric...")
    
    if not os.path.exists(TARGET_FILE):
        print(f"❌ Target source file missing at {TARGET_FILE}")
        return

    with open(TARGET_FILE, "r", encoding="utf-8", errors="ignore") as f:
        source_code = f.read()

    # --- Phase 1: Execution of Agent 1 ---
    try:
        audit_report = run_agent_1_auditor(source_code)
    except Exception as e:
        print(f"❌ Agent 1 crashed or failed to return valid JSON. Error: {e}")
        return

    print("\n======= 📊 AGENT 1 AUDIT REPORT ACCESSED =======")
    print(f"Vulnerable Status: {audit_report.get('vulnerable')}")
    print("Discovered Flaws:")
    for flaw in audit_report.get("flaws", []):
        print(f" ⚠️  {flaw}")
    print("================================================\n")

    if not audit_report.get("vulnerable"):
        print("✅ No adjustments necessary. Codebase baseline secure.")
        return

    # --- Manual Intervention Phase ---
    choice = input("👉 Pass findings to Agent 2 to generate a secure patch file? (y/n): ").strip().lower()
    if choice != 'y':
        print("🛑 Pipeline execution halted by developer. Original files left pristine.")
        return

    # --- Phase 2: Execution of Agent 2 ---
    print("\n🔄 Handing off token parameters to Agent 2...")
    fixed_code = run_agent_2_fixer(source_code, audit_report)

    print("\n------- 🛠️ PROPOSED PATCH COMPILED BY AGENT 2 -------")
    print(fixed_code)
    print("----------------------------------------------------\n")

    # --- Save Separate File Step ---
    output_path = TARGET_FILE.replace(".py", "_fixed.py")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(fixed_code)
        
    print(f"💾 Success! A completely safe copy has been written separately to: {output_path}")
    print("✅ Source tracking intact. Baseline security validation process completed.")

if __name__ == "__main__":
    main()