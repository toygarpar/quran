import json
import markdown
import os

with open("quran_content.json") as f:
    data = json.load(f)

html = f"""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>{data['site_title']}</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <script>
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
        document.documentElement.classList.add('dark');
    }}
    </script>
    <link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>
    <style>
        body {{
            background-color: #111827; /* dark gray */
            color: #f9fafb; /* light text */
        }}
        .prose {{
            color: #f9fafb;
        }}
        .prose h1, .prose h2, .prose h3 {{
            color: #60a5fa;
        }}
        pre code {{
            background-color: #1f2937;
            color: #f9fafb;
            display: block;
            padding: 1em;
            overflow-x: auto;
            border-radius: 0.5rem;
        }}
        code {{
            background-color: #374151;
            padding: 0.2em 0.4em;
            border-radius: 0.25rem;
        }}
        a {{
            color: #93c5fd;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body class='font-sans p-6'>
    <div class='max-w-3xl mx-auto'>
        <h1 class='text-4xl font-bold mb-2'>{data['site_title']}</h1>
        <p class='text-lg text-gray-300 mb-6'>{data['intro']}</p>
        <h2 class='text-2xl font-semibold mb-4'>Sureler - Surahs</h2>
        <div class='space-y-6'>
"""

for post in data["posts"]:
    md_file = post["post"]
    html_file = md_file.replace(".md", ".html")
    tags_html = " ".join(
        f"<span class='inline-block bg-blue-200 text-blue-900 text-xs px-2 py-1 rounded mr-1'>{tag}</span>"
        for tag in post.get("tags", [])
    )

    with open(md_file) as f:
        post_html = markdown.markdown(
            f.read(),
            extensions=["extra", "codehilite", "tables", "fenced_code"]
        )

    with open(html_file, "w") as f_post:
        f_post.write(f"""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>{post['title']}</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>
    <style>
        body {{
            background-color: #111827;
            color: #f9fafb;
        }}
        .prose {{
            color: #f9fafb;
        }}
        .prose h1, .prose h2, .prose h3 {{
            color: #60a5fa;
        }}
        pre code {{
            background-color: #1f2937;
            color: #f9fafb;
            display: block;
            padding: 1em;
            overflow-x: auto;
            border-radius: 0.5rem;
        }}
        code {{
            background-color: #374151;
            padding: 0.2em 0.4em;
            border-radius: 0.25rem;
        }}
        a {{
            color: #93c5fd;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body class='font-sans p-6'>
    <div class='max-w-3xl mx-auto'>
        <a href='../index.html' class='block mb-4'>← Sure Listesine Geri Dön</a>
        <h1 class='text-3xl font-bold mt-4'>{post['title']}</h1>
        <p class='text-sm text-gray-400 mb-4'>{post['date']}</p>
        {tags_html}
        <div class='prose max-w-none mt-4'>{post_html}</div>
    </div>
</body>
</html>
""")

    html += f"""
        <div class='border-b pb-4'>
            <h3 class='text-xl font-semibold'>{post['title']}</h3>
            <p class='text-sm text-gray-400'>{post['date']}</p>
            <p class='mb-2'>{post['summary']}</p>
            {tags_html}
            <a href='{html_file}' class='block mt-1'>Sureye Git →</a>
        </div>
"""

html += """
        </div>
    </div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)

print("✅ Surahs generated with enhanced dark theme! Open index.html to view it.")
