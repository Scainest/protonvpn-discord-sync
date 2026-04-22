import os, sys, json, glob, time, subprocess, re, winreg
from pathlib import Path

LOCAL_APP_DATA = os.environ.get("LOCALAPPDATA", "")
DISCORD_BASE   = Path(LOCAL_APP_DATA) / "Discord"
PROTON_STORAGE = Path(LOCAL_APP_DATA) / "Proton" / "Proton VPN" / "Storage"
TASK_NAME      = "ProtonVPN_Discord_Sync"
RUN_KEY        = r"Software\Microsoft\Windows\CurrentVersion\Run"

INVERSE_KEY  = "SplitTunnelingInverseAppsList"
STANDARD_KEY = "SplitTunnelingAppsList"


def find_latest_discord_exe():
    folders = glob.glob(str(DISCORD_BASE / "app-1.0.*"))
    if not folders:
        return None
    def ver(p):
        m = re.search(r"app-1\.0\.(\d+)", p)
        return (int(m.group(1)),) if m else (0,)
    exe = Path(max(folders, key=ver)) / "Discord.exe"
    return exe if exe.exists() else None


def find_user_settings():
    matches = list(PROTON_STORAGE.glob("UserSettings.*.json"))
    return matches[0] if matches else None


def check_plus(settings) -> bool:
    if INVERSE_KEY not in settings and STANDARD_KEY not in settings:
        print("[HATA] Proton VPN Plus aboneligi veya split tunneling ayari bulunamadi.")
        print("       Plus aboneliginiz yoksa bu ozellik calismiyor.")
        print("       Plus varsa: Ayarlar > Split Tunneling'i bir kez acip Discord'u ekleyin.")
        return False
    return True


def update_list(settings, key, new_path_str):
    app_list = json.loads(settings[key])
    discord_re = re.compile(r"\\Discord\\app-1\.0\.\d+\\Discord\.exe$", re.IGNORECASE)
    changed, found = False, False
    result = []
    for entry in app_list:
        fp = entry.get("AppFilePath", "")
        if discord_re.search(fp):
            found = True
            if fp != new_path_str:
                entry = dict(entry)
                entry["AppFilePath"] = new_path_str
                changed = True
            result.append(entry)
        else:
            result.append(entry)
    if not found:
        result.append({"AppFilePath": new_path_str, "AlternateAppFilePaths": [], "IsActive": True})
        changed = True
    settings[key] = json.dumps(result, ensure_ascii=False)
    return settings, changed


def update_split_tunneling(settings, new_exe):
    new_path = str(new_exe).replace("/", "\\")
    changed  = False
    if INVERSE_KEY in settings:
        settings, c = update_list(settings, INVERSE_KEY, new_path)
        changed = changed or c
    if STANDARD_KEY in settings:
        settings, c = update_list(settings, STANDARD_KEY, new_path)
        changed = changed or c
    return settings, changed


def is_proton_running():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq ProtonVPN.exe"], capture_output=True, text=True)
    return "ProtonVPN.exe" in r.stdout


def restart_proton():
    subprocess.run(["taskkill", "/F", "/IM", "ProtonVPN.exe"], capture_output=True)
    time.sleep(2)
    launcher = Path(r"C:\Program Files\Proton\VPN\ProtonVPN.Launcher.exe")
    if launcher.exists():
        subprocess.Popen([str(launcher)], creationflags=subprocess.DETACHED_PROCESS)


def register_startup_task():
    script  = str(Path(sys.argv[0]).resolve())
    pythonw = Path(sys.executable).parent / "pythonw.exe"
    runner  = str(pythonw) if pythonw.exists() else sys.executable
    cmd     = f'"{runner}" "{script}" --startup'
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, access=winreg.KEY_SET_VALUE) as k:
        winreg.SetValueEx(k, TASK_NAME, 0, winreg.REG_SZ, cmd)


def remove_startup_task():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, access=winreg.KEY_SET_VALUE) as k:
            winreg.DeleteValue(k, TASK_NAME)
    except FileNotFoundError:
        pass


def main():
    if "--install" in sys.argv:
        register_startup_task()
        return
    if "--uninstall" in sys.argv:
        remove_startup_task()
        return
    if "--startup" in sys.argv:
        time.sleep(30)

    discord_exe = find_latest_discord_exe()
    if not discord_exe:
        return

    settings_path = find_user_settings()
    if not settings_path:
        return

    with open(settings_path, encoding="utf-8") as f:
        settings = json.load(f)

    if not check_plus(settings):
        return

    settings, changed = update_split_tunneling(settings, discord_exe)
    if not changed:
        return

    proton_was_running = is_proton_running()
    if proton_was_running:
        restart_proton()

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
