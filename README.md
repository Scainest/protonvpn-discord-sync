# Proton VPN — Discord Auto-Sync

Discord updates itself into a new versioned folder (`app-1.0.xxxx`) every time it updates, which breaks the file path saved in Proton VPN's Split Tunneling list. This script automatically detects the latest Discord version and keeps the path up to date — no manual intervention needed.

## How It Works

1. Scans `%LOCALAPPDATA%\Discord\app-1.0.*` and finds the highest version
2. Opens Proton VPN's settings file (`UserSettings.*.json`)
3. Replaces the outdated Discord path in the Split Tunneling list
4. If Proton VPN is running, restarts it so changes take effect
5. Runs silently at every startup (30-second delay to let Proton VPN load first)

Supports both **Inverse mode** (only selected apps bypass VPN) and **Standard mode** (only selected apps go through VPN).

## Requirements

- Windows 10/11
- Python 3.10+
- Proton VPN (desktop app, v4+)
- Proton VPN **Plus** subscription (Split Tunneling is a Plus feature)

## Installation

### Option A — Clone & install

```bash
git clone https://github.com/Scainest/protonvpn-discord-sync
cd protonvpn-discord-sync
python sync_discord.py --install
```

### Option B — Single-file installer

Download `kurulum.py` from [Releases](../../releases) and double-click it. It will:
- Create `Documents\ProtonVPNDiscordSync\`
- Write `sync_discord.py` there
- Register the startup task automatically

## Usage

| Command | Description |
|---|---|
| `python sync_discord.py` | Run once manually |
| `python sync_discord.py --install` | Register Windows startup entry |
| `python sync_discord.py --uninstall` | Remove startup entry |

## Notes

- Runs via `pythonw.exe` at startup — no console window appears
- If Proton VPN is open when a path change is detected, it will be restarted automatically
- If no Plus subscription is detected (Split Tunneling keys missing), the script exits silently

## License

MIT
