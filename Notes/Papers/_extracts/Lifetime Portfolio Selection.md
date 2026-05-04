# Lifetime Portfolio Selection

**Source:** lifetime_portfolio_selection.pdf

---

## Lifetime Portfolio Selection: A Simple Derivation 

Gordon Irlam (gordoni@gordoni.com) 

July 9, 2018 

## **Abstract** 

Merton’s portfolio problem involves finding the optimal asset allocation between a risky and a risk free asset, and the optimal consumption over time, so as to maximize aggregate utility of consumption. This paper gives a simple and straightforward solution to Merton’s portfolio problem for lognormally distributed returns and isoelastic utility in the discrete and continous time cases. 

## **1 Introduction** 

Given a risk free asset and a risky, or volatile asset, Merton’s portfolio problem involves determine the asset allocation and consumption that will maximize lifetime utility. For lognormally distributed returns, constant relative risk aversion, and a fixed finite or infinite lifespan, Merton’s portfolio problem has an analytical solution. This was shown by Merton (1969) in the continuous time case. Samuelson (1969) studied the discrete time case, and determined the optimal consumption in the discrete time case. However, the optimal asset allocation for the discrete time case was not explored analytically. Nor has the relationship between the discrete time case and the continuous time case been explored. 

Despite the importance of the solution to Merton’s portfolio problem to the field of finance, it is rarely covered in introductory finance texts such as Bodie et al. (2009), and is primarily studied within economics, not finance. Part of the reason for this may be because introductory finance courses normally deal with discrete rather than continuous time, and also because Merton solved the problem by making inspired guesses as to the solution of systems of simultaneous second order differential equations. 

Consequently there is a need for a solution to Merton’s portfolio problem in the discrete time case that is straightforward, and does not involving the simultaneous solution of system of second order differential equations. In addition there is a need to explore optimal asset allocation in the discrete time case, and to see how the discrete time case maps onto the continuous time case as the time interval goes to zero. 

1 

## **2 Preliminaries** 

## **2.1 The lognormal distribution** 

Let **Z** represent the return distribution. As a result of the central limit theorem and the multiplicative nature of returns, returns from the stock market approximate the lognormal distribution. The lognormal distribution is given by, 

**==> picture [320 x 15] intentionally omitted <==**

where _µ_ and _sigma_ are the mean and standard deviation of the underlying normal distribution, and **N** (0 _,_ 1) is the standard normal, or Gaussian, distribution. 

Denote the mean by _m_ , and the standard deviation, or volatility, by _s_ . Here, the mean _m_ denotes the multiplicative return factor, so a 5% increase in value would have the value 1 _._ 05. 

Assuming lognormality, 

**==> picture [272 x 37] intentionally omitted <==**

Two useful facts regarding the lognormal distribution are, 

**==> picture [349 x 15] intentionally omitted <==**

and if **E** is the expectation operator, 

**==> picture [362 x 36] intentionally omitted <==**

both of which can be seen from the definition of the lognormal distribution. 

## **2.2 Geometric Brownian motion** 

Geometric Brownian motion describes a continuous process that exhibits lognormality over different time scales _τ_ . It is common to define, 

**==> picture [263 x 25] intentionally omitted <==**

where _α_ is the geometric Brownian motion drift parameter (sometimes confusingly also referred to as _µ_ ), so that, 

**==> picture [336 x 12] intentionally omitted <==**

Geometric Brownian motion satisfies, 

**==> picture [261 x 29] intentionally omitted <==**

2 

where _α[′]_ and _σ[′]_ are the underlying lognormal distribution parameter values for arbitrary timescale _τ_ , and _α[′′]_ and _σ[′′]_ are the parameter values for the unit timescale, which is commonly 1 year. These equations can be derived by viewing geometric Brownian motion as the product (or sum in log space) of a large number of independent variables and the central limit theorem. 

## **2.3 Geometric asset combination** 

Let _r_ be the risk free rate, that is the return on cash, or some other risk free asset, on an annual or other time period basis. In accordance with convention, r is defined as an additive quantity, so a return of 2%, would be represented as the value 0 _._ 02. 

Let _α[′]_ and _σ[′]_ describe describe the risky asset which exhibits geometric Brownian motion. Let _π_ be the risky asset fraction. 

It is common to combine the returns of assets additively. This is done when allocations to the asset are set at some point in time and then allowed to wander in accordance with the returns received. 

