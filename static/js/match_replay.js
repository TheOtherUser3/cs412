// File: match_replay.js
// Author: Dawson Maska (dawsonwm@bu.edu), 12/8/2025
// Description: JS code to implement the match replay rendering.

(function () {
    const canvas = document.getElementById("replayCanvas");
    // Safety first
    if (!canvas) return;  

    const ctx = canvas.getContext("2d");

    const playBtn = document.getElementById("playBtn");
    const pauseBtn = document.getElementById("pauseBtn");
    const speedButtons = document.querySelectorAll(".speed-btn");

    const turnCounterEl = document.getElementById("turnCounter");
    const scoreBot1El = document.getElementById("scoreBot1");
    const scoreBot2El = document.getElementById("scoreBot2");

    const BASE_INTERVAL = 100; // ms at 1x speed

    let moves = [];
    let currentIndex = 0;
    let playing = false;
    let speed = 1;
    let timerId = null;

    let scoreBot1 = 0;
    let scoreBot2 = 0;

    // Cell sizes based on board dimensions and canvas size
    const cellWidth = canvas.width / BOARD_WIDTH;
    const cellHeight = canvas.height / BOARD_HEIGHT;

    // load move events from API

    async function loadMoves() {
        try {
            const response = await fetch(MOVE_EVENTS_API_URL);
            if (!response.ok) {
                console.error("Failed to load move events:", response.status);
                return;
            }

            const data = await response.json();
            // Safely process API response
            moves = Array.isArray(data) ? data : data.results;

            if (!Array.isArray(moves) || moves.length === 0) {
                console.warn("No moves found for this match.");
                drawEmpty();
                return;
            }

            // Initialize UI to move 0
            currentIndex = 0;
            scoreBot1 = 0;
            scoreBot2 = 0;
            renderMove(moves[0], true);
            updateUI(moves[0]);
        } catch (err) {
            console.error("Error fetching move events:", err);
        }
    }

    // Drawing helpers

    function clearCanvas() {
        ctx.fillStyle = "#050b08";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function drawGrid() {
        ctx.strokeStyle = "rgba(255,255,255,0.03)";
        ctx.lineWidth = 1;

        for (let x = 0; x <= BOARD_WIDTH; x++) {
            const px = x * cellWidth;
            ctx.beginPath();
            ctx.moveTo(px, 0);
            ctx.lineTo(px, canvas.height);
            ctx.stroke();
        }

        for (let y = 0; y <= BOARD_HEIGHT; y++) {
            const py = y * cellHeight;
            ctx.beginPath();
            ctx.moveTo(0, py);
            ctx.lineTo(canvas.width, py);
            ctx.stroke();
        }
    }

    function drawObstacles() {
        if (!Array.isArray(BOARD_OBSTACLES)) return;
        ctx.fillStyle = "#243326";

        for (const [x, y] of BOARD_OBSTACLES) {
            ctx.fillRect(
                x * cellWidth,
                y * cellHeight,
                cellWidth,
                cellHeight
            );
        }
    }

    function drawApples(apples) {
        if (!Array.isArray(apples)) return;
        ctx.fillStyle = "#e74c3c";

        for (const [x, y] of apples) {
            const paddingX = cellWidth * 0.15;
            const paddingY = cellHeight * 0.15;
            ctx.fillRect(
                x * cellWidth + paddingX,
                y * cellHeight + paddingY,
                cellWidth - 2 * paddingX,
                cellHeight - 2 * paddingY
            );
        }
    }

    function drawSnake(body, color) {
        if (!body || body.length === 0) return;

        for (let i = 0; i < body.length; i++) {
            const seg = body[i];

            const x = Array.isArray(seg) ? seg[0] : seg.x;
            const y = Array.isArray(seg) ? seg[1] : seg.y;

            // Draw the segment
            ctx.fillStyle = color;
            ctx.fillRect(
                x * cellWidth,
                y * cellHeight,
                cellWidth,
                cellHeight
            );

            // If this is the head (index 0), draw eyes
            if (i === 0) {
                const eyeSize = Math.min(cellWidth, cellHeight) * 0.15;
                const eyeOffsetX = cellWidth * 0.2;
                const eyeOffsetY = cellHeight * 0.2;

                ctx.fillStyle = "#000000";

                // Left eye
                ctx.fillRect(
                    x * cellWidth + eyeOffsetX,
                    y * cellHeight + eyeOffsetY,
                    eyeSize,
                    eyeSize
                );

                // Right eye
                ctx.fillRect(
                    x * cellWidth + cellWidth - eyeOffsetX - eyeSize,
                    y * cellHeight + eyeOffsetY,
                    eyeSize,
                    eyeSize
                );
            }
        }
    }


    function drawEmpty() {
        clearCanvas();
        drawGrid();
        drawObstacles();
    }

    // render a single move 

    function renderMove(move, resetScores = false) {
        if (resetScores) {
            scoreBot1 = 0;
            scoreBot2 = 0;
            // recompute from start if needed later
        }

        clearCanvas();
        drawGrid();
        drawObstacles();
        drawApples(move.apple_positions || move.apples || []);

    
        drawSnake(move.bot1_body, BOT1_COLOR);
        drawSnake(move.bot2_body, BOT2_COLOR);
    }

    // UI + playback control 

    function updateUI(move) {
        // Turn
        turnCounterEl.textContent = move.move_number ?? currentIndex;

        // Score (incrementally)
        if (move.bot1_ate) scoreBot1 += 1;
        if (move.bot2_ate) scoreBot2 += 1;

        scoreBot1El.textContent = scoreBot1;
        scoreBot2El.textContent = scoreBot2;
    }

    function setSpeed(newSpeed) {
        speed = newSpeed;
        speedButtons.forEach(btn => {
            btn.classList.toggle(
                "active",
                Number(btn.dataset.speed) === speed
            );
        });

        // If we’re already playing, restart the timer with new speed
        if (playing) {
            if (timerId) clearTimeout(timerId);
            scheduleNextFrame();
        }
    }

    function scheduleNextFrame() {
        if (!playing) return;

        if (!moves || moves.length === 0) return;
        if (currentIndex >= moves.length) {
            // Stop at the end for now
            playing = false;
            return;
        }

        const move = moves[currentIndex];
        renderMove(move);
        updateUI(move);

        currentIndex += 1;

        timerId = setTimeout(
            scheduleNextFrame,
            BASE_INTERVAL / speed
        );
    }

    function play() {
        if (!moves || moves.length === 0) return;
        if (playing) return;

        // If we reached the end, restart
        if (currentIndex >= moves.length) {
            currentIndex = 0;
            scoreBot1 = 0;
            scoreBot2 = 0;
        }

        playing = true;
        scheduleNextFrame();
    }

    function pause() {
        playing = false;
        if (timerId) {
            clearTimeout(timerId);
            timerId = null;
        }
    }

    // Event wiring 

    if (playBtn) {
        playBtn.addEventListener("click", () => {
            play();
        });
    }

    if (pauseBtn) {
        pauseBtn.addEventListener("click", () => {
            pause();
        });
    }

    speedButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const value = Number(btn.dataset.speed || "1");
            setSpeed(value);
        });
    });

    // launch the replay
    loadMoves();
})();

