from pathlib import Path

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')
# Remove the old recursive admin-entry shim. Creator Studio owns the admin route now.
old = '''<script id="asia-admin-entry-fix">(function(){var oldLoad=window.loadAdmin;window.loadAdmin=function(){if(window.go)return window.go('admin');if(oldLoad)return oldLoad.apply(this,arguments)};})();</script>'''
if old in s:
    s = s.replace(old, '')
p.write_text(s, encoding='utf-8')
print('admin entry recursion removed')
