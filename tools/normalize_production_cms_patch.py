from pathlib import Path

p = Path('tools/patch_production_cms.py')
s = p.read_text(encoding='utf-8')
s = s.replace("r'<main id=\\\"admin\\\" class=\\\"view\\\">.*?</main></div><nav class=\\\"nav\\\">'", "r'<main id=\\\"admin\\\" class=\\\"view\\\">.*?</main>'")
s = s.replace("admin_markup + '<nav class=\\\"nav\\\">'", "admin_markup.replace('</main></div>', '</main>')")
p.write_text(s, encoding='utf-8')
print('normalized CMS patch matcher')
