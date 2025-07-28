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

### Manual Setup

If you prefer to set up manually:

1. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Set up Firework AI API key (Optional but Recommended):**
   
   The game uses dobby-unhinged-llama-3-3-70b-new's AI to make the dealer think like a human player. To enable this:
   
    Set the API key in one of these ways:
   - **Option 1**: Set as environment variable in .env:
     ```bash
     FIREWORK_API_KEY="your_api_key"
     ```

3. **Run the game:**
   ```bash
   python3 blackjack.py
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

## AI Dealer

The AI dealer uses ** AI** for intelligent decision-making that thinks like a human player:

### With  AI (Recommended):
- **Human-like thinking**: Considers psychological factors and player behavior
- **Advanced strategy**: Analyzes risk, probability, and game context
- **Realistic gameplay**: Includes thinking time and detailed analysis
- **Adaptive behavior**: Responds to player's hand strength and betting patterns

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
