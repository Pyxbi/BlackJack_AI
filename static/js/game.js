class BlackjackGame {
    constructor() {
        this.gameState = {
            player_hand: [],
            dealer_hand: [],
            player_value: 0,
            dealer_value: '?',
            game_state: 'waiting',
            result: '',
            player_balance: 1000,
            player_bet:0
        };
        this.initializeElements();
        this.bindEvents();
        this.updateUI();
    }

    initializeElements() {
        this.elements = {
            dealBtn: document.getElementById('deal-btn'),
            hitBtn: document.getElementById('hit-btn'),
            standBtn: document.getElementById('stand-btn'),
            newGameBtn: document.getElementById('new-game-btn'),
            playerCards: document.getElementById('player-cards'),
            dealerCards: document.getElementById('dealer-cards'),
            playerValue: document.getElementById('player-value'),
            dealerValue: document.getElementById('dealer-value'),
            balance: document.getElementById('balance'),
            bet: document.getElementById('bet'),
            statusMessage: document.getElementById('status-message'),
            resultMessage: document.getElementById('result-message'),
            betInput: document.getElementById('bet-input'),
            rulesBtn: document.getElementById('rules-btn'),
            rulesModal: document.getElementById('rules-modal'),
            closeRules: document.getElementById('close-rules')
        };
    }

    bindEvents() {
        this.elements.dealBtn.addEventListener('click', () => this.startGame());
        this.elements.hitBtn.addEventListener('click', () => this.hit());
        this.elements.standBtn.addEventListener('click', () => this.stand());
        this.elements.newGameBtn.addEventListener('click', () => {
            this.clearMessages();
            this.startGame();
        });
        this.elements.betInput.addEventListener('input', (e) => this.handleBetInput(e));
        this.elements.rulesBtn.addEventListener('click', () => this.openRulesModal());
        this.elements.closeRules.addEventListener('click', () => this.closeRulesModal());
        window.addEventListener('click', (e) => {
            if (e.target === this.elements.rulesModal) this.closeRulesModal();
        });
    }

    handleBetInput(e) {
        const value = parseInt(e.target.value, 10);
        if (!isNaN(value)) {
            this.bet = value;
        } else {
            this.bet = 0;
        }
    }

    async startGame() {
        const betInputValue = parseInt(this.elements.betInput.value, 10);
        const balanceText = this.elements.balance.textContent.replace(/\$/g, '');
        const balance = parseInt(balanceText, 10);
    
        if (isNaN(betInputValue) || betInputValue <= 0) {
            this.elements.statusMessage.textContent = 'Please enter a valid bet.';
            return;
        }
    
        if (betInputValue > balance) {
            this.elements.statusMessage.textContent = 'Bet must be less than or equal to your balance!';
            return;
        }
        this.elements.playerValue.classList.remove('hidden');

    
        try {
            const response = await fetch('/api/start_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ bet: betInputValue })
            });
    
            if (response.ok) {
                this.gameState = await response.json();
                this.updateUI();
                this.elements.statusMessage.textContent = 'Game started! Your turn to hit or stand.';
            }
        } catch (error) {
            console.error('Error starting game:', error);
            this.elements.statusMessage.textContent = 'Error starting game. Please try again.';
        }
    }
    

    async hit() {
        try {
            const response = await fetch('/api/hit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.ok) {
                this.gameState = await response.json();
                this.updateUI();
                if (this.gameState.game_state === 'game_over') {
                    this.handleGameOver();
                }
            }
        } catch (error) {
            console.error('Error hitting:', error);
            this.elements.statusMessage.textContent = 'Error hitting. Please try again.';
        }
    }

    async stand() {
        try {
            const response = await fetch('/api/stand', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.ok) {
                this.gameState = await response.json();
                this.updateUI();
                if (this.gameState.game_state === 'game_over') {
                    this.handleGameOver();
                }
            }
        } catch (error) {
            console.error('Error standing:', error);
            this.elements.statusMessage.textContent = 'Error standing. Please try again.';
        }
    }

    handleGameOver() {
        this.elements.resultMessage.textContent = this.gameState.result;
        if (this.gameState.result.includes('win')) {
            this.addWinnerAnimation();
        }
        this.elements.newGameBtn.style.display = 'inline-block';
        this.elements.dealBtn.style.display = 'none';
        this.elements.dealerValue.classList.remove('hidden');
    }

    addWinnerAnimation() {
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.classList.add('winner');
            setTimeout(() => card.classList.remove('winner'), 1500);
        });
    }

    updateUI() {
        this.updateCards();
        this.updateValues();
        this.updateBalance();
        this.updateButtons();
        this.updateStatus();
    }

    updateCards() {
        // Update player cards
        this.elements.playerCards.innerHTML = '';
        this.gameState.player_hand.forEach((card, index) => {
            const cardElement = this.createCardElement(card, false);
            cardElement.style.animationDelay = `${index * 0.2}s`;
            cardElement.classList.add('dealing');
            this.elements.playerCards.appendChild(cardElement);
        });
        // Update dealer cards
        this.elements.dealerCards.innerHTML = '';
       this.gameState.dealer_hand.forEach((card, index) => {
    const isHidden = card.hidden === true;
    const cardElement = this.createCardElement(card, isHidden);
    cardElement.style.animationDelay = `${index * 0.2}s`;
    cardElement.classList.add('dealing');
    this.elements.dealerCards.appendChild(cardElement);
});

    }

    createCardElement(card, isHidden) {
        const cardDiv = document.createElement('div');
        cardDiv.className = `card ${isHidden ? 'hidden' : ''}`;
        if (!isHidden) {
            const isRed = card.suit === 'Hearts' || card.suit === 'Diamonds';
            const isBlack = card.suit === 'Clubs' || card.suit === 'Spades';
            if (isRed) cardDiv.classList.add('red');
            if (isBlack) cardDiv.classList.add('black');
            cardDiv.innerHTML = `
                <div class="card-value">${card.value}</div>
                <div class="card-suit">${this.getSuitSymbol(card.suit)}</div>
            `;
        } else {
            // Show a custom card back (joker style)
            cardDiv.innerHTML = `
                <div class="card-back">
                    <span class="joker-icon">🃏</span>
                </div>
            `;
        }
        return cardDiv;
    }

    getSuitSymbol(suit) {
        const suitSymbols = {
            'Hearts': '♥',
            'Diamonds': '♦',
            'Clubs': '♣',
            'Spades': '♠'
        };
        return suitSymbols[suit] || suit;
    }

    updateValues() {
        this.elements.playerValue.textContent = this.gameState.player_value;
        this.elements.dealerValue.textContent = this.gameState.dealer_value;
    }

    updateBalance() {
        this.elements.balance.textContent = this.gameState.player_balance;
        this.elements.bet.textContent = this.gameState.player_bet;
        this.elements.betInput.value = this.gameState.player_bet;
    }

    updateButtons() {
        const isPlaying = this.gameState.game_state === 'playing';
        const isGameOver = this.gameState.game_state === 'game_over';
        this.elements.dealBtn.disabled = isPlaying;
        this.elements.hitBtn.disabled = !isPlaying;
        this.elements.standBtn.disabled = !isPlaying;
        if (isGameOver) {
            this.elements.hitBtn.style.display = 'none';
            this.elements.standBtn.style.display = 'none';
        } else {
            this.elements.hitBtn.style.display = 'inline-block';
            this.elements.standBtn.style.display = 'inline-block';
        }
    }

    updateStatus() {
        if (this.gameState.game_state === 'waiting') {
            this.elements.statusMessage.textContent = 'Welcome to Blackjack! Click "Deal" to start.';
        } else if (this.gameState.game_state === 'playing') {
            this.elements.statusMessage.textContent = 'Your turn! Hit or stand?';
        } else if (this.gameState.game_state === 'dealer_turn') {
            this.elements.statusMessage.textContent = 'Dealer is playing...';
        }
    }

    openRulesModal() {
        this.elements.rulesModal.classList.add('active');
    }

    closeRulesModal() {
        this.elements.rulesModal.classList.remove('active');
    }

    clearMessages() {
        this.elements.statusMessage.textContent = '';
        this.elements.resultMessage.textContent = '';
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new BlackjackGame();
});

// Add some visual effects
document.addEventListener('DOMContentLoaded', () => {
    // Add card dealing sound effect (visual only)
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            card.style.transform = 'scale(1.05)';
            setTimeout(() => {
                card.style.transform = 'scale(1)';
            }, 150);
        });
    });
}); 