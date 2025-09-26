let dropZone = document.getElementById('drop_zone');
        let fileInfoDiv = document.getElementById('file_info');
        let inputElement = document.createElement('input');
        inputElement.type = 'file';
        let selectedFile;

        dropZone.ondragover = function(event) {
            event.preventDefault();
            this.style.backgroundColor = '#eee';
        };

        dropZone.ondragleave = function() {
            this.style.backgroundColor = '';
        };

        dropZone.ondrop = function(event) {
            event.preventDefault();
            this.style.backgroundColor = '';
            handleFiles(event.dataTransfer.files);
        };

        dropZone.onclick = function() {
            inputElement.click();
        };

        inputElement.onchange = function() {
            handleFiles(this.files);
        };

        function handleFiles(files) {
            selectedFile = files[0];
            fileInfoDiv.innerHTML = `
                <p>Selected file: ${selectedFile.name}</p>
                <button id="upload_button">Upload</button>
                <button id="cancel_button">Cancel</button>
            `;
            document.getElementById('upload_button').onclick = uploadFile;
            document.getElementById('cancel_button').onclick = cancelUpload;
            dropZone.style.display = 'none'; // Hide the drop zone
        }

        function uploadFile() {
    let formData = new FormData();
    formData.append('file', selectedFile);

    fetch('/revenue/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        console.log('File uploaded successfully:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

        function cancelUpload() {
            selectedFile = null;
            fileInfoDiv.innerHTML = '';
            dropZone.style.display = 'block'; // Show the drop zone
        }// JavaScript Document