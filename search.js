// Simple client-side search for static site
(function() {
    let searchData = [];
    let searchVisible = false;

    // Load search index
    fetch('/search.json')
        .then(response => response.json())
        .then(data => {
            searchData = data;
        })
        .catch(err => console.error('Failed to load search index:', err));

    // Toggle search overlay
    window.toggleSearch = function() {
        const overlay = document.getElementById('search-overlay');
        searchVisible = !searchVisible;
        
        if (searchVisible) {
            overlay.style.display = 'flex';
            document.getElementById('search-input').focus();
            document.body.style.overflow = 'hidden';
        } else {
            overlay.style.display = 'none';
            document.body.style.overflow = '';
        }
    };

    // Close search on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && searchVisible) {
            toggleSearch();
        }
    });

    // Perform search
    window.performSearch = function(query) {
        if (!query || query.length < 2) {
            document.getElementById('search-results').innerHTML = '';
            return;
        }

        query = query.toLowerCase();
        const results = searchData.filter(item => 
            item.title.toLowerCase().includes(query) ||
            item.category.toLowerCase().includes(query)
        );

        const resultsHtml = results.slice(0, 20).map(result => `
            <a href="${result.url}" class="search-result-item">
                <div class="result-title">${result.title}</div>
                <div class="result-meta">${result.category}</div>
            </a>
        `).join('');

        document.getElementById('search-results').innerHTML = resultsHtml || 
            '<div style="text-align: center; padding: 40px; color: var(--muted);">No results found</div>';
    };
})();

