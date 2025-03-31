document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const platform = document.getElementById('platformSelect').value;
    const query = document.getElementById('queryInput').value;
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const submitButton = e.target.querySelector('button');
    
    submitButton.disabled = true;
    loading.classList.remove('hidden');
    results.classList.add('hidden');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `platform=${encodeURIComponent(platform)}&query=${encodeURIComponent(query)}`
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }

        // Update statistics
        const statsContent = document.getElementById('statsContent');
        statsContent.innerHTML = `
            <p>Total posts analyzed: ${data.stats.total}</p>
            <p>Positive: ${data.stats.positive} (${((data.stats.positive/data.stats.total)*100).toFixed(1)}%)</p>
            <p>Negative: ${data.stats.negative} (${((data.stats.negative/data.stats.total)*100).toFixed(1)}%)</p>
            <p>Neutral: ${data.stats.neutral} (${((data.stats.neutral/data.stats.total)*100).toFixed(1)}%)</p>
        `;

        // Update word cloud
        const wordcloudImg = document.getElementById('wordcloudImg');
        wordcloudImg.src = data.wordcloud + '?t=' + new Date().getTime();

        // Update posts
        const tweetsContent = document.getElementById('tweetsContent');
        tweetsContent.innerHTML = data.results.map(post => `
            <div class="tweet">
                <p>${post.text}</p>
                <p class="sentiment-${post.sentiment}">Sentiment: ${post.sentiment} (Polarity: ${post.polarity.toFixed(2)})</p>
                <small>${post.platform} - ${post.created_at}</small>
            </div>
        `).join('');

        results.classList.remove('hidden');
    } catch (error) {
        alert(error.message);
        console.error(error);
    } finally {
        loading.classList.add('hidden');
        setTimeout(() => {
            submitButton.disabled = false;
        }, 5000);
    }
});