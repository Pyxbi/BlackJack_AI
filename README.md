# Blackjack Game - Player vs AI

A modern web-based Blackjack game where you play against an AI dealer. Built with Flask backend and modern HTML/CSS/JavaScript frontend.

## Features

- 🎮 **Player vs AI Dealer**: Play against an intelligent AI dealer
- 🎨 **Modern UI**: Beautiful casino-style interface with animations
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🃏 **Real Blackjack Rules**: Follows standard casino Blackjack rules
- 💰 **Betting System**: Track your balance and bets
- 🎯 **AI Decision Making**: Smart dealer AI that follows basic strategy

## Game Rules

- Get as close to 21 as possible without going over
- Face cards (J, Q, K) = 10 points
- Aces = 1 or 11 (automatically optimized)
- Dealer must hit on 16 and below, stand on 17 and above
- Beat the dealer to win!

## Installation

### Quick Setup (Recommended)

1. **Clone or download the project files**

2. **Run the setup script:**
   ```bash
   python setup.py
   ```
   
   This will:
   - Check Python version compatibility
   - Install all required dependencies
   - Help you set up Gemini AI (optional)
   - Test the installation

3. **Start the game:**
   ```bash
   python blackjack.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:5100
   ```

### Manual Setup

If you prefer to set up manually:

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Gemini AI (Optional but Recommended):**
   
   The game uses Google's Gemini AI to make the dealer think like a human player. To enable this:
   
   a. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   
   b. Set the API key in one of these ways:
   - **Option 1**: Set as environment variable:
     ```bash
     export GEMINI_API_KEY='your_api_key_here'
     ```
   - **Option 2**: Add to `config.py`:
     ```python
     GEMINI_API_KEY = 'your_api_key_here'
     ```
   
   c. The game will work without the API key, but the dealer will use basic strategy instead of intelligent AI.

3. **Run the game:**
   ```bash
   python blackjack.py
   ```

## How to Play

1. **Start the Game**: Click "Deal Cards" to begin
2. **Your Turn**: You'll see your two cards and one of the dealer's cards
3. **Make Decisions**:
   - **Hit**: Take another card
   - **Stand**: Keep your current hand
4. **Dealer's Turn**: The AI dealer will play automatically
5. **Results**: See who wins and your updated balance
6. **New Game**: Click "New Game" to play again

## Project Structure

```
pythonProject/
├── blackjack.py          # Main Flask application
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/
│   └── index.html       # Main game interface
└── static/
    ├── css/
    │   └── style.css    # Game styling
    └── js/
        └── game.js      # Game logic and interactions
```

## AI Dealer

The AI dealer uses **Gemini AI** for intelligent decision-making that thinks like a human player:

### With Gemini AI (Recommended):
- **Human-like thinking**: Considers psychological factors and player behavior
- **Advanced strategy**: Analyzes risk, probability, and game context
- **Realistic gameplay**: Includes thinking time and detailed analysis
- **Adaptive behavior**: Responds to player's hand strength and betting patterns

### Without Gemini AI (Fallback):
- **Basic strategy**: Follows standard casino rules
- **Risk assessment**: Considers hand values and probabilities
- **Consistent behavior**: Predictable but fair gameplay

### AI Features:
- **Thinking time**: Simulates realistic dealer decision-making
- **Detailed logging**: Shows AI reasoning and decisions
- **Context awareness**: Considers player's cards and betting patterns
- **Psychological factors**: Makes decisions that would affect player confidence

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Modern CSS with gradients and animations
- **AI**: Custom decision-making algorithm

## Customization

You can easily customize the game by:
- Modifying betting amounts in `blackjack.py`
- Changing the visual theme in `static/css/style.css`
- Adjusting AI behavior in the `ai_dealer_decision()` method
- Adding new features like splitting pairs or doubling down

## Future Enhancements

- [ ] Split pairs functionality
- [ ] Double down option
- [ ] Insurance bets
- [ ] Multiple deck support
- [ ] Sound effects
- [ ] Statistics tracking
- [ ] Advanced AI strategies

## License

This project is open source and available under the MIT License.

---

**Enjoy playing Blackjack! 🃏** # BlackJack_AI
# BlackJack_AI
# BlackJack_AI
