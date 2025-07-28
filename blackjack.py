import random
import json
import os
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from config import *

FIREWORKS_API_KEY = getattr(globals(), 'FIREWORKS_API_KEY', None) or getattr(__import__('config'), 'FIREWORKS_API_KEY', None)
FIREWORKS_API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
FIREWORKS_MODEL = "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new"

app = Flask(__name__)
CORS(app)

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return f"{self.value} of {self.suit}"
    
    def get_value(self):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11  # Will be handled specially in hand calculation
        else:
            return int(self.value)

class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = []
        self.dealer_hand = []
        self.game_state = "waiting"  # waiting, playing, dealer_turn, game_over
        self.result = ""
        self.player_bet = DEFAULT_BET
        self.player_balance = DEFAULT_BALANCE
    
    def start_new_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = []
        self.dealer_hand = []
        self.game_state = "playing"
        self.result = ""
        
        # Deal initial cards
        self.player_hand.append(self.deck.deal())
        self.dealer_hand.append(self.deck.deal())
        self.player_hand.append(self.deck.deal())
        self.dealer_hand.append(self.deck.deal())
    
    def calculate_hand_value(self, hand):
        value = 0
        aces = 0
        
        for card in hand:
            if card.value == 'A':
                aces += 1
            else:
                value += card.get_value()
        
        # Add aces
        for _ in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
        
        return value
    
    def hit(self):
        if self.game_state == "playing":
            self.player_hand.append(self.deck.deal())
            player_value = self.calculate_hand_value(self.player_hand)
            
            if player_value > 21:
                self.game_state = "game_over"
                self.result = "Bust! You lose!"
                self.player_balance -= self.player_bet
            elif player_value == 21:
                self.dealer_turn()
    
    def stand(self):
        if self.game_state == "playing":
            self.dealer_turn()
    
    def dealer_turn(self):
        self.game_state = "dealer_turn"
        
        # AI dealer logic using OpenAI API
        dealer_decision = self.ai_dealer_decision()
        
        while dealer_decision == "hit":
            self.dealer_hand.append(self.deck.deal())
            dealer_value = self.calculate_hand_value(self.dealer_hand)
            
            if dealer_value > 21:
                self.game_state = "game_over"
                self.result = "Dealer busts! You win!"
                self.player_balance += self.player_bet
                return
            elif dealer_value >= 17:
                break
            
            dealer_decision = self.ai_dealer_decision()
        
        self.determine_winner()
    
    def ai_dealer_decision(self):
        """AI dealer decision using Fireworks LLM"""
        try:
            dealer_value = self.calculate_hand_value(self.dealer_hand)
            player_value = self.calculate_hand_value(self.player_hand)
            dealer_up_card = self.dealer_hand[0].get_value() if self.dealer_hand else 0
            if FIREWORKS_API_KEY and FIREWORKS_API_URL and FIREWORKS_MODEL:
                decision = self.ai_model_dealer_strategy(dealer_value, player_value, dealer_up_card)
                return decision
            else:
                decision = self.advanced_dealer_strategy(dealer_value, player_value, dealer_up_card)
                return decision
        except Exception as e:
            print(f"AI decision error: {e}")
            dealer_value = self.calculate_hand_value(self.dealer_hand)
            return "hit" if dealer_value < 17 else "stand"

    def ai_model_dealer_strategy(self, dealer_value, player_value, dealer_up_card):
        """AI-powered dealer strategy using Fireworks API"""
        try:
            if AI_THINKING_TIME > 0:
                time.sleep(AI_THINKING_TIME)
            prompt = (
                f"You are an expert Blackjack dealer with years of experience playing against human players.\n"
                f"You need to make a strategic decision whether to HIT or STAND based on the current game state.\n\n"
                f"Current Game State:\n"
                f"- Your hand value: {dealer_value}\n"
                f"- Player's hand value: {player_value}\n"
                f"- Your up card value: {dealer_up_card}\n"
                f"- Your cards: {[f'{card.value} of {card.suit}' for card in self.dealer_hand]}\n"
                f"- Player's cards: {[f'{card.value} of {card.suit}' for card in self.player_hand]}\n\n"
                f"Blackjack Rules:\n"
                f"- Dealer must hit on 16 and below\n"
                f"- Dealer must stand on 17 and above\n"
                f"- Goal is to get as close to 21 as possible without busting\n"
                f"- Face cards (J, Q, K) = 10, Aces = 1 or 11\n\n"
                f"Think like a skilled human dealer would in this situation. Consider:\n"
                f"1. The risk of busting if you hit (especially with 12-16)\n"
                f"2. The player's hand strength and their likely next move\n"
                f"3. The probability of winning with your current hand vs the player's hand\n"
                f"4. Psychological factors - what would make the player nervous?\n"
                f"5. Card counting implications (if any high cards have been played)\n"
                f"6. The dealer's reputation and house edge\n\n"
                f"Additional Context:\n"
                f"- You're playing in a casino environment\n"
                f"- The player can see your up card and is making decisions based on it\n"
                f"- You want to maximize house edge while appearing fair\n"
                f"- Consider the player's betting pattern and confidence level\n\n"
                f"Respond with ONLY 'HIT' or 'STAND' based on your expert analysis."
            )
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {FIREWORKS_API_KEY}"
            }
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are Dobby-70B, an AI assistant with an 'unhinged' personality. "
                        "Please respond in a helpful, direct style."
                    )
                },
                {"role": "user", "content": prompt}
            ]
            payload = {
                "model": FIREWORKS_MODEL,
                "max_tokens": 1024,
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 40,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "messages": messages
            }
            response = requests.post(FIREWORKS_API_URL, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    decision = data["choices"][0]["message"]["content"].strip().upper()
                    if decision in ["HIT", "STAND"]:
                        if LOG_AI_DECISIONS:
                            print(f"🤖 Fireworks API Decision: {decision}")
                            print(f"   Dealer: {dealer_value}, Player: {player_value}")
                            print(f"   Dealer cards: {[f'{card.value} of {card.suit}' for card in self.dealer_hand]}")
                            print(f"   Player cards: {[f'{card.value} of {card.suit}' for card in self.player_hand]}")
                        return decision.lower()
                    else:
                        print(f"⚠️  Invalid Fireworks response: {decision}, using fallback strategy")
                        return self.advanced_dealer_strategy(dealer_value, player_value, dealer_up_card)
                else:
                    print("No text returned from the model (choices are empty). Using fallback strategy.")
                    return self.advanced_dealer_strategy(dealer_value, player_value, dealer_up_card)
            else:
                print(f"Error: {response.status_code} {response.text}. Using fallback strategy.")
                return self.advanced_dealer_strategy(dealer_value, player_value, dealer_up_card)
        except Exception as e:
            print(f"❌ Fireworks API error: {e}, using fallback strategy")
    
    def determine_winner(self):
        self.game_state = "game_over"
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        if player_value > dealer_value:
            self.result = "You win!"
            self.player_balance += self.player_bet
        elif dealer_value > player_value:
            self.result = "Dealer wins!"
            self.player_balance -= self.player_bet
        else:
            self.result = "It's a tie!"
    
    def get_game_state(self):
        # Hide dealer cards unless it's dealer_turn or game_over
        dealer_hand = []
        for _ in self.dealer_hand:
            if self.game_state in ["dealer_turn", "game_over"]:
                dealer_hand.append({"suit": _.suit, "value": _.value})
            else:
                dealer_hand.append({"suit": "", "value": "?", "hidden": True})

        return {
            "player_hand": [{"suit": card.suit, "value": card.value} for card in self.player_hand],
            "dealer_hand": dealer_hand,
            "dealer_up_card": (
                {"suit": self.dealer_hand[0].suit, "value": self.dealer_hand[0].value}
                if self.dealer_hand and self.game_state in ["dealer_turn", "game_over"]
                else {"suit": "", "value": "?"}
            ),
            "player_value": self.calculate_hand_value(self.player_hand),
            "dealer_value": (
                self.calculate_hand_value(self.dealer_hand)
                if self.game_state in ["dealer_turn", "game_over"]
                else "?"
            ),
            "game_state": self.game_state,
            "result": self.result,
            "player_balance": self.player_balance,
            "player_bet": self.player_bet
        }




# Global game instance
game = BlackjackGame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    bet = data.get('bet', 100)
    # Validate bet
    if bet <= 0 or bet > game.player_balance:
        return jsonify({'error': 'Invalid bet amount.'}), 400
    game.player_bet = bet
    game.start_new_game()
    return jsonify(game.get_game_state())

@app.route('/api/hit', methods=['POST'])
def hit():
    game.hit()
    return jsonify(game.get_game_state())

@app.route('/api/stand', methods=['POST'])
def stand():
    game.stand()
    return jsonify(game.get_game_state())

@app.route('/api/game_state', methods=['GET'])
def get_game_state():
    return jsonify(game.get_game_state())

if __name__ == '__main__':
    print("🎰 Starting Blackjack Game with AI Dealer...")
    print(f"🌐 Server will be available at: http://localhost:{GAME_PORT}")
    print("=" * 50)
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=GAME_PORT)
