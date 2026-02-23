def add_image_preview_js():
    """Добавляет JavaScript для предпросмотра изображений"""
    return """
    <script>
    function showImagePreview(input) {
        let preview = document.getElementById('image-preview-' + input.name);
        if (!preview) {
            preview = document.createElement('div');
            preview.id = 'image-preview-' + input.name;
            preview.style.marginTop = '10px';
            input.parentNode.appendChild(preview);
        }

        const url = input.value;
        if (url) {
            preview.innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px;">
                    <img src="${url}" 
                         style="max-width: 100px; max-height: 100px; border-radius: 4px; border: 1px solid #ddd; padding: 3px; object-fit: cover;"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='block'">
                    <div style="display: none; color: red;">
                        <i class="fa-solid fa-triangle-exclamation"></i> Ошибка загрузки
                    </div>
                </div>
            `;
        } else {
            preview.innerHTML = '';
        }
    }

    function uploadImage(input, fieldId) {
        const file = input.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload-image', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.url) {
                    document.getElementById(fieldId).value = data.url;
                    showImagePreview(document.getElementById(fieldId));
                }
            })
            .catch(error => {
                console.error('Ошибка загрузки:', error);
                alert('Не удалось загрузить изображение');
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        const imageInputs = document.querySelectorAll('input[name$="_url"]');
        imageInputs.forEach(input => {
            if (input.value) {
                showImagePreview(input);
            }

            // Добавляем кнопку загрузки
            const wrapper = document.createElement('div');
            wrapper.style.display = 'flex';
            wrapper.style.gap = '10px';
            wrapper.style.alignItems = 'center';

            const uploadBtn = document.createElement('button');
            uploadBtn.type = 'button';
            uploadBtn.className = 'btn btn-outline-secondary';
            uploadBtn.innerHTML = '<i class="fa-solid fa-upload"></i> Загрузить';
            uploadBtn.onclick = function() {
                const fileInput = document.createElement('input');
                fileInput.type = 'file';
                fileInput.accept = 'image/*';
                fileInput.style.display = 'none';
                fileInput.onchange = function(e) {
                    uploadImage(e.target, input.id);
                };
                document.body.appendChild(fileInput);
                fileInput.click();
                document.body.removeChild(fileInput);
            };

            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input.cloneNode(true));
            wrapper.appendChild(uploadBtn);

            const oldInput = input;
            input.parentNode.removeChild(oldInput);
            wrapper.firstChild.id = oldInput.id;
            wrapper.firstChild.name = oldInput.name;
            wrapper.firstChild.value = oldInput.value;
        });
    });
    </script>
    """


def add_css_styles():
    """Добавляет CSS стили"""
    return """
    <style>
    .color-preview {
        width: 30px;
        height: 20px;
        border-radius: 4px;
        border: 1px solid #ddd;
    }
    input[type="color"] {
        width: 60px;
        height: 40px;
        padding: 0;
        border: 1px solid #ddd;
        border-radius: 4px;
        cursor: pointer;
    }
    .image-preview-thumb {
        max-width: 50px;
        max-height: 50px;
        border-radius: 4px;
        object-fit: cover;
    }
    .btn-upload {
        margin-left: 10px;
    }
    </style>
    """