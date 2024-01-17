import dataclasses
import time
import json
import threading
import websocket


@dataclasses.dataclass
class OrderbookPrice:
    price: float
    volume: int

    def __str__(self):
        return f'{self.volume} units @ {self.price}'


@dataclasses.dataclass
class Orderbook:
    bids: list[OrderbookPrice]
    asks: list[OrderbookPrice]

    def __str__(self):
        output = ""

        output += "bids:\n"
        for bid in self.bids:
            output += str(bid) + '\n'
        output += "asks:\n"
        for ask in self.asks:
            output += str(ask) + '\n'

        return output


@dataclasses.dataclass
class RequestResult:
    success: bool


@dataclasses.dataclass
class Transaction:
    timestamp: int
    price: float
    volume: int
    ticker: str


class Exchange:
    ws: websocket.WebSocketApp | None

    updating: bool
    position: dict[str, int]
    wealth: int
    orderbook: dict[str, Orderbook]
    transactions: list[Transaction]

    def __init__(self, name: str, password: str, hostname: str = 'localhost', port: int = 8080):
        self.name = name
        self.password = password
        self.hostname = hostname
        self.port = port
        self.ws = None

        # thread running the websocket
        self.thread = None
        # whether the socket has stopped
        self.stopped = False
        # whether the authorization was successful
        self.connected = False

        self.position = {}
        self.wealth = 0
        self.orderbook = {}
        self.updating = False
        self.transactions = []

    def connect(self):
        self.ws = websocket.WebSocketApp(
            f"ws://{self.hostname}:{self.port}",
            on_open=lambda ws: self.on_open(),
            on_message=lambda ws, msg: self.on_message(msg),
            on_close=lambda ws, status, message: self.on_close(status, message),
            on_error=lambda ws, error: self.on_error(error)
        )

        self.thread = threading.Thread(target=self.start)
        self.thread.start()

        # wait until connected or stopped
        while not (self.connected or self.stopped):
            time.sleep(0.1)

        if not self.connected:
            raise RuntimeError('failed to connect')

    def start(self):
        """code to start the websocket, setting stop flag when it finishes"""

        try:
            self.ws.run_forever()
        except Exception as e:
            print(e)
        finally:
            self.stopped = True

    def close(self):
        """force close function"""

        # close if it exists
        if self.ws is not None:
            instance = self.ws
            self.ws = None
            instance.close()

    def on_open(self):
        self.ws.send(json.dumps({
            'type': 'auth',
            'name': self.name,
            'passphase': self.password
        }))

    def on_message(self, message):
        data = json.loads(message)
        if 'type' not in data:
            print('incorrect payload format, no type field')
            return

        if data['type'] == 'auth':
            if not data['ok']:
                raise RuntimeError(f'failed to authorize, reason {data["message"]}')
            else:
                self.connected = True
                print('connected and authorized client')

        elif data['type'] == 'tick':
            self.updating = True

            # update position
            self.position = data['position']

            # update wealth
            self.wealth = data['user']['wealth'] / 100

            # update orderbook
            self.orderbook.clear()
            for ticker, both in data['orderbook'].items():
                bids = []
                for entry in both['bids']:
                    bids.append(OrderbookPrice(price=entry['price'] / 100, volume=entry['volume']))

                asks = []
                for entry in both['asks']:
                    asks.append(OrderbookPrice(price=entry['price'] / 100, volume=entry['volume']))

                self.orderbook[ticker] = Orderbook(bids=bids, asks=asks)

            # update transactions
            self.transactions = []
            for transaction in data['transactions']:
                self.transactions.append(
                    Transaction(
                        timestamp=transaction['id'],
                        volume=transaction['volume'],
                        price=transaction['price'],
                        ticker=transaction['ticker']
                    )
                )
            self.updating = False


        elif data['type'] == 'order':
            pass

        elif data['type'] == 'delete':
            pass

        else:
            print(f'unknown data type {data["type"]}')

    def on_close(self, status, message):
        """onclose callback that prompts the state"""

        if self.ws is not None:
            self.ws = None

            raise RuntimeError(f'force closed with code {status}, reason {message}')

        print('gracefully closed')

    def on_error(self, error):
        """error printer"""

        print(f'error: {error}')

    ### METHODS ###
    def get_last_price_book(self, ticker: str) -> Orderbook | None:
        while self.updating:
            time.sleep(1 / 120)

        return self.orderbook.get(ticker)

    def get_positions(self) -> dict[str, int]:
        return self.position

    def get_pnl(self) -> float:
        return self.wealth

    def insert_order(self, ticker: str, price: float, volume: int, side: str, order_type: str):
        if ticker not in self.position:
            print(f'WARNING, ticker {ticker} is not available')

        request = {
            'type': 'order',
            'ticker': ticker,
            'price': round(price * 100),
            'volume': volume,
            'bid': side.lower() == 'bid',
            'ioc': order_type.lower() == 'ioc'
        }
        self.ws.send(json.dumps(request))

        # a hack to keep the interface working
        return RequestResult(success=True)

    def delete_orders(self, ticker: str):
        request = {
            'type': 'delete',
            'ticker': ticker
        }
        self.ws.send(json.dumps(request))

        # a hack to keep the interface working
        return RequestResult(success=True)

    def poll_new_trade_ticks(self, ticker: str):
        while self.updating:
            time.sleep(1 / 120)
        pass
