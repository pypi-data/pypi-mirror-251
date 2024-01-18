import time

from ...order import LIMIT


class LiveBroker:
    def __new__(self, symbol: str, timestamp_unit: str):
        if timestamp_unit == 's':
            self.ts_mul = 1
        elif timestamp_unit == 'ms':
            self.ts_mul = 1_000
        elif timestamp_unit == 'us':
            self.ts_mul = 1_000_000
        elif timestamp_unit == 'ns':
            self.ts_div = 1_000_000_000
        pass

    @property
    def position(self):
        """
        Current position.
        """
        #
        return self.local.state.position

    @property
    def balance(self):
        """
        Current balance..
        """
        raise NotImplementedError

    @property
    def fee(self):
        raise NotImplementedError

    @property
    def trade_num(self):
        raise NotImplementedError

    @property
    def trade_qty(self):
        raise NotImplementedError

    @property
    def trade_amount(self):
        raise NotImplementedError

    @property
    def orders(self):
        """
        Orders dictionary.
        """
        return self.local.orders

    @property
    def tick_size(self):
        """
        Tick size
        """
        return self.local.depth.tick_size

    @property
    def lot_size(self):
        """
        Lot size
        """
        return self.local.depth.lot_size

    @property
    def high_ask_tick(self):
        """
        The highest ask price in the market depth in tick.
        """
        return self.local.depth.high_ask_tick

    @property
    def low_bid_tick(self):
        """
        The lowest bid price in the market depth in tick.
        """
        return self.local.depth.low_bid_tick

    @property
    def best_bid_tick(self):
        """
        The best bid price in tick.
        """
        return self.local.depth.best_bid_tick

    @property
    def best_ask_tick(self):
        """
        The best ask price in tick.
        """
        return self.local.depth.best_ask_tick

    @property
    def best_bid(self):
        """
        The best bid price.
        """
        return self.best_bid_tick * self.tick_size

    @property
    def best_ask(self):
        """
        The best ask price.
        """
        return self.best_ask_tick * self.tick_size

    @property
    def bid_depth(self):
        """
        Bid market depth.
        """
        return self.local.depth.bid_depth

    @property
    def ask_depth(self):
        """
        Ask market depth.
        """
        return self.local.depth.ask_depth

    @property
    def mid(self):
        """
        Mid-price of BBO.
        """
        return (self.best_bid + self.best_ask) / 2.0

    @property
    def equity(self):
        """
        Current equity value.
        """
        return self.local.state.equity(self.mid)

    @property
    def last_trade(self):
        """
        Last market trade. If ``None``, no last market trade.
        """
        if self.local.trade_len > 0:
            return self.last_trades[self.local.trade_len - 1]
        else:
            return None

    @property
    def last_trades(self):
        """
        An array of last market trades.
        """
        return self.local.last_trades[:self.local.trade_len]

    @property
    def local_timestamp(self):
        return self.current_timestamp

    def submit_buy_order(
            self,
            order_id: int,
            price: float,
            qty: float,
            time_in_force: int,
            order_type: int = LIMIT,
            wait: bool = False
    ):
        r"""
        Places a buy order.

        Args:
            order_id: The unique order ID; there should not be any existing order with the same ID on both local and
                      exchange sides.
            price: Order price.
            qty: Quantity to buy.
            time_in_force: Available Time-In-Force options vary depending on the exchange model. See to the exchange
                           model for details.

                           - ``GTX``: Post-only
                           - ``GTC``: Good 'till Cancel
                           - ``FOK``: Fill or Kill
                           - ``IOC``: Immediate or Cancel
            order_type: Currently, only ``LIMIT`` is supported. To simulate a ``MARKET`` order, set the price very high.
            wait: If ``True``, wait until the order placement response is received.

        Returns:
            ``True`` if the method reaches the specified timestamp within the data. If the end of the data is reached
            before the specified timestamp, it returns ``False``.
        """
        self.local.submit_order(order_id, BUY, price, qty, order_type, time_in_force, self.current_timestamp)

        if wait:
            return self.goto(UNTIL_END_OF_DATA, wait_order_response=order_id)
        return True

    def submit_sell_order(
            self,
            order_id: int,
            price: float,
            qty: float,
            time_in_force: int,
            order_type: int = LIMIT,
            wait: boolean = False
    ):
        r"""
        Places a sell order.

        Args:
            order_id: The unique order ID; there should not be any existing order with the same ID on both local and
                      exchange sides.
            price: Order price.
            qty: Quantity to sell.
            time_in_force: Available Time-In-Force options vary depending on the exchange model. See to the exchange
                           model for details.

                           - ``GTX``: Post-only
                           - ``GTC``: Good 'till Cancel
                           - ``FOK``: Fill or Kill
                           - ``IOC``: Immediate or Cancel
            order_type: Currently, only ``LIMIT`` is supported. To simulate a ``MARKET`` order, set the price very low.
            wait: If ``True``, wait until the order placement response is received.

        Returns:
            ``True`` if the method reaches the specified timestamp within the data. If the end of the data is reached
            before the specified timestamp, it returns ``False``.
        """
        return True

    def modify(self, order_id: int, price: float, qty: float, wait: boolean = False):
        r"""
        Modify the specified order.

        - If the adjusted total quantity(leaves_qty + executed_qty) is less than or equal to
          the quantity already executed, the order will be considered expired. Be aware that this adjustment doesn't
          affect the remaining quantity in the market, it only changes the total quantity.
        - Modified orders will be reordered in the match queue.

        Args:
            order_id: Order ID to modify.
            price: Order price.
            qty: Quantity to sell.
            wait: If ``True``, wait until the order placement response is received.

        Returns:
            ``True`` if the method reaches the specified timestamp within the data. If the end of the data is reached
            before the specified timestamp, it returns ``False``.
        """
        return True

    def cancel(self, order_id: int, wait: boolean = False):
        r"""
        Cancel the specified order.

        Args:
            order_id: Order ID to cancel.
            wait: If ``True``, wait until the order placement response is received.

        Returns:
            ``True`` if the method reaches the specified timestamp within the data. If the end of the data is reached
            before the specified timestamp, it returns ``False``.
        """
        return True

    def wait_order_response(self, order_id: int, timeout: int = -1):
        r"""
        Wait for the specified order response by order ID.

        Args:
            order_id: The order ID to wait for.
            timeout: Maximum waiting time; The default value of `-1` indicates no timeout.

        Returns:
            ``True`` if the method reaches the specified timestamp within the data. If the end of the data is reached
            before the specified timestamp, it returns ``False``.
        """
        pass

    def wait_next_feed(self, include_order_resp: bool, timeout: int = -1):
        """
        Waits until the next feed is received.

        Args:
            include_order_resp: Whether to include order responses in the feed to wait for.
            timeout: Maximum waiting time; The default value of `-1` indicates no timeout.

        Returns:
            ``True`` if the method reaches the specified timestamp within the data. If the end of the data is reached
            before the specified timestamp, it returns ``False``.
        """
        pass

    def clear_inactive_orders(self):
        r"""
        Clear inactive(``CANCELED``, ``FILLED``, ``EXPIRED``, or ``REJECTED``) orders from the local ``orders``
        dictionary.
        """
        pass

    def clear_last_trades(self):
        r"""
        Clears the last trades(market trades) from the buffer.
        """
        pass

    def get_user_data(self, event: int):
        r"""
        Retrieve custom user event data.

        Args:
            event: Event identifier. Refer to the data documentation for details on incorporating custom user data with
                   the market feed data.

        Returns:
            The latest event data for the specified event.
        """
        pass

    def elapse(self, duration: float):
        r"""
        Elapses the specified duration.

        Args:
            duration: Duration to elapse. Unit should be the same as the feed data's timestamp unit.
        """
        time.sleep(duration / self.ts_div)
        return True

    def goto(self):
        raise NotImplementedError

    def connect(self):
        # spawn child process
        # do async tasks
        
        pass
