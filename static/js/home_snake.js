// File: home_snake.js
// Author: Dawson Maska (dawsonwm@bu.edu), 11/20/2025
// Description: JS code to implement snake navigation on the home page.

// ===== Canvas Setup =====
const canvas = document.getElementById("snakeCanvas");
const ctx = canvas.getContext("2d");

// Grid size (square grid)
const gridCols = 50;  // number of cells horizontally (1000 / 20)
const gridRows = 30;  // number of cells vertically   (600 / 20)
let cellSize;
let offsetX = 0;
let offsetY = 0;

// ===== Handle canvas resize =====
function resizeCanvas() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    // Guarantee square cells based on fixed ratio grid
    cellSize = Math.min(
        canvas.width / gridCols,
        canvas.height / gridRows
    );

    const gridPixelWidth = cellSize * gridCols;
    const gridPixelHeight = cellSize * gridRows;

    // Make sure snake properly wraps around when going through side of screen
    offsetX = (canvas.width - gridPixelWidth) / 2;
    offsetY = (canvas.height - gridPixelHeight) / 2;
}

resizeCanvas();
window.addEventListener("resize", resizeCanvas);

// ===== Snake (3 segments on nav screen) =====
let snake = [
    { x: 12, y: 12 },
    { x: 11, y: 12 },
    { x: 10, y: 12 },
];

let dx = 1;
let dy = 0;

// ===== Input =====
document.addEventListener("keydown", e => {
    if (e.key === "ArrowUp" || e.key === "w") { dx = 0; dy = -1; }
    if (e.key === "ArrowDown" || e.key === "s") { dx = 0; dy = 1; }
    if (e.key === "ArrowLeft" || e.key === "a") { dx = -1; dy = 0; }
    if (e.key === "ArrowRight" || e.key === "d") { dx = 1; dy = 0; }
});

// ===== Update Snake =====
function update() {
    const head = snake[0];
    const newHead = { x: head.x + dx, y: head.y + dy };

    // Wraparound
    if (newHead.x < 0) newHead.x = gridCols - 1;
    if (newHead.x >= gridCols) newHead.x = 0;
    if (newHead.y < 0) newHead.y = gridRows - 1;
    if (newHead.y >= gridRows) newHead.y = 0;

    snake.unshift(newHead);
    snake = snake.slice(0, 3);  // Keep only 3 segments
}

// ===== Draw Snake =====
function draw() {
    ctx.fillStyle = "#111";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "lime";
    for (let seg of snake) {
        ctx.fillRect(
            offsetX + seg.x * cellSize,
            offsetY + seg.y * cellSize,
            cellSize,
            cellSize
        );
    }
}

// ===== Navigation collision =====
function checkNavigation() {
    const head = snake[0];

    const headPxX = offsetX + head.x * cellSize + cellSize / 2;
    const headPxY = offsetY + head.y * cellSize + cellSize / 2;

    const zones = [
        { id: "zone-bots", url: "/test/bots/" },
        { id: "zone-boards", url: "/test/boards/" },
        { id: "zone-matches", url: "/test/matches/" },
        { id: "zone-leaderboard", url: "/test/leaderboard/" }
    ];

    for (let z of zones) {
        const elem = document.getElementById(z.id);
        if (!elem) continue;

        const rect = elem.getBoundingClientRect();
        const canvasRect = canvas.getBoundingClientRect();

        const px = canvasRect.left + headPxX;
        const py = canvasRect.top + headPxY;

        if (px >= rect.left && px <= rect.right &&
            py >= rect.top && py <= rect.bottom) {
            window.location.href = z.url;
        }
    }
}

// ===== Game Loop =====
function loop() {
    update();
    draw();
    checkNavigation();
    setTimeout(loop, 120);
}

loop();