It is less common to combine the returns of assets multiplicatively. This should be done if the allocations to the assets are continuously adjusted in order to maintain a target asset allocation. This is is done here. An easy way of thinking about this is to consider the returns to be an interleaved product, with the risky asset factor being received _π_ of the time, and the risk free factor being received 1 _− π_ of the time. Let _µv_ and _σv_ describe the portion of the return from the risky, or volatile, asset. The resulting return is then, 

**==> picture [374 x 50] intentionally omitted <==**

which is lognormal. Comparing to equation gives 1, 

**==> picture [301 x 29] intentionally omitted <==**

and thus, 

**==> picture [386 x 41] intentionally omitted <==**

## **2.4 Utility** 

Utility defines the desirability of different levels of consumption _C_ . 

Only utility with Constant Relative Risk Aversion (CRRA) will be considered here. This is termed isoelastic utility. It is defined by, 

**==> picture [269 x 27] intentionally omitted <==**

3 

where _γ_ is termed the coefficient of relative risk aversion. The absolute value of utility doesn’t matter, only differences in value, so sometimes you will see the above equation written as 

**==> picture [87 x 28] intentionally omitted <==**

so that _U_ (1) = 0. 

Marginal utility is the incremental value of an incremental unit of consumption, 

**==> picture [267 x 12] intentionally omitted <==**

Confusingly, sometimes the symbol _γ_ denotes 1 _− γ_ . 

## **2.5 Notation** 

In this paper there are three sets of symbols. The symbols adorned by ” represent given values for the unit timescale. The symbols adorned by ’ represent given values for the _τ_ timescale. And the unadorned symbols represent actual allocations for the _τ_ timescale. 

I don’t normally speak of _r[′]_ since, 

**==> picture [28 x 10] intentionally omitted <==**

## **3 The discrete time period case** 

The discrete time period version of Merton’s portfolio problem is as follows. Over a series of time periods, _t_ = 0 _,_ 1 _, ...T_ , for an investment between a risk free asset with return _r_ and a risky asset that exhibits lognormal returns for each time period described by _α[′]_ and _σ[′]_ , to determine the continuously reblanced risky allocation fraction _π_ and the consumption amount _c_ ( _t_ ), so as to maximize expected aggregate CRRA utility of consumption for a coefficient of relative risk aversion _γ_ . 

Let _c_ ( _t_ ) be the fraction of wealth consumed at time _t_ . Wealth starts at some given value _W_ (0) at time _t_ = 0 and evolves according to the wealth equation, 

**==> picture [302 x 11] intentionally omitted <==**

for some returns distribution **Z** . 

## **3.1 Asset allocation** 

Consider a single time period. 

Later, in section 3.2.2 we will see how maximizing utility of terminal wealth for the time peirod is the same as maximizing utility of consumption, but for now take it as given that maximizing utility of terminal wealth is a reasonable thing to want to do. 

4 

We seek to maximize expected utility of wealth, _W_ ( _t_ + 1), for returns distribution **Z** given given by equation 1. 

**==> picture [354 x 198] intentionally omitted <==**

Solving by finding where the derivative with respect to _π_ equals 0 gives, 

**==> picture [300 x 51] intentionally omitted <==**

Note that the solution is independent of the time period. 

It is important to note that even though utility is assessed once at the end of a time period, the asset allocation normally needs to be continuously maintained over the entire time period at the target asset allocation specified by equation 14. As a result of this continuous rebalancing it is impossible to get “wiped out” despite the possible recommended use of leverage by equation 14. The use of daily resetting leveraged ETFs is closer to what is required than investing once on margin for an entire time period. 

## **3.2 Consumption** 

This section follows the work of Samuelson. 

We seek to determine the optimal consumption amount for over a series of discrete time periods, _t_ = 0 _,_ 1 _, ...T_ . We do this by maximizing the aggregate utility for time periods _t, t_ + 1 _, ...T_ , denoted _J_ ( _t, W_ ( _t_ )), at _t_ = 0. _J_ is defined by 

**==> picture [381 x 34] intentionally omitted <==**

5 

Define the certainty equivalence fraction _b_ ( _t_ ) by, 

**==> picture [298 x 25] intentionally omitted <==**

That is _b_ ( _t_ ) is the consumption fraction that gives the same expected utility in a single time period as the average expected utility over periods _t, t_ + 1 _, ...T_ . 

For the final time period, 

**==> picture [78 x 12] intentionally omitted <==**

Suppose _b_ ( _t_ + 1) known and independent of wealth _W_ ( _t_ + 1). 

For a given _W_ ( _t_ ) we seek to maximize _J_ as follows, 

**==> picture [118 x 49] intentionally omitted <==**

**==> picture [414 x 27] intentionally omitted <==**

_⇒_ **E** ⟨ _U[′]_ ( _c_ ( _t_ ) _W_ ( _t_ )) _W_ ( _t_ ) _−_ ( _T − t_ ) _U[′]_ ( _b_ ( _t_ + 1) _W_ ( _t_ )(1 _− c_ ( _t_ )) **Z** ) _b_ ( _t_ + 1) _W_ ( _t_ ) **Z** ⟩ = 0 Using the definition of marginal utility, equation 12, this implies, 

**==> picture [350 x 14] intentionally omitted <==**

For future use note, 

**==> picture [363 x 15] intentionally omitted <==**

Defining, 

**==> picture [274 x 19] intentionally omitted <==**

Then raising 17 to the power _[−] γ_[1][gives,] 

**==> picture [326 x 63] intentionally omitted <==**

Now consider _J_ . Using equation 16 and 13, as before, 15 becomes, 

**==> picture [318 x 12] intentionally omitted <==**

Using the definition of utility 11, 

**==> picture [352 x 28] intentionally omitted <==**

6 

By 18, 

**==> picture [419 x 105] intentionally omitted <==**

Comparing this to the definition of the _b_ ( _t_ ), equation 16, gives, 

**==> picture [134 x 17] intentionally omitted <==**

which is independent of wealth. 

So, according to equation 20, 

**==> picture [83 x 30] intentionally omitted <==**

which is also independent of wealth, as per Samuelson. 

Also, as per Samuelson, 

**==> picture [297 x 85] intentionally omitted <==**

Hence the problem is solved, since **E** ⟨ **Z**[1] _[−][γ]_[⟩] , and thus _a_ , is determined for the lognormal distribution by equation 4. 

## **3.2.1 time horizon** 

In the limit as as _T →∞_ , from 22 we approach the steady state given by, 

**==> picture [267 x 71] intentionally omitted <==**

7 

## **3.2.2 Maximizing utility of wealth** 

By equations 21 and 11, 

**==> picture [134 x 12] intentionally omitted <==**

but for a given _t_ , _c_ ( _t_ ) _[−][γ]_ , is a constant. This justifies our maximization of utility of wealth rather than utility of consumption in the single time period case earlier in section 3.1. The consumption derivation did not depend on the asset allocation result, so there is no problem of assuming what is proved. 

## **4 The continuous time case** 

Suppose the risky asset exhibits geometric Brownian motion in accordance with equations 7 and 8 based on unit time period parameters _α[′′]_ and _σ[′′]_ . In addition suppose, 

**==> picture [276 x 13] intentionally omitted <==**

for the unit timescale risk free rate _r[′′]_ . Then we are concerned with the limits for _π_ and _c_ ( _t_ ) as _τ →_ 0. 

## **4.1 Asset allocation** 

The optimal asset allocation in the continuous time case is given by, 

**==> picture [375 x 85] intentionally omitted <==**

## **4.2 Consumption** 

First compute _a_ assuming lognormality, and then using equation 23 compute the limit of the consumption rate at time _t_ , _ccts_ ( _t_ ), as _τ →_ 0. 

8 

**==> picture [442 x 170] intentionally omitted <==**

Thus, 

**==> picture [294 x 125] intentionally omitted <==**

Replacing ordinal time _t_ by continuous time _τt_[,][and][single][period][consumption] _[c]_[(] _[t]_[)][by][the][con-] sumption rate, _ccts_ ( _t_ ) = _[c]_[(] _τ[t]_[)][,][and][taking][the][limit][as] _[τ][→]_[0,] 

**==> picture [97 x 48] intentionally omitted <==**

As per Merton. 

## **4.2.1 time horizon** 

**==> picture [274 x 69] intentionally omitted <==**

9 

Replacing single period consumption _c_ ( _t_ ) by the consumption rate, _ccts_ = _[c]_[(] _τ[t]_[)][,][and][taking][the][limit] as _τ →_ 0, 

**==> picture [58 x 35] intentionally omitted <==**

## **5 Conclusion** 

I have presented a straightforward solution of Merton’s portfolio problem for both the discrete and continuous time cases. 

## **6 Acknowledgments** 

I am grateful to Michael Moore for reviewing this manuscript. 

## **References** 

Bodie, Z. et al. (2009). _Investments_ . Tata McGraw-Hill Education. 

Merton, R. C. (1969). Lifetime portfolio selection under uncertainty: The continuous-time case. _The review of Economics and Statistics_ , pages 247–257. 

Samuelson, P. A. (1969). Lifetime portfolio selection by dynamic stochastic programming. _The Review of Economics and Statistics_ , 51(3):239–246. 

10 

