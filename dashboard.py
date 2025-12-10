import streamlit as st
import pandas as pd
import time
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="MCP Sentinel Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Başlık
st.title("🛡️ MCP Sentinel - Canlı Güvenlik Paneli")
st.markdown("---")

# --- LOG OKUMA FONKSİYONU ---
def load_data():
    if not os.path.exists("security_log.txt"):
        return pd.DataFrame(columns=["Zaman", "Karar", "Araç", "Sebep"])

    data = []
    with open("security_log.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for line in lines:
        try:
            # Örnek Satır: [14:30:22] ENGELLENDI [BLOCK] -> Arac: delete_files | Sebep: Tehlikeli
            parts = line.strip().split(" -> ")
            left_part = parts[0] # [14:30:22] ENGELLENDI [BLOCK]
            right_part = parts[1] # Arac: delete_files | Sebep: Tehlikeli
            
            # Zaman ve Karar'ı ayır
            time_stamp = left_part.split("] ")[0].replace("[", "")
            decision = left_part.split("] ")[1]
            
            # Araç ve Sebep'i ayır
            tool_info = right_part.split(" | ")
            tool = tool_info[0].replace("Arac: ", "")
            reason = tool_info[1].replace("Sebep: ", "")
            
            data.append([time_stamp, decision, tool, reason])
        except:
            continue
            
    df = pd.DataFrame(data, columns=["Zaman", "Karar", "Araç", "Sebep"])
    return df

# --- CANLI VERİ AKIŞI ---
placeholder = st.empty()

# Sonsuz döngü ile ekranı güncelle (Simüle edilmiş Real-Time)
# Not: Streamlit'te 'st.rerun()' kullanmak yerine basit bir döngü içi container güncellemesi yapıyoruz.

while True:
    df = load_data()
    
    with placeholder.container():
        # 1. METRİKLER (KARTLAR)
        if not df.empty:
            total_req = len(df)
            blocked = len(df[df["Karar"].str.contains("ENGELLENDI")])
            allowed = len(df[df["Karar"].str.contains("IZIN VERILDI")])
            
            k1, k2, k3 = st.columns(3)
            k1.metric("Toplam İstek", total_req, "📦")
            k2.metric("Engellenen Saldırı", blocked, "⛔", delta_color="inverse")
            k3.metric("İzin Verilen", allowed, "✅")
            
            # 2. GRAFİKLER VE TABLO
            c1, c2 = st.columns([2, 1])
            
            with c1:
                st.subheader("📊 Son Güvenlik Olayları")
                # Tabloyu tersten göster (En yeni en üstte)
                st.dataframe(df.iloc[::-1], use_container_width=True, height=400)
                
            with c2:
                st.subheader("🎯 Saldırı Hedefleri")
                if blocked > 0:
                    blocked_df = df[df["Karar"].str.contains("ENGELLENDI")]
                    st.bar_chart(blocked_df["Araç"].value_counts())
                else:
                    st.info("Henüz saldırı tespit edilmedi. Sistem güvenli.")
                    
        else:
            st.warning("Henüz log kaydı yok. Lütfen saldırı testini başlatın.")
            
    # 2 saniyede bir güncelle
    time.sleep(2)