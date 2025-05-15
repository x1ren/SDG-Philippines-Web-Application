async function fetchNews() {
    try {
        const response = await fetch('api/news');
        const articles = await response.json();
        renderNews(articles);
    } catch (error) {
        console.error("Error fetching news:", error);
        showErrorMessage();
    }
}

function renderNews(articles) {
    const newsContainer = document.querySelector('.news-container');
    newsContainer.innerHTML = ''; 
    

    const newsGrid = document.createElement('div');
    newsGrid.className = 'news-grid';
    
  
    for (let i = 0; i < 5 && i < articles.length; i++) {
        const article = articles[i];
        const card = createNewsCard(article, i === 0);
        newsGrid.appendChild(card);
    }
    
    newsContainer.appendChild(newsGrid);
}

function createNewsCard(article, isFeature = false) {
    const card = document.createElement('div');
    card.className = isFeature ? 'news-card feature-card' : 'news-card';
    card.setAttribute('data-url', article.url);
    card.addEventListener('click', function() {
        window.open(this.getAttribute('data-url'), '_blank', 'noopener noreferrer');
    });
    
    const thumbnailUrl = article.image || '/assets/placeholder-news.jpg';
    const formattedDate = formatPublishDate(article.publishedAt);
    
    card.innerHTML = `
        <div class="card-image-container">
            <img class="card-image" src="${thumbnailUrl}" alt="${article.title}" onerror="this.onerror=null; this.src='/assets/placeholder-news.jpg';">
            <div class="source-badge">${article.source.name}</div>
        </div>
        <div class="card-content">
            <h3 class="card-title">${article.title}</h3>
            <p class="card-description">${article.description || 'Read the full article for more details.'}</p>
            <div class="card-meta">
                <span class="card-date">${formattedDate}</span>
                <span class="card-link">Read More</span>
            </div>
        </div>
    `;
    
    return card;
}

function formatPublishDate(dateString) {
    const date = new Date(dateString);
    
  
    if (isNaN(date)) return '';
    

    const today = new Date();
    if (date.toDateString() === today.toDateString()) {
        return `Today, ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }
    
 
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    if (date.toDateString() === yesterday.toDateString()) {
        return `Yesterday, ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }
    

    return date.toLocaleDateString([], { 
        month: 'short', 
        day: 'numeric',
        year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
    });
}

function showErrorMessage() {
    const newsContainer = document.querySelector('.news-container');
    newsContainer.innerHTML = `
        <div class="error-message">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <p>Unable to load news at this time. Please try again later.</p>
            <button onclick="fetchNews()" class="retry-button">Retry</button>
        </div>
    `;
}


function addStyles() {
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        /* Modern News Styling */
        .news-container {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            cursor: pointer;
        }
        
        .news-grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            grid-gap: 24px;
        }
        
        .news-card {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            background-color: #fff;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            grid-column: span 4;
            display: flex;
            flex-direction: column;
        }
        
        .news-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }
        
        .feature-card {
            grid-column: span 8;
            grid-row: span 2;
        }
        
        .card-image-container {
            position: relative;
            padding-top: 56.25%; /* 16:9 aspect ratio */
            overflow: hidden;
        }
        
        .card-image {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        .news-card:hover .card-image {
            transform: scale(1.05);
        }
        
        .source-badge {
            position: absolute;
            top: 12px;
            left: 12px;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .card-content {
            padding: 16px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        
        .card-title {
            margin: 0 0 12px 0;
            font-size: 18px;
            font-weight: 600;
            line-height: 1.3;
            color: #111827;
        }
        
        .feature-card .card-title {
            font-size: 24px;
        }
        
        .card-description {
            margin: 0 0 16px 0;
            font-size: 14px;
            line-height: 1.5;
            color: #4B5563;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex-grow: 1;
        }
        
        .card-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
            padding-top: 12px;
            border-top: 1px solid #E5E7EB;
        }
        
        .card-date {
            font-size: 13px;
            color: #6B7280;
        }
        
        .card-link {
            font-size: 14px;
            font-weight: 500;
            color: #2563EB;
            text-decoration: none;
            transition: color 0.2s ease;
        }
        
        .card-link:hover {
            color: #1E40AF;
            text-decoration: underline;
        }
        
        .error-message {
            text-align: center;
            padding: 40px 20px;
            background-color: #FEF2F2;
            border-radius: 8px;
            color: #991B1B;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
        }
        
        .retry-button {
            background-color: #DC2626;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        
        .retry-button:hover {
            background-color: #B91C1C;
        }
        
        /* Responsive design */
        @media (max-width: 1024px) {
            .news-card {
                grid-column: span 6;
            }
            
            .feature-card {
                grid-column: span 12;
            }
        }
        
        @media (max-width: 768px) {
            .news-grid {
                grid-gap: 16px;
            }
            
            .news-card {
                grid-column: span 12;
            }
        }
        
        @media (max-width: 480px) {
            .news-container {
                padding: 16px;
            }
            
            .card-content {
                padding: 12px;
            }
            
            .card-title {
                font-size: 16px;
            }
            
            .feature-card .card-title {
                font-size: 18px;
            }
        }
    `;
    document.head.appendChild(styleElement);
}

document.addEventListener('DOMContentLoaded', () => {
    addStyles();
    fetchNews();
});


if (document.readyState === 'complete' || document.readyState === 'interactive') {
    addStyles();
    fetchNews();
}