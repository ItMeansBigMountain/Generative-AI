// Constants
const WELCOME_MESSAGE = `
=================================
   SURVIVAL ASSISTANT ACTIVATED   
=================================
Welcome! I'm your offline survival companion.
Type /help to see available commands.
What's your situation?`;

// DOM Elements
const output = document.getElementById('output');
const input = document.getElementById('input');
const send = document.getElementById('send');
let isTyping = false;

// Text Animation
async function typeWriter(text, element, speed = 30) {
    isTyping = true;
    let i = 0;
    element.style.opacity = '1';
    
    return new Promise(resolve => {
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            } else {
                isTyping = false;
                resolve();
            }
        }
        type();
    });
}

// Message Display
function addToOutput(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = isUser ? 'user-message' : 'assistant-message';
    output.appendChild(messageDiv);
    
    if (isUser) {
        messageDiv.textContent = text;
    } else {
        typeWriter(text, messageDiv);
    }
    
    output.scrollTop = output.scrollHeight;
}

// Command Handler
async function handleCommand(command) {
    switch(command.toLowerCase()) {
        case '/help':
            addToOutput(`Available Commands:
/help   - Show this help message
/reset  - Reset conversation
/clear  - Clear screen
/status - Show system status`);
            return true;
        case '/clear':
            output.innerHTML = '';
            addToOutput('Screen cleared.');
            return true;
        case '/status':
            addToOutput(`System Status:
- Battery: 100%
- Storage: Available
- LLM Status: Connected
- Emergency Mode: Ready`);
            return true;
        default:
            return false;
    }
}

// Query Handler
async function sendQuery() {
    if (isTyping) return;
    
    const query = input.value.trim();
    if (!query) return;

    addToOutput(query, true);
    input.value = '';

    if (await handleCommand(query)) return;

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({prompt: query})
        });
        const data = await response.json();
        addToOutput(data.response);
    } catch (error) {
        addToOutput('Error: ' + error);
    }
}

// Event Listeners
send.addEventListener('click', sendQuery);
input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !isTyping) sendQuery();
});

// Initialize
window.addEventListener('load', () => {
    addToOutput(WELCOME_MESSAGE);
});
