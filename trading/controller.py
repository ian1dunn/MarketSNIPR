
class Controller:
    def __init__(self):
        self.positions = []
        self.step = 0

    # TODO State updates after each simulated day - then agent can perform trades
    # TODO All API data should be cached for faster training, refresh on call to update()
    def update(self):
        self.step += 1  # TODO

    def reset(self):
        pass

    def is_done(self):
        # Has reached end of available training data
        pass

    # ACCOUNT INFORMATION

    def get_buying_power(self):
        # Get buying power (cash balance)
        pass

    def get_portfolio_value(self):
        pass

    # Get gain/loss of portfolio

    # Get current equity

    # POSITIONS

    # Get list of all open positions
    def get_open_positions(self):
        # Return list of tickers
        pass

    # Get a position
    def get_position_data(self, ticker: str):
        # Return tuple with most recent closing price and array of indicators
        pass

    # ORDERS

    # Create order

    # Get all orders
