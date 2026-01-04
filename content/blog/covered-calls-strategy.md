---
author: Kishore Kumar
date: 2024-05-15 08:10:14+0530
doc: 2025-05-18 17:07:02+0530
tags:
- domain-finance-quantitative
title: Covered Calls Strategy
---
# Introduction
The covered call strategy is an options trading strategy ([Derivatives - Options](/blog/derivatives-options)) in which an investor holds a long position in an underlying asset and simultaneously writes (sells) call options on that same asset. This strategy is employed by investors seeking to generate income from the premium received by selling the call options, while also benefiting from potential stock price appreciation up to the strike price of the call option.

# How It Works
![pasted-image-20240507114807](/images/pasted-image-20240507114807.webp)
A call option is a contract that gives the buyer the right, but not the obligation, to purchase a specified quantity of an underlying asset at a predetermined strike price within a specific period. In the covered call strategy, the investor owns the underlying asset (e.g., shares of a stock) and writes (sells) call options on those shares. 

**Example:** For instance, consider an investor holding 100 shares of a stock currently trading at ₹400 per share (market value). The investor can sell a call option with a strike price of ₹420 and an option premium of ₹4 per share (₹400 total premium). The call option expires in 30 days.

If the stock price remains below ₹420 at expiration, the call option will not be exercised, and the investor retains the ₹400 premium as income. However, if the stock price rises above ₹420, the call option holder may exercise the option, requiring the investor to sell the shares at the strike price of ₹420, regardless of the higher market price. The payoff profile of the covered call strategy is characterized by a capped upside potential but limited downside risk. The maximum profit is equal to the call option premium received, plus the difference between the strike price and the purchase price of the underlying asset (if the option is exercised). The maximum loss is limited to the initial cost of purchasing the underlying asset, minus the premium received. The covered call strategy generates income from the call option premium, providing a cushion against potential downside risk in the underlying asset. However, the strategy also caps the upside potential, as the investor is obligated to sell the underlying asset at the strike price if the option is exercised. Additionally, the investor faces the risk of having the underlying asset called away, potentially missing out on further appreciation.

# Advantages
## Dividend Income
If the underlying asset is a dividend-paying stock, the investor continues to receive dividends while the covered call position is held.
## Stock Price Appreciation
By selling out-of-the-money call options, the investor can benefit from potential stock price appreciation up to the strike price of the call option.
## Option Premium Income
The premium received from selling the call option generates additional income for the investor. If the option expires unexercised, the investor can sell a new call option on the same underlying position, generating recurring premium income.
## Downside Hedge
The covered call strategy is sometimes regarded as a downside hedge for an investor's portfolio. If the portfolio remains flat or declines in value, the income generated from selling call options can partially offset the losses, providing a cushion against downside risk compared to simply holding the underlying assets.
# Disadvantages
## Capped Upside Potential
While the covered call strategy provides three potential sources of return (dividend income, stock price appreciation up to the strike price, and option premium income), the third source of return is achieved by significantly restricting the second source – stock price appreciation. As illustrated by the payoff graph, the covered call strategy caps the upside potential, as any appreciation beyond the strike price is transferred to the call option buyer. Consequently, the strategy effectively hedges potential upside gains.
## Higher Tax
The premiums received from selling call options are generally considered short-term capital gains, which are taxed at a higher rate than long-term capital gains. Additionally, if the options are exercised, requiring the sale and repurchase of the underlying asset, the investor may need to report and pay taxes on the capital gains, potentially reducing the tax-deferral benefits of holding the position.
## Share Holding Power Reduction
If the stock price fluctuates significantly, even if it remains flat over the long term, the covered call strategy may result in a gradual reduction in the number of shares held due to the exercise of call options. This can lead to realizing losses, despite the overall position being flat.
## Risk-Adjusted Return Considerations
While some people argue that covered call strategies may offer superior risk-adjusted returns, meaning higher returns per unit of risk taken, this claim is subject to debate and may depend on the specific market conditions and underlying assets involved.

---

## Related Reading

- [Efficient-Market-Hypothesis](/blog/efficient-market-hypothesis)
- [What is the Stock Market?](/blog/what-is-the-stock-market)
