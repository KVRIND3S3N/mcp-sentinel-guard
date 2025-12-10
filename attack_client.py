import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# HEDEF: Biz direkt sunucuya değil, GATEWAY'e bağlanıyoruz!
TARGET_SERVER = "sentinel_gateway.py"

async def run_attack():
    server_params = StdioServerParameters(command=sys.executable, args=[TARGET_SERVER], env=None)
    
    print(f"🔌 [HOST] {TARGET_SERVER} (Gateway) adresine bağlanılıyor...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # --- TEST 1: MASUM İSTEK ---
            print("\n🔹 TEST 1: Masum İstek Gönderiliyor...")
            try:
                res1 = await session.call_tool("read_public_data", arguments={"query": "Hava Durumu"})
                print(f"   CEVAP: {res1.content[0].text}")
            except Exception as e:
                print(f"   HATA: {e}")

            # --- MOLA (GOOGLE KIZMASIN DİYE) ---
            print("\n⏳ 5 Saniye bekleniyor (Rate Limit onlemi)...")
            await asyncio.sleep(5) 

            # --- TEST 2: SALDIRI ---
            print("\n🔹 TEST 2: Saldırı Yapılıyor (Silme)...")
            try:
                res2 = await session.call_tool("delete_system_files", arguments={"file_path": "C:/Windows"})
                print(f"   CEVAP: {res2.content[0].text}")
            except Exception as e:
                 print(f"   HATA: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_attack())