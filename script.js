document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const text = document.getElementById('textInput').value;
    const resultSection = document.getElementById('resultSection');
    const resultContent = document.getElementById('resultContent');
    const loader = document.getElementById('loader');
    
    if (!text.trim()) {
        alert("Please enter some text first!");
        return;
    }

    // Show loader, hide previous results
    resultSection.classList.remove('hidden');
    resultContent.classList.add('hidden');
    loader.classList.remove('hidden');

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ description: text })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        alert("Failed to analyze text. Ensure the backend server is running.");
        resultSection.classList.add('hidden');
    } finally {
        loader.classList.add('hidden');
        if (!loader.classList.contains('hidden') === false && !resultSection.classList.contains('hidden')) {
             resultContent.classList.remove('hidden');
        }
    }
});

function displayResults(data) {
    const levelSpan = document.getElementById('levelValue');
    const confidenceSpan = document.getElementById('confidenceValue');
    const list = document.getElementById('recommendationList');

    // Set Level
    levelSpan.textContent = data.depression_level;
    levelSpan.className = 'badge'; // reset
    levelSpan.classList.add(data.depression_level.toLowerCase());

    // Set Score
    confidenceSpan.textContent = data.sadness_score;

    // Set Recommendations
    list.innerHTML = '';
    data.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        list.appendChild(li);
    });
}
