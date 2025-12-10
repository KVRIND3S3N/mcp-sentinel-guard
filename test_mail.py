import smtplib
from email.mime.text import MIMEText
import sys

# --- AYARLAR (Lütfen Doldur) ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
MY_EMAIL = "GMAIL_USER"
MY_PASSWORD = "GMAIL_APP_PASSWORD"  # <--- 16 haneli kod buraya
TO_EMAIL = "GMAIL_USER"

def mail_testi_yap():
    print(f"🔌 1. Sunucuya bağlanılıyor ({SMTP_SERVER}:{SMTP_PORT})...")
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls() # Güvenli bağlantıyı başlat
        server.ehlo()
        print("✅ Sunucu bağlantısı OK.")

        print("🔑 2. Giriş yapılıyor...")
        server.login(MY_EMAIL, MY_PASSWORD)
        print("✅ Giriş Başarılı!")

        print("📨 3. Mail gönderiliyor...")
        msg = MIMEText("Bu, Windows üzerinden gönderilen test mailidir.")
        msg['Subject'] = "Windows Mail Testi"
        msg['From'] = MY_EMAIL
        msg['To'] = TO_EMAIL

        server.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        
        print("-" * 30)
        print("🚀 SONUÇ: BAŞARILI! Mail gönderildi.")
        print("Lütfen SPAM klasörünü de kontrol et.")
        print("-" * 30)

    except smtplib.SMTPAuthenticationError:
        print("❌ HATA: Şifre Yanlış!")
        print("Lütfen normal Gmail şifreni değil, 16 haneli 'Uygulama Şifresi'ni kullandığından emin ol.")
    except Exception as e:
        print(f"❌ BEKLENMEYEN HATA: {e}")

if __name__ == "__main__":
    mail_testi_yap()