let gameState = null;
let currentCastingCard = null;

async function fetchState() {
    const res = await fetch('/api/state');
    gameState = await res.json();
    render();
}

async function sendAction(action, extraData = {}) {
    const payload = { action, player: gameState.turn, ...extraData };
    const res = await fetch('/api/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await res.json();
    if(data.success && data.state) {
        gameState = data.state;
        render();
    } else {
        alert(data.error || "Action failed");
    }
}

function drawPip() { sendAction('draw_pip'); }
function passTurn() { sendAction('pass_turn'); }
function resetGame() { sendAction('reset'); location.reload(); }

function canCastCard(player, card) {
    const cost = card.cost;
    if (card.school === 'Shadow') {
        return player.pips.filter(p => p === 'Shadow').length >= cost;
    }
    const powerPips  = player.pips.filter(p => p === 'Power').length;
    const schoolPips = player.pips.filter(p => p === player.school).length;
    const normalPips = player.pips.filter(p => p === 'Normal').length;
    const powerValuePips = powerPips + schoolPips;
    if (player.school === card.school) {
        return powerValuePips * 2 + normalPips >= cost;
    } else {
        return schoolPips * 2 + powerPips + normalPips >= cost;
    }
}

function initiateCast(cardId, cardName) {
    if(!gameState) return;
    const isP1Turn = gameState.turn === gameState.p1.name;
    const activeP = isP1Turn ? gameState.p1 : gameState.p2;
    if(!activeP.has_drawn_pip) {
        alert("You must draw a pip first!"); return;
    }
    if(activeP.has_cast) {
        alert("You already cast this turn!"); return;
    }

    // Update modal target button labels to show actual player names
    const selfBtn = document.getElementById('btn-target-self');
    const oppBtn  = document.getElementById('btn-target-opp');
    if (isP1Turn) {
        selfBtn.textContent = `Self (${gameState.p1.name})`;
        selfBtn.onclick = () => confirmCast('p1');
        oppBtn.textContent  = `Opponent (${gameState.p2.name})`;
        oppBtn.onclick = () => confirmCast('p2');
    } else {
        selfBtn.textContent = `Opponent (${gameState.p1.name})`;
        selfBtn.onclick = () => confirmCast('p1');
        oppBtn.textContent  = `Self (${gameState.p2.name})`;
        oppBtn.onclick = () => confirmCast('p2');
    }

    currentCastingCard = cardId;
    document.getElementById('spell-name-display').innerText = cardName;
    document.getElementById('cast-modal').classList.remove('hidden');
}

async function confirmCast(targetId) {
    const targetName = targetId === 'p1' ? gameState.p1.name : gameState.p2.name;
    document.getElementById('cast-modal').classList.add('hidden');
    
    // Custom inline fetch to trigger animations immediately on cast success
    const payload = { action: 'cast_spell', player: gameState.turn, card_id: currentCastingCard, target_name: targetName };
    const res = await fetch('/api/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    
    const data = await res.json();
    if(data.success && data.state) {
        // Did we fizzle? Look at the newest log
        const newLogs = data.state.logs;
        const lastLog = newLogs[newLogs.length - 1] || "";
        const didDamage = newLogs.some(log => log.includes('damage'));
        if (!lastLog.includes('Fizzle') && didDamage) {
            // Trigger Hit Animation
            const targetArea = document.getElementById(`${targetId}-area`);
            targetArea.classList.add('hit-anim');
            setTimeout(() => targetArea.classList.remove('hit-anim'), 500);
        } else if (lastLog.includes('Fizzle')) {
            alert('Your spell fizzled!');
        }

        gameState = data.state;
        render();
    } else {
        alert(data.error || "Not enough pips to cast this spell!");
    }

    currentCastingCard = null;
}

function closeModal() {
    document.getElementById('cast-modal').classList.add('hidden');
    currentCastingCard = null;
}

function renderPlayer(p, containerPrefix, isOpponent) {
    const isActive = gameState.turn === p.name;
    const area = document.getElementById(`${containerPrefix}-area`);
    if(isActive) area.classList.add('active-turn');
    else area.classList.remove('active-turn');

    document.getElementById(`${containerPrefix}-name`).innerText = p.name;
    
    // Health
    const pct = Math.max(0, (p.health / p.max_health) * 100);
    document.getElementById(`${containerPrefix}-health-fill`).style.width = `${pct}%`;
    document.getElementById(`${containerPrefix}-health-text`).innerText = `${p.health} / ${p.max_health}`;

    // Status FX
    const statusContainer = document.getElementById(`${containerPrefix}-status`);
    statusContainer.innerHTML = '';
    p.dots.forEach(d => {
        statusContainer.innerHTML += `<div class="status-badge dot">${d.name} (${d.damage}/R)</div>`;
    });
    p.wards.forEach(w => {
        const schoolClass = 'ward-' + w.school.toLowerCase();
        let label = w.name;
        if (w.type === 'shield')                                     label += ` (-${w.value})`;
        else if (w.type === 'trap_flat' || w.type === 'trap_fixed') label += ` (+${w.value})`;
        statusContainer.innerHTML += `<div class="status-badge ward ${schoolClass}">${label}</div>`;
    });
    p.charms.forEach(c => {
        const schoolClass = 'charm-' + c.school.toLowerCase();
        let label = c.name;
        if (c.type === 'blade_flat' || c.type === 'blade_fixed') label += ` (+${c.value})`;
        else if (c.type === 'weakness') label += ` (x${c.value})`;
        statusContainer.innerHTML += `<div class="status-badge charm ${schoolClass}">${label}</div>`;
    });

    // Pips
    const pipsContainer = document.getElementById(`${containerPrefix}-pips`);
    pipsContainer.innerHTML = '';
    const pipLabel = { Normal:'N', Power:'PP', Shadow:'Sh', Fizzle:'Fz', Critical:'★',
                       Fire:'🔥', Death:'💀', Life:'🌿', Ice:'❄', Storm:'⚡', Myth:'🔮', Balance:'⚖' };
    p.pips.forEach(pipType => {
        const label = pipLabel[pipType] || pipType[0];
        pipsContainer.innerHTML += `<div class="pip ${pipType}" title="${pipType}">${label}</div>`;
    });

    // Hand
    const handContainer = document.getElementById(`${containerPrefix}-hand`);
    handContainer.innerHTML = '';
    p.hand.forEach(c => {
        // Card is playable only if: it's your turn, pip drawn, not yet cast, and you can afford it
        const globallyBlocked = !isActive || !p.has_drawn_pip || p.has_cast;
        const affordable = canCastCard(p, c);
        const disabledClass = (globallyBlocked || !affordable) ? 'disabled' : '';
        let imgHtml = '';
        if(isOpponent) {
             imgHtml = `<img src="/static/cards/Center%20card%20Back%20Final.png" class="card" alt="hidden card">`;
        } else {
             imgHtml = `<img src="/static/cards/${c.image}" class="card ${disabledClass}" onclick="initiateCast('${c.id}', '${c.name}')" title="Cost: ${c.cost} | ${c.school}">`;
        }
        handContainer.innerHTML += imgHtml;
    });
}

function render() {
    if(!gameState) return;
    if(gameState.game_over) {
        document.getElementById('current-turn').innerText = "GAME OVER";
    } else {
        document.getElementById('current-turn').innerText = `${gameState.turn}'s Turn (R${gameState.round})`;
    }

    document.getElementById('bag-count').innerText = `Pips: ${gameState.bag_count}`;
    
    // Render P1 (Bottom, always visible hand)
    renderPlayer(gameState.p1, 'p1', false);
    
    // Render P2 (Top. Need a way to show their hand? For local 2P pass-and-play, maybe we reveal both?
    // The prompt says "playable 2-player local web application". Let's reveal both hands for testing.)
    renderPlayer(gameState.p2, 'p2', false); // changed isOpponent to false for Local 2P
    
    // Disable buttons if not P1 turn (for demo, assume we just pass mouse or click around)
    // Actually since we turned off isOpponent=true, let's keep controls enabled for whoever the active player's screen side is.
    const activeP = gameState.turn === gameState.p1.name ? gameState.p1 : gameState.p2;
    document.getElementById('btn-draw').disabled = activeP.has_drawn_pip || gameState.game_over;
    document.getElementById('btn-pass').disabled = gameState.game_over;

    const logList = document.getElementById('log-list');
    logList.innerHTML = '';
    [...gameState.logs].reverse().forEach(logLine => {
        logList.innerHTML += `<li>${logLine}</li>`;
    });
}

// Init
setInterval(fetchState, 2000); // Poll explicitly if you play in two tabs
fetchState();
