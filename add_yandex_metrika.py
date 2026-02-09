# Add Yandex Metrika counter to schedule site
# Usage: python3 add_yandex_metrika.py <COUNTER_ID>
# Example: python3 add_yandex_metrika.py 12345678

import sys
import os
import re

BASE = "/root/photoimpuls-bot/schedule"
INDEX_HTML = os.path.join(BASE, "index.html")
APP_TSX = os.path.join(BASE, "src", "App.tsx")

def get_metrika_head_code(counter_id):
    """Generate Yandex Metrika script for <head>."""
    return f'''<!-- Yandex.Metrika counter -->
<script type="text/javascript">
   (function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
   m[i].l=1*new Date();
   for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
   k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})
   (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

   ym({counter_id}, "init", {{
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true,
        webvisor:true
   }});
</script>
<!-- /Yandex.Metrika counter -->'''

def get_metrika_noscript_code(counter_id):
    """Generate Yandex Metrika noscript for <body>."""
    return f'''<!-- Yandex.Metrika noscript -->
<noscript><div><img src="https://mc.yandex.ru/watch/{counter_id}" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika noscript -->'''

def add_to_index_html(counter_id):
    """Add Metrika code to index.html: script in <head>, noscript in <body>."""
    if not os.path.isfile(INDEX_HTML):
        print(f"File not found: {INDEX_HTML}")
        return False
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()
    if f"ym({counter_id}" in content or f"yandex.ru/watch/{counter_id}" in content:
        print("index.html: Metrika code already present.")
        return True
    head_code = get_metrika_head_code(counter_id)
    noscript_code = get_metrika_noscript_code(counter_id)
    # Add script to <head>
    if "</head>" in content:
        content = content.replace("</head>", head_code + "\n</head>", 1)
    else:
        return False
    # Add noscript to <body> (before </body>)
    if "</body>" in content:
        content = content.replace("</body>", noscript_code + "\n</body>", 1)
    else:
        # If no </body>, add before </html> or at the end
        if "</html>" in content:
            content = content.replace("</html>", noscript_code + "\n</html>", 1)
        else:
            content = content + "\n" + noscript_code
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(content)
    print("index.html: Metrika code added (script in head, noscript in body).")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 add_yandex_metrika.py <COUNTER_ID>")
        print("Example: python3 add_yandex_metrika.py 12345678")
        print("\nTo get COUNTER_ID:")
        print("1. Go to https://metrika.yandex.ru/")
        print("2. Create a counter for http://185.198.152.146:8080")
        print("3. Copy the number from ym(XXXXXX, 'init') - that's your COUNTER_ID")
        sys.exit(1)
    counter_id = sys.argv[1].strip()
    if not counter_id.isdigit():
        print("Error: COUNTER_ID must be a number (e.g., 12345678)")
        sys.exit(1)
    print(f"Adding Yandex Metrika counter {counter_id}...")
    if add_to_index_html(counter_id):
        print("Done! Rebuild the site: cd /root/photoimpuls-bot/schedule && npm run build && sudo systemctl restart schedule")
    else:
        print("Failed to add Metrika code.")
