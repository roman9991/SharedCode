function uploadFiles() {
    const files = document.getElementById('dicomFiles').files;
    const formData = new FormData();
    for (let file of files) {
        formData.append('dicomFiles', file);
    }

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(res => res.json())
      .then(data => {
          alert('Uploaded: ' + data.uploaded.join(', '));
          // Load first file for viewing
          if (data.uploaded.length > 0) {
              const imageId = 'wadouri:/uploads/' + data.uploaded[0];
              cornerstone.enable(document.getElementById('viewer'));
              cornerstone.loadImage(imageId).then(image => {
                  cornerstone.displayImage(document.getElementById('viewer'), image);
              });
          }
      });
}
