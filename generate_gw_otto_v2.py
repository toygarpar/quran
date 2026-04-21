import json
import markdown
import os

with open("quran_content.json", encoding="utf-8") as f:
    data = json.load(f)

# Define styles separately to avoid f-string bracket conflicts and duplication
ottoman_styles = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

    body {
        background-color: #1A1714;
        color: #F2E8CF;
        font-family: 'Lora', serif;
    }

    strong, b {
        color: #FFC107;
        font-weight: 700;
        text-shadow: 0 0 8px rgba(255, 193, 7, 0.4);
    }
    
    .surah-card {
        background-color: #24201D;
        border-left: 4px solid #BC9353;
        padding: 1.5rem;
        border-radius: 0.25rem;
        transition: transform 0.2s;
        margin-bottom: 1.5rem;
    }

    .surah-card:hover {
        transform: translateX(5px);
        background-color: #2C2723;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #BC9353;
    }

    .prose {
        color: #F2E8CF;
        max-width: none;
        line-height: 1.8;
    }

    .prose p {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .tag-ottoman {
        background-color: #38A3A5;
        color: #1A1714;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 0.2rem 0.6rem;
        border-radius: 0.25rem;
        margin-right: 0.5rem;
        display: inline-block;
    }

    input#searchInput {
        background-color: #24201D;
        border: 1px solid #BC9353;
        color: #F2E8CF;
        width: 100%;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }

    input#searchInput::placeholder {
        color: #8D8273;
    }

    a {
        color: #BC9353;
        text-decoration: none;
        font-weight: 600;
    }

    a:hover {
        color: #F2E8CF;
        text-decoration: underline;
    }

    hr {
        border-color: #3D352E;
        margin: 2rem 0;
    }
</style>
"""

# Start building index.html with correct layout
html = f"""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>{data['site_title']}</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>
    {ottoman_styles}
</head>
<body class='p-6'>
    <div class='max-w-3xl mx-auto'>
        <h1 class='text-5xl font-bold mb-4'>{data['site_title']}</h1>
        <p class='text-xl mb-8' style='color: #8D8273;'>{data['intro']}</p>

        <input type="text" id="searchInput" placeholder="Sure ismiyle ara (Search by Surah)...">

        <div id="surahList">
"""

# Loop through posts and generate individual pages + list on index.html
for idx, post in enumerate(data["posts"]):
    md_file = post["post"]
    html_file = md_file.replace(".md", ".html")
    tags_html = "".join(
        f"<span class='tag-ottoman'>{tag}</span>"
        for tag in post.get("tags", [])
    )

    # Read Markdown file and convert to HTML
    with open(md_file, encoding="utf-8") as f:
        post_html = markdown.markdown(
            f.read(),
            extensions=["extra", "codehilite", "tables", "fenced_code", "nl2br", "footnotes", "sane_lists", "smarty"]
        )

    # Write individual surah page
    with open(html_file, "w", encoding="utf-8") as f_post:
        f_post.write(f"""
<!DOCTYPE html>
<html lang='tr'>
<head>
    <meta charset='UTF-8'>
    <title>{post['title']}</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>
    {ottoman_styles}
</head>
<body class='p-6'>
    <div class='max-w-3xl mx-auto'>
        <a href='../index.html' style='color: #38A3A5;'>← Listeye Dön</a>
        <header class='mt-8 mb-12'>
            <h1 class='text-4xl font-bold'>{post['title']}</h1>
            <p style='color: #8D8273;' class='mt-2 text-sm'>{post['date']}</p>
            <div class='mt-4'>{tags_html}</div>
        </header>
        <article class='prose'>
            {post_html}
        </article>
        <hr>
        <footer class='pb-12 text-center'>
            <p style='color: #8D8273;'>Toygar Par - Quran Project</p>
        </footer>
    </div>
</body>
</html>
""")

    # Add surah card to index.html
    html += f"""
        <div class='surah-card' id='surah-{idx}'>
            <h3 class='text-2xl font-bold surah-title'>{post['title']}</h3>
            <p style='color: #8D8273;' class='text-xs mb-2'>{post['date']}</p>
            <p class='mb-4' style='color: #F2E8CF;'>{post['summary']}</p>
            <div class='mb-4'>{tags_html}</div>
            <a href='{html_file}'>İncele →</a>
        </div>
"""

# Close index.html and add search script
html += """
        </div>
    </div>

    <!-- Search Script -->
    <script>
        const searchInput = document.getElementById('searchInput');
        const cards = document.querySelectorAll('.surah-card');

        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            cards.forEach(card => {
                const title = card.querySelector('.surah-title').innerText.toLowerCase();
                card.style.display = title.includes(term) ? 'block' : 'none';
            });
        });
    </script>
</body>
</html>
"""

# Write final index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Surahs generated with enhanced dark theme and working search! Open index.html to view it.")