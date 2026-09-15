from pathlib import Path
import re

HTML = Path('app/src/main/assets/index.html')
s = HTML.read_text()

# A previous runtime patch accidentally emitted duplicate Media3 script tags.
s = re.sub(r'(?:\s*<script id="asia-media-runtime">){2,}', '\n<script id="asia-media-runtime">', s)

# Keep renderHistory and the remaining app functions inside the main JavaScript block.
s = s.replace('</script>\nfunction renderHistory()', 'function renderHistory()', 1)

# Remove any accidental blank script markers left by repeated patch runs.
s = re.sub(r'\n\s*<script id="asia-media-runtime">\s*<script id="asia-media-runtime">', '\n<script id="asia-media-runtime">', s)

HTML.write_text(s)

# Fail the build instead of shipping another visibly broken WebView document.
if s.count('<script id="asia-media-runtime">') != 1:
    raise SystemExit('Expected exactly one asia-media-runtime script block')
if '</script>\nfunction renderHistory()' in s:
    raise SystemExit('renderHistory is outside the main script block')
