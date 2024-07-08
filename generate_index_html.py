import os

# 在这里定义GitHub用户名和仓库名称
GITHUB_USERNAME = 'yixiu001'
GITHUB_REPOSITORY = 'Figurebed'

def generate_index_html(root_dir):
    base_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/raw/main/"
    cdn_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}@main/"

    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>一休github简易图床系统</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f0f0f0;
            }
            h1 {
                text-align: center;
            }
            .directory {
                margin: 10px 0;
            }
            .file {
                margin-left: 20px;
            }
            .collapsible {
                cursor: pointer;
                padding: 10px;
                text-align: left;
                background-color: #f2f2f2;
                border: none;
                outline: none;
                font-size: 15px;
                width: 100%;
                transition: 0.4s;
            }
            .active, .collapsible:hover {
                background-color: #ccc;
            }
            .content {
                padding: 0 18px;
                display: none;
                overflow: hidden;
                background-color: #f9f9f9;
            }
            img {
                max-width: 100px;
                height: auto;
            }
        </style>
    </head>
    <body>
        <h1>一休github简易图床系统</h1>
    '''

    def generate_directory_html(directory, level=0):
        content = ''
        for entry in sorted(os.listdir(directory)):
            if entry.startswith('.'):
                continue
            path = os.path.join(directory, entry)
            rel_path = os.path.relpath(path, root_dir)
            if os.path.isdir(path):
                content += f'''
                <button class="collapsible">{'&nbsp;' * 4 * level + entry}</button>
                <div class="content">
                    {generate_directory_html(path, level + 1)}
                </div>
                '''
            elif entry.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                https_url = base_url + rel_path
                cdn_url_complete = cdn_url + rel_path
                content += f'''
                <div class="file">
                    <img src="{https_url}" alt="{entry}"><br>
                    <a href="{https_url}" target="_blank">{https_url}</a><br>
                    <a href="{cdn_url_complete}" target="_blank">{cdn_url_complete}</a>
                </div>
                '''
        return content

    html_content += generate_directory_html(root_dir)
    html_content += '''
        <script>
            var coll = document.getElementsByClassName("collapsible");
            var i;

            for (i = 0; i < coll.length; i++) {
                coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var content = this.nextElementSibling;
                    if (content.style.display === "block") {
                        content.style.display = "none";
                    } else {
                        content.style.display = "block";
                    }
                });
            }
        </script>
    </body>
    </html>
    '''

    with open(os.path.join(root_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_index_html('.')
