# Mc Final Draft

**Source:** MC_final_draft.pdf

---

## **Monte Carlo expected wealth and risk measure trade-off portfolio optimization** _[∗]_ 

Raino A. E. M¨akinen _[†]_ and Jari Toivanen _[‡]_ 

**Abstract.** A multi-period portfolio optimization is described with Monte Carlo sampled risky asset paths under realistic constraints on the investment policies. The proposed approach can be used with various asset and risk models. It is flexible as it does not require dynamic programming or any transformations. As examples, the variance and semivariance risks are considered leading to mean-variance and mean-semivariance formulations, respectively. A quasi-Newton method with an adjoint gradient computation can solve the resulting optimization problems efficiently. Numerical examples show efficient frontiers together with optimal asset allocations computed for mean-variance and meansemivariance portfolios with two and five assets. 

- **Key words.** dynamic portfolio management, mean-variance optimization, mean-semivariance optimization, constrained optimization, Monte Carlo simulation 

## **AMS subject classifications.** 65C05, 90C31, 90C55, 91G10, 91G60 

**1. Introduction.** The single-period mean-variance optimization introduced by Markowitz [23] is the classical way to select investment portfolios. Dynamic and multi-period generalization of this approach offers a more realistic model for portfolios as they can incorporate more constraints for investments as well as time and wealth-dependent asset allocations. These generalizations offer robust asset allocations which are insensitive to model misspecification as was shown by van Staden et al. [29]. Continuous dynamic asset allocation problems have known analytical solutions with certain constraints. For example, Bielecki et al. [3] derive a solution when bankruptcy is not allowed and when shorting selling is not allowed Li et al. [22] give an explicit solution. When discrete re-balancing is performed and realistic constraints are imposed on the portfolios an analytical solution is not available in general and portfolio strategies need to be found numerically. This paper considers this case. 

Brandt et al. [4] consider Monte Carlo simulation-based discrete-time portfolio allocation problems. While their approach is fairly flexible it assumes the asset allocation to be independent of current wealth. This is restrictive and leads to suboptimal investment strategies. Instead, it is preferable to consider time and wealth-dependent asset allocations to maximize the final wealth under a given level of risk aversion. These are called pre-commitment strategies by Basak et al. [2] which are typically not time-consistent; see [28], for example. In the case of the mean-variance optimization, there is an induced objective function for which the solution is time-consistent [11], [26], [31]. Cong et al. [6] and [7] construct these precommitment strategies based on Monte Carlo simulated risky asset paths. Their approach drives a sub-optimal multi-stage strategy to an optimal one using backward recursive programming. They perform the common transformation of the mean-variance problem with nonlinear conditional variance to a linear-quadratic (LQ) problem by an embedding technique 

> _∗_ Submitted to the editors DATE. 

> **Funding:** This work was funded by the Academy of Finland under project no. 295897. 

> _†_ Faculty of Information Technology, University of Jyv¨askyl¨a, Finland (raino.a.e.makinen@jyu.fi). 

> _‡_ Faculty of Information Technology, University of Jyv¨askyl¨a, Finland (jari.a.toivanen@jyu.fi). 

**1** 

**R.A.E. MAKINEN[¨] AND J. TOIVANEN** 

**2** 

by Li et al. [21]. Another approach to construct pre-commitment strategies is to formulate a Hamilton–Jacobi–Bellman (HJB) partial differential equation for the strategy. This is an elegant approach that avoids sampling risky asset paths, but its numerical implementation is fairly cumbersome and, unlike Monte Carlo-based methods, it does not scale well for multiple risky assets. This HJB PDE approach has been considered by Wang et al. [32], Dang et al. [8], and Forsyth et al. [12], for example. 

Recently, several studies including [5],[15],[25],[24], [30], have proposed neural networks (NNs) for financial optimization problems without relying on dynamic programming. These studies describe the control by a NN and the loss function is given by the financial objective. The resulting NN training problem is solved using the usual stochastic gradient methods in this context. Here we propose a similar, non dynamic programming based approach describing the control by a more traditional polynomial interpolation similar to many dynamic programming-based financial optimization studies including [6], [7], [8], [12], [32]. We solve the resulting optimization problems by a quasi-Newton optimization method. The proposed approach has two benefits: polynomial interpolations have well-established approximation convergence properties and the quasi-Newton methods have fast convergence leading to shorter computation times. 

This paper describes an optimization approach based on Monte Carlo simulated risky asset paths. The optimization is performed directly to the objective function given by the desired combination of the expected final wealth and the risk measure without any transformation. This leads to a nonlinear optimization problem for time and wealth-dependent asset allocations for which it is easy to impose constraints. This proposed approach is flexible and can be easily generalized for many cases. 

Quasi-Newton methods offer an efficient way to solve the resulting optimization problems. Particularly methods based Broyden–Fletcher–Goldfarb–Shanno (BFGS) approximation [10] of the Hessian matrix have been shown to be efficient and are very popular. These methods require the gradient of the objective function with respect to the optimization variables, that is, the time-wealth-dependent asset allocations. The adjoint technique gives an efficient way to compute this gradient. With Monte Carlo simulations Giles [13] and [14] describe this technique. Kaebe et al. [17] employ it to calibrate a market model. To our knowledge in the scientific literature, these techniques have not been used before to construct asset allocation strategies. Instead of applying automatic differentiation to compute the gradient, we derive an analytical expression for the gradient, which can be used for the efficient implementation of the method. The efficient frontier of possible portfolios is obtained by optimizing the portfolios with varying levels of investor risk aversion. We present numerical examples for the case of one and four risky assets. 

The outline of this paper is the following: Section 2 describes the mean wealth-risk measure optimization problem. Section 3 gives the details of Monte Carlo simulation of the wealth as well as computation of the variance and semivariance of the final wealth which are the risk measures studied in this paper. Section 4 proposes a numerical solution method for the resulting optimization problem. Section 5 presents numerical examples of portfolio optimization. Section 6 gives the conclusions. 

**MONTE CARLO PORTFOLIO OPTIMIZATION** 

**3** 

**2. Mean wealth-risk measure portfolio optimization.** Let there be _I_ + 1 investment assets. Let the _i_ :th asset _S[i]_ follow the stochastic differential equation 

(2.1) _dS[i]_ = _µ[i] S[i] dt_ + _σ[i] S[i] dZ[i] ,_ 

where _µ[i]_ is the growth rate, _σ[i]_ is the volatility, and _Z[i]_ is the Wiener process. The correlation between these processes is specified by the correlation matrix. When the volatility is zero the asset is riskless. 

The accumulated total wealth _W_ : [0 _, T_ ] _→_ R follows the stochastic differential equation 

**==> picture [324 x 53] intentionally omitted <==**

where _π_ is a contribution rate, _p[i]_ = _p[i]_ ( _t, W_ ) is the proportion of the wealth invested in the _i_ :th asset _St[i]_[at][time] _[t]_[,][and] _[w]_[0][is][the][initial][wealth.][The][last][asset] _[S][I]_[+1][is][assumed][to][be] riskless, that is, _σ[I]_[+1] = 0 and _r_ := _µ[I]_[+1] is the riskless interest rate. Thus, the number of risky assets is _I_ . The proportion of the wealth invested in the riskless asset is _p[I]_[+1] = 1 _−_[�] _[I] i_ =1 _[p][i]_[.] Eliminating the proportion of the riskless asset from (2.2) we obtain the equivalent SDE that is better suited for computations: 

**==> picture [357 x 53] intentionally omitted <==**

Let _P_ = ( _p_[1] _· · · p[I]_ ) _[T]_ contain the proportions _p[i]_ , _i_ = 1 _, . . . , I_ . Furthermore, let E[ _WP_ ( _T_ )] and RM[ _WP_ ( _T_ )] denote the expected value and risk measure for the final wealth _W_ ( _T_ ) when following an investment strategy _P_ . Typical risk measures are the variance Var[ _·_ ] and the semivariance Semivar[ _·_ ]. The semivariance is a special case of downside risk models [9]. Under a discrete time investment strategy, it leads to a well-posed problem [16]. The aim is to find a strategy _Pλ[∗][∈P][ad]_[such][that] 

**==> picture [328 x 18] intentionally omitted <==**

where _λ >_ 0 describes the investor’s risk aversion which grows with _λ_ . Varying _λ_ gives the Pareto optimal portfolios. The set _Pad_ defines allowed strategies. Forbidding short selling leads the lower bound _p_ min for the proportions _p[i]_ , _i_ = 1 _, . . . , I_ , to be zero. Let _p_ max be the allowed amount of leverage. For example, allowing a 2:1 leverage ratio corresponds to _p_ max = 2, while no leverage corresponds to _p_ max = 1. The proportions have to satisfy _p[i] ≤ p_ max. Furthermore, the sum of the proportions has to be at most _p_ max, that is,[�] _[I] i_ =1 _[p][i][≤][p]_[max][.] 

**3. Monte Carlo simulation of wealth.** For the moment, let the investment policy _P_ be given and fixed. We approximate the solution of the stochastic differential equation (2.3) by using the classical Euler–Maruyama scheme. Let ∆ _t_ = _T/N_ be the time step, and let 

**R.A.E. MAKINEN[¨] AND J. TOIVANEN** 

**4** 

_**Z** ∈_ R _[K][×][I][×][N]_ be an array of normally distributed pseudorandom numbers. In this paper, _K_ is the number of Brownian paths. 

Let _Wk[n]_[denote the] _[ k]_[:th random approximation of] _[ W]_[(] _[n]_[∆] _[t]_[).][These values at the] _[ n]_[:th time] step are collected to the vector _**W**[n]_ = ( _W_ 1 _[n][· · ·][ W][ n] K_[)] _[ ∈]_[R] _[K]_[.][One][step][of][the][numerical][scheme] reads 

**==> picture [421 x 34] intentionally omitted <==**

where the vectors _**P**[n] i_[(] _**[W]**[ n]_[)][contain][the][proportions][evaluated][at][(] _[t][n][, W] k[ n]_[)][for] _[k]_[=][1] _[, . . . , K]_[,] i.e. _**P**[n] i_[(] _**[W]**[ n]_[) =] � _p[i]_ ( _tn, W_ 1 _[n]_[)] _[ · · ·][ p][i]_[(] _[t][n][, W] K[ n]_[)] �. 

Moreover, the vector _**Z**[n] i[∈]_[R] _[K]_[contains][the] _[K]_[random][numbers][for][the] _[i]_[:th][asset][at][the] time step _n_ , and _⊙_ is the elementwise vector product operator.[1] This can be expressed in a more compact form 

**==> picture [24 x 12] intentionally omitted <==**

**==> picture [151 x 13] intentionally omitted <==**

where 

**==> picture [24 x 11] intentionally omitted <==**

**==> picture [307 x 33] intentionally omitted <==**

The expected final wealth is given by 

**==> picture [282 x 15] intentionally omitted <==**

Its variance and semivariance are given by 

**==> picture [24 x 12] intentionally omitted <==**

**==> picture [259 x 35] intentionally omitted <==**

respectively. Note that unlike here sometimes the semivariance is defined with the inverse of the number of samples below the expected value instead of the inverse of the number of all samples. 

**4. Fully discrete optimization problem.** Until now the policy _P_ has been a continuous vector-valued function of time and wealth. Next, we introduce a parameterized strategy _Ph_ = ( _p_[1] _h[· · ·][ p][I] h_[),][where][each][proportion][depends][only][on][a][finite][number][of][parameters.] Consider the _M × N_ grid _G_ := _{_ 0= _W_ 1 _<W_ 2 _<...<WM_ = _W_ max _} × {_ 0= _t_ 0 _<t_ 1 _<...<tN −_ 1 _}_ , where _tn_ = _n_ ∆ _t_ and _W_ max is large enough such that _Wk_ ( _t_ ) _∈_ [0 _, W_ max] for all paths. Let _{ψm,n_ ( _t, W_ ) _}_ be the set of piecewise bilinear _C_[0] -continuous basis functions associated with _G_ , where each _ψm,n_ has the value one at ( _tm, Wn_ ) and zero elsewhere. Moreover let us use the following notation for a set of _I·M ·N_ parameters 

**==> picture [295 x 14] intentionally omitted <==**

> 1Here we adopt the Matlab style notation: If _**x** ,_ _**y** ,_ _**z** ∈_ R _n, β∈_ R then _**z**_ = _**x** ⊙_ _**y**_ + _β_ means _zi_ = _xiyi_ + _β, i_ =1 _, ..., n_ . 

**MONTE CARLO PORTFOLIO OPTIMIZATION** 

**5** 

Now, we can define the following discretized proportions of the strategy _Ph_ : 

**==> picture [183 x 33] intentionally omitted <==**

The parameterized and discretized optimization problem then reads 

(4.1) 

**==> picture [98 x 17] intentionally omitted <==**

where the discrete objective function is defined by 

**==> picture [342 x 14] intentionally omitted <==**

The set of admissible parameters in (4.1) is defined by 

**==> picture [351 x 14] intentionally omitted <==**

where the lower bound vector Pmin and the upper bound vector Pmax result from the lower and upper bounds for the proportions _p[i]_ , _i_ = 1 _, . . . , I_ , and the linear constraint _**A**_ P _≤_ _**b**_ results from the limit for the leverage. The definitions of these vectors and the matrix _**A**_ are given by Pmin = _p_ min _**e** I·M ·N_ , Pmax = _p_ max _**e** I·M ·N_ , _**A**_ = _**I** M ·N ⊗_ _**e**[T] I_[,][and] _**[b]**_[ =] _[ p]_[max] _**[e]**[M][·][N]_[,][where] _**e** n_ = (1 _· · ·_ 1) _[T] ∈_ R _[n]_ , _In_ is the _n×n_ identity matrix, and _⊗_ is the Kronecker product operator. 

To efficiently utilize gradient-type methods for the numerical solution of (4.1), it is essential to have the exact gradient _∇_ P _Jλ_ ( _**W**[N]_ (P)) rather than relying on its finite difference approximation. Exact gradient computations can be performed manually or with the assistance of automatic differentiation tools readily accessible in popular software libraries for machine learning and artificial intelligence, such as TensorFlow [1]. In what follows, we derive a concise expression for the gradient using the classical adjoint approach. Following that, we provide a brief overview of the advantages and challenges associated with the application of automatic differentiation tools. The partial derivatives of the objective function with respect to the parameters defining the discrete investment strategy can be computed using the adjoint formulation [13] holding fixed the randomly generated Brownian path increments for every particular path calculation. In what follows, we assume a general parametrization of _p[i] h_[=] _[p][h]_[(] _**[p]**[i][, t, W]_[),] _**[p]**[i][∈]_[R] _[M][·][N]_[,][that] is, the calculations are not restricted to any particular parametrization. We assume that the mapping P _�→_ _**W**[N]_ is smooth and derive formally the explicit formula for _[∂] ∂p[J] j[λ]_[,][where] _[p][j]_[is][a] component of P. 

Using the notations of Section 3 we can express the Monte Carlo simulation of the wealth as the state problem 

**==> picture [349 x 34] intentionally omitted <==**

Define the Lagrangian with a set of Lagrange multipliers Y := _{_ _**Y**_[0] _, ...,_ _**Y**[N] }_ : 

**==> picture [435 x 33] intentionally omitted <==**

**R.A.E. MAKINEN[¨] AND J. TOIVANEN** 

**6** 

As W := _{_ _**W**_[0] _, ...,_ _**W**[N] }_ satisfies (4.4) for all P, we may choose Y freely. We have _Jλ_ ( _**W**[N]_ ) = _Lλ_ (P _,_ W _,_ Y) and 

**==> picture [434 x 66] intentionally omitted <==**

Above we have denoted 

**==> picture [351 x 97] intentionally omitted <==**

Rearranging terms in (4.6) gives 

**==> picture [433 x 72] intentionally omitted <==**

If we choose Y to be the solution of the adjoint model 

**==> picture [418 x 42] intentionally omitted <==**

then only the first term in (4.8) is nonzero and we avoid calculating _[∂] ∂p_ _**[W]** j[ n]_[.][Thus,][we][finally] have 

**==> picture [312 x 33] intentionally omitted <==**

_Remark_ 4.1. In the derivation of the formulas (4.9), (4.10), the part depending on the specific parametrization is contained in the derivatives appearing in (4.7). The continuous piecewise linear parametrization of the investment policy, _ph_ is not continuously differentiable with respect to _W_ . Thus, it may happen that (4.10) only gives a directional derivative. However, it is well-known that standard quasi-Newton methods are relatively robust and efficient even in the nonsmooth case. For more discussion on that topic, see [19], [20], for example. 

**MONTE CARLO PORTFOLIO OPTIMIZATION** 

**7** 

_Remark_ 4.2. When it comes to using graph-based automatic differentiation tools like TensorFlow for solving large-scale stochastic optimal control problems, researchers noted, as seen in [18], that these tools, while optimized for training neural networks, face significant challenges due to high memory and initialization requirements. For this reason, it is preferable to use a manually computed gradient like the one in (4.10) when the number of parameters is large. 

A ”common subexpression elimination technique” introduced in [18] selectively uses the automatic differentiation leading to a comparable efficiency with a manually computed gradient. Applying this technique to our case would involve using the automatic differentiation to calculate derivatives _∇_ _**W** Jλ_ , _∂∂_ _**WS**_[,][and] _[∂] ∂_ _**[S]**_ P[in][equations][(4.9)–(4.10)][instead][of][applying][it] directly to the black box P _�→ Jλ_ (P). 

**5. Numerical portfolio optimization examples.** In this section, we present two examples dealing with one risky asset and one example dealing with four risky and correlating assets. The computations have been performed using Matlab [27] with the gradient computations implemented using (4.10). The final time and time step for Monte Carlo simulations is _T_ = 20 and ∆ _t_ = 0 _._ 25, respectively, leading to _N_ = 80 time steps. In this section, we have used _K_ = 1000000 paths. For the strategy _p_ there are _M_ = 31 grid points in the _W_ direction with the last grid point at _W_ max = 30 and the grid is refined for small _W_ values. In practical computations, we employ the constant approximation _p_ ( _tn, x_ ) = _p_ ( _tn, W_ max) _, x>W_ max to ensure the use of a reasonably small constant _W_ max. 

In optimization, the quasi-Newton method with the BFGS approximation of the Hessian matrix was used. To guarantee a robust convergence of the optimizer for all the sampled _λ_ values, we used 50 iterations for optimizations with one risky asset and 250 iterations for optimizations with four risky assets. The likely reason that a larger number of required iterations in the case of the higher-dimensional problem is not the larger number of parameters, but the multiple correlated investment assets. 

**5.1. Portfolio with one risky asset and no leverage.** We start by considering a pension plan example with one risky asset, that is, _I_ = 1 with the parameters: the interest rate _r_ = 0 _._ 03, the volatility of the risky asset _σ_[1] = 0 _._ 15, the growth rate of the risky asset _µ_[1] = 0 _._ 0795, the contribution rate _π_ = 0 _._ 1, and the initial wealth _w_ 0 = 1. Short selling is forbidden leading to _p_ min = 0. Borrowing is not allowed leading the maximum proportion of the wealth invested in the risky asset to be _p_ max = 1. 

We compute the efficient frontiers using the variance and the semivariance as the risk measure. Furthermore, we compute also the efficient frontier given by the constant proportions _p_ when increasing this constant from zero to one. These efficient frontiers are formed by performing the optimization for 11 values for the risk aversion parameter _λ_ . 

The mean-variance and mean-semivariance frontier plots for all three investment strategies are shown in Figure 1. The final wealth probability distributions for the three strategies when E[ _W_ ( _T_ )] = 8 are depicted in Figure 2. The corresponding mean-variance and meansemivariance optimized controls _p_ are depicted in Figure 3. 

We studied the convergence with respect to _M_ (the number of discretization points in the _W_ -direction) and with respect to _K_ (the number of paths). The other parameters were the same as above. Let _Ji,M,K_ := _Jλi_ (P _[∗]_ ), where P _[∗]_ is the optimal control computed with _M_ 

**R.A.E. MAKINEN[¨] AND J. TOIVANEN** 

**8** 

**==> picture [403 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 10<br>9 9<br>8 8<br>7 7<br>6 6<br>Mean-Var Mean-Var<br>5 5<br>Mean-SemiVar Mean-SemiVar<br>Constant Constant<br>4 4<br>0 1 2 3 4 5 6 0 0.5 1 1.5 2 2.5 3<br>Std(W) SemiStd(W)<br>E(W) E(W)<br>**----- End of picture text -----**<br>


**Figure 1.** _The mean-variance and mean-semivarience frontiers for the mean-variance optimized portfolios, the mean-semivariance optimized portfolios and the constant proportion portfolios._ 

**==> picture [193 x 148] intentionally omitted <==**

**----- Start of picture text -----**<br>
0.08<br>Mean-Var         Std(W) = 2.4<br>0.07 Mean-SemiVar Std(W) = 4.2<br>Constant           Std(W) = 3.4<br>0.06 E(W) = 8<br>0.05<br>0.04<br>0.03<br>0.02<br>0.01<br>0<br>0 5 10 15 20 25 30<br>**----- End of picture text -----**<br>


**Figure 2.** _The probability distributions for the final wealth when_ E[ _W_ ( _T_ )] = 8 _for the three investment strategies._ 

gridpoints in the _W_ -direction and using _K_ paths. Let _Ji[†]_[=] _[ J][i,]_[61] _[,]_[10][6][and] _[J] i[♯]_[=] _[ J][i,]_[31] _[,]_[4] _[×]_[10][6][.][We] consider the values _J[†]_[approximations][to][the][exact][optimal][objective][function][values] _i[, J] i[♯]_[good] and we compare with it the values obtained using smaller _M_ or _K_ . In the latter case, we take the average of 100 cost evaluations using a different sets of paths. The results of the tests are depicted in Figure 4. From these tests, we can conclude that the empirical error in _Jλ_ is roughly _∼_ 1 _/M_[2] and _∼_ 1 _/√K_ . These results are consistent with the theoretical convergence properties of piecewise linear interpolation and the Monte Carlo method. 

**5.2. Portfolio with one risky asset and leverage.** We keep the parameters the same as in Section 5.1 except now the maximum leverage is given by _p_ max = 1 _._ 5. This is the example considered by Wang and Forsyth [32] and Cong and Oosterlee [6]. The mean-variance and mean-semivariance efficient frontiers are formed by performing the optimization for 11 values for the risk aversion parameter _λ_ . The mean-variance and mean-semivariance frontiers are shown in Figure 5. The mean-variance frontier agrees well with the efficient frontiers presented 

**MONTE CARLO PORTFOLIO OPTIMIZATION** 

**9** 

**==> picture [413 x 156] intentionally omitted <==**

**----- Start of picture text -----**<br>
20 1 20 1<br>0.8 0.8<br>15 15<br>0.6 0.6<br>10 10<br>0.4 0.4<br>5 5<br>0.2 0.2<br>0 0 0 0<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>W W<br>time time<br>**----- End of picture text -----**<br>


**Figure 3.** _Mean-variance and mean-semivariance optimized proportions p for E_ [ _W_ ] = 8 _._ 

**==> picture [244 x 184] intentionally omitted <==**

**==> picture [232 x 183] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 [-1]<br>10 [-2]<br>10 [-3] K=16000<br>K=32000<br>K=64000<br>K=128000<br>K=256000<br>K=512000<br>10 [-4]<br>1 2 3 4 5 6 7 8 9 10 11<br>i<br>err(i,K)<br>**----- End of picture text -----**<br>


**Figure 4.** _Left: Difference err_ ( _i, M_ ) := _|Jλi,M,_ 106 _− Ji[†][|][.][Right:][Difference][err]_[(] _[i, K]_[)][:=] _[|J][λ] i[,]_[31] _[,K][−][J] i[♯][|][.] Due to logarithmic y-axes, values with err_ = 0 _are not plotted._ 

## in [32, 6]. 

**5.3. Portfolio with four risky assets.** This is a generalization of the previous examples which adds three more risky assets. The volatilities of the four risky assets are given by the vector _**σ**_ = (0 _._ 15 0 _._ 12 0 _._ 09 0 _._ 06) _[T]_ and their growth rates are given by the vector _**µ**_ = (0 _._ 0795 0 _._ 07 0 _._ 06 0 _._ 05) _[T]_ . The correlation matrix between the risky assets is 

**==> picture [111 x 39] intentionally omitted <==**

As before the interest rate is _r_ = 0 _._ 03, the final time is _T_ = 20, and the initial wealth _w_ 0 = 1. The short selling is not allowed and there is no leverage leading to _p_ min = 0 and _p_ max = 1. The mean-variance and mean-semivariance efficient frontiers are formed by performing the optimization for 13 values for the risk aversion parameter _λ_ . The mean-variance and mean- 

**R.A.E. MAKINEN[¨] AND J. TOIVANEN** 

**10** 

**==> picture [405 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
16 16<br>14 14<br>12 12<br>10 10<br>8 8<br>Mean-Var Mean-Var<br>6 6<br>Mean-SemiVar Mean-SemiVar<br>Constant Constant<br>4 4<br>0 5 10 15 0 1 2 3 4 5 6 7<br>Std(W) SemiStd(W)<br>E(W) E(W)<br>**----- End of picture text -----**<br>


**Figure 5.** _The mean-variance and mean-semivariance frontiers for the mean-variance and meansemivarience optimized portfolios and the constant proportion portfolios when the maximum levarage is p_ max = 1 _._ 5 _._ 

semivariance frontier plots for the two optimized investment strategies are shown in Figure 6. The final wealth probability distributions for the mean-varience optimized portfolios with E[ _W_ ( _T_ )] = 8 for two (one risky) and five (four risky) asset cases are depicted in Figure 7. 

**==> picture [403 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 10<br>9 9<br>8 8<br>7 7<br>6 6<br>5 5<br>Mean-Var Mean-Var<br>Mean-SemiVar Mean-SemiVar<br>4 4<br>0 1 2 3 4 5 6 0 0.5 1 1.5 2 2.5 3<br>Std(W) SemiStd(W)<br>E(W) E(W)<br>**----- End of picture text -----**<br>


**Figure 6.** _The mean-variance and semi-semivariance frontiers for the mean-variance and meansemivariance optimized portfolios for four risky assets._ 

**6. Conclusions.** We presented a very generic Monte Carlo-based approach for portfolio optimization. The models for the asset and the risk can be easily changed. The approach does not require dynamic programming or any transformations. Restrictions on the investment policies can be easily incorporated. In this paper, we used the variance and the semivariance as the risk measure. The numerical examples considered cases with two and five assets. 

**7. Acknowledgements.** We thank the anonymous referees whose constructive comments improved the paper. 

**MONTE CARLO PORTFOLIO OPTIMIZATION** 

**11** 

**==> picture [193 x 149] intentionally omitted <==**

**----- Start of picture text -----**<br>
0.05<br>2 asset Std(W) = 2.4<br>5 asset Std(W) = 2.0<br>0.04 E(W) = 8<br>0.03<br>0.02<br>0.01<br>0<br>0 5 10 15 20 25 30<br>**----- End of picture text -----**<br>


**Figure 7.** _The probability distributions for the final wealth when_ E[ _W_ ( _T_ )] = 8 _for one and four risky assets._ 

## **REFERENCES** 

- [1] M. Abadi, P. Barham, J. Chen, Z. Chen, A. Davis, et al., _TensorFlow: A system for large-scale machine learning_ , in Proceedings of the 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI ’16), 2016, pp. 265–283. 

- [2] S. Basak and G. Chabakauri, _Dynamic mean-variance asset allocation_ , Rev. Financ. Stud., 23 (2010), pp. 2970–3016, https://doi.org/10.1093/rfs/hhq028. 

- [3] T. R. Bielecki, H. Jin, S. R. Pliska, and X. Y. Zhou, _Continuous-time mean-variance portfolio selection with bankruptcy prohibition_ , Math. Finance, 15 (2005), pp. 213–244, https://doi.org/10. 1111/j.0960-1627.2005.00218.x. 

- [4] M. W. Brandt, A. Goyal, P. Santa-Clara, and J. R. Stroud, _A simulation approach to dynamic portfolio choice with an application to learning about return predictability_ , Rev. Financ. Stud., 18 (2005), pp. 831–873. 

- [5] H. Buehler, L. Gonon, J. Teichmann, and B. Wood, _Deep hedging_ , Quant. Finance, 19 (2019), pp. 1271––1291. 

- [6] F. Cong and C. W. Oosterlee, _Multi-period mean-variance portfolio optimization based on MonteCarlo simulation_ , J. Econom. Dynam. Control, 64 (2016), pp. 23–38, https://doi.org/10.1016/j.jedc. 2016.01.001. 

- [7] F. Cong and C. W. Oosterlee, _On pre-commitment aspects of a time-consistent strategy for a meanvariance investor_ , J. Econom. Dynam. Control, 70 (2016), pp. 178–193, https://doi.org/10.1016/j. jedc.2016.07.010. 

- [8] D.-M. Dang and P. A. Forsyth, _Continuous time mean-variance optimal portfolio allocation under jump diffusion: an numerical impulse control approach_ , Numer. Methods Partial Differ. Equ, 30 (2014), pp. 664–698, https://doi.org/10.1002/num.21836. 

- [9] P. C. Fishburn, _Mean-risk analysis with risk associated with below-target returns_ , Am. Econ. Rev., 67 (1977), pp. 116–126. 

- [10] R. Fletcher, _Practical methods of optimization_ , A Wiley-Interscience Publication, John Wiley & Sons, Ltd., Chichester, second ed., 1987. 

- [11] P. A. Forsyth, _Multiperiod mean conditional value at risk asset allocation: Is it advantageous to be time consistent?_ , SIAM J. Financial Math., 11 (2020), pp. 358––384. 

- [12] P. A. Forsyth and K. R. Vetzal, _Dynamic mean variance asset allocation: tests for robustness_ , Int. J. Financ. Eng., 4 (2017), pp. 1750021, 37, https://doi.org/10.1142/S2424786317500219. 

- [13] M. B. Giles, _Monte Carlo evaluation of sensitivities in computational finance_ , Tech. Report 12, OxfordMan Institute, University of Oxford, Oxford, UK, 2007. 

- [14] M. B. Giles, _Vibrato Monte Carlo sensitivities_ , in Monte Carlo and quasi-Monte Carlo methods 2008, Springer, Berlin, 2009, pp. 369–382, https://doi.org/10.1007/978-3-642-04107-5 ~~2~~ 3. 

**R.A.E. MAKINEN[¨] AND J. TOIVANEN** 

**12** 

- [15] J. Han and E. Weinan, _Deep learning approximation for stochastic control problems_ , in NIPS Deep Reinforcement Learning Workshop, 2016. 

- [16] H. Jin, J.-A. Yan, and X. Y. Zhou, _Continuous-time mean–risk portfolio selection_ , Ann. inst. Henri Poincare (B) Probab. Stat., 41 (2005), pp. 559–580, https://doi.org/10.1016/j.anihpb.2004.09.009. 

- [17] C. Kaebe, J. H. Maruhn, and E. W. Sachs, _Adjoint-based Monte Carlo calibration of financial market models_ , Finance Stoch., 13 (2009), pp. 351–379, https://doi.org/10.1007/s00780-009-0097-9. 

- [18] P. Lambrianides, Q. Gong, and D. Venturi, _A new scalable algorithm for computational optimal control under uncertainty_ , J. Comp. Phys., 420 (2020), https://doi.org/10.1016/j.jcp.2020.109710. 

- [19] C. Lemar´echal, _Numerical experiments in nonsmooth optimization_ , in Progress in Nondifferentiable Optimization, E. A. Nurminski, ed., International Institute for Applied Systems Analysis (IIASA), Laxenburg, Austria, 1982, pp. 61–84. 

- [20] A. S. Lewis and M. L. Overton, _Nonsmooth optimization via quasi-Newton methods_ , Math. Program., 141 (2013), pp. 135–163, https://doi.org/10.1007/s10107-012-0514-2. 

- [21] D. Li and W.-L. Ng, _Optimal dynamic portfolio selection: multiperiod mean-variance formulation_ , Math. Finance, 10 (2000), pp. 387–406, https://doi.org/10.1111/1467-9965.00100. 

- [22] X. Li, X. Y. Zhou, and A. E. B. Lim, _Dynamic mean-variance portfolio selection with noshorting constraints_ , SIAM J. Control Optim., 40 (2002), pp. 1540–1555, https://doi.org/10.1137/ S0363012900378504. 

- [23] H. M. Markowitz, _Portfolio selection_ , J. Finance, 7 (1952), pp. 77–91. 

- [24] A. M. Reppen and H. Mete Soner, _Deep empirical risk minimization in finance: looking into the future_ , Mathematical Finance, 33 (2023), pp. 116––145. 

- [25] A. M. Reppen, H. Mete Soner, and V. Tissot-Daguette, _Deep stochastic optimization in finance_ , arxiv.org/abs/2205.04604, (2022). 

- [26] M. Strub, D. Li, and X. Cui, _An enhanced mean-variance framework for robo-advising applications_ , SSRN 3302111, (2019). 

- [27] The MathWorks Inc., _MATLAB R2022b_ , Natick, MA, USA, 2022, https://www.mathworks.com. 

- [28] P. M. van Staden, D.-M. Dang, and P. A. Forsyth, _Mean-quadratic variation portfolio optimization: A desirable alternative to time-consistent mean-variance optimization?_ , SIAM J. Financial Math., 10 (2019), pp. 815–856, https://doi.org/10.1137/18M1222570. 

- [29] P. M. van Staden, D.-M. Dang, and P. A. Forsyth, _The surprising robustness of dynamic meanvariance portfolio optimization to model misspecification errors_ , Eur. J. Oper. Res., 289 (2021), pp. 774–792, https://doi.org/10.1016/j.ejor.2020.07.021. 

- [30] P. M. Van Staden, P. A. Forsyth, and Y. Li, _Beating a benchmark: dynamic programming may not be the right numerical approach_ , SIAM J. Financial Math., 14 (2023). 

- [31] E. Vigna, _On time consistency for mean-variance portfolio selection_ , Int. J. Theor. Appl. Finance, 23 (2020). 

- [32] J. Wang and P. A. Forsyth, _Numerical solution of the Hamilton-Jacobi-Bellman formulation for continuous time mean variance asset allocation_ , J. Econom. Dynam. Control, 34 (2010), pp. 207–230, https://doi.org/10.1016/j.jedc.2009.09.002. 

