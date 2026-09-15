from pathlib import Path
import re

HTML = Path('app/src/main/assets/index.html')
s = HTML.read_text()

# The playback patch is already inside the main JavaScript block. Extra script
# opening tags become literal JavaScript and break the WebView parser.
s = re.sub(r'(?:\s*<script id="asia-media-runtime">)+', '\n', s)

# Keep renderHistory and the remaining app functions inside the main JavaScript block.
s = s.replace('</script>\nfunction renderHistory()', 'function renderHistory()', 1)

# Remove any duplicate closing/opening artifacts from older patch runs.
s = s.replace('<script id="asia-media-runtime">', '')

HTML.write_text(s)

# Fail the build instead of shipping another visibly broken WebView document.
if '<script id="asia-media-runtime">' in s:
    raise SystemExit('Nested asia-media-runtime script tag remains')
if '</script>\nfunction renderHistory()' in s:
    raise SystemExit('renderHistory is outside the main script block')
