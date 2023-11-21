# Inverse Bollinger Trading Simulator
## Introduction 
 This repository is dedicated to KRISS 23/24 Fall Research project by Judy Park and Hangyeol Bae, HKUST.

 Inverse Bollinger band is basically betting against the traditional Bollinger band, assuming non mean reversion. We buy when 20 MA hits upper Bollinger band, and sell when 20 MA hits lower band. We will clear our position if our profit/loss has reached our setting.

 We have hypothesized that biotech stocks, under certain events, will not mean-revert due to their volatile nature. Thus, we will use this simulator to test our model in such cases - to be described further.

## Getting started
 * ticker_crawler.py: contains `ticker_crawler` function used to crawl historical data, uses `yfinance` module
 * strategy.py: contains strategy
 * main.py: uses `backtrader` module to test strategy

![snapshot](https://github.com/Hanthebot/Inverse-Bollinger-Trading-Simulator/blob/main/data/snapshot_0_1_0.jpg?raw=true)
*Snapshot 0.1.0*

## Roadmap
- [x] Build general outline [0.0.1]
- [ ] Implement algorithm
  - [x] Implement general algorithm (Bolinger band, inverse logic) [0.1.0]
  - [ ] Finalize order size calculation
  - [ ] Implement stop loss / take profit / order cancel algorithm
- [ ] Select target stock / period
- [ ] Run simulation: trial & error
- [ ] Find best-profit parameter value
- [ ] Tabulate all information needed for the report

## Acknowledgments
 This project heavily adopts following modules:
 1. https://www.backtrader.com
 2. https://pypi.org/project/yfinance/

 Following resources were viewed or used as a reference.
 1. https://www.backtrader.com/docu/quickstart/quickstart/
 2. https://www.backtrader.com/docu/strategy/
 3. https://www.backtrader.com/blog/posts/2018-02-06-dynamic-indicator/dynamic-indicator/
 4. https://stackoverflow.com/questions/72273407/can-you-add-parameters-to-backtrader-strategy
 5. https://sjblog1.tistory.com/42
 6. https://aplab.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%A3%BC%EC%8B%9D-%EB%B0%B1%ED%85%8C%EC%8A%A4%ED%8A%B8
 7. https://algotrading101.com/learn/yfinance-guide/
 8. https://community.backtrader.com/topic/3979/help-with-yahoofinance-data
