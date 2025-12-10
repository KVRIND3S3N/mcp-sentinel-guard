from fpdf import FPDF
import datetime
import os

# PDF Rapor Sınıfı
class SecurityReport(FPDF):
    def header(self):
        # Logo veya Başlık
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'MCP SENTINEL - GUVENLIK IHLA RAPORU', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        # Alt bilgi
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

def create_pdf_report(tool_name, arguments, reason):
    """
    Saldırı detaylarını içeren bir PDF raporu oluşturur.
    """
    pdf = SecurityReport()
    pdf.add_page()
    
    # Zaman Damgası
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"RAPOR_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # --- İÇERİK ---
    pdf.set_font("Arial", size=12)
    
    # 1. Bölüm: Olay Özeti
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"OLAY TARIHI: {timestamp}", ln=True)
    pdf.ln(5)
    
    # 2. Bölüm: Teknik Detaylar
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "1. SALDIRI DETAYLARI", ln=True)
    pdf.set_font("Arial", size=11)
    
    pdf.multi_cell(0, 10, f"HEDEF ARAC (TOOL): {tool_name}")
    pdf.multi_cell(0, 10, f"KULLANILAN PARAMETRELER: {str(arguments)}")
    pdf.ln(5)
    
    # 3. Bölüm: Yapay Zeka Analizi
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(220, 50, 50) # Kırmızı Renk
    pdf.cell(0, 10, "2. GEMINI AI ANALIZI", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(0, 0, 0) # Siyah Renk
    
    pdf.multi_cell(0, 10, f"KARAR: ENGELLENDI (BLOCKED)")
    pdf.multi_cell(0, 10, f"AI GEREKCESI: {reason}")
    pdf.ln(10)
    
    # 4. Bölüm: Sonuç
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 10, "Bu rapor MCP Sentinel Gateway tarafindan otomatik olarak olusturulmustur. Lutfen sistem yoneticisi ile iletisime geciniz.")
    
    # PDF'i Kaydet
    pdf.output(filename)
    return filename