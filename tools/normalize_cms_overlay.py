from pathlib import Path
import re

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')
# Remove previous generated CMS overlay blocks before the canonical CMS patch re-adds them.
s = re.sub(r'<style id="asia-cms-overlay-css">.*?</style>', '', s, flags=re.S)
s = re.sub(r'<section id="asiaAdminCMS">.*?</section>', '', s, flags=re.S)
s = re.sub(r'<script id="asia-cms-overlay-runtime">.*?</script>', '', s, flags=re.S)
s = re.sub(r'<script id="asia-admin-entry-fix">.*?</script>', '', s, flags=re.S)
p.write_text(s, encoding='utf-8')
print('CMS overlay normalized')
