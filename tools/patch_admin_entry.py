from pathlib import Path
p=Path('app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
js='''<script id="asia-admin-entry-fix">(function(){var oldLoad=window.loadAdmin;window.loadAdmin=function(){if(window.go)return window.go('admin');if(oldLoad)return oldLoad.apply(this,arguments)};})();</script>'''
if 'asia-admin-entry-fix' not in s:s=s.replace('</body>',js+'</body>',1)
p.write_text(s,encoding='utf-8')
print('admin entry fixed')
