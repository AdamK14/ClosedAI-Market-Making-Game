from flask import Flask, jsonify, request
from app.game.market import Market
from app.game.player import Player
from app.game.round_manager import RoundManager

app = Flask(__name__)

# Initialize the game
market = Market(initial_price=100.0, volatility=0.25, expirations=[...], strikes=[...])
player = Player()
round_manager = RoundManager(market, player)

@app.route("/start-round", methods=["GET"])
def start_round():
    """
    Starts a new round and returns market conditions.
    """
    round_manager.start_round()
    return jsonify({
        "stock_price": market.get_underlying_price(),
        "option_chain": market.option_chain.to_dict(orient="records"),
        "news_event": market.news_manager.latest_news
    })

@app.route("/submit-quotes", methods=["POST"])
def submit_quotes():
    """
    Accepts player input for bid/ask quotes.
    """
    data = request.json
    strike = data["strike"]
    option_type = data["type"]
    bid = data["bid_price"]
    ask = data["ask_price"]

    market.option_chain.loc[
        (market.option_chain["strike"] == strike) &
        (market.option_chain["type"] == option_type),
        ["bid_price", "ask_price"]
    ] = [bid, ask]

    return jsonify({"status": "Quotes submitted successfully"})

@app.route("/simulate-round", methods=["GET"])
def simulate_round():
    """
    Simulates the round and returns the results.
    """
    round_manager.simulate_round()
    return jsonify({
        "stock_price": market.get_underlying_price(),
        "option_chain": market.option_chain.to_dict(orient="records"),
        "total_pnl": player.total_pnl
    })

if __name__ == "__main__":
    app.run(debug=True)
