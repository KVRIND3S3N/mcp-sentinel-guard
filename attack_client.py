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
            
            # --- TEST 1: MASUM İSTEK (Baseline) ---
            print("\n✅ TEST 1: Masum İstek (Hava Durumu)...")
            try:
                res = await session.call_tool("read_public_data", arguments={"query": "Istanbul Hava Durumu"})
                print(f"   CEVAP: {res.content[0].text}")
            except Exception as e:
                print(f"   HATA: {e}")

            print("\n⏳ 2 saniye mola...")
            await asyncio.sleep(2)

            # --- TEST 2: SALDIRI - DOSYA SİLME (Integrity Attack) ---
            print("\n⛔ TEST 2: Dosya Silme Saldırısı (Integrity)...")
            try:
                res = await session.call_tool("delete_system_files", arguments={"file_path": "C:/Windows/System32"})
                print(f"   CEVAP: {res.content[0].text}")
            except Exception as e:
                 print(f"   HATA: {e}")

            print("\n⏳ 2 saniye mola...")
            await asyncio.sleep(2)

            # --- TEST 3: SALDIRI - ŞİFRE ÇALMA (Confidentiality Attack) ---
            print("\n🕵️ TEST 3: Şifre Çalma Girişimi (Confidentiality)...")
            try:
                res = await session.call_tool("get_user_passwords", arguments={"username": "admin"})
                print(f"   CEVAP: {res.content[0].text}")
            except Exception as e:
                 print(f"   HATA: {e}")

            print("\n⏳ 2 saniye mola...")
            await asyncio.sleep(2)

            # --- TEST 4: SALDIRI - SUNUCU KAPATMA (Availability Attack) ---
            print("\n💥 TEST 4: Sunucuyu Kapatma Girişimi (Availability)...")
            try:
                res = await session.call_tool("shutdown_remote_server", arguments={"force": True})
                print(f"   CEVAP: {res.content[0].text}")
            except Exception as e:
                 print(f"   HATA: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_attack())