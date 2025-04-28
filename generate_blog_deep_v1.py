import json
import markdown
import os

with open("blog_content.json") as f:
    data = json.load(f)

# Generate each post's HTML file first
posts_html_content = []
for post in data["posts"]:
    md_file = post["post"]
    html_file = md_file.replace(".md", ".html")
    
    # Read Markdown content and convert to HTML
    with open(md_file) as f:
        post_html = markdown.markdown(f.read())
    
    # Create the necessary directories if they don't exist
    os.makedirs(os.path.dirname(html_file), exist_ok=True)
    
    # Write the converted HTML to a file
    with open(html_file, "w") as f_post:
        f_post.write(post_html)
    
    # Prepare content for the index page
    tags_html = "  ".join(
        f"<span class='inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-1 dark:bg-blue-peria dark:text-white'>{tag}</span>"
        for tag in post.get("tags", [])
    )
    
    posts_html_content.append(f"""
    <div class='mb-6'>
        <h3 class='text-xl font-semibold mb-2'><a href='{html_file}' class='hover:text-blue-500 dark:hover:text-blue-400'> {post['title']}</a></h3>
        <p class='text-gray-600 dark:text-gray-300 mb-2'>Posted on {post.get('date', '')}</p>
        <div class='mb-2'>
            {tags_html}
        </div>
        <p class='mb-4 text-gray-700 dark:text-gray-200'>{post.get('excerpt', '')}</p>
    </div>
""")

# Generate the index.html
index_html = f"""
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
<body class="bg-gray-50 dark:bg-gray-900">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-8 text-center dark:text-white">{data['site_title']}</h1>
        <div class='space-y-6'>
            {''.join(posts_html_content)}
        </div>
    </div>
</body>
</html>
"""

# Write the index.html
with open("index.html", "w") as f_index:
    f_index.write(index_html)

print("Index page and post pages generated successfully!")