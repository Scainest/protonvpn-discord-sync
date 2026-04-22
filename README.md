# Proton VPN — Discord Auto-Sync

## Türkçe

Discord her güncellendiğinde yeni bir sürüm klasörü (`app-1.0.xxxx`) oluşturur ve Proton VPN'in Split Tunneling listesindeki eski yol geçersiz hale gelir. Bu script, her açılışta en güncel Discord sürümünü otomatik olarak algılayıp Proton VPN ayarlarını günceller — elle müdahaleye gerek kalmaz.

### Nasıl Çalışır?

1. `%LOCALAPPDATA%\Discord\app-1.0.*` klasörlerini tarayarak en yüksek sürümü bulur
2. Proton VPN ayar dosyasını (`UserSettings.*.json`) açar
3. Split Tunneling listesindeki eski Discord yolunu günceller
4. Proton VPN açıksa kapatıp yeniden başlatır (değişiklik anında geçerli olsun diye)
5. Bilgisayar açılışında sessizce çalışır (30 saniye bekler, VPN'in yüklenmesi için)

Hem **Katma Kipi** (sadece seçili uygulamalar VPN'i bypass eder) hem de **Standart Mod** (sadece seçili uygulamalar VPN üzerinden geçer) desteklenir.

### Gereksinimler

- Windows 10/11
- Python 3.10+
- Proton VPN masaüstü uygulaması (v4+)
- Proton VPN **Plus** aboneliği (Split Tunneling sadece Plus'ta var)

### Kurulum

**Seçenek A — Klonla ve kur:**

```bash
git clone https://github.com/Scainest/protonvpn-discord-sync
cd protonvpn-discord-sync
python sync_discord.py --install
```

**Seçenek B — Tek dosya kurulum:**

`kurulum.py` dosyasını [Releases](../../releases) sayfasından indirip çift tıkla. Otomatik olarak:
- `Documents\ProtonVPNDiscordSync\` klasörünü oluşturur
- `sync_discord.py` dosyasını oraya yazar
- Başlangıç kaydını ekler

### Komutlar

| Komut | Açıklama |
|---|---|
| `python sync_discord.py` | Bir kez manuel çalıştır |
| `python sync_discord.py --install` | Windows başlangıç kaydını ekle |
| `python sync_discord.py --uninstall` | Başlangıç kaydını kaldır |

### Notlar

- `pythonw.exe` ile çalışır — konsol penceresi açılmaz
- Yol değişikliği tespit edildiğinde Proton VPN açıksa otomatik yeniden başlatılır
- Plus aboneliği yoksa (Split Tunneling anahtarları dosyada bulunamazsa) script sessizce çıkar

---

## English

Discord creates a new versioned folder (`app-1.0.xxxx`) on every update, which breaks the file path saved in Proton VPN's Split Tunneling list. This script automatically detects the latest Discord version and keeps the path up to date — no manual intervention needed.

### How It Works

1. Scans `%LOCALAPPDATA%\Discord\app-1.0.*` and finds the highest version
2. Opens Proton VPN's settings file (`UserSettings.*.json`)
3. Replaces the outdated Discord path in the Split Tunneling list
4. If Proton VPN is running, restarts it so changes take effect
5. Runs silently at every startup (30-second delay to let Proton VPN load first)

Supports both **Inverse mode** (only selected apps bypass VPN) and **Standard mode** (only selected apps go through VPN).

### Requirements

- Windows 10/11
- Python 3.10+
- Proton VPN (desktop app, v4+)
- Proton VPN **Plus** subscription (Split Tunneling is a Plus feature)

### Installation

**Option A — Clone & install:**

```bash
git clone https://github.com/Scainest/protonvpn-discord-sync
cd protonvpn-discord-sync
python sync_discord.py --install
```

**Option B — Single-file installer:**

Download `kurulum.py` from [Releases](../../releases) and double-click it. It will:
- Create `Documents\ProtonVPNDiscordSync\`
- Write `sync_discord.py` there
- Register the startup task automatically

### Usage

| Command | Description |
|---|---|
| `python sync_discord.py` | Run once manually |
| `python sync_discord.py --install` | Register Windows startup entry |
| `python sync_discord.py --uninstall` | Remove startup entry |

### Notes

- Runs via `pythonw.exe` at startup — no console window appears
- If Proton VPN is open when a path change is detected, it will be restarted automatically
- If no Plus subscription is detected (Split Tunneling keys missing), the script exits silently

## License

MIT
