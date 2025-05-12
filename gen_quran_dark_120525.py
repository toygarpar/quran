import json
import markdown
import os

with open("quran_content.json") as f:
    data = json.load(f)

# Start building index.html with correct layout
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
    <!-- Fixed Tailwind CSS CDN -->
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
        p {{
            margin-top: 1em;
            margin-bottom: 1em;
            line-height: 1.7;
        }}
    </style>
</head>
<body class='font-sans p-6'>
    <div class='max-w-3xl mx-auto'>
        <h1 class='text-4xl font-bold mb-2'>{data['site_title']}</h1>
        <p class='text-lg text-gray-300 mb-6'>{data['intro']}</p>

        <!-- Search Bar -->
        <input type="text" id="searchInput" placeholder="Sure ismiyle ara..." class="w-full p-2 mb-4 rounded bg-gray-800 text-white border border-gray-600">

        <h2 class='text-2xl font-semibold mb-4'>Sureler - Surahs</h2>
        <div class='space-y-6' id="surahList">
"""

# Loop through posts and generate individual pages + list on index.html
for idx, post in enumerate(data["posts"]):
    md_file = post["post"]
    html_file = md_file.replace(".md", ".html")
    tags_html = " ".join(
        f"<span class='inline-block bg-blue-200 text-blue-900 text-xs px-2 py-1 rounded mr-1'>{tag}</span>"
        for tag in post.get("tags", [])
    )

    # Read Markdown file and convert to HTML
    with open(md_file) as f:
        post_html = markdown.markdown(
            f.read(),
            extensions=["extra", "codehilite", "tables", "fenced_code", "nl2br", "fenced_code", "footnotes", "sane_lists", "smarty"]
        )

    # Write individual surah page
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
        p {{
            margin-top: 1em;
            margin-bottom: 1em;
            line-height: 1.7;
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

    # Add surah card to index.html
    html += f"""
        <div class='border-b pb-4' id='surah-{idx}'>
            <h3 class='text-xl font-semibold surah-title'>{post['title']}</h3>
            <p class='text-sm text-gray-400'>{post['date']}</p>
            <p class='mb-2'>{post['summary']}</p>
            {tags_html}
            <a href='{html_file}' class='block mt-1'>Sureye Git →</a>
        </div>
"""

# Close index.html and add search script
html += """
        </div>
    </div>

    <!-- Search Script -->
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const searchInput = document.getElementById('searchInput');
            const surahCards = document.querySelectorAll('#surahList .border-b');

            searchInput.addEventListener('input', function () {
                const query = this.value.toLowerCase();

                surahCards.forEach(card => {
                    const title = card.querySelector('.surah-title').textContent.toLowerCase();
                    if (title.includes(query)) {
                        card.style.display = '';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    </script>
</body>
</html>
"""

# Write final index.html
with open("index.html", "w") as f:
    f.write(html)

print("✅ Surahs generated with enhanced dark theme and working search! Open index.html to view it.")