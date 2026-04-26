document.addEventListener('DOMContentLoaded', () => {
    const userSelect = document.getElementById('userSelect');
    const profileCard = document.getElementById('profileCard');
    const txBody = document.getElementById('txBody');
    const txCount = document.getElementById('txCount');
    const btnAnalyze = document.getElementById('btnAnalyze');
    const aiContent = document.getElementById('aiContent');
    const aiLoading = document.getElementById('aiLoading');

    // DOM Elements for Profile
    const pUserId = document.getElementById('p_user_id');
    const pNeed = document.getElementById('p_need');
    const pSpecialist = document.getElementById('p_specialist');
    const pTags = document.getElementById('p_tags');

    let currentUser = null;

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
            profileCard.classList.add('hidden');
            btnAnalyze.disabled = true;
            txBody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Selecciona un usuario para ver transacciones</td></tr>';
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
            
            // Populate Profile
            profileCard.classList.remove('hidden');
            pUserId.textContent = data.profile.user_id;
            pNeed.textContent = data.profile.necesidad_principal || 'No definida';
            pSpecialist.textContent = data.profile.perfil_final_tda || 'Estándar';
            
            // Tags
            pTags.innerHTML = '';
            let tags = [];
            try {
                if (data.profile.tags_personalidad) {
                    // Extract tags if it's a string representation of a list
                    let tagsStr = data.profile.tags_personalidad.replace(/'/g, '"');
                    tags = JSON.parse(tagsStr);
                }
            } catch(e) {
                tags = [data.profile.tags_personalidad];
            }
            
            if(tags && tags.length > 0 && tags[0]) {
                tags.forEach(t => {
                    const span = document.createElement('span');
                    span.className = 'tag';
                    span.textContent = t;
                    pTags.appendChild(span);
                });
            } else {
                pTags.innerHTML = '<span class="text-muted text-sm">Sin tags</span>';
            }

            // Populate Transactions
            txBody.innerHTML = '';
            if (data.transactions && data.transactions.length > 0) {
                txCount.textContent = `${data.transactions.length} movimientos`;
                data.transactions.forEach(tx => {
                    const tr = document.createElement('tr');
                    
                    const isIncome = tx.tipo_operacion && tx.tipo_operacion.match(/deposito|abono|ingreso/i);
                    const amountClass = isIncome ? 'positive' : 'negative';
                    const amountPrefix = isIncome ? '+' : '-';
                    
                    tr.innerHTML = `
                        <td>${formatDate(tx.fecha_hora)}</td>
                        <td>${tx.comercio_nombre || 'No especificado'}</td>
                        <td><span class="badge" style="background: rgba(255,255,255,0.1); border:none; color:white;">${tx.categoria_mcc || '-'}</span></td>
                        <td>${tx.tipo_operacion || '-'}</td>
                        <td class="text-right tx-amount ${amountClass}">${amountPrefix}$${parseFloat(tx.monto).toLocaleString('es-MX', {minimumFractionDigits: 2})}</td>
                    `;
                    txBody.appendChild(tr);
                });
            } else {
                txCount.textContent = '0 movimientos';
                txBody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No hay transacciones recientes</td></tr>';
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
        
        try {
            const res = await fetch(`/api/analyze/${currentUser}`, {
                method: 'POST'
            });
            const data = await res.json();
            
            aiLoading.classList.add('hidden');
            aiContent.classList.remove('hidden');
            
            let htmlContent = '';
            
            // Si la respuesta es texto plano, la parseamos rudimentariamente o la mostramos como está
            if (data.analysis) {
                // Remove some markdown artifacts if present
                const cleanText = data.analysis.replace(/```json/g, '').replace(/```/g, '').trim();
                
                try {
                    // Si el agente retornó JSON válido, lo mostramos bonito
                    const parsed = JSON.parse(cleanText);
                    htmlContent = `
                        <div class="ai-response">
                            <h4 style="color: var(--accent); margin-bottom: 10px;">
                                <i class="fa-solid fa-lightbulb"></i> Recomendación: ${parsed.Decisión || parsed.decision || 'Acción Proactiva'}
                            </h4>
                            <p style="margin-bottom: 15px; font-size: 1.1rem;">"${parsed.Mensaje || parsed.mensaje}"</p>
                            <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; border-left: 3px solid var(--accent);">
                                <strong style="color: var(--text-secondary); font-size: 0.8rem; text-transform: uppercase;">Procedencia y Análisis:</strong><br/>
                                <span style="font-size: 0.9rem;">${parsed.Procedencia || parsed.procedencia || 'Análisis de transacciones y NLP'}</span>
                            </div>
                        </div>
                    `;
                } catch(e) {
                    // Mostrar como texto plano pero con estilo
                    htmlContent = `<div class="ai-response"><i class="fa-solid fa-sparkles text-accent"></i>\n\n${cleanText}</div>`;
                }
            } else {
                htmlContent = `<div class="ai-response" style="color: var(--danger)">No se obtuvo respuesta del agente.</div>`;
            }
            
            aiContent.innerHTML = htmlContent;
            
        } catch (err) {
            console.error('Error in AI analysis:', err);
            aiLoading.classList.add('hidden');
            aiContent.classList.remove('hidden');
            aiContent.innerHTML = `<div class="ai-response" style="color: var(--danger)">Error al procesar con IA: ${err.message}</div>`;
            btnAnalyze.disabled = false;
        }
    });

    function resetAIPanel() {
        aiLoading.classList.add('hidden');
        aiContent.classList.remove('hidden');
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

    function formatDate(dateStr) {
        if (!dateStr) return '-';
        try {
            const d = new Date(dateStr);
            return d.toLocaleDateString('es-MX', { month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' });
        } catch(e) {
            return dateStr;
        }
    }
});
