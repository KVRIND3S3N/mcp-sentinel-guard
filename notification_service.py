import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import sys
import os
from dotenv import load_dotenv
load_dotenv()
# --- AYARLAR (BURAYI DOLDUR) ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
MY_EMAIL = os.getenv("GMAIL_USER")      
MY_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")      
TO_EMAIL = os.getenv("GMAIL_USER")      

def send_alert_email(tool_name, arguments, reason):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Konudaki emojiyi kaldirdik
    subject = f"[ACIL] MCP SENTINEL UYARISI: {tool_name}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="background-color: #d32f2f; color: white; padding: 15px;">
            <h1>SALDIRI ENGELLENDI</h1>
        </div>
        <div style="padding: 20px; border: 1px solid #ddd;">
            <p><strong>Sayin Yonetici,</strong></p>
            <p>Sistemde supheli bir islem tespit edildi.</p>
            <ul>
                <li><strong>Zaman:</strong> {timestamp}</li>
                <li><strong>Hedef:</strong> {tool_name}</li>
                <li><strong>Sebep:</strong> {reason}</li>
            </ul>
        </div>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart()
        msg['From'] = MY_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

        # BURADAKI EMOJILERI KALDIRDIK
        print("[MAIL] Gmail sunucusuna baglaniliyor...")
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        
        print("[MAIL] Uyari maili basariyla gonderildi!")
        return True

    except Exception as e:
        # Burada da emoji vardi, kaldirdik
        print(f"[MAIL HATA] Gonderilemedi: {e}")
        return False