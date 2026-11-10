# SMCEP T4–T5 VM audit kayıtlarının doğrulanması

**Tarih:** 10 Kasım 2026  
**Kaynaklar:** `SMCEP_T4_Research_Archive.zip`, `SMCEP_T5_Research_Archive.zip`  
**Yöntem:** Arşivler salt okunur açıldı. Her döngünün `audit_test_package` dosyasındaki 20 test yuvası, VM `audit_evaluation` dosyasındaki 20 durum kaydı ile görev/koşul/test indeksi düzeyinde karşılaştırılmak üzere sayıldı. Buradaki oranlar mevcut VM kayıtlarının yeniden sayımıdır; deneyler yeniden çalıştırılmadı.

| Aşama | Döngü | Frozen PASS / 10 | Evolving PASS / 10 | Diğer durumlar | VM değerlendirme kaynağı |
|---|---:|---:|---:|---|---|
| T4 | 1 | 2 | 10 | Frozen 3 FAIL, 5 SYNTAX_ERROR | `vm_evaluations/t4_cycle_1_audit_evaluation_v1.json` |
| T4 | 2 | 10 | 6 | Evolving 3 FAIL, 1 ERROR | `vm_evaluations/t4_cycle_2_audit_evaluation_v1.json` |
| T4 | 3 | 10 | 7 | Evolving 3 ERROR | `vm_evaluations/t4_cycle_3_audit_evaluation_v1.json` |
| T5 | 1 | 7 | 7 | Frozen 3 FAIL, Evolving 3 FAIL | `VM/t5_cycle_1_audit_evaluation_v1.json` |
| T5 | 2 | 10 | 5 | Evolving 5 API_DELIVERY_FAILED | `VM/t5_cycle_2_audit_evaluation_v1.json` |
| T5 | 3 | 10 | 10 | Yok | `VM/t5_cycle_3_audit_evaluation_v1.json` |

## Toplamlar

- T4 Frozen 22/30 (%73,3); Evolving 23/30 (%76,7); birleşik 45/60 (%75,0).
- T5 Frozen 27/30 (%90,0); Evolving 22/30 (%73,3); birleşik 49/60 (%81,7).
- T4–T5 birlikte Frozen 49/60 (%81,7), Evolving 45/60 (%75,0), toplam 94/120 (%78,3).
- **Operasyonel PASS oranlarıdır**; farklı görevlerin ve döngülerin bağımsız örneklem sayılması veya nedensel kapasite artışı yorumu uygun değildir.

## Eşleştirme ve metodolojik notlar

- T4 paketleri: `drive_t4/t4_cycle_{1,2,3}_audit_test_package_v1.json`; VM sonuçları: `vm_evaluations/t4_cycle_{1,2,3}_audit_evaluation_v1.json`.
- T5 paketleri: `COLAB_DRIVE/t5_cycle_{1,2,3}_audit_test_package_v1.json` ve bunların `VM/` altındaki aynı SHA-256'ya sahip kopyaları; sonuçlar `VM/t5_cycle_{1,2,3}_audit_evaluation_v1.json`; kapanış kayıtları `VM/t5_cycle_{1,2,3}_audit_closure_v1.json`.
- Paketlerin `execution_status: NOT_EXECUTED` alanı **paket üretim anındaki durumu** gösterir; VM değerlendirme dosyalarının varlığını geçersiz kılmaz.
- VM değerlendirme dosyalarında `phase: T3`, `expected_tests: 60`, `completed_tests: 20` gibi eski runner etiketleri bulunur. Bu raporda döngü ve aşama ataması dosya yolları, T5 kapanış dosyalarındaki `legacy_runner_phase_label: T3` açıklaması ve test paketi eşleştirmesi üzerinden yapılmıştır. `expected_tests: 60` alanı döngü başına 60 yürütülmüş test olarak yorumlanmadı.
- T5 döngü 2'de 5 `API_DELIVERY_FAILED` kod değerlendirmesi değildir. `VM/t5_cycle_2_audit_closure_v1.json` bu olayı ve sonradan belgelenen tek yeniden denemeyi kaydeder. Kodun gerçekten teslim edilip değerlendirildiği Evolving testleri **5/5 PASS**; tüm planlanan test yuvalarına göre operasyonel sonuç **5/10 PASS**.
- T5 kapanış dosyaları, paket ve değerlendirme SHA-256 bağlantılarıyla ek yürütme kanıtı sunar. T4 için ayrı kapanış dosyaları bu arşivde yoktur; VM değerlendirme kayıtları mevcuttur.
- Sonuçlar arşivlenmiş yürütme kayıtlarından hesaplandı; VM üzerinde bağımsız yeniden çalıştırma yapılmadı. Bu nedenle `execution evidence` ile `independent reproduction` ayrı tutulmalıdır.

## Makaleye aktarım

T4–T5 gerçek LLM pilotları altı audit döngüsünde toplam 120 test yuvası için VM değerlendirme kaydı içerir. Operasyonel PASS oranları T4'te Frozen %73,3 ve Evolving %76,7; T5'te Frozen %90,0 ve Evolving %73,3'tür. T5'in ikinci döngüsündeki Evolving 5 test yuvası API teslimat hatasından etkilenmiştir; teslim edilmiş kodlarda bu döngünün sonucu 5/5'tir. Bu karşılaştırmalar kalıcı gelişim kapasitesinin ortaya çıktığını göstermez; operasyonel sorunlar ve seçim prosedürleri ayrıca raporlanmalıdır.
