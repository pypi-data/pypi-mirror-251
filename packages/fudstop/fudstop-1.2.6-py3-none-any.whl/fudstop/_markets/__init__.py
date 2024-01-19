import sys
from pathlib import Path

import json
# Add the project directory to the sys.path
project_dir = str(Path(__file__).resolve().parents[1])
if project_dir not in sys.path:
    sys.path.append(project_dir)
import os
import random
from asyncpg.exceptions import UniqueViolationError
from aiohttp.client_exceptions import ContentTypeError
from collections import deque
from dotenv import load_dotenv
from _markets.list_sets.dicts import hex_color_dict
from apis.discord_.discord_sdk import DiscordSDK
from _markets.list_sets.ticker_lists import most_active_tickers
from analyzers import OptionDataAnalyzer
from market_handlers.database_ import MarketDBManager
from datetime import datetime, timedelta
from _markets.market_handlers.list_sets import indices_names_and_symbols_dict, CRYPTO_DESCRIPTIONS,CRYPTO_HOOKS
load_dotenv()
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
from monitor import EquityOptionTradeMonitor
from polygon.websocket import WebSocketClient, Market
from polygon.websocket.models import WebSocketMessage, EquityAgg,EquityQuote,EquityTrade,IndexValue
from fudstop.apis.polygonio.mapping import option_condition_desc_dict,option_condition_dict,OPTIONS_EXCHANGES,stock_condition_desc_dict,stock_condition_dict,indicators,quote_conditions,STOCK_EXCHANGES
from list_sets.dicts import all_forex_pairs, crypto_currency_pairs
from apis.polygonio.technicals import Technicals
from apis.webull.webull_trading import WebullTrading
# Create a reverse dictionary
all_forex_pairs = {v: k for k, v in all_forex_pairs.items()}
from typing import List
import asyncio
import time
from asyncio import Queue
import pandas as pd
import logging
from _markets.webhook_dicts import option_conditions_hooks
from apis.polygonio.async_polygon_sdk import Polygon
from apis.polygonio.polygon_options import PolygonOptions



class Inserts:
    def __init__(self, host:str='localhost', user:str='chuck', password:str='fud', port:int=5432, database:str='markets'):
        self.host=host
        self.user=user
        self.password=password
        self.port=port
        self.database=database





    async def insert_theta_resistant(self, data):
        query = '''
            INSERT INTO options_data (
                underlying_symbol, strike, call_put, expiry, open, high, low, close, vwap,
                change_percent, oi, vol, vol_oi, iv, iv_percentile, intrinsic_value,
                extrinsic_value, time_value, bid, mid, ask, spread, spread_pct,
                trade_size, trade_price, trade_exchange, moneyness, velocity, profit_potential,
                delta, delta_theta_ratio, gamma, gamma_risk, vega, vega_impact, theta, theta_decay
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20,
                      $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34, $35, $36, $37)
        '''
        await self.conn.execute(query, *data)

    async def close_connection(self):
        await self.conn.close()
