import os
import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from agents.collaborative_agents import get_coder_agent, get_validator_agent

async def process_spec(spec_path, generated_dir):
    spec_name = os.path.basename(spec_path)
    print(f"\n--- Memproses {spec_name} dalam Tim Kolaborasi ---")
    
    with open(spec_path, 'r') as f:
        spec_content = f.read()

    # Inisialisasi Agen
    coder = get_coder_agent()
    validator = get_validator_agent()

    # Berhenti jika Validator bilang "VALID" atau sudah 6 kali diskusi
    termination = TextMentionTermination("VALID") | MaxMessageTermination(6)
    
    team = RoundRobinGroupChat([coder, validator], termination_condition=termination)

    prompt = f"Tugas: Implementasikan spesifikasi ini ke dalam kode Python.\n\nSpesifikasi:\n{spec_content}"
    
    # Jalankan kolaborasi
    result = await Console(team.run_stream(task=prompt))
    
    # Ambil pesan terakhir dari Coder (biasanya sebelum atau sesudah VALID)
    # Kita cari pesan yang mengandung code block
    final_code = ""
    for msg in reversed(result.messages):
        if "```python" in msg.content:
            final_code = msg.content.split("```python")[1].split("```")[0].strip()
            break
        elif "```" in msg.content:
            final_code = msg.content.split("```")[1].split("```")[0].strip()
            break

    if "VALID" in result.messages[-1].content.upper() and final_code:
        output_filename = spec_name.replace(".spec.yaml", ".py").replace("-", "_")
        output_path = os.path.join(generated_dir, output_filename)
        with open(output_path, 'w') as f:
            f.write(final_code)
        print(f"✅ Berhasil! Kode divalidasi dan disimpan di {output_path}")
    else:
        print(f"❌ Gagal memvalidasi {spec_name} setelah diskusi.")

async def main():
    specs_dir = "chefgenie-autogen/specs"
    generated_dir = "chefgenie-autogen/generated"
    os.makedirs(generated_dir, exist_ok=True)

    spec_files = [os.path.join(specs_dir, f) for f in os.listdir(specs_dir) if f.endswith(".spec.yaml")]
    
    for spec_file in spec_files:
        await process_spec(spec_file, generated_dir)

if __name__ == "__main__":
    asyncio.run(main())
