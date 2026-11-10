# SMCEP — T4–T7 ham kayıt doğrulama notu

**Tarih:** 10 Kasım 2026  
**Kaynaklar:** `SMCEP_T4_Research_Archive.zip`, `SMCEP_T5_Research_Archive.zip`, `SMCEP_T6_v1_3_Final_Archive.zip`, `SMCEP_T7_Research_Archive_v1.zip`. Bu belge özgün kayıtları değiştirmeden oluşturulmuştur.

## T4–T5: bağımsız audit veri varlığı

- T4'te üç döngü için üç `locked_audit` çıktı paketi ve üç audit test paketi bulunuyor. Her döngünün çıktı paketinde iki görev × iki koşul = dört model yanıtı; toplam **12 yanıt kaydı** var.
- T5'te üç döngü için üç `locked_audit` çıktı paketi ve üç audit test paketi bulunuyor. Yine **12 yanıt kaydı** var. T5'in VM kopyaları da mevcut; bunları bağımsız ek deneme saymamak gerekir.
- Bu sayı **başarı oranı değildir**: çıktı paketlerindeki yanıt sayısıdır. Testlerin geçme/kalma sonuçları ayrı değerlendirme dosyalarından yeniden hesaplanmalıdır.
- T4'ün iki özgün yöntem belgesi bulunamadığı için önceden dondurulmuş protokol iddiası yalnızca mevcut kanıtların desteklediği ölçüde kurulmalıdır.

## T6: SQLite'dan doğrudan sayım

- `events`: **527**; `candidates`: **186**; `evaluations`: **164**; `measurements`: **54**.
- Aday sayısı: Frozen **28**, Linear **79**, Hybrid **79**. Bu sayılar ayrı bağımsız deney tekrarları değildir.
- `PROCEDURE_SELECTION` olayları: {'linear': {'RETAIN_CURRENT': 8, 'INCONCLUSIVE_KEEP_CURRENT': 2}, 'hybrid': {'RETAIN_CURRENT': 9, 'INCONCLUSIVE_KEEP_CURRENT': 1}}.
- Hybrid arşiv güncellemeleri: **10**; şampiyon soy derinliği değerleri: **[0]**.
- Ölçüm tablosunda üç koşulda da kontrol noktaları **0, 5, 10** için `P_t = 1.0`. `C_t_improvement_rate`, `C_t_improvement_magnitude`, `C_t_improvement_per_token` alanlarının hepsi **NULL**. NULL değerini sıfır gelişim miktarıyla eşitlememeliyiz; ölçümün sayısal olarak tanımlanmadığını ifade etmeliyiz.
- 33 başlatılan adım, 32 `PILOT_STEP_FINISHED`, 1 kesinti ve bir telafi/uzlaştırma kaydı görülüyor; tamamlanma iddiası olay zinciriyle birlikte okunmalıdır.

## T7: gerçek model kalibrasyonu ve simülasyon ayrımı

- `T7_calibration_v0_1_final_audit.json`: **48/48**; tavan etkisi gerekçesiyle ana deney için reddedilmiş.
- `T7_calibration_v0_2_final_audit.json`: **36/36**; aynı gerekçeyle reddedilmiş.
- `T7_semisynthetic_final_audit_v1.json`: **100 tekrar**, **3.600 kayıt**, kontrol noktaları **0, 20, 50**. Bunlar **varsayıma bağlı stokastik simülasyon** kayıtlarıdır, gerçek modelin 50 nesil öz-gelişimi değildir.
- 50. nesilde Hybrid − Linear `C_probe` ortalama farkı: neutral **0.000**, complementary **+0.009**, costly **−0.077**. Simülasyonun varsayımları dışında nedensel genelleme yapılmamalıdır.

## Makale için ilk kanıt sınırları

1. T4–T5: prosedür önerisi, seçim ve bağımsız audit iş akışı belgelenmiş; kalıcı öz-gelişim iddiası desteklenmiyor.
2. T6: görev başarısı tavan düzeyinde; `C_t` ölçümlerinin NULL olması nedeniyle sayısal meta-kapasite kazanımı raporlanamaz.
3. T7: gerçek LLM kalibrasyonları ve simülasyon ayrı alt bölümlerde sunulmalı.
4. Sıradaki denetim: T4–T5 test paketlerinden yeniden başarı hesaplama; T6 seçim olaylarının ayrıntılı karşılaştırması; ardından LaTeX revizyonu ve GitHub yayın paketi.
