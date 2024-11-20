// Image upload prediction
const imageForm = document.getElementById('imageForm');
const imageInput = document.getElementById('imageInput');
const imageResult = document.getElementById('imageResult');

imageForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('file', imageInput.files[0]);

    const response = await fetch('/predict/image', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    imageResult.innerText = `Prediction: ${data.prediction}`;
});

// Tweet submission prediction
const tweetInput = document.getElementById('tweetInput');
const tweetSubmit = document.getElementById('tweetSubmit');
const tweetResult = document.getElementById('tweetResult');

tweetSubmit.addEventListener('click', async () => {
    const content = tweetInput.value;
    if (!content) return alert('Please enter a tweet!');

    const response = await fetch('/predict/tweet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content })
    });

    const data = await response.json();
    tweetResult.innerText = `Prediction: ${data.prediction}`;
});
