document.addEventListener('DOMContentLoaded', () => {
    const boardDiv = document.getElementById('board');
    const statusDiv = document.getElementById('status');
    const newGameBtn = document.getElementById('new-game-btn');

    let gameActive = false;

    // Create board cells
    for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.addEventListener('click', handleCellClick);
            boardDiv.appendChild(cell);
        }
    }

    newGameBtn.addEventListener('click', startNewGame);

    async function startNewGame() {
        gameActive = true;
        const response = await fetch('/start', { method: 'POST' });
        const data = await response.json();
        updateBoard(data.board);
        statusDiv.textContent = data.status;
    }

    async function handleCellClick(event) {
        if (!gameActive) return;

        const cell = event.target;
        // Prevent move if cell is already taken
        if (cell.textContent !== '') return;

        const row = cell.dataset.row;
        const col = cell.dataset.col;

        const response = await fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ row, col }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            statusDiv.textContent = errorData.error || 'An error occurred.';
            return;
        }
        
        const data = await response.json();
        updateBoard(data.board);
        statusDiv.textContent = data.status;

        if (data.game_over) {
            gameActive = false;
        }
    }

    function updateBoard(boardState) {
        const cells = document.querySelectorAll('.cell');
        cells.forEach(cell => {
            const row = cell.dataset.row;
            const col = cell.dataset.col;
            const symbol = boardState[row][col].trim(); // trim whitespace
            cell.textContent = symbol;
            cell.classList.remove('X', 'O');
            if (symbol) {
                cell.classList.add(symbol);
            }
        });
    }
});