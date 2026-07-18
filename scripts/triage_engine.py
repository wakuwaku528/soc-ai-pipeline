import os
import glob
import json
from anthropic import Anthropic
from dotenv import load_dotenv

# 1. Load security environment variables
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("[!] Error: ANTHROPIC_API_KEY not found. Check your .env file.")
    exit(1)

client = Anthropic(api_key=api_key)

# 2. Look for raw telemetry files dropped from the Azure VM
incoming_files = glob.glob("incoming/*.txt")
if not incoming_files:
    print("[*] Pipeline Idle: No raw log files found in the 'incoming/' directory.")
    exit(0)

target_file = incoming_files[0]
print(f"[*] Pipeline Active: Ingesting {target_file}...")

with open(target_file, "r", encoding="utf-8") as f:
    raw_log_data = f.read()

# 3. Executing the engineered Prompt Pipeline
system_prompt = (
    "You are an expert Tier 1 SOC Analyst performing automated triage on raw infrastructure logs. "
    "Your sole task is to analyze the provided log for security anomalies and output your analysis "
    "strictly as a structured JSON object. Do not include any conversational introductions, markdown formatting, "
    "or explanations outside the JSON block. Your output must perfectly match this schema:\n\n"
    "{\n"
    "  'event_detected': true/false,\n"
    "  'severity': 'LOW'/'MEDIUM'/'HIGH'/'CRITICAL',\n"
    "  'event_id': 'string_or_null',\n"
    "  'target_user': 'string_or_null',\n"
    "  'source_ip': 'string_or_null',\n"
    "  'summary': 'A concise one-sentence description of the activity.'\n"
    "}"
)

user_content = f"Please triage the following raw telemetry dump:\n\n<raw_telemetry>\n{raw_log_data}\n</raw_telemetry>"

try:
    # 4. Fire payload to the Claude API
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0.0, # 0.0 ensures deterministic, rigid analysis instead of creative text
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}]
    )
    
    # 5. Output the result
    print("\n=== AI INCIDENT TRIAGE REPORT ===")
    print(response.content[0].text)
    print("=================================\n")
    
    # Archive the file so it isn't re-processed next run
    filename = os.path.basename(target_file)
    os.rename(target_file, f"archive/{filename}")
    print(f"[*] Clean up: Ingested log safely moved to archive/{filename}")

except Exception as e:
    print(f"[!] Pipeline Error interacting with Claude API: {e}")