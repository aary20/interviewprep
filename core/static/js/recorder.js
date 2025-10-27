// static/core/js/recorder.js
let mediaRecorder;
let audioChunks = [];

document.getElementById('start-recording').addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        mediaRecorder.ondataavailable = e => {
        audioChunks.push(e.data);
        };

        mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob);

        fetch('/upload_audio/', {
            method: 'POST',
            body: formData
        }).then(response => {
            alert("Voice answer uploaded!");
        });

        audioChunks = [];
        };
    });
});

document.getElementById('stop-recording').addEventListener('click', () => {
    mediaRecorder.stop();
});
