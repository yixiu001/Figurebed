import os

def generate_index_html(root_dir):
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Index</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f0f0f0;
            }
            h1 {
                text-align: center;
            }
            .gallery {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }
            .gallery-item {
                margin: 10px;
                border: 1px solid #ccc;
                background-color: #fff;
                box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            }
            .gallery-item img {
                max-width: 100%;
                height: auto;
                display: block;
            }
            .gallery-item a {
                text-decoration: none;
                color: #333;
                display: block;
                padding: 10px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>Image Index</h1>
        <div class="gallery">
    '''

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                file_path = os.path.relpath(os.path.join(subdir, file), root_dir)
                html_content += f'''
                <div class="gallery-item">
                    <a href="{file_path}" target="_blank">
                        <img src="{file_path}" alt="{file}">
                        {file}
                    </a>
                </div>
                '''

    html_content += '''
        </div>
    </body>
    </html>
    '''

    with open(os.path.join(root_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_index_html('.')

