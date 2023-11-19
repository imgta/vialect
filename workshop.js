// Global variables to store chat session data
const queryUrl = 'https://chat.openai.com/backend-api/conversation';
const replyUrl = 'https://chat.openai.com/backend-api/lat/r';
let queryModel = '';
let replyModel = '';
let chatData = {
    queryChars: 0,
    replyChars: 0,
    inputTokens: 0,
    outputTokens: 0
};

// Assuming a character-to-token ratio of 3.23/1
function getCosts(model, inToken, outToken) {
    const costFactors = {
        'text-davinci-002-render-sha': { input: 0.001/1000, output: 0.002/1000 },
        'gpt-4': { input: 0.03/1000, output: 0.06/1000 }
    };
    const factor = costFactors[model] || { input: 0, output: 0 };
    return (inToken * factor.input) + (outToken * factor.output);
}
// Retrieve stored costs from local storage
function getStoredCosts() {
    const storedCost = localStorage.getItem('gptAccruedCost');
    return storedCost ? parseFloat(storedCost) : 0;
}
// Save the current cost to local storage
function saveCostsToStorage(cost) {
    localStorage.setItem('gptAccruedCost', cost.toString());
}
// Reset costs in local storage and UI
function resetCosts() {
    localStorage.setItem('gptAccruedCost', '0');
    displayCost(0.0);
}

function rightPt() {
    return `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/></svg>
    `
}

function leftPt() {
    return `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/></svg>
    `
}

// Create and inject the UI for displaying costs
function createAndInjectUI() {
    const uiHTML = `
        <div id="gpt-cost"
        style="
            position: fixed; bottom: 45px;
            display: flex;
            right: 0;
            padding: 10px;
            align-items: center;
            border-radius: 0 5px 5px 0;
            background-color: rgba(32,33,35,0.85);
            box-shadow: 0 0 5px rgba(0,0,0,0.5);
            transition: right 0.3s;
        ">
            <button id="toggle-btn" style="margin-right: 10px; cursor: pointer;">
                ${rightPt()}
            </button>
            <strong>GPT Costs</strong>:
            <div>
                <span id="cost-amt" style="color: rgb(163 105 37); padding-left: 10px;"> $0.0000000</span>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', uiHTML);
    document.getElementById('toggle-btn').addEventListener('click', toggleCostDisplay);
}

// Toggle the cost display
function toggleCostDisplay() {
    const costDisplay = document.getElementById('gpt-cost');
    const toggleBtn = document.getElementById('toggle-btn');
    if (costDisplay.style.right === '0px') {
        costDisplay.style.right = '-12rem';
        toggleBtn.innerHTML = `${leftPt()}`;
    } else {
        costDisplay.style.right = '0';
        toggleBtn.innerHTML = `${rightPt()}`;
    }
}

// Display estimated costs on page
function displayCost(cost) {
    const costText = document.getElementById('#cost-amt');
    costText.textContent = ` $${cost.toFixed(7)}`;
}

// Update the cost display
function updateCostDisplay(cost) {
    const costText = document.getElementById('#cost-amt');
    costText.textContent = ` $${cost.toFixed(7)}`;
}

// Override window.fetch function to intercept ChatGPT POST request
(function(originalFetch) {
    window.fetch = function(url, req) {
        if (req && req.method === 'POST') {
            if (url.includes(queryUrl) || url.includes(replyUrl)) {
                let payload = null;
                try {
                    payload = JSON.parse(req.body);
                } catch (error) {
                    console.error('JSON parsing error:', error);
                }

                if (payload) {
                    if (url.includes(queryUrl)) {
                        queryModel = payload.model;
                        chatData.queryChars += payload.messages[0].content.parts[0].length;
                        chatData.inputTokens += Math.ceil(chatData.queryChars/3.23);
                    } else if (url.includes(replyUrl)) {
                        replyModel = payload.model;
                        chatData.outputTokens += payload.count_tokens;
                        chatData.replyChars += Math.ceil(chatData.outputTokens*3.23);
                    }
                }
            }
        }
        return originalFetch(url, req);
    };
})(window.fetch);

// Observer updates accrual costs dynamically
let observer;
let lastObserve = Date.now();
const THROTTLE_TIME = 1000;
const chatContainer = document.querySelector('div[role="presentation"].flex.h-full.flex-col');

if (chatContainer) {
    observer = new MutationObserver((mutations) => {
        // Thottle observer to update between time intervals
        const now = Date.now();
        if (now - lastObserve > THROTTLE_TIME) {
            lastObserve = now;
            if (replyModel && chatData.inputTokens && chatData.outputTokens) {
                const cost = getCosts(replyModel, chatData.inputTokens, chatData.outputTokens);
                displayCost(cost);
            }
        }
    });
    observer.observe(chatContainer, { childList: true, subtree: true });
}

// Initialize cost display with history
createAndInjectUI();
displayCost(getStoredCosts());

// Observer + display removal on script is deactivation
window.addEventListener('unload', () => {
    if (observer) {
        observer.disconnect();
    }
    let costDisplay = document.getElementById('gpt-cost');
    if (costDisplay) costDisplay.remove();
});
