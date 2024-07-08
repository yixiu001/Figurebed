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
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <div class="sidebar">
            <h1>目录</h1>
    '''

    directory_html = ''
    table_content = {}

    def generate_directory_html(directory, level=0):
        content = ''
        first_directory = None
        for entry in sorted(os.listdir(directory)):
            if entry.startswith('.'):
                continue
            path = os.path.join(directory, entry)
            rel_path = os.path.relpath(path, root_dir).replace("\\", "/")
            if os.path.isdir(path):
                if first_directory is None:
                    first_directory = rel_path
                content += f'''
                <button class="collapsible" data-path="{rel_path}">{'&nbsp;' * 4 * level + entry}</button>
                <div class="content-section">
                    {generate_directory_html(path, level + 1)[0]}
                </div>
                '''
            elif entry.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                dir_path = rel_path.rsplit("/", 1)[0]
                if dir_path not in table_content:
                    table_content[dir_path] = []
                https_url = base_url + rel_path
                cdn_url_complete = cdn_url + rel_path
                table_content[dir_path].append((entry, https_url, cdn_url_complete))
        return content, first_directory

    directory_html, first_directory = generate_directory_html(root_dir)

    html_content += directory_html
    html_content += '''
        </div>
        <div class="content">
            <h1>图片信息</h1>
            <table id="image-table">
                <tr>
                    <th>缩略图</th>
                    <th>HTTPS 访问地址</th>
                    <th>jsdelivr CDN 加速地址</th>
                </tr>
    '''

    html_content += '''
            </table>
        </div>
        <script src="script.js"></script>
        <script>
            var tableContent = ''' + str(table_content) + ''';
            var firstDirectory = ''' + '"' + first_directory + '"' + ''';
            initCollapsible(tableContent, firstDirectory);
        </script>
    </body>
    </html>
    '''

    with open(os.path.join(root_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_index_html('.')
