import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF
from datetime import datetime
print("--- DİKKAT: YENİ GÜNCEL KOD BAŞLATILDI ---")
# 1. Dosya Seçme
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
dosya_yolu = filedialog.askopenfilename(title="CSV Dosyasını Seç", filetypes=[("CSV Dosyaları", "*.csv")])

if not dosya_yolu:
    print("Dosya seçilmedi!")
    exit()

# PDF ADI BURADA DEĞİŞİYOR
pdf_adi = "Satis_Raporu.pdf" 

# 2. Veri Analizi
df = pd.read_csv(dosya_yolu)
df['TARİH'] = pd.to_datetime(df['TARİH'], format='%d/%m/%y')

ciro_gun = df.groupby('GÜN')['TOPLAM SATIŞ'].sum().sort_values(ascending=False)
urun_perf = df.groupby('ÜRÜN')['TOPLAM SATIŞ'].sum().reset_index().sort_values(by='TOPLAM SATIŞ', ascending=False)
ortalama_sepet = (df['TOPLAM SATIŞ'] / df['ADET']).mean()

# 3. Grafik Kaydet
plt.style.use('ggplot')
plt.figure(figsize=(8,4))
ciro_gun.plot(kind='bar', color='#3498db')
plt.title("Günlük Ciro Analizi")
plt.tight_layout()
plt.savefig("grafik_ciro.png")
plt.close()

# 4. PDF Oluşturma
pdf = FPDF()
pdf.add_page()

# Font Ayarları
font_path = r'C:\Windows\Fonts\arial.ttf'
pdf.add_font('TurkishArial', '', font_path)
pdf.add_font('TurkishArialBold', '', r'C:\Windows\Fonts\arialbd.ttf')

# Logo ve Başlık
if os.path.exists("logo.png"):
    pdf.image("logo.png", x=10, y=8, w=30)

pdf.set_font('TurkishArialBold', size=20)
pdf.cell(0, 15, "SATIŞ ANALİZ RAPORU", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

# Tablo Oluşturma (Ürün Performansı)
pdf.set_font('TurkishArialBold', size=12)
pdf.set_fill_color(200, 220, 255)
pdf.cell(95, 10, " Ürün Adı", border=1, fill=True)
pdf.cell(95, 10, " Toplam Kazanç (TL)", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

pdf.set_font('TurkishArial', size=10)
for index, row in urun_perf.iterrows():
    pdf.cell(95, 8, f" {row['ÜRÜN']}", border=1)
    pdf.cell(95, 8, f" {row['TOPLAM SATIŞ']:,.2f}", border=1, new_x="LMARGIN", new_y="NEXT")

# Grafik Ekle
pdf.add_page()
pdf.image("grafik_ciro.png", x=10, y=20, w=190)

# PDF Çıktısı
try:
    pdf.output(pdf_adi)
    print(f"--- İŞLEM BAŞARILI ---")
    print(f"Dosya oluşturuldu: {os.path.abspath(pdf_adi)}")
except PermissionError:
    print("HATA: PDF dosyası şu an açık! Lütfen PDF'i kapatıp kodu tekrar çalıştırın.")
    # Kodun en sonuna ekle
print(f"Sistem şu an bu dosyayı oluşturdu: {pdf_adi}")
print(f"Klasör yolu: {os.getcwd()}")
print(f"YENİ PDF OLUŞTURULDU: {pdf_adi}")