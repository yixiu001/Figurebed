document.addEventListener("DOMContentLoaded", function() {
    fetch('files.json')
        .then(response => response.json())
        .then(fileStructure => {
            function populateDirectory(data, parentElement, path = '') {
                for (const key in data) {
                    if (typeof data[key] === 'object' && !data[key].https_url) {
                        const folder = document.createElement('div');
                        folder.innerHTML = `<button class="collapsible" data-path="${path}/${key}">${key}</button>`;
                        parentElement.appendChild(folder);
                        const contentSection = document.createElement('div');
                        contentSection.className = 'content-section';
                        contentSection.style.display = 'none';
                        folder.appendChild(contentSection);
                        populateDirectory(data[key], contentSection, path + '/' + key);
                    }
                }

                const coll = document.getElementsByClassName("collapsible");
                for (let i = 0; i < coll.length; i++) {
                    coll[i].addEventListener("click", function() {
                        const content = this.nextElementSibling;
                        if (content.style.display === "block") {
                            content.style.display = "none";
                        } else {
                            content.style.display = "block";
                        }
                        this.classList.toggle("active");
                        populateTable(this.getAttribute("data-path"));
                    });
                }
            }

            function populateTable(directory) {
                const imageTable = document.getElementById("image-table");
                while (imageTable.rows.length > 1) {
                    imageTable.deleteRow(1);
                }

                const images = getImagesFromDirectory(fileStructure, directory);
                images.forEach(item => {
                    const row = imageTable.insertRow();
                    const cell1 = row.insertCell(0);
                    const cell2 = row.insertCell(1);
                    const cell3 = row.insertCell(2);

                    cell1.innerHTML = `<img src="${item.https_url}" alt="${item.name}">`;
                    cell2.innerHTML = `<span class="link" onclick="copyToClipboard('${item.https_url}')">${item.https_url}</span>`;
                    cell3.innerHTML = `<span class="link" onclick="copyToClipboard('${item.cdn_url}')">${item.cdn_url}</span>`;
                });
            }

            function getImagesFromDirectory(data, directory) {
                const images = [];
                const dirParts = directory.split('/').filter(part => part);

                function traverse(currentData, currentPath = '') {
                    for (const key in currentData) {
                        if (typeof currentData[key] === 'object' && !currentData[key].https_url) {
                            if (dirParts.length === 0 || dirParts[0] === key) {
                                dirParts.shift();
                                traverse(currentData[key], currentPath + '/' + key);
                            }
                        } else if (typeof currentData[key] === 'object' && currentData[key].https_url) {
                            if (currentPath === directory) {
                                images.push({
                                    name: key,
                                    https_url: currentData[key].https_url,
                                    cdn_url: currentData[key].cdn_url
                                });
                            }
                        }
                    }
                }

                traverse(data);
                return images;
            }

            function copyToClipboard(text) {
                navigator.clipboard.writeText(text).then(function() {
                    alert('链接已复制: ' + text);
                }, function(err) {
                    console.error('复制失败: ', err);
                });
            }

            const directoryElement = document.getElementById('directory');
            populateDirectory(fileStructure, directoryElement);
        });
});
