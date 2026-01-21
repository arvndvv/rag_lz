document.addEventListener('DOMContentLoaded', () => {
    // Connect to Socket.IO
    const socket = io();
    const logContainer = document.getElementById('log-container');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    // Tabs
    const tabLogs = document.getElementById('tab-logs');
    const tabHistory = document.getElementById('tab-history');
    const historyContainer = document.getElementById('history-container');

    tabLogs.addEventListener('click', () => {
        tabLogs.classList.add('active');
        tabHistory.classList.remove('active');
        logContainer.classList.remove('hidden');
        historyContainer.classList.add('hidden');
    });

    tabHistory.addEventListener('click', () => {
        tabHistory.classList.add('active');
        tabLogs.classList.remove('active');
        historyContainer.classList.remove('hidden');
        logContainer.classList.add('hidden');
        loadHistory();
    });

    async function loadHistory() {
        historyContainer.innerHTML = '<div class="log-entry system">Loading history...</div>';
        try {
            const res = await fetch('/history');
            const history = await res.json();

            historyContainer.innerHTML = '';
            if (history.length === 0) {
                historyContainer.innerHTML = '<div class="log-entry system">No history found.</div>';
                return;
            }

            history.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'history-item';
                itemDiv.innerHTML = `
                    <div class="history-question">${item.question}</div>
                    <div class="history-date">${new Date(item.timestamp).toLocaleString()}</div>
                `;
                itemDiv.addEventListener('click', () => loadHistoryDetails(item.id));
                historyContainer.appendChild(itemDiv);
            });
        } catch (e) {
            historyContainer.innerHTML = `<div class="log-entry ERROR">Error loading history: ${e.message}</div>`;
        }
    }

    async function loadHistoryDetails(id) {
        try {
            const res = await fetch(`/history/${id}`);
            const data = await res.json();

            if (data.error) {
                alert(data.error);
                return;
            }

            // Clear chat and show history
            chatMessages.innerHTML = '';

            // Add a separator or indicator
            const refDiv = document.createElement('div');
            refDiv.style.textAlign = 'center';
            refDiv.style.color = '#888';
            refDiv.style.margin = '10px 0';
            refDiv.innerText = `Viewing History: ${new Date(data.timestamp).toLocaleString()}`;
            chatMessages.appendChild(refDiv);

            addMessage(data.question, 'user');
            addMessage(data.answer, 'bot');

            // Show Context if available
            if (data.context) {
                const contextDiv = document.createElement('div');
                contextDiv.className = 'context-container';

                const toggleBtn = document.createElement('button');
                toggleBtn.textContent = 'Show Context';
                toggleBtn.className = 'toggle-context-btn';

                const contentPre = document.createElement('pre');
                contentPre.className = 'context-content hidden';
                contentPre.textContent = data.context;

                toggleBtn.addEventListener('click', () => {
                    if (contentPre.classList.contains('hidden')) {
                        contentPre.classList.remove('hidden');
                        toggleBtn.textContent = 'Hide Context';
                    } else {
                        contentPre.classList.add('hidden');
                        toggleBtn.textContent = 'Show Context';
                    }
                });

                contextDiv.appendChild(toggleBtn);
                contextDiv.appendChild(contentPre);
                chatMessages.appendChild(contextDiv);
            }

            // Show logs
            logContainer.innerHTML = '';
            if (data.logs) {
                const logs = data.logs.split('\n');
                logs.forEach(logLine => {
                    if (!logLine.trim()) return;
                    const entry = document.createElement('div');
                    entry.className = 'log-entry';
                    if (logLine.includes('ERROR')) entry.classList.add('ERROR');
                    else if (logLine.includes('WARNING')) entry.classList.add('WARNING');
                    else entry.classList.add('INFO');
                    entry.textContent = logLine;
                    logContainer.appendChild(entry);
                });
            } else {
                logContainer.innerHTML = '<div class="log-entry system">No logs recorded for this session.</div>';
            }

            // Switch to Logs tab to see the logs
            tabLogs.click();

        } catch (e) {
            console.error(e);
            alert('Error loading details');
        }
    }

    // Handle WebSocket Logs
    socket.on('log_message', (msg) => {
        const entry = document.createElement('div');
        entry.className = 'log-entry';

        // Simple heuristic for log level styling
        if (msg.data.includes('ERROR')) entry.classList.add('ERROR');
        else if (msg.data.includes('WARNING')) entry.classList.add('WARNING');
        else entry.classList.add('INFO');

        entry.textContent = msg.data;
        logContainer.appendChild(entry);

        // Auto-scroll
        logContainer.scrollTop = logContainer.scrollHeight;
    });

    // Handle Chat Submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (!text) return;

        // Add user message to UI
        addMessage(text, 'user');
        userInput.value = '';

        // Disable input while processing
        const button = chatForm.querySelector('button');
        button.disabled = true;

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 480000); // 8 minutes timeout

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: text }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            const data = await response.json();

            if (data.error) {
                addMessage('Error: ' + data.error, 'bot');
            } else {
                addMessage(data.response, 'bot');
            }
        } catch (error) {
            addMessage('Network Error: ' + error.message, 'bot');
        } finally {
            button.disabled = false;
        }
    });

    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // Simple markdown-ish to html replacement for newlines
        // For full markdown we'd use a library, but basic whitespace is key
        contentDiv.innerHTML = text.replace(/\n/g, '<br>');

        msgDiv.appendChild(contentDiv);
        chatMessages.appendChild(msgDiv);

        // Auto-scroll
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
