import os

# 在这里定义GitHub用户名和仓库名称
GITHUB_USERNAME = 'yixiu001'
GITHUB_REPOSITORY = 'Figurebed'

def generate_index_html(root_dir):
    base_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/raw/main/"
    cdn_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}@main/"

    html_content = '''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>一休github简易图床系统</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
            }
            h1 {
                text-align: center;
            }
            .sidebar {
                width: 25%;
                overflow-y: auto;
                padding: 20px;
                background-color: #f7f7f7;
                border-right: 1px solid #ddd;
            }
            .content {
                flex: 1;
                padding: 20px;
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
            .content-section {
                padding: 0 18px;
                display: none;
                overflow: hidden;
                background-color: #f9f9f9;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
                text-align: left;
            }
            img {
                max-width: 100px;
                height: auto;
            }
            .link {
                color: blue;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h1>目录</h1>
    '''

    directory_html = ''

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
                <div class="content-section">
                    {generate_directory_html(path, level + 1)}
                </div>
                '''
            elif entry.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                https_url = base_url + rel_path
                cdn_url_complete = cdn_url + rel_path
                table_content.append((entry, https_url, cdn_url_complete))
        return content

    table_content = []

    directory_html += generate_directory_html(root_dir)

    html_content += directory_html
    html_content += '''
        </div>
        <div class="content">
            <h1>图片信息</h1>
            <table>
                <tr>
                    <th>缩略图</th>
                    <th>HTTPS 访问地址</th>
                    <th>jsdelivr CDN 加速地址</th>
                </tr>
    '''

    for entry, https_url, cdn_url_complete in table_content:
        html_content += f'''
        <tr>
            <td><img src="{https_url}" alt="{entry}"></td>
            <td><span class="link" onclick="copyToClipboard('{https_url}')">{https_url}</span></td>
            <td><span class="link" onclick="copyToClipboard('{cdn_url_complete}')">{cdn_url_complete}</span></td>
        </tr>
        '''

    html_content += '''
            </table>
        </div>
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

            function copyToClipboard(text) {
                navigator.clipboard.writeText(text).then(function() {
                    alert('链接已复制: ' + text);
                }, function(err) {
                    console.error('复制失败: ', err);
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
