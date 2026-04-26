document.addEventListener('DOMContentLoaded', () => {
    const userSelect = document.getElementById('userSelect');
    const txBody = document.getElementById('txBody');
    const txCount = document.getElementById('txCount');
    const btnAnalyze = document.getElementById('btnAnalyze');
    const aiContent = document.getElementById('aiContent');
    const aiLoading = document.getElementById('aiLoading');
    const chatInputContainer = document.getElementById('chatInputContainer');
    const chatInput = document.getElementById('chatInput');
    const btnSendChat = document.getElementById('btnSendChat');

    let currentUser = null;
    let chatHistory = [];

    // Fetch users list
    fetch('/api/users')
        .then(res => res.json())
        .then(data => {
            userSelect.innerHTML = '<option value="">Selecciona un cliente...</option>';
            data.users.forEach(u => {
                const opt = document.createElement('option');
                opt.value = u.user_id;
                opt.textContent = u.user_id;
                userSelect.appendChild(opt);
            });
        })
        .catch(err => {
            console.error('Error fetching users:', err);
            userSelect.innerHTML = '<option value="">Error al cargar</option>';
        });

    // Handle user selection
    userSelect.addEventListener('change', async (e) => {
        const userId = e.target.value;
        if (!userId) {
            btnAnalyze.disabled = true;
            txBody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Selecciona un usuario para ver transacciones</td></tr>';
            txCount.textContent = '0 movimientos';
            resetAIPanel();
            return;
        }

        try {
            // Fetch Dashboard Data
            const res = await fetch(`/api/dashboard/${userId}`);
            const data = await res.json();
            
            currentUser = userId;
            btnAnalyze.disabled = false;
            resetAIPanel();

            // Populate Transactions (Only 3 columns now)
            txBody.innerHTML = '';
            if (data.transactions && data.transactions.length > 0) {
                txCount.textContent = `${data.transactions.length} movimientos`;
                data.transactions.forEach(tx => {
                    const tr = document.createElement('tr');
                    
                    const isIncome = tx.tipo_operacion && tx.tipo_operacion.match(/deposito|abono|ingreso/i);
                    const amountClass = isIncome ? 'positive' : 'negative';
                    const amountPrefix = isIncome ? '+' : '-';
                    
                    tr.innerHTML = `
                        <td>${tx.comercio_nombre || 'No especificado'}</td>
                        <td><span class="badge" style="background: rgba(0,0,0,0.05); padding: 4px 8px; border-radius: 4px; color: #4b5563; font-weight: 500;">${tx.categoria_mcc || '-'}</span></td>
                        <td class="text-right tx-amount ${amountClass}">${amountPrefix}$${parseFloat(tx.monto).toLocaleString('es-MX', {minimumFractionDigits: 2})}</td>
                    `;
                    txBody.appendChild(tr);
                });
            } else {
                txCount.textContent = '0 movimientos';
                txBody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">No hay transacciones recientes</td></tr>';
            }

        } catch (err) {
            console.error('Error loading dashboard:', err);
            alert('Error al cargar datos del usuario');
        }
    });

    // Handle AI Analysis
    btnAnalyze.addEventListener('click', async () => {
        if (!currentUser) return;
        
        btnAnalyze.disabled = true;
        aiContent.classList.add('hidden');
        aiLoading.classList.remove('hidden');
        chatInputContainer.classList.add('hidden');
        chatHistory = [];
        
        try {
            const res = await fetch(`/api/analyze/${currentUser}`, {
                method: 'POST'
            });
            const data = await res.json();
            
            aiLoading.classList.add('hidden');
            aiContent.classList.remove('hidden');
            
            let htmlContent = '';
            
            if (data.analysis) {
                const cleanText = data.analysis.replace(/```json/g, '').replace(/```/g, '').trim();
                
                try {
                    const parsed = JSON.parse(cleanText);
                    
                    // Initial bot prompt to save in history
                    chatHistory.push({ role: "assistant", content: cleanText });
                    
                    htmlContent = `
                        <div class="mockup-card">
                            <div class="mockup-header">
                                <div class="mockup-header-left">
                                    <div class="mockup-logo">HEY</div>
                                    <div class="mockup-title">
                                        <strong>Hey Banco</strong>
                                        <small>Hace un momento</small>
                                    </div>
                                </div>
                                <div class="mockup-pill-nuevo">NUEVO</div>
                            </div>
                            <div class="mockup-success">
                                <i class="fa-regular fa-circle-check"></i> ANÁLISIS COMPLETADO EXITOSAMENTE
                            </div>
                            <div class="mockup-body">
                                <div class="mockup-recommendation-label">
                                    RECOMENDACIÓN <span class="mockup-pill-yellow">${parsed.Decision || parsed.decision || 'Recomendación Hey'}</span>
                                </div>
                                <div class="mockup-message-box">
                                    ${parsed.Mensaje || parsed.mensaje || cleanText}
                                </div>
                                
                                <div class="mockup-why-title">¿POR QUÉ ESTA TARJETA?</div>
                                
                                <div class="mockup-reason-yellow">
                                    <div class="mockup-reason-icon-circle">!</div>
                                    <div>
                                        <strong>${parsed.Razon1_Titulo || 'Motivo Principal'}:</strong> ${parsed.Razon1_Desc || ''}
                                    </div>
                                </div>
                                
                                <div class="mockup-reason-blue">
                                    <div class="mockup-reason-icon-square"><i class="fa-solid fa-layer-group"></i></div>
                                    <div>
                                        <strong>${parsed.Razon2_Titulo || 'Perfil'}:</strong> ${parsed.Razon2_Desc || ''}
                                    </div>
                                </div>
                                
                                <div class="mockup-actions">
                                    <button class="mockup-btn-yellow">Ver detalles ↗</button>
                                    <button class="mockup-btn-black">Solicitar ↗</button>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    // Show chat input!
                    chatInputContainer.classList.remove('hidden');
                    
                } catch(e) {
                    htmlContent = `<div class="chat-message-ai"><i class="fa-solid fa-sparkles"></i>\n\n${cleanText}</div>`;
                }
            } else {
                htmlContent = `<div class="chat-message-ai" style="color: red">No se obtuvo respuesta del agente.</div>`;
            }
            
            aiContent.innerHTML = htmlContent;
            
        } catch (err) {
            console.error('Error in AI analysis:', err);
            aiLoading.classList.add('hidden');
            aiContent.classList.remove('hidden');
            aiContent.innerHTML = `<div class="chat-message-ai" style="color: red">Error al procesar con IA: ${err.message}</div>`;
            btnAnalyze.disabled = false;
        }
    });

    // Handle Chat Logic
    btnSendChat.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });

    async function sendChatMessage() {
        const msg = chatInput.value.trim();
        if (!msg || !currentUser) return;
        
        chatInput.value = '';
        
        // Append user message
        const userDiv = document.createElement('div');
        userDiv.className = 'chat-message-user';
        userDiv.textContent = msg;
        aiContent.appendChild(userDiv);
        aiContent.scrollTop = aiContent.scrollHeight;
        
        // Append loading message
        const loadDiv = document.createElement('div');
        loadDiv.className = 'chat-message-ai';
        loadDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
        aiContent.appendChild(loadDiv);
        aiContent.scrollTop = aiContent.scrollHeight;
        
        try {
            const res = await fetch(`/api/chat/${currentUser}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg, history: chatHistory })
            });
            const data = await res.json();
            
            // Remove loading
            aiContent.removeChild(loadDiv);
            
            // Append real AI response
            const aiDiv = document.createElement('div');
            aiDiv.className = 'chat-message-ai';
            aiDiv.innerHTML = marked.parse(data.reply);
            aiContent.appendChild(aiDiv);
            
            // Update history
            chatHistory.push({ role: 'user', content: msg });
            chatHistory.push({ role: 'assistant', content: data.reply });
            
            aiContent.scrollTop = aiContent.scrollHeight;
        } catch (err) {
            aiContent.removeChild(loadDiv);
            const errDiv = document.createElement('div');
            errDiv.className = 'chat-message-ai';
            errDiv.style.color = 'red';
            errDiv.textContent = `Error: ${err.message}`;
            aiContent.appendChild(errDiv);
        }
    }

    function resetAIPanel() {
        aiLoading.classList.add('hidden');
        aiContent.classList.remove('hidden');
        chatInputContainer.classList.add('hidden');
        aiContent.innerHTML = `
            <div class="empty-state">
                <div class="pulsing-circle">
                    <i class="fa-solid fa-robot"></i>
                </div>
                <p>La IA está lista para analizar los datos financieros de este usuario.</p>
                <p class="text-sm text-muted">Presiona "Analizar con IA" para comenzar.</p>
            </div>
        `;
    }
});
