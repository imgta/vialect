
// Global variables to store chat session data
const queryUrl = 'https://chat.openai.com/backend-api/conversation';
const replyUrl = 'https://chat.openai.com/backend-api/lat/r';
let queryModel = '';
let replyModel = '';
let chatData = {
    queryChars: 0,
    inputTokens: 0,
    replyChars: 0,
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
// Display estimated costs on page
function displayCost(cost) {
    let costDisplay = document.getElementById('gpt-cost-estimator');
    if (!costDisplay) {
        costDisplay = document.createElement('div');
        costDisplay.id = 'gpt-cost-estimator';
        // Display styling
        Object.assign(costDisplay.style, {
            position: 'fixed', bottom: '10px', right: '10px',
            backgroundColor: 'rgba(32,33,35,0.85)', padding: '10px',
            borderRadius: '5px', boxShadow: '0 0 5px rgba(0,0,0,0.5)'
        });
        document.body.appendChild(costDisplay);
    }
    costDisplay.textContent = `Accrued Costs: $${cost.toFixed(7)}`;
}
// Override window.fetch function to intercept ChatGPT POST request
(function(originalFetch) {
    window.fetch = function(url, req) {
        if (req && req.method === 'POST') {
            if (url.includes(queryUrl)) {
                try {
                    const payload = JSON.parse(req.body);
                    queryModel = payload.model;
                    chatData.queryChars += payload.messages[0].content.parts[0].length;
                    chatData.inputTokens += Math.ceil(chatData.queryChars/3.23);
                } catch (error) {
                    console.error(error);
                }
            }
            if (url.includes(replyUrl)) {
                try {
                    const payload = JSON.parse(req.body);
                    replyModel = payload.model;
                    chatData.outputTokens += payload.count_tokens;
                    chatData.replyChars += Math.ceil(chatData.outputTokens*3.23);
                } catch (error) {
                    console.error(error);
                }
            }
        }
        return originalFetch(url, req);
    };
})(window.fetch);
// Update accrual costs in display dynamically
const observer = new MutationObserver(() => {
    if (replyModel && chatData.inputTokens && chatData.outputTokens) {
        const cost = getCosts(replyModel, chatData.inputTokens, chatData.outputTokens);
        displayCost(cost);
    }
});
// Initiate document observations
observer.observe(document, { childList: true, subtree: true });
// Observer + display removal on script is deactivation
window.addEventListener('unload', () => {
    observer.disconnect();
    let costDisplay = document.getElementById('gpt-cost-estimator');
    if (costDisplay) costDisplay.remove();
});
