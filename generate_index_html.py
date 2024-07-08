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
                overflow-y: auto;
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
        <script>
            var coll = document.getElementsByClassName("collapsible");
            var imageTable = document.getElementById("image-table");
            var tableContent = ''' + str(table_content) + ''';
            var firstDirectory = ''' + '"' + first_directory + '"' + ''';

            function populateTable(directory) {
                while (imageTable.rows.length > 1) {
                    imageTable.deleteRow(1);
                }
                if (tableContent[directory]) {
                    tableContent[directory].forEach(function(item) {
                        var row = imageTable.insertRow();
                        var cell1 = row.insertCell(0);
                        var cell2 = row.insertCell(1);
                        var cell3 = row.insertCell(2);
                        cell1.innerHTML = '<img src="' + item[1] + '" alt="' + item[0] + '">';
                        cell2.innerHTML = '<span class="link" onclick="copyToClipboard(\'' + item[1] + '\')">' + item[1] + '</span>';
                        cell3.innerHTML = '<span class="link" onclick="copyToClipboard(\'' + item[2] + '\')">' + item[2] + '</span>';
                    });
                }
            }

            for (var i = 0; i < coll.length; i++) {
                coll[i].addEventListener("click", function() {
                    var active = document.querySelector('.collapsible.active');
                    if (active && active !== this) {
                        active.classList.remove('active');
                        active.nextElementSibling.style.display = 'none';
                    }
                    this.classList.toggle("active");
                    var content = this.nextElementSibling;
                    if (content.style.display === "block") {
                        content.style.display = "none";
                    } else {
                        content.style.display = "block";
                    }
                    populateTable(this.getAttribute("data-path"));
                });
            }

            function copyToClipboard(text) {
                navigator.clipboard.writeText(text).then(function() {
                    alert('链接已复制: ' + text);
                }, function(err) {
                    console.error('复制失败: ', err);
                });
            }

            // 默认展开第一个目录并显示其内容
            if (firstDirectory) {
                populateTable(firstDirectory);
                var firstCollapsible = document.querySelector('.collapsible[data-path="' + firstDirectory + '"]');
                firstCollapsible.classList.add("active");
                firstCollapsible.nextElementSibling.style.display = "block";
            }
        </script>
    </body>
    </html>
    '''

    with open(os.path.join(root_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_index_html('.')
