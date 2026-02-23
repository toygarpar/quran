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
</head>
<body class='bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-100 font-sans p-6'>
    <div class='max-w-3xl mx-auto'>
        <h1 class='text-4xl font-bold mb-2'>{data['site_title']}</h1>
        <p class='text-lg text-gray-600 dark:text-gray-300 mb-6'>{data['intro']}</p>
        <h2 class='text-2xl font-semibold mb-4'>Sureler - Surahs</h2>
        <div class='space-y-6'>
"""

for post in data["posts"]:
    md_file = post["post"]
    html_file = md_file.replace(".md", ".html")
    tags_html = " ".join(
        f"<span class='inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-1 dark:bg-blue-800 dark:text-white'>{tag}</span>"
        for tag in post.get("tags", [])
    )

    with open(md_file) as f:
        post_html = markdown.markdown(f.read())

    with open(html_file, "w") as f_post:
        f_post.write(f"""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>{post['title']}</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>
</head>
<body class='bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-100 font-sans p-6'>
    <div class='max-w-3xl mx-auto'>
        <a href='../index.html' class='text-blue-600 hover:underline'>← Sure Listesine Geri Dön</a>
        <h1 class='text-3xl font-bold mt-4'>{post['title']}</h1>
        <p class='text-sm text-gray-500 dark:text-gray-400 mb-4'>{post['date']}</p>
        {tags_html}
        <div class='prose dark:prose-invert max-w-none mt-4'>{post_html}</div>
    </div>
</body>
</html>
""")

    html += f"""
        <div class='border-b pb-4'>
            <h3 class='text-xl font-semibold'>{post['title']}</h3>
            <p class='text-sm text-gray-500 dark:text-gray-400'>{post['date']}</p>
            <p class='mb-2'>{post['summary']}</p>
            {tags_html}
            <a href='{html_file}' class='text-blue-600 hover:underline block mt-1'>Sureye Git →</a>
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

print("✅ Surahs generated! Open index.html to view it.")
