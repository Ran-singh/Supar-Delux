"""
add-songs.py  -  helper for the Bus Driver Playlist (it does NOT change any file).

How to use (open a terminal inside the bus-playlist folder):
    python add-songs.py

It will:
  1) find every .mp3 in the "songs" folder that is not in PLAYLIST yet, and print a
     ready-to-paste line for each one (exact file name and path);
  2) check every "src" already in PLAYLIST and tell you if its file is missing.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "index.html"), encoding="utf-8") as f:
    html = f.read()

# Only look inside "var PLAYLIST = [ ... ];"
block = re.search(r"var PLAYLIST = \[(.*?)\n\s*\];", html, re.S)
code = re.sub(r"/\*.*?\*/", "", block.group(1), flags=re.S) if block else ""   # ignore /* comments */
listed = re.findall(r'src:\s*"([^"]+)"', code)

print("== Songs already in PLAYLIST ==")
for src in listed:
    ok = os.path.isfile(os.path.join(HERE, src))
    print(("  OK       " if ok else "  MISSING  ") + src)
if not listed:
    print("  (none found - check that index.html still has 'var PLAYLIST = [')")

songs_dir = os.path.join(HERE, "songs")
files = sorted(f for f in os.listdir(songs_dir) if f.lower().endswith(".mp3")) if os.path.isdir(songs_dir) else []
new = [f for f in files if "songs/" + f not in listed]

print("\n== New MP3 files found in songs/ (not in PLAYLIST yet) ==")
if not new:
    print("  none")
for f in new:
    name = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").strip().title()
    print('  { title: "%s", artist: "Singer", src: "songs/%s", cover: "assets/bus.jpg", mood: "raat" },' % (name, f))

if new:
    print("\nPaste the line(s) above at the '▼ NAYA GAANA YAHAN ADD KARO ▼' spot in index.html.")
    print("Remember: last song in the list must have NO comma at the end; all others need one.")
    print("Then change title / artist / mood as you like.")
