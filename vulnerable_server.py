# BU DOSYA: GERÇEK İŞLEMİ YAPAN SAVUNMASIZ SUNUCUDUR (SERVER LAYER)
# İçinde hiçbir güvenlik kontrolü yoktur.

def unsafe_delete_files(path: str) -> str:
    """Gerçek silme işlemini yapan fonksiyon."""
    # Gerçek hayatta burada os.remove(path) olurdu.
    return f"DOSYA SİLİNDİ: {path} (Vulnerable Server tarafından yapıldı)"

def unsafe_read_data(query: str) -> str:
    """Gerçek okuma işlemini yapan fonksiyon."""
    # Gerçek hayatta burada veritabanı sorgusu olurdu.
    return f"VERİ OKUNDU: {query} (Vulnerable Server'dan geldi)"