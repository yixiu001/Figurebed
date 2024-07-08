document.addEventListener("DOMContentLoaded", function() {
    var githubUsername = 'GITHUB_USERNAME';
    var githubRepository = 'GITHUB_REPOSITORY';

    fetch('files.json')
        .then(response => response.json())
        .then(fileStructure => {
            function populateDirectory(data, parentElement = document.getElementById('directory'), level = 0) {
                for (const key in data) {
                    if (typeof data[key] === 'object' && !data[key].https_url) {
                        const folder = document.createElement('div');
                        folder.style.marginLeft = level * 20 + 'px';
                        folder.innerHTML = `<button class="collapsible" data-path="${key}">${key}</button>`;
                        parentElement.appendChild(folder);
                        const contentSection = document.createElement('div');
                        contentSection.className = 'content-section';
                        contentSection.style.display = 'none';
                        folder.appendChild(contentSection);
                        populateDirectory(data[key], contentSection, level + 1);
                    }
                }

                var coll = document.getElementsByClassName("collapsible");
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
            }

            function populateTable(directory) {
                var imageTable = document.getElementById("image-table");
                while (imageTable.rows.length > 1) {
                    imageTable.deleteRow(1);
                }
                var images = getImagesFromDirectory(fileStructure, directory);
                images.forEach(function(item) {
                    var row = imageTable.insertRow();
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);
                    var cell3 = row.insertCell(2);
                    cell1.innerHTML = '<img src="' + item.https_url + '" alt="' + item.name + '">';
                    cell2.innerHTML = '<span class="link" onclick="copyToClipboard(\'' + item.https_url + '\')">' + item.https_url + '</span>';
                    cell3.innerHTML = '<span class="link" onclick="copyToClipboard(\'' + item.cdn_url + '\')">' + item.cdn_url + '</span>';
                });
            }

            function getImagesFromDirectory(data, directory) {
                var images = [];
                for (const key in data) {
                    if (typeof data[key] === 'object' && !data[key].https_url) {
                        images = images.concat(getImagesFromDirectory(data[key], directory + '/' + key));
                    } else if (typeof data[key] === 'object' && data[key].https_url) {
                        if (directory === '' || directory.split('/').indexOf(key.split('/')[0]) !== -1) {
                            images.push({
                                name: key,
                                https_url: data[key].https_url,
                                cdn_url: data[key].cdn_url
                            });
                        }
                    }
                }
                return images;
            }

            function copyToClipboard(text) {
                navigator.clipboard.writeText(text).then(function() {
                    alert('链接已复制: ' + text);
                }, function(err) {
                    console.error('复制失败: ', err);
                });
            }

            populateDirectory(fileStructure);
            if (Object.keys(fileStructure).length > 0) {
                populateTable(Object.keys(fileStructure)[0]);
            }
        });
});
