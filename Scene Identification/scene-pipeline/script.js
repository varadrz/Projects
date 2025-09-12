document.getElementById('videoInput').addEventListener('change', handleFileSelect);

function handleFileSelect(e) {
  const dropArea = document.querySelector('.drop-area span');
  if (e.target.files.length > 0) {
    dropArea.textContent = e.target.files[0].name;
  } else {
    dropArea.textContent = "Drag & drop a video, or click to select a file";
  }
}

document.getElementById('videoForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const input = document.getElementById('videoInput');
  if (input.files.length === 0) return;
  const file = input.files[0];

  const formData = new FormData();
  formData.append('video', file);

  fetch('/analyze', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('output').style.display = 'block';
    document.getElementById('summary').textContent = data.summary;
    document.getElementById('jsonData').textContent = JSON.stringify(data.analytics, null, 2);
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data.analytics, null, 2));
    document.getElementById('downloadLink').setAttribute("href", dataStr);
  })
  .catch(() => {
    alert('Failed to analyze video.');
  });
});
