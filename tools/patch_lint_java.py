from pathlib import Path

p = Path('app/src/main/java/com/hellobaroda/navratri/MainActivity.java')
s = p.read_text()
old = 't.setTypeface(null,1)'
new = 't.setTypeface(null,android.graphics.Typeface.BOLD)'
if old in s:
    s = s.replace(old, new)
p.write_text(s)
