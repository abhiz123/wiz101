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

function initiateCast(cardId, cardName) {
    if(!gameState) return;
    const activeP = gameState.turn === gameState.p1.name ? gameState.p1 : gameState.p2;
    if(!activeP.has_drawn_pip) {
        alert("You must draw a pip first!"); return;
    }
    if(activeP.has_cast) {
        alert("You already cast this turn!"); return;
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
        if (!lastLog.includes('Fizzle') && lastLog.includes('damage')) {
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
        statusContainer.innerHTML += `<div class="status-badge ward">${w.name}</div>`;
    });
    p.charms.forEach(c => {
        statusContainer.innerHTML += `<div class="status-badge charm">${c.name}</div>`;
    });

    // Pips
    const pipsContainer = document.getElementById(`${containerPrefix}-pips`);
    pipsContainer.innerHTML = '';
    p.pips.forEach(pipType => {
        pipsContainer.innerHTML += `<div class="pip ${pipType}">${pipType[0]}</div>`;
    });

    // Hand
    const handContainer = document.getElementById(`${containerPrefix}-hand`);
    handContainer.innerHTML = '';
    p.hand.forEach(c => {
        // Evaluate if playable
        let disabledClass = (!isActive || !p.has_drawn_pip || p.has_cast) ? 'disabled' : '';
        // Frontend logic check (simplified, relies on backend constraint to block)
        let imgHtml = '';
        if(isOpponent) {
             imgHtml = `<img src="/static/cards/Center%20card%20Back%20Final.png" class="card" alt="hidden card">`;
        } else {
             imgHtml = `<img src="/static/cards/${c.image}" class="card ${disabledClass}" onclick="initiateCast('${c.id}', '${c.name}')" title="Cost: ${c.cost}">`;
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
