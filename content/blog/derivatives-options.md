---
author: Kishore Kumar
date: 2024-03-07 19:09:58+0530
doc: 2025-05-18 17:07:02+0530
tags:
- domain-finance-economics
- domain-finance-quantitative
title: Derivatives - Options
---
In [What is the Stock Market?](/blog/what-is-the-stock-market), we learnt about what a stock market is, what stocks (or shares) of companies are and why people trade for them on the stock market. We use the blanket term **Equities** to refer to the company stocks traded on the stock market. 

> Equity, typically referred to as shareholders' equity (or owners' equity for privately held companies), represents the amount of money that would be returned to a company's shareholders if all of the assets were liquidated and all of the company's debt was paid off in the case of liquidation. - [Equity Definition: What it is, How It Works and How to Calculate It - Investopedia](https://www.investopedia.com/terms/e/equity.asp)

What we will discuss in this chapter, is a specific **derivative** of an financial instrument (here, a stock), called an **option**. 

>A derivative is a security whose underlying asset dictates its pricing, risk, and basic term structure. Each derivative has an underlying asset that dictates its pricing, risk, and basic term structure. The perceived risk of the underlying asset influences the perceived risk of the derivative. - [Derivatives 101 - Investopedia](https://www.investopedia.com/articles/optioninvestor/10/derivatives-101.asp)

# History & Origin

>The earliest known options were bought around 600 BC by the Greek Philosopher Thales of Miletus. He believed that the coming summer would yield a bumper crop of olives. To make money of this idea, he could have purchased olive presses, which if you were right, would be in great demand, but he didn't have enough money to buy the machines. So instead he went to all the existing olive press owners and paid them a little bit of money to **secure the option to rent their presses in the summer for a specified price**. When the harvest came, Thales was right, there were so many olives that the price of renting a press skyrocketed. Thales paid the press owners their pre-agreed price, and then he rented out the machines at a higher rate and pocketed the difference. Thales had executed the first known call option.
>
>**CALL OPTION**
>A call option gives you the right, but not the obligation to buy something at a later date for a set price known as the strike price.  Call options are useful if you expect the price to go up.
>
>**PUT OPTION**
>You can also buy a put option, which gives you the right, but not the obligation to sell something at a later date for the strike price. Put options are useful if you expect the price to go down. 
>
>- [The Trillion Dollar Equation - Veritasium](https://www.youtube.com/watch?v=A5w-dEgIU1M&t=148s)

# A Toy Example 
Imagine you're bullish on Reliance Industries (RIL) and think its share price will rise. The current price of RIL is ₹1000, but you can buy a **call option** that gives you the **right, but not the obligation**, to buy RIL shares i**n one year** for **₹1000** (the **strike price**) by paying a **premium**, say ₹100.

>**Quick side note:** There are two main *styles* of options: American and European. American options allow you to exercise the option at any point before the expiry date. European options allow you to exercise the option on the expiry date. We'll focus on European options for now. In certain places, if the trader doesn’t specify exercising instructions, it goes for compulsory exercising by the regulatory authority and that day is termed as the exercise date for that option.

So, if after a year the price of RIL shoots up to ₹1300, you can use your option to buy shares at ₹1000 and immediately sell them at ₹1300. Here, after factoring in the ₹100 premium you paid, you've pocketed a profit of ₹200 (₹1300 selling price - ₹1000 strike price - ₹100 premium).

However, if the share price tanks to ₹700 in a year, you simply let the option expire, losing only the ₹100 you paid for it.
## PnL ANALYSIS
![pasted-image-20240310192917](/images/pasted-image-20240310192917.webp)
- **If the stock price falls below the strike price, you lose the option premium.** (In this case, you lose ₹100)
- **But if the price climbs higher than the strike price, you earn the difference minus the option cost.** (Here, you make a profit of ₹200)

|                |                    | **PRICE INCREASES** |            | **PRICE DECREASES** |            |
| -------------- | ------------------ | ------------------- | ---------- | ------------------- | ---------- |
| **Instrument** | **Money Invested** | **Profit/Loss**     | **Return** | **Profit/Loss**     | **Return** |
| Stock          | ₹1000              | ₹300                | **30%**    | -₹300               | **-30%**   |
| Option         | ₹100               | ₹200                | **200%**   | -₹100               | **-100%**  |
The key thing to note here is the percentage difference in returns between the profit and loss scenarios. Options provide **massive leverage**. With the same ₹1000, I can instead choose to buy 10 options and possibly make ₹2000 in profit or stand to lose the entire amount invested (₹1000). 
### Strike Price
The predetermined price at which the holder of a stock option has the right (call option) or obligation (put option) to buy or sell the underlying stock / financial instrument.
### In-the-Money (ITM) Option
An option is considered "in the money" if the current market price of the stock is already **favorable** for the option holder to exercise the option.
- For a **call option**, the stock price should be **higher** than the strike price.
- For a **put option**, the stock price should be **lower** than the strike price.
### Out-(Of)-the-Money (OTM) Option
An option is considered "out of the money" if the current market price of the stock is **not favorable** for the option holder to exercise the option.
- For a **call option**, the stock price should be **lower** than the strike price.
- For a **put option**, the stock price should be **higher** than the strike price.
# Advantages of Using Options
## Limited Downside Risk
Compared to buying the stock directly, options limit your potential losses. If you had bought RIL shares instead of the option and the price went down to ₹10, you'd lose ₹990. The downside risk with stocks is possibly infinite. With options, you only lose the premium, no matter how low the stock price goes. That said, most traders usually always place a stop-loss on the stocks they have in holding to artificially limit their downside. However, if the stock crashes in a single day, it might not be possible to trade at the stop loss and you might still stand to lose a lot more. With an option, you have a **fixed** downside. 
## Leverage
Options offer leverage, which means you can amplify your returns. If you had directly bought RIL at ₹1000 and the price went up to ₹1300, your investment would've grown by 30%. But with the option, you only paid ₹100 upfront. So your profit of ₹200 is actually a 200% return on your investment (₹200 profit / ₹100 option cost). However, remember that if the price falls, you lose your entire ₹100 premium, whereas owning the stock would only mean a loss equivalent to the fall in price. This is both useful and extremely risky if used as a gambling option. In practice, downside with stable stocks is not much compared to the 100% downside with options. 
## Hedging
Options can be a hedging tool to manage risk in your portfolio. They were originally created to mitigate risk, and can act like insurance for your stock holdings. To understand this better, let's walk through another toy example. 
### Toy Example
Imagine you're a big believer in HDFC Bank's long-term prospects, but you're worried about a potential market crash and want to hedge yourself against this risk. You currently hold 100 shares of HDFC Bank, currently priced at ₹2500 each (total investment: ₹2,50,000). To hedge against this risk, you **buy put options**. Think of a put option as an **insurance policy** for your stock. You can buy a put option that gives you the right, but not the obligation, to sell your HDFC Bank shares at a predetermined price (strike price) by a specific expiry date. For example, let's say you buy a put option with a strike price of ₹2500 and an expiry date of 3 months for a premium of ₹50 per share (total premium cost: ₹5000 for 100 shares). Now, let's do some PnL analysis. 
#### PnL ANALYSIS
- **SCENARIO 1: Market Crash**
	The worst happens. The market crashes, and HDFC Bank's share price drops to ₹2000. Without the options hedge, you would lose ₹$(2500 - 2000) \times 100$ = ₹50,000. But, because you hedged yourself by buying put options, you can exercise your put option and sell your 100 HDFC Bank shares at the predetermined strike price of ₹2500 each (total sell value: ₹2,50,000). Here's the PnL breakdown:
	- Loss from stock price drop => ₹50,000
	- Profit from put option: ₹2500 (strike price) $\times$ 100 shares - ₹2000 (cost of buying HDFC share now) $\times$ 100 shares - ₹5000 (premium) = ₹45.000
	By using the put option, you limited your loss to the cost of the premium (₹5000) instead of the entire ₹50,000 drop in stock price. 
	
- **SCENARIO 2: HDFC Stock Booms!**
	Thankfully, the market remains stable, and HDFC Bank's share price even goes up to ₹2800. In this case, you wouldn't exercise the put option since you can sell your shares at a higher price in the open market. The put option would simply expire, and you would lose the initial premium of ₹5000. But that's a small price to pay for the security the put option provided during those nervous market moments.
#### Key Takeaway
Options offer a flexible way to hedge your stock portfolio. While they won't completely eliminate risk, they can act as a safety net to minimize your losses in case the stock price takes a tumble. Think of it as setting a stop loss on your stock investments that you know you're guaranteed to bottom out at and you pay the insurance cost upfront. 
# Going Long vs Short on Options
## Call Options
### Long Call
Buying a call option grants you the **right, but not the obligation**, to purchase a stock at a specific price (strike price) by a certain date (expiry). You're essentially betting the stock price will rise above the strike price by expiry. It's a **bullish** strategy.
### Short Call
Selling a call option obligates you to sell the underlying stock at the strike price by expiry if the buyer exercises the option. You collect a premium upfront for taking on this obligation. This strategy is used when you're **neutral** or **slightly bullish** on the stock price, believing it won't significantly rise above the strike price by expiry. It carries **unlimited potential loss** if the stock price soars.
## Put Options
### Long Put
Buying a put option grants you the **right, but not the obligation**, to sell a stock at a specific price (strike price) by a certain date (expiry). You're essentially betting the stock price will fall below the strike price by expiry. It's a **bearish** strategy.
### Short Put
Selling a put option obligates you to buy the underlying stock at the strike price by expiry if the buyer exercises the option. You collect a premium upfront for taking on this obligation. This strategy is used when you're **bullish** on the stock's long-term prospects but believe it might dip in the short term. It offers **limited profit** but protects against a significant price decline (capped at the difference between the strike price and the purchase price).
# Settlement Methods
This is an exchange specific problem, but different exchanges tackle the method of future / option contract settlement in different ways. The two ways of dealing with this implementation detail are **cash settlement** and **physical delivery**.
## Cash Settlement
Cash settlement simplifies stock option contracts in India by eliminating the physical delivery of shares. 

>A **cash settlement** is a settlement method used in certain futures and options contracts where, upon expiration or exercise, the seller of the financial instrument does not deliver the actual (physical) underlying asset but instead transfers the associated cash position. - [Cash Settlement - Investopedia](https://www.investopedia.com/terms/c/cashsettlement.asp)

Imagine you believe RIL's share price will fall and decide to go short on a call option contract for 100 shares. Traditionally, exercising this option would require you to purchase those 100 shares on contract expiry. With cash settlement, you only deal with the price difference at expiry.

- **Profit Scenario:** Let's say you entered the contract when RIL was trading at ₹2,500 per share, with the contract quoting a predetermined purchase price of ₹2,800 per share. If the share price plummets to ₹2,000 at expiry, **the seller wouldn't have to arrange funds for the unwanted shares**. Instead, the long position (who bet on the price going up) would simply credit you with the difference – (₹2,800 - ₹2,000) $\times$ 100 shares = ₹30,000.
- **Loss Scenario:** Conversely, if RIL's share price skyrockets to ₹3,500, you wouldn't have to buy 100 shares at ₹3,500 either. You can just pay the difference: ₹70,000. 

It eliminates the hassle of physical share delivery, focusing solely on the price differential at expiry. This translates to a more efficient and safer market for stock exchanges as the risk they have to take up is less. Since the one taking the loss side of the trade doesn't need to have assets to buy the entire underlying stock and just needs to pay the difference, which is often much cheaper in comparison.

## Physical Delivery
Physical delivery in stock options is the traditional method where the underlying shares are physically exchanged upon expiry. While cash settlement simplifies things, physical delivery offers a different experience. Physical delivery adds an extra layer of complexity compared to cash settlement. It requires managing the logistics of share certificates and potential delivery costs.

The Indian National Stock Exchange (since July 2018 expiry contracts), uses physical delivery as the mode of settlement of futures contracts. 

>As stated in this [SEBI circular](https://www.sebi.gov.in/legal/circulars/apr-2018/review-of-framework-for-stocks-in-derivatives-segment_38629.html), starting from July 2018 expiry, F&O positions are being settled moved from cash settlement mode to compulsory physical delivery settlement in a phased manner. Starting from October 2019 expiry, all stock F&O contracts will be compulsorily physically settled. If you hold a position in any Stock F&O contract, at expiry, you will be required to give/take delivery of stocks. 
>
>- **In the money contracts (ITM)**
>	All ITM contracts which aren’t CTM will be mandatorily exercised by the exchange. This means that anyone holding an ITM option contract will receive/give delivery of stocks depending on whether one is holding call/put options. All the costs arising out of this delivery obligation will be applied to the client’s account.
>
>- **Out of the money contracts (OTM)**
>	All OTM options will expire worthless. There will be no delivery obligations arising out of this.
>
>**Spread and covered contracts**
>	Spread contracts that result in both – take and give delivery obligation will be netted off for the client. For example, you have a bull call spread of Reliance of the same expiry, a lot of long call options of strike 1300 and a lot of short call options of strike 1320 and the spot expires at 1330, this will result in a net-off and there won’t be any delivery obligation.
>	
>- [Policy on settlement of compulsory delivery derivative contracts — Update Oct 2019 - Zerodha](https://zerodha.com/z-connect/general/policy-on-settlement-of-compulsory-delivery-derivative-contracts-update-oct-2019)
>
>Physical delivery of stock options can potentially lead to systemic risk in the capital markets and pose a risk to traders. 
>
>**The physical delivery risk**
>	Like I mentioned earlier, if you hold stock futures or any in the money stock option at the close of expiry, you are assigned to give or take delivery of the entire contract value worth of stocks. Since the risk goes up with respect to the client not having enough cash to take delivery or stock to give delivery, the margins required to hold a future or short option position goes up as we get closer to expiry. Margins required are a minimum of 40% of the contract value for futures on the last day of expiry. For in the money long or buy option positions, a delivery margin is assigned from 4 days before expiry. The margins for in the money long options [go up from 10% to 50% of contract value](https://support.zerodha.com/category/trading-and-markets/margin-leverage-and-product-and-order-types/articles/policy-on-physical-settlement)—50% on the last two days of expiry. If the customer doesn’t have sufficient funds or stocks to give or take delivery, the broker squares off the contract. If the customer shows an intent to hold after the higher margin is blocked, it shows an intent to give or take delivery. 
>	
>	The risk though comes from out of the money options that suddenly turn in the money on the last day of expiry. No additional margins are blocked for OTM options in the expiry week, and when it suddenly turns in the money, a customer with small amounts of premium and no margin can get assigned to give or take large delivery positions, causing significant risk to the trader and the brokerage firm.
>	
>- [Physical delivery of stock F&O & their risks - Zerodha](https://zerodha.com/z-connect/general/physical-delivery-of-stock-fo-their-risks)

### A Case Study on the Risk Involved in Physical Delivery Settlement
>This happened on Dec expiry, Thursday 30th Dec 2021. Shares of Hindalco closed at Rs 449.65 at expiry. This meant that the Hindalco 450 PE expired just in the money by 35 paise. This meant that everyone who had bought this 450 PE and held it at the expiry was required to deliver Hindalco stock—1075 shares for every 1 lot of Hindalco held. 
>
>This is what happened to Hindalco shares on 30th Dec:
>
>![pasted-image-20240312051304](/images/pasted-image-20240312051304.webp)
>
>The stock was above Rs 450 for most of the expiry day and even a few days prior to it. Since it was out of money, no additional physical margins would have been charged, and everyone holding this strike would have assumed that it would expire out of the money. In all likelihood, everyone who held this put option would have written off the trade as a loss and assumed that the maximum loss would be limited to the premium paid. 
>
>So at 3 pm, when the Hindalco stock price went below 450, this was how the marketdepth looked like. Those who realized that this option would expire in the money trying to exit, but with no buyers to be able to do so even at Rs 0.05 when the intrinsic value of the strike was Rs 0.35.
>
>Everyone holding long puts would have been forced assigned to deliver Hindalco shares. 1 lot of Hindalco = 1075 shares = ~Rs 5lks contract value. Customers who had bought put options with a few thousand rupees were potentially required to deliver tens of lakhs of Hindalco stock. Failing to deliver would have meant short delivery. The [consequences of short delivery](https://support.zerodha.com/category/trading-and-markets/trading-faqs/general/articles/what-is-short-delivery-and-what-are-its-consequences) are losses in terms of auction penalty, apart from the market risk of Hindalco stock price going up from the close of expiry to the auction date. Hindalco stock was up 5% already on Friday, and the auction happens on T+3 days or on Tuesday, and assuming the stock price doesn’t go up further, that is still a whopping loss of Rs 25 (5% of Hindalco) for Rs 0.35 worth of premium at market close. 
>
>If this wasn’t puts but calls, there wouldn’t be a short delivery risk, but there would still be a market risk that the customer would be exposed to from the close of expiry to when the customer can sell the stock. But in case of buy delivery (Buy futures, buy calls, short puts), the stock can be sold the next day itself and hence there is no marked to market risk of 3 days. The risk is exponentially more in the case of F&O positions that can lead to short delivery (Short futures, sell calls, buy puts). 
>
>The risk exists with futures, short options, and buy ITM options as well. But since there are sufficient margins that also go up closer to expiry, a customer who provides additional margin is willingly holding the position, or else the position is squared off. Because there are no additional physical delivery margins for OTM options and because most option buyers think that when they buy options the maximum they can lose is equal to the premium paid and take no action, the risks go up for the entire ecosystem.
>
>Apart from the risk to the trader, this can be a systemic issue because if a customer account goes into debit, the liability falls on the broker. A large individual trader or group of customers of a broker could potentially go into a large enough debit to bankrupt the brokerage firm and, in turn, put the risk on other customers as well. Stocks can move drastically on expiry day, and out of the money, option contracts can suddenly move just in the money with no liquidity to exit, making it impossible for brokerage risk management teams to do anything. All option contracts are settled based on the last 30 min average price of the underlying stock and not the last traded price, making this even trickier without knowing if a CTM option strike will actually close in the money or not until post the market closing. And like I explained earlier, the risk is not just in terms of the auction and short delivery, but also marked to market risk for 3 days.
>
>Forcing traders to give or take large delivery positions can potentially be misused by large traders or operators wanting to manipulate the price movement of stocks.
>- [Physical delivery of stock F&O & their risks](https://zerodha.com/z-connect/general/physical-delivery-of-stock-fo-their-risks)

# References
1. [The Trillion Dollar Equation](https://www.youtube.com/@veritasium)
2. [What is Zerodha's policy on the physical settlement of equity derivatives on expiry?](https://support.zerodha.com/category/trading-and-markets/margins/margin-leverage-and-product-and-order-types/articles/policy-on-physical-settlement)
3. [Cash Settlement - Investopedia](https://www.investopedia.com/terms/c/cashsettlement.asp)
4. [Physical Delivery - Investopedia](https://www.investopedia.com/terms/p/physicaldelivery.asp)
5. [Policy on settlement of compulsory delivery derivative contracts — Update Oct 2019 - Zerodha](https://zerodha.com/z-connect/general/policy-on-settlement-of-compulsory-delivery-derivative-contracts-update-oct-2019)
6. [Physical delivery of stock F&O & their risks - Zerodha](https://zerodha.com/z-connect/general/physical-delivery-of-stock-fo-their-risks)


---

## Related Reading

- [Covered Calls Strategy](/blog/covered-calls-strategy)
- [Efficient-Market-Hypothesis](/blog/efficient-market-hypothesis)
