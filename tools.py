import os
import shutil
import subprocess

HOME = os.path.expanduser("~")

# 🔥 COMMON FOLDERS
KNOWN_PATHS = {
    "desktop": os.path.join(HOME, "Desktop"),
    "downloads": os.path.join(HOME, "Downloads"),
    "documents": os.path.join(HOME, "Documents"),
}

# 🔥 APP PATHS (YOUR SYSTEM)
APP_PATHS = {
    "valorant": r"C:\Riot Games\Riot Client\RiotClientServices.exe --launch-product=valorant --launch-patchline=live",
    "brave": r"C:\Users\heman\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "spotify": r"C:\Users\heman\AppData\Roaming\Spotify\Spotify.exe",
    "whatsapp": "start whatsapp:"
}

# ---------------- PATH RESOLUTION ---------------- #

def resolve_path(p):
    if not p:
        return p

    p = p.lower().strip().replace("\\", "/")

    # 🔥 HANDLE DRIVE (c drive, d drive, etc.)
    if "drive" in p:
        parts = p.split("drive")
        drive_letter = parts[0].strip()[-1]
        rest = parts[1].strip()

        base = f"{drive_letter.upper()}:/"

        if rest:
            return os.path.join(base, rest.replace("/", os.sep))
        return base

    # 🔥 HANDLE COMMON FOLDERS
    for key, value in KNOWN_PATHS.items():
        if key in p:
            return p.replace(key, value)

    # 🔥 FULL PATH ALREADY
    if ":" in p:
        return p

    # 🔥 DEFAULT → DESKTOP
    return os.path.join(KNOWN_PATHS["desktop"], p)


# ---------------- SEARCH SYSTEM ---------------- #

def find_item(name):
    name = name.lower()

    # 🔥 PRIORITY: Desktop first
    desktop = os.path.join(HOME, "Desktop")

    for root, dirs, files in os.walk(desktop):
        for f in files:
            if name in f.lower():
                return os.path.join(root, f)
        for d in dirs:
            if name in d.lower():
                return os.path.join(root, d)

    # 🔥 THEN full system
    for root, dirs, files in os.walk(HOME):
        for f in files:
            if name in f.lower():
                return os.path.join(root, f)
        for d in dirs:
            if name in d.lower():
                return os.path.join(root, d)

    return None


# ---------------- ACTIONS ---------------- #

def create_folder(path):
    path = resolve_path(path)
    os.makedirs(path, exist_ok=True)
    return f"✅ Folder created: {path}"


def create_file(path):
    path = resolve_path(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("")
    return f"✅ File created: {path}"


def move(src, dest):
    src = resolve_path(src)
    dest = resolve_path(dest)
    shutil.move(src, dest)
    return f"✅ Moved: {src} → {dest}"


def delete(path):
    path = resolve_path(path)

    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)

    return f"🗑️ Deleted: {path}"


def list_files(path):
    path = resolve_path(path)

    if not os.path.exists(path):
        return "❌ Path not found"

    return "\n".join(os.listdir(path))


# ---------------- OPEN SYSTEM ---------------- #

def open_item(name):
    name = name.lower().strip()

    # 🔥 1. OPEN APPS DIRECTLY
    if name in APP_PATHS:
        try:
            subprocess.Popen(APP_PATHS[name], shell=True)
            return f"🚀 Opened app: {name}"
        except Exception as e:
            return f"❌ Error opening {name}: {e}"

    # 🔥 2. OPEN DIRECT PATH
    path = resolve_path(name)

    if os.path.exists(path):
        os.startfile(path)
        return f"📂 Opened: {path}"

    # 🔥 3. SEARCH WHOLE SYSTEM
    found = find_item(name)

    if found:
        os.startfile(found)
        return f"🔍 Opened: {found}"

    return "❌ Not found"