# Cesifo1 Wp10909

**Source:** cesifo1_wp10909.pdf

---

**==> picture [236 x 130] intentionally omitted <==**

## 10909 2024 

January 2024 

## **Machine Learning for Continuous-Time Finance** _Victor Duarte, Diogo Duarte, Dejanir H. Silva_ 

## **Impressum:** 

CESifo Working Papers ISSN 2364-1428 (electronic version) Publisher and distributor: Munich Society for the Promotion of Economic Research - CESifo GmbH 

The international platform of Ludwigs-Maximilians University’s Center for Economic Studies and the ifo Institute 

Poschingerstr. 5, 81679 Munich, Germany 

Telephone +49 (0)89 2180-2740, Telefax +49 (0)89 2180-17845, email office@cesifo.de 

Editor: Clemens Fuest 

https://www.cesifo.org/en/wp 

An electronic version of the paper may be downloaded 

- from the SSRN website: www.SSRN.com 

- · from the RePEc website: www.RePEc.org 

- · from the CESifo website: https://www.cesifo.org/en/wp 

CESifo _Working Paper No. 10909_ 

## Machine Learning for Continuous-Time Finance 

## Abstract 

We develop an algorithm for solving a large class of nonlinear high-dimensional continuous-time models in finance. We approximate value and policy functions using deep learning and show that a combination of automatic differentiation and Ito’s lemma allows for the computation of exact expectations, resulting in a negligible computational cost that is independent of the number of state variables. We illustrate the applicability of our method to problems in asset pricing, corporate finance, and portfolio choice and show that the ability to solve high-dimensional problems allows us to derive new economic insights. 

_Victor Duarte Diogo Duarte University of Illinois at Urbana-Champaign Florida International University Gies College of Business College of Business 1206 South Sixth Street, 461 Wohlers Hall 11200 S.W. 8[th] St., 236 USA – Champaign, IL, 61820 USA – Miami, FL 33199 vduarte@illinois.edu diogo.durate@fiu.edu Dejanir H. Silva Purdue University Krannert School of Management 403 W State St USA – West Lafayette, IN 47907 dejanir@purdue.edu_ 

## December 30, 2023 

This paper benefited from comments by Markus Brunnermeier, Julia Fonseca, Daniel Greenwald, Leonid Kogan, Deborah Lucas, Karel Mertens, Alexis Montecinos, Jonathan Parker, Alex Richter, Adrien Verdelhan, Gianluca Violante, and seminar participants at the WEAI Annual Meeting, the Macro Financial Modeling Summer Session, the MIT Finance Seminar, Princeton, New York Fed, Dallas Fed, UT Dallas, John Hopkins Carey, Rice Jones, UIUC Gies College of Business. Generous financial support for this project was provided by The Becker Friedman Institute’s Macro Financial Modeling Initiative. 

Dynamic programming is one of the cornerstones of modern financial economics. The behavior of investors, managers, households, and governments are typically represented as the result of maximizing their respective value functions. Dynamic programming is, however, plagued by the “curse of dimensionality” (Bellman, 1957)—it becomes exponentially more challenging in terms of computing time and memory as the number of state variables increases. The curse of dimensionality encompasses three separate challenges, sometimes referred to as the three curses of dimensionality (Powell, 2007). The first curse refers to the challenge of approximating a high-dimensional nonlinear function on a computer. The second curse of dimensionality refers to the computation of expectations involved in Bellman equations. Last, the third curse corresponds to maximizing an objective function at each iteration step. Each of these challenges imposes severe limitations on the advancement of financial economics. Therefore, most financial research today is restricted to models featuring either small state spaces or linearized solutions.[1] 

This paper proposes a novel algorithm that handles nonlinear stochastic dynamic programming problems with large state spaces, addressing the three curses of dimensionality and opening up the possibility of studying models set in a richer economic environment. To address the first curse of dimensionality, we use deep neural networks to represent value functions and optimal policies. To overcome the second curse of dimensionality, we show how to combine the auto-differentiation feature of modern machine-learning libraries and Ito’s lemma to efficiently compute exact expectations in continuous-time dynamic systems driven by Brownian shocks.[2] To overcome the third curse of dimensionality, we employ a version of the generalized policy iteration of Sutton and Barto (1998) based on policy gradients (Lillicrap et al., 2015). For this reason, we refer to our method as _deep policy iteration_ (DPI hereafter), as it combines value and policy function approximations using deep neural networks and generalized 

> 1We call a state space _small_ if it has less than five dimensions and _large_ otherwise. 

> 2Throughout the paper, the term _exact_ should be interpreted as exact up to machine precision. 

2 

policy iteration to handle high-dimensional problems. 

We then apply our method to a range of problems in finance. These applications serve two main purposes. First, they illustrate our method’s versatility by showing how to handle different problems involving features such as large state spaces, kinks, and jumps or by showing how to efficiently perform global sensitivity analysis in structural models. Second, they enable us to document the performance and accuracy of our method in the context of standard finance problems, as well as to compare our solution to leading alternative numerical methods, such as the Smolyak-based projection method and finite differences. 

Different from previous work that used _shallow_ neural networks to solve or estimate economic models (Haugh and Kogan, 2004; Norets, 2012), we propose using _deep learning_ to approximate value and policy functions.[3] Deep learning is fundamentally different from classical machine learning, as it requires an entirely new ecosystem of software, hardware, and methods that were only recently developed. Starting with Mnih et al. (2015), deep learning has emerged to become the de-facto technology for functional approximation in _reinforcement learning_ , the subfield of machine learning that studies intertemporal optimization, being successfully deployed to solve problems with hundreds of state variables.[4] 

In contrast to reinforcement learning applications, we make explicit use of the state dynamics to develop a much more efficient algorithm for the types of problems financial economists study. In a continuous-time setting, we implement an efficient algorithm to compute instantaneous drifts and volatilities for arbitrary functions. We show that the computational cost of evaluating the drift and volatility does not scale with the number of state variables. Furthermore, that cost scales less than linearly with the number of shocks. This allows us to compute exact expectations required to 

> 3Shallow networks are neural networks with a single hidden layer. Section 1 defines neural networks and hidden layers. 

> 4See Silver et al. (2016), Silver et al. (2017), and Heess et al. (2017), for instance. 

3 

perform Bellman iterations. 

Finally, we use policy gradients (Lillicrap et al., 2015) to improve the policy function at each policy iteration step. This approach consists in gradually improving the policy function using only the gradient at each step. Since gradients can be computed with negligible cost by using _backpropagation_ (Rumelhart et al., 1988), this addresses the third curse of dimensionality. 

To illustrate the broad applicability of our method, we consider large-dimensional problems in three core areas of finance: asset pricing, corporate finance, and portfolio choice. For asset pricing, we consider the Lucas orchard economy of Martin (2013), a multi-tree extension of the classical one-tree exchange economy of Lucas (1978). We show that the DPI algorithm is able to solve a Lucas exchange economy with up to 100 trees while sustaining low root mean square error (RMSE hereafter). Moreover, we show that the time-to-solution scales approximately linearly with the number of state variables, illustrating our method’s ability to alleviate the curse(s) of dimensionality. In contrast, the Smolyak projection method, a numerical method commonly used to handle large-dimensional problems, fails to sustain low RMSEs as the state space grows. More importantly, the Smolyak method quickly exhausts computer memory and is unable to produce a solution for an economy with more than 25 trees. 

We also show that the focus on low-dimensional problems, an assumption typically made for tractability reasons, may have important economic implications. In particular, we argue that many of the interesting asset-pricing effects found in the cases of two trees (Cochrane et al., 2008), typically involving the behavior of small firms, disappear as we increase the number of trees. The reason is that, with only two trees, either both trees are of similar size, and the economy is well-diversified, or we have one tree that is small, and the economy is severely under-diversified. In contrast, with a large number of trees, it is possible to study small firms in reasonably diversified economies. While changes in the dividend share of a small firm have a large impact on aggregate 

4 

consumption volatility for under-diversified economies, this is not the case when the economy is more diversified. We show that the strong valuation effects for small firms found with just a few trees disappear as we increase the number of trees, as their impact on aggregate volatility becomes more muted. Therefore, the ability to solve high-dimensional problems may allow us to relax assumptions made based only on tractability and instead focus on the assumptions that are of economic interest. 

Our second application is a dynamic corporate finance model, in the spirit of Hennessy and Whited (2007), where firms face equity issuance and investment adjustment costs. An important feature of this application is that the solution may feature kinks, as the marginal incentives to invest vary depending on whether the firm is issuing equity or paying dividends (or neither). To show the method’s ability to solve this problem, we compare our solution to the one from a finite differences method with a fine grid, which we use as our benchmark. Our findings closely match the results from finite differences, indicating the accuracy of our solution. Therefore, our method can handle problems with severe nonlinearities, even when a classical solution to the continuous-time problem is not available, such as in the case of the problems with kinks.[5] 

For any given value of the parameters, our version of the Hennessy-Whited model can be solved using standard methods, such as finite differences. However, we are often interested in the solution for a very large number of parameter values. For instance, to be able to show which features of the data are particularly informative about a given parameter, one needs to show how equilibrium moments change with the parameters, which can be computationally very costly. We show how to perform global sensitivity analysis in an efficient manner by including as inputs of the network not only the state variables but also the parameters of interest.[6] In our application, 

> 5For a recent discussion of viscosity solutions, the appropriate solution concept when the value function is not differentiable everywhere, see e.g. Achdou et al. (2022). 

> 6On the importance of sensitivity analysis for structural work, see e.g. Andrews et al. (2017) and Catherine et al. (2022). 

5 

this requires effectively solving a problem with seven state variables, the two original states plus five parameters. As a result, we obtain the model’s solution for any point of the state space or the parameter space. By simultaneously solving for an entire class of models, our method eliminates the need to repeatedly solve the model for each new parameter value, which gives an efficient way of assessing how parameters affect the model predictions. This feature is potentially useful when performing structural estimation.[7] 

In our third application, we show how the DPI algorithm can be used to solve a portfolio choice problem in which the interest rate and risk premium are time-varying and driven by a large number of return predictors. Since closed-form solutions are typically not available for high-dimensional portfolio problems, we propose a new way to assess the accuracy of our method. In particular, we reverse engineer the process for the interest rate and the risk premium such that the policy functions are any given closed-form expressions. We can then solve the portfolio problem with the reverse-engineered process for the returns using the DPI method and then compare our solution to the known closed-form expressions. This process of reverse engineering a problem provides an effective laboratory for evaluating the performance of our solution method for high-dimensional problems. We find that the DPI method provides accurate solutions even with 10 return predictors and captures a wide range of relationships between the portfolio share and a return predictor, depending on the region of the state space. 

Having demonstrated DPI’s ability to solve high-dimensional nonlinear portfolio choice problems, we proceed to analyze optimal asset allocation in an empirically motivated model with multiple risky assets and realistic return dynamics. The optimal portfolio features a substantial degree of market timing. At times, the investor is heavily invested in stocks, such as in the early 1950s and 1960s, and sometimes the 7For an application of these ideas to the context of structural estimation, see Duarte (2018). 

6 

investor is nearly out of the stock market, as in the early 1970s or early 2000s. Moreover, macroeconomic variables, and in particular fiscal variables, explain a sizeable fraction of the variation in portfolio shares. 

To keep the exposition as simple as possible, we focus on the case of Brownian shocks and economies with a representative agent for our three applications. However, with minor modifications, our methods can also be applied to models with jumps.In Appendix B, we solve the model of time-varying disasters in Wachter (2013). One important distinction relative to models with Brownian shocks is that expectations appear explicitly even in continuous time. We show that, by using simulation methods analogous to the least-squares Monte Carlo method of Longstaff and Schwartz (2001), we can apply the DPI algorithm even in problems with jumps. We compare our solution to the closed-form expression provided by Wachter (2013) and show that our method accurately captures the behavior of an economy subject to rare disasters. 

The rest of the paper is organized as follows. The remainder of this section contains the related literature. Section 1 sets forth the machine-learning tools and terminology. Section 2 presents our method. Section 3 discusses our three applications, and Section 4 concludes. 

**Related Literature.** Our work is related to the rapidly growing literature on machine-learning applications in finance. In recent years, we have witnessed rapid adoption of these techniques in several domains of finance, such as asset pricing (Gu et al., 2020; Bianchi et al., 2021; Chen et al., 2023), corporate finance (Li et al., 2021; Cao et al., 2023), derivatives and credit markets (Duarte et al., 2020; Chen et al., 2021; Sadhwani et al., 2021; Fuster et al., 2022; Bali et al., 2023), among others. These applications focus on the use of machine-learning techniques for reduced-form empirical work, while our focus is on numerical methods for structural models.[8] 

> 8For a recent discussion of these applications in asset pricing, with a focus on shrinkage methods, see e.g. Nagel (2021). 

7 

Our paper is also related to the literature using finite-difference methods (Achdou et al., 2022; Brunnermeier and Sannikov, 2014; Ahn et al., 2018) or projection methods (Moreira and Savov, 2017; Drechsler et al., 2018; Kargar, 2021) in continuous time. While these methods are only suitable for small-scale problems, we show how to use deep learning, combined with an efficient way to compute Hamilton-Jacobi-Bellman equations with Brownian shocks, to handle large-scale problems.[9] 

Since this paper was first made publicly available, a number of articles have employed related methods and adopted deep learning for solving or estimating nonlinear dynamic problems in economics. Applications include structural estimation (Duarte, 2018; Chen et al., 2021; Kase et al., 2022), models with discrete choice (Maliar and Maliar, 2022), business cycles (Bybee et al., 2021; Bretscher et al., 2022), heterogeneity and wealth distribution (Maliar et al., 2021; Han et al., 2021; Azinovic et al., 2022; Fernández-Villaverde et al., 2023), life-cycle models (Duarte et al., 2021), macrofinance models (Gopalakrishna, 2021; Sauzet, 2021), climate economics and finance (Folini et al., 2021), among others. Despite recent rapid advancements in the field, our approach stands out distinctly. By innovatively combining a gradient-based generalized policy iteration method, which eliminates the need for root-finding routines, with a cost-effective computation of the value function drift, we effectively address the three curses of dimensionality. This enables researchers to delve into high-dimensional problems in financial economics. 

## **1 Machine Learning** 

This section covers basic machine-learning concepts and methods needed to implement the algorithm presented in Section 2. For excellent textbook treatments, see Sutton and Barto (1998) and Goodfellow et al. (2016). The reader who is already familiar 

> 9For an early use of machine-learning techniques in discrete time, see the work on Gaussian processes by Scheidegger and Bilionis (2019). 

8 

with deep learning and generalized policy iteration may want to skip to the next section. 

## **1.1 Supervised Learning and Neural Networks** 

The goal of supervised learning is, broadly speaking, to learn how to represent functions. For a concrete example, consider a set of observations _{Xi, Yi}[N] i_ =1[and][suppose][that] we are interested in constructing a function _V_ such that _V_ ( _Xi_ ) = _Yi_ . For instance, _Xi_ may be a digital picture and _Yi_ an indicator of whether a particular person appears in the image. Since a greyscale digital picture with one megapixel, for example, has one million dimensions, listing all possible combinations of _Xi_ and _Yi_ in a lookup table is an impossibly difficult task. The machine-learning solution for this problem is to assume a flexible parametric function _V_ ( _Xi_ ; _**θ**_ ), where _**θ**_ is a vector of parameters, and use data to recover _**θ**_ . To represent this highly nonlinear function, we need functional forms that can capture complex and nonlinear interactions between the regressors. A particularly powerful set of function approximators is the class of neural networks. 

The starting point of constructing a neural network is building a linear model of the type _Yi_ = _⟨_ **W** 0 _,_ **X** _i⟩_ + _b_ 0, where _Yi ∈_ R is the dependent variable, **X** _i ∈_ R _[d]_ is a data point, **W** 0 _∈_ R _[d]_ is a vector of coefficients, _b_ 0 _∈_ R is a coefficient (i.e., bias), and the operator _⟨·, ·⟩_ represents the inner product in R _[d]_ . The next step is to apply a nonlinear function _σ_ ( _·_ ), known in the literature as an activation function, to the output. Figure 1 shows three commonly used activation functions. Panel (a) shows the rectified linear unit (Jarrett et al., 2009), which is the default choice in most applications, while Panels (b) and (c) show the sigmoid and hyperbolic tangent activation functions. 

Let **G** 0 = _σ_ ( _⟨_ **W** 0 _,_ **X** _i⟩_ + _b_ 0) be the output of this nonlinear function, known in the literature as the hidden unit. When we perform this operation on a set of vectors and coefficients _{_ **W** _j, bj}j∈_ 0 _,_ 1 _,...,nG−_ 1 and stack them into a vector **G** _∈_ R _[n][G]_ , we obtain a hidden layer. In the final step, a single-layer neural network takes a linear combination 

9 

Figure 1: Activation functions 

**==> picture [429 x 113] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 . 0 1 . 0 1 . 00<br>0 . 75<br>2 . 5 0 . 8<br>0 . 50<br>2 . 0<br>0 . 6 0 . 25<br>1 . 5 0 . 00<br>0 . 4 − 0 . 25<br>1 . 0<br>− 0 . 50<br>0 . 5 0 . 2 − 0 . 75<br>0 . 0 − 1 . 00<br>− 3 − 2 − 1 0 1 2 3 0 . 0 − 3 − 2 − 1 0 1 2 3 − 3 − 2 − 1 0 1 2 3<br>x x x<br>(a) ReLu (b) Sigmoid (c) Tanh<br>}{ Max 0 x, )( xσ )tanh( x<br>**----- End of picture text -----**<br>


Panel (a) shows the rectified linear unit (ReLu), the most common activation function used in machine learning applications. Panels (b) and (c) show two possible alternatives, the sigmoid function _σ_ ( _x_ ) = 1+1 _e[−][x]_[and][the][hyperbolic][tangent][tanh(] _[x]_[) =][1] 1+ _[−] e[e][−][−]_[2][2] _[x][x]_[.] 

of **G** to produce the final output _Y_ = _⟨_ **G** _,_ **W** _nG⟩_ + _bnG_ . 

Panel (a) of Figure 2 shows a neural network with five hidden units. When this neural network is extended by adding many hidden layers, stacked on top of each other, it receives the name of a deep neural network. Panel (b) of Figure 2 shows a deep neural network with two hidden layers. The number of hidden layers, also known as the depth of the neural network, is an important feature to accurately capture nonlinear relationships. Empirically, deep neural networks have been found to perform much better than single-layer networks[10] . 

An important theoretical result in the neural network literature is the so-called Universal Approximation Theorem, which states that any continuous function on compact subsets of R _[n]_ can be uniformly approximated by enough hidden units (Cybenko, 1989; Hornik, 1991).[11] This result may be familiar to financial economists who know the Options Spanning Theorem of Ross (1976), which states that any contract can be formed as a portfolio of options. Indeed, in the particular case where ( _i_ ) the activation function _σ_ ( _·_ ) is the rectified linear unit, ( _ii_ ) the input _X_ is scalar, and ( _iii_ ) the weights are unit weights ( _Wj_ = 1 _∀j_ ), the output of the _j_ -th hidden unit is the payoff of a call option on _X_ with strike _−bj_ . Thus, the output layer combines 

> 10See Chapter 6 of Goodfellow et al. (2016) and references therein. 

> 11 More precisely, the theorem shows that the set of linear combinations of sigmoidal activation functions is dense in the set of continuous functions on the unit cube. 

10 

Figure 2: Feedforward Neural Network 

**==> picture [418 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a) Single Layer (b) Deep Neural Network<br>Input Hidden Output Input Hidden Hidden Output<br>layer layer layer layer layer layer layer<br>X 1 [(] [i] [)] X 1 [(] [i] [)]<br>X 2 [(] [i] [)] X 2 [(] [i] [)]<br>V V<br>X [(] [i] [)] X [(] [i] [)]<br>3 3<br>X 4 [(] [i] [)] X 4 [(] [i] [)]<br>**----- End of picture text -----**<br>


_⊤_ The green circles represent each entry of the input vector **X**[(] _[i]_[)] = _X_ 1[(] _[i]_[)] _[, X]_ 2[(] _[i]_[)] _[, X]_ 3[(] _[i]_[)] _[, X]_ 4[(] _[i]_[)] . The � � hidden units are represented by blue circles. Each hidden unit performs a composition of a nonlinear function (activation function) and a linear transformation of the outputs of the previous layer. The outputs of the final hidden layer are combined linearly to produce the final output. _**θ**_ is the collection of all parameters of the network. 

many call options to produce a given payoff. In our options analogy, a two-layer neural network would correspond to a portfolio of options on portfolios of call options. 

If the output of a neural network has to satisfy some model-implied constraints, we can apply a final nonlinear transformation to ensure that the constraints are not violated. For instance, if a network represents consumption choice, we can apply the exponential or softplus functions as the final transformation to impose nonnegativity. Likewise, sigmoid or hyperbolic tangent functions can be used to bound functions. 

## **1.2 Stochastic Gradient Descent and Backpropagation** 

The standard (nonstochastic) method of gradient descent (or simply, steepest descent) of Cauchy (1847) consists of moving the parameter _**θ**_ of the parametric representation of _V_ ( **X** ), represented by _V_ ( **X** ; _**θ**_ ), in the direction that minimizes some measure of error the fastest. A natural measure of fitness is the one-half mean-squared error 

11 

(MSE hereafter) over _N_ observations, i.e., 

**==> picture [164 x 36] intentionally omitted <==**

Starting with an initial guess _**θ**_ , the gradient descent algorithm updates _**θ**_ according to 

**==> picture [316 x 57] intentionally omitted <==**

where _η_ is the learning rate and _∇_ _**θ**_ denotes the gradient operator with respect to the parameter vector _**θ**_ . 

The key insight of the Stochastic Gradient Descent (SGD hereafter) algorithm is to approximate the expectation (i.e., average) in Eq.(1) with a small independent and identically distributed (i.i.d.) sample of the data set _{_ **X** _i, Yi}_ . Thus, for _n ≪ N_ , we can approximate Eq.(1) by 

**==> picture [331 x 32] intentionally omitted <==**

where _In_ is a random i.i.d. sample of _{_ 1 _,_ 2 _, ..., N }_ with _n_ points.[12] This subsample of points used to approximate the gradient is called the mini-batch. 

The use of stochastic methods to compute the MSE loss is one of the key aspects that separate machine learning from pure optimization, and it is essential to make machine learning feasible in high-dimensional problems. As Goodfellow et al. (2016) explain, computing the MSE loss for a sample with 10,000 observations is 100 times more costly in terms of computational resources than performing the same computation 

> 12Typical values for _n_ and _N_ are 128 and 1,000,000 (see, for example, Krizhevsky et al. (2012)). For guidelines on how to choose the batch size, see Goodfellow et al. (2016). 

12 

for a sample with 100 observations but only reduces the standard deviation of the gradient of the larger sample by a factor of 10 since the standard error of the mean scales with the square root of the number of observations. 

A critical aspect of the iteration in Eq.(2) is that it involves all first-order partial derivatives of the network _V_ with respect to its parameters. Therefore, a naive finite-difference approach to compute the derivatives would be too costly. For example, if the network has 100,000 parameters, we would need to compute _V_ ( **X** _i_ ; _**θ**_ + _ε_ **e** _j_ ) for every _j ∈{_ 1 _, . . . ,_ 100 _,_ 000 _}_ , with _ε ∈_ R, and **e** _j ∈_ R[100] _[,]_[000] is the canonical basis vector in the _j_ -th direction. Fortunately, machine-learning software relies on a more efficient method of computing partial derivatives, called backpropagation (Rumelhart et al., 1988). This algorithm is based on the sequential application of the chain rule, starting from the final layer and moving backward to the initial layer. It can be shown that computing all first-order partial derivatives using backpropagation always has the same cost as computing the function itself.[13] Compared to a finite-difference approach applied to the example above, backpropagation provides an economy of five orders of magnitude. 

## **1.3 Discrete-time Markov Decision Process** 

Throughout the paper, we assume that infinitely lived agents face a Markov decision process; that is, there exists a vector of states **s** _∈S ⊂_ R _[n]_ that subsumes all relevant information for decision-making. At each instant _t_ , subject to possible environment constraints, the agent chooses a control **c** _t ∈A_ from which she derives instantaneous utility _u_ ( **c** _t_ ). Her goal is to choose a sequence of controls to maximize the expected 

> 13See Baydin et al. (2015) for a survey on backpropagation and other automatic differentiation methods. 

13 

value of the sum of discounted future utilities: 

**==> picture [170 x 37] intentionally omitted <==**

The function _V[∗]_ is called the _optimal state-value function_ . The function that maps states to optimal controls _**π**[∗]_ : _S →A_ is called the _optimal policy function_ . More generally, given an arbitrary policy function _**π**_ : _S →A_ (not necessarily optimal), we define the _state-value function associated with_ _**π**_ as 

**==> picture [146 x 37] intentionally omitted <==**

This function represents the expected value of the sum of discounted future utilities for an agent that chooses her controls following the policy _**π**_ . 

A canonical class of algorithms for solving this Markov decision process is called _policy iteration_ (Howard, 1960). It consists of iterating between two steps: policy evaluation and policy improvement. As discussed below, a particular case of policy iteration is the canonical _value function iteration_ method. 

Under technical conditions, the value function _V_ _**π**_ satisfies the Bellman equation 

**==> picture [303 x 13] intentionally omitted <==**

where **s** _[′]_ denotes the state vector next period.[14] The right-hand side of Eq.(3) is the Bellman target, and we denote it by _TVπ_ ( **s** ). 

**Direct policy evaluation.** This functional equation can be solved exactly on a computer only if the state space _S_ = _{s_ 1 _, s_ 2 _, ..., sN }_ is finite and the number of states is sufficiently small. In this case, the Bellman equation is linear and can be solved 14For details on the Bellman equation, see Stokey et al. (1989) and Ljungqvist and Sargent (2000). 

14 

with standard linear algebra tools: 

**==> picture [118 x 15] intentionally omitted <==**

where **I** is the identity matrix, **P** _**π**_ is the transition probability matrix describing the state dynamics when the agent chooses her controls using the policy _**π**_ , **V** _**π**_ is the vector of stacked values for every state, **V** _**π**_ = [ _V_ _**π**_ ( _s_ 1) _, V_ _**π**_ ( _s_ 2) _, ..., V_ _**π**_ ( _sN_ )], and _U_ _**π**_ is the vector of stacked utilities for every state: **U** _**π**_ = [ _u_ ( _**π**_ ( _s_ 1)) _, u_ ( _**π**_ ( _s_ 2)) _, ..., u_ ( _**π**_ ( _sN_ ))]. 

**Iterative policy evaluation.** An alternative algorithm for computing _V_ _**π**_ consists of turning the Bellman equation in Eq.(3) into assignments. Starting from an initial arbitrary guess _V_ _**π**_[0][,][construct][a][sequence] � _V_ _**π**[k]_ � _k∈_ N[according][to] 

**==> picture [267 x 15] intentionally omitted <==**

This iteration produces the unique solution of Eq.(3). 

**Policy improvement.** Knowing the value function _V_ _**π**_ associated with the policy _**π**_ makes it possible to find a better policy _**π**[′]_ : _S →A_ . Let 

**==> picture [324 x 20] intentionally omitted <==**

The Policy Improvement Theorem (Bellman, 1957; Howard, 1960) guarantees that _V_ _**π** ′_ ( **s** ) _≥ V_ _**π**_ ( **s** ) _, ∀_ **s** _∈S_ . This step is therefore called _policy improvement_ . 

Alternating between policy evaluation and policy improvement is guaranteed to produce the optimal state-value function _V[∗]_ and the optimal policy _**π**[∗]_ . If the policy evaluation step consists of a single iteration of iterative policy evaluation in Eq.(4), the algorithm is called value function iteration. 

15 

**Large state and action spaces.** When the number of states is large or takes on a continuum of values, all numerical solution methods have to rely on an approximate version of Eq.(3). Likewise, when the action space _A_ is large, in general, the maximization on the right-hand side of Eq.(5) cannot be performed exactly. An algorithm that alternates some approximate version of policy evaluation with an approximate version of policy improvement is called _generalized policy iteration_ (Sutton and Barto, 1998). 

## **2 Solution Method** 

In this section, we show how to combine the tools presented in Section 1 with Ito’s lemma to solve high-dimensional nonlinear dynamic stochastic problems in continuous time. This combination allows us to efficiently compute exact expectations when the underlying shocks follow Brownian motions, yielding the new and surprising result that the associated computational cost does not increase with the number of states, and increases at most linearly with the number of shocks, therefore avoiding the second curse of dimensionality (Powell, 2007). 

## **2.1 Ito’s Lemma and Automatic Differentiation** 

The computational advantage of continuous time over discrete time counterparts is that, in continuous time, expectations can be computed with partial derivatives when the underlying shocks follow Brownian motions. For example, Achdou et al. (2014) and Brunnermeier and Sannikov (2016) present algorithms that perform orders of magnitude faster than their discrete-time counterparts for small-scale problems with one or two state variables. When the state space is low dimensional, one can discretize the state space and approximate partial derivatives with finite differences, and thus computing expectations using Ito’s lemma is computationally cheap. 

16 

This approach, however, does not scale to problems with a large number of state variables.[15] Consider the vector of state variables **s** that follows the stochastic differential equation: 

**==> picture [274 x 15] intentionally omitted <==**

where **s** _∈_ R _[n]_ , **f** : R _[n] →_ R _[n]_ is the drift, and **g** : R _[n] →_ R _[n][×][m]_ represents the matrix of loadings on the _m_ -dimensional vector of standard Brownian motions _d_ **B** . 

Let _V_ ( **s** ) denote an arbitrary function of **s** with continuous second-order partial derivatives. Ito’s lemma states that: 

**==> picture [349 x 25] intentionally omitted <==**

where _∇_ **s** _V_ is the gradient and **Hs** _V_ the Hessian matrix. 

A naive implementation of Ito’s lemma would involve computing all first- and second-order partial derivatives, which naturally scales poorly with the number of state variables. The next proposition shows how to bypass these costly computations and avoid the second curse of dimensionality. This result is also part of what distinguishes our algorithm from standard reinforcement-learning implementations, as the state dynamics are typically not known in these applications. 

**Proposition 1.** _For a given_ **s** _, define the auxiliary function F_ : R _→_ R _as_ 

**==> picture [322 x 34] intentionally omitted <==**

_where_ **g** _i_ ( **s** ) _represents column i of the matrix_ **g** ( **s** ) _. Then,_ 

> 15For example, a ten-dimensional grid with 100 points in each direction requires 1017 terabytes of RAM. 

17 

**==> picture [263 x 25] intentionally omitted <==**

Proposition 1 contains two main insights. First, Eq.(9) shows that we can bypass the computation of a multidimensional Ito’s lemma on the right-hand side by computing the second derivative of a univariate function on the left-hand side instead. Note that the second derivative of _F_ is effectively a directional derivative of _V_ .[16] Second, since the cost of evaluating a second-order derivative with either backward or forward automatic differentiation is a small multiple of the cost of evaluating _F_ (0) = _V_ ( **s** ), the total computational cost of evaluating[E] _dt[dV]_[(] **[s]**[)][is][a][small][multiple][of] _[m][·][cost]_[(] _[V]_[ )][.][17] 

To understand the computational gains generated by Proposition 1, consider the following illustrative example where we compute the derivative in Eq.(9) using secondorder forward mode automatic differentiation. Suppose we have 100 state variables **s** _t_ = ( _s_ 1 _,t, s_ 2 _,t, ..., s_ 100 _,t_ ), where each component _si,t_ , _i_ = 1 _, ...,_ 100 has a drift process _µi,t_ and a volatility process _σi,t_ on the same Brownian shock _dBt_ . 

Now consider evaluating the function _V_ ( **s** _t_ ) =[�][100] _i_ =1 _[s]_[2] _i,t_[numerically.][Squaring][each] term and adding them all up requires a total of 199 floating point operations (FLOPs), corresponding to 100 multiplications and 99 additions. But if we are interested in computing the drift of _V_ , how many operations do we need to perform when using Proposition 1? 

To obtain the drift of _V_ using Proposition 1, we must compute the second 

> 16Formally, E _dtdV_[(] **[s]**[)][is][the][sum][of][the][first-order][directional][derivative] _[∇]_ **[s]** _[V]_[ (] **[s]**[)] _[⊤]_ **[f]**[(] **[s]**[)][and][the][second-] order directional derivative[1] 2[Tr] � **g** ( **s** ) _[⊤]_ **Hs** _V_ ( **s** ) **g** ( **s** )�. 

> 17With forward-mode automatic differentiation, this cost is independent of the number of outputs, while with backward-mode it is independent of the number of inputs (see Griewank and Walther (2008) for formal bounds). Since the auxiliary function _F_ has one input and one output, the choice of backward or forward mode is typically not important when using efficient automatic differentiation systems. However, depending on the software, the backward mode can be much slower. Therefore, systematic experimentation is advised to determine the optimal combination of forward and backward modes for superior performance. 

18 

derivative of _F_ ( _ϵ_ ) _≡ V_ **s** _t_ + _ϵ ·_ _**[σ]**[t][ϵ]_[2] , where _**µ** t_ = ( _µ_ 1 _,t, µ_ 2 _,t, ..., µ_ 100 _,t_ ) and � ~~_√_~~ 2[+] 2 _[·]_ _**[ µ]**[t]_ � _**σ** t_ = ( _σ_ 1 _,t, σ_ 2 _,t, ..., σ_ 100 _,t_ ). For a given Taylor series _x_ = _x_ 0 + _ϵ · x_ 1 + _[ϵ]_[2][auto-] 2 _[·][ x]_[2][,] matic differentiation in forward mode produces the Taylor series of a function _f_ ( _x_ ) by chaining the Taylor series of each elementary function that composes _f_ ( _x_ ). The function _V_ in this example contains two elementary operations: the square function and the addition, so we only need propagation rules for these two functions. The Taylor expansion of the addition is immediate: the series of the sum is the sum of the series. For the square function, its second-order Taylor expansion yields 

**==> picture [185 x 62] intentionally omitted <==**

where _y_ 0 = _x_[2] 0 _[,][y]_[1][= 2] _[·][x]_[0] _[·][x]_[1][, and] _[ y]_[2][= 2] _[·]_[(] _[x]_[0] _[·][x]_[2][+] _[x]_[2] 1[)][.][Note in particular that we need] 4 FLOPs to compute the second-order Taylor coefficient _y_ 2: one for the multiplication _x_ 0 _· x_ 1, one for the multiplication _x_ 1 _· x_ 1, one for the addition _x_ 0 _· x_ 1 + _x_[2] 1[,][and][one][for] the multiplication 2 _·_ ( _x_ 0 _· x_ 1 + _x_[2] 1[)][.] 

Now consider the original series _x_ = _si_ + _ϵ ·[σ][i]_ + _[ϵ]_[2][In][this][case,] _[x]_[0][=] _[ s][i][, x]_[1][=] ~~_√_~~ 2 2 _[·][ µ][i]_[.] _σi_[and] _[x]_[2][=] _[µ][i]_[.][First,][we][need][100][FLOPs][for][the][terms] _[σ][i]_[To][compute][the] ~~_√_~~ 2 _[,]_ ~~_√_~~ 2[.] second-order term of the Taylor expansion of the quadratic function, we need another 400 FLOPs, as shown above. Finally, for the summation operation, we need another 99 additions to obtain the second-order derivative of the auxiliary function _F_ . In summary, we need a total of 599 FLOPs to compute the drift of _V_ , a small multiple of the cost of evaluating _V_ itself. 

The cost of computing the drift of a high-dimensional function is significantly higher using leading alternative methods. Table 1 shows the computational cost and memory requirements to compute the drift of _V_ using different approaches. As shown, using finite differences to compute all first- and second-order partial derivatives of _V_ to 

19 

Table 1: Computational Cost of Numerical Derivatives 

|**Method**|**FLOPs**|**Memory**|**Error**|
|---|---|---|---|
|1. Finite diferences|9,190,800|112,442,048|1.58%|
|2. Naive autodif|2,100,501|25,673,640|0.00%|
|3. Analytical|20,501|44,428|0|
|4. Proposition 1|599|6,044|0.00%|



_Notes:_ The table shows the computational cost for computing the drift of _V_ ( _s_ ) =[�][100] _i_ =1 _[s] i_[2][,] assuming _si_ = _µi_ = _σi_ = 1 for _i_ = 1 _, . . . ,_ 100, using four different methods: 1) finite differences (with _h_ = 0 _._ 001), 2) a naive use of automatic differentiation (where the Hessian is computed by nested calls to the Jacobian function), 3) using the analytical partial derivatives, and 4) the method described in Proposition 1 combined with forward-mode automatic differentiation. The column FLOPs shows the number of floating point operations required by each approach. The column Memory is measured as bytes accessed. The column Error measures the absolute value of the relative error of each method in percentage terms. 

obtain its drift as in Eq.(7), requires over 9 million FLOPs, with a total memory cost of over 112 million bytes. This substantial amount of memory is orders of magnitude larger than the memory usage for the method proposed in Proposition 1, which is about 6,000 bytes. 

It should be emphasized that the large performance difference between the two methods is not only due to the use of automatic differentiation. As shown in Table 1, a naive use of automatic differentiation, where the Hessian is computed by nested calls of the Jacobian function, is only slightly more efficient than finite differences. The reason is that the number of first- and second-order partial derivatives grows rapidly with the number of state variables. By effectively computing a directional derivative as in Proposition 1, we bypass the computation of all these partial derivatives, resulting in this large performance difference. Interestingly, the method proposed in Proposition 1 is more efficient even when the partial derivatives can be computed and evaluated in closed form. As shown in Table 1, it takes 20,501 FLOPs and 44,428 bytes to compute the drift of _V_ using the analytical expressions for the partial derivatives in Eq.(7). 

The efficiency gains provided by Proposition 1 generalize to more complex functional forms for _V_ . To see how this theoretical result translates into real-world applications, 

20 

Figure 3: Ito’s Lemma Computational Cost 

**==> picture [415 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
One Brownian Shock 100 State Variables<br>Actual Cost<br>1 . 4 Theoretical Lower Bound 4 . 5<br>4 . 0<br>1 . 2<br>3 . 5<br>3 . 0<br>1 . 0<br>2 . 5<br>0 . 8 2 . 0<br>1 . 5<br>0 . 6<br>1 . 0<br>0 20 40 60 80 100 0 20 40 60 80 100<br>Number of State Variables Number of Shocks<br>(a) (b)<br>EdV dt EdV dt<br>of of<br>Cost Cost<br>Computational Computational<br>**----- End of picture text -----**<br>


_Notes._ This figure shows how the cost of computing the drift of a function _V_ scales with the number of state variables and with the number of Brownian shocks. We define the cost as the execution time of[E] _dt[dV]_[(] **[s]**[)][divided][by][the][execution][time][of] _[V]_[ (] **[s]**[)][.][The][left][panel][fixes][the][number][of][Brownian][shocks] at 1 and varies the number of state variables from 1 to 100, while the panel on the right fixes the number of state variables at 100 and varies the number of shocks from 1 to 100. In this example, _V_ is represented by a 2-layer neural network, and the executing times are computed 10,000 times on a mini-batch of 512 samples of the state space. 

we perform two experiments. In the experiments, we use a more complex functional form than the quadratic function used in the previous illustrative numerical example, and we set _V_ as a 2-layer neural network. Panel (a) shows the cost of computing E _dV dt_[(] **[s]**[)][as][we][vary][the][number][of][state][variables,][holding][the][number][of][Brownian] shocks fixed and equal to one ( _m_ = 1). This cost is defined as the execution time of E _dtdV_[(] **[s]**[)][divided][by][the][execution][time][of] _[V]_[ (] **[s]**[)][.][As][shown,][this][cost][is][slightly][greater] than one, regardless of the number of state variables, showing that evaluating the value-function drift in Eq.(9) is essentially as costly as doing a single evaluation of _V_ ( **s** ). 

Panel (b) of Figure 3 shows the cost of computing the value-function drift as we vary the number of Brownian shocks, holding fixed the number of state variables at 100. As the number of Brownian shocks increases, the computational cost as measured by the wall-clock time scales less than one-for-one, as we compute the summation terms in Eq.(8) in parallel. 

21 

## **2.2 The Deep Policy Iteration Algorithm** 

In this subsection, we show the update rules for the neural network parameters based on a generalized policy iteration. For ease of exposition, we make a few simplifying assumptions that can be easily relaxed. First, the update rules are based on the simplest version of the SGD, shown in Eq.(2). Second, we alternate between exactly one step of policy evaluation and one step of policy improvement. Third, we use a quadratic loss function for the policy evaluation step. 

Consider the class of standard optimal control problems in continuous time where infinitely lived agents face a Markovian decision process, with the vector of state variables **s** _∈S ⊂_ **R** _[n]_ subsuming all relevant information for decision-making. An agent chooses the policy **c** : _S →_ Γ to maximize her lifetime expected utility: 

**==> picture [192 x 30] intentionally omitted <==**

**==> picture [180 x 40] intentionally omitted <==**

where, at every point in the state space **s** _t_ , the agent chooses controls **c** _t_ to maximize _V_ ( **s** _t_ ) subject to the evolution of the state variables and a set of constraints on the controls Γ( **s** _t_ ). 

Under technical conditions, an intermediate step in the heuristic derivation of the associated HJB equation is 

**==> picture [208 x 20] intentionally omitted <==**

22 

where 

**==> picture [362 x 49] intentionally omitted <==**

where _F_ is the auxiliary function defined in Proposition 1. The solution to this problem is a pair of functions _V_ ( **s** ) and **c** ( **s** ) that satisfy at every point **s** in the state space, the following system of equations 

**==> picture [298 x 50] intentionally omitted <==**

Representing the infinite-dimensional objects _V_ and **c** on a computer requires an approximation using a finite set of parameters that we denote by the vectors _**θ** V_ and _**θ** C_ , respectively. A standard way of solving the problem in Eq.(10) is to choose a finite subset of the state space _{_ **s** _i}[I] i_ =1[and parameterize the value and policy functions using] as many parameters as there are states: **c** ( **s** _i_ ; _**θ** C_ ) = _**θ** C,i_ and _Vπ_ ( **s** _i_ ; _**θ** V_ ) = _**θ** V,i_ , where _**θ** V,i_ is the _i_ -th entry of the vector _**θ** V_ and _**θ** C,i_ is the _i_ -th entry of the vector _**θ** C_ . With a slight abuse of notation, we denote the HJB error for state **s** _i_ by HJB( **s** _i_ ; _**θ** C,_ _**θ** V_ ). Under this approximation, functional equations become vector equations, and the problem can be exactly solved with policy iteration, as described in Section 1.3. In this case, the method consists of guessing initial _**θ**_[0] _V_[and] _**[θ]**_[0] _C_[and][constructing][a][sequence] _{_ _**θ**[j] C[,]_ _**[ θ]**[j] V[}][j][∈]_[N][as][follows:] 

**==> picture [305 x 51] intentionally omitted <==**

until some stopping criterion is met. 

23 

Different from existing numerical methods that rely on a discretization of the state space and the iteration of Eq.(11), we propose approximating the value function _V_ and the policy **c** with a deep neural network and alternating between the following three steps, until a pre-specified stopping criteria is met. 

**Step 1–Sampling** Consider a random sample of points _{_ **s** _i}[I] i_ =1[in][the][state][space.] This mini-batch of size _I_ can be sampled either from a uniform distribution between hypothesized bounds of the state space or from a guess (perhaps informed by previous iterations) about what the ergodic distribution looks like. 

**Step 2–Policy Improvement** The policy improvement step, illustrated in the second row of Eq.(10), involves an optimization step for every state. This step of optimizing for every single state can be computationally very costly and is the driver of the third curse of dimensionality. Moreover, in general, this step cannot be solved exactly. 

Consider then the following alternative approximate policy improvement strategy. For each state **s** _i_ in the mini-batch and starting from the initial guess **c** 0 _,i ≡_ **c** ( **s** _i_ ; _**θ**[j] C[−]_[1][)][,] do one step of gradient descent on _−_ HJB( **s** _i,_ **c** _,_ _**θ**[j] V[−]_[1] ) using a learning rate of 1. The new control for each point in the mini-batch is 

**==> picture [303 x 16] intentionally omitted <==**

We can use these new values in Eq.(12) as _targets_ to train the policy network. The objective is to find _**θ**[j] C_[to][minimize][the][quadratic][loss][function] 

**==> picture [160 x 63] intentionally omitted <==**

24 

Since the gradient of the loss function _L_ ( _**θ**_ ) is given by 

**==> picture [218 x 36] intentionally omitted <==**

where _**J θ**_ **c** ( **s** _i_ ; _**θ**_ ) denotes the Jacobian of **c** ( **s** _i_ ; _**θ**_ ) with respect to _**θ**_ , we can update _**θ** C_ by taking one step along this gradient. Thus, an application of the one-step SGD evaluated at the starting point _**θ**_ = _**θ**[j] C[−]_[1] gives 

**==> picture [363 x 116] intentionally omitted <==**

where the second row follows from Eq.(12) and the last row from an application of the chain rule. Plugging Eq.(13) into the update rule for gradient descent with learning rate _ηC_ yields: 

## **Policy Improvement** 

**==> picture [333 x 35] intentionally omitted <==**

**Step 3–Policy Evaluation** For the policy evaluation step, we present two alternative update rules. Each has advantages and disadvantages that are discussed below. 

The first update rule is the analog of iterative policy evaluation in Eq.(4). The _continuous-time Bellman target_ is 

**==> picture [330 x 16] intentionally omitted <==**

25 

Given the sample _{_ **s** _i}_ , _**θ**[j] V_[minimizes][the][quadratic][loss][function] 

**==> picture [314 x 63] intentionally omitted <==**

Since the gradient of the loss function _L_ ( _**θ**_ ) is given by 

**==> picture [374 x 35] intentionally omitted <==**

we can update _**θ** V_ by taking one step along this gradient. Thus, an application of the one-step SGD evaluated at the starting point _**θ**_ = _**θ**[j] V[−]_[1] gives 

**==> picture [358 x 35] intentionally omitted <==**

Plugging Eq.(16) into the update rule for gradient descent with learning rate _ηV_ yields **Policy Evaluation 1** 

**==> picture [360 x 36] intentionally omitted <==**

An alternative to the policy evaluation step is the analog of direct policy evaluation in Eq.(1.3). Directly minimizing the MSE of the Bellman residuals using SGD gives 

## **Policy Evaluation 2** 

**==> picture [375 x 36] intentionally omitted <==**

In the machine-learning literature, methods that directly minimize the Bellman residuals are known to be slower than methods based on iterative policy evaluation. Furthermore, notice that the update rule in Eq.(18) involves relatively costly thirdorder derivatives since it requires the gradient of the HJB residual. Nevertheless, 

26 

residual methods are typically more stable than iterative policy evaluation when using nonlinear function approximation (Baird, 1995). Therefore, as a rule of thumb, we recommend starting with the update rule in Eq.(17), and switching to Eq.(18) if the value function starts to diverge. 

## **2.3 Hyperparameters** 

Note that a researcher has flexibility in how to implement such an algorithm. Design choices include the architecture of the networks (number of hidden layers and units), the optimization algorithm, the activation function, the learning rate, the number of steps for policy evaluation and policy improvement, and the sampling strategy. These are called _hyperparameters_ . As with any numerical solution method, there are two ways of choosing the hyperparameters. The first one is to use a hyperparameter tuner software that searches for optimal values based on a given performance criterion.[18] The second way is to use previous work as a baseline and experiment with variations of that baseline. Since one of the contributions of this study is to establish such baselines for future work, we deliberately avoid automatic hyperparameter tuning because it is not necessary for our applications. 

We use the same neural network architecture and hyperparameters for all applications in this paper. In particular, we use a 3-layer neural network with 256 hidden units and layer normalization in the first layer, 128 hidden units in the second layer and 64 units in the third layer. In our experience, such large networks have enough expressive power to accurately represent highly nonlinear functions with dozens of dimensions. For the policy functions, we use the ReLu activation function, which is one of the most commonly used activation functions in deep learning. For the value functions, we use a sigmoid linear unit (SiLu) activation function, which is similar to ReLu, but has the property of being twice continuously differentiable, as required 

> 18See, for instance, Liaw et al. (2018), Song et al. (2023), and Rapin and Teytaud (2018). 

27 

by Ito’s Lemma. For the SGD optimization of the policy evaluation step, we use the Adam optimizer with default hyperparameter values: learning rate = 10 _[−]_[3] , _β_ 1 = 0 _._ 9, and _β_ 2 = 0 _._ 999. We find that using a smaller learning rate for the policy improvement step helps to prevent divergence, and initialize it at 10 _[−]_[4] . Both learning rates decrease by 1% every 15,000 iterations. We choose a batch size of 2,048, which is large enough to keep the GPU at 100 % utilization. 

## **3 Applications** 

To showcase the broad applicability of our method, we solve three problems with a high degree of complexity in three core areas of finance, namely asset pricing, corporate finance, and portfolio choice. We start with the many-tree extension of the classical asset pricing model of Lucas (1978). We then consider a structural corporate finance model in the spirit of Hennessy and Whited (2007). Finally, we study a high-dimensional version of the portfolio choice problem of Campbell and Viceira (1999). While we focus on models with CRRA preferences and Brownian shocks to keep the exposition of the different applications as simple as possible, our method also works in more complex economies where investors have Epstein-Zin preferences and state variables are driven by jump-diffusion processes (see Appendix B). 

## **3.1 Asset Pricing** 

Consider first the two-tree economy of Cochrane et al. (2008), who extend the Lucas economy by adding another exogenously specified tree producing the same consumption good. Under restrictive assumptions, the authors derive closed-form expressions for the equilibrium objects, which we use to check the accuracy of the numerical solutions produced by our method. Later, we consider a richer version of the model with a large number of trees for which closed-form solutions are not available. 

28 

**Two trees.** We keep the exposition of the benchmark model to its minimum and refer readers to Cochrane et al. (2008) for a detailed description of the model. In short, there is a representative consumer that chooses a consumption stream to maximize the lifetime expected utility 

**==> picture [146 x 29] intentionally omitted <==**

The aggregate consumption process _C_ = ( _Ct_ ) _t≥_ 0 is the sum of the dividend streams _D_ 1 _t_ and _D_ 2 _t_ produced by the two trees. The exogenous dividend process _Di_ = ( _Dit_ ) _t≥_ 0, with _i ∈{_ 1 _,_ 2 _}_ , follows a standard geometric Brownian motion: 

**==> picture [103 x 27] intentionally omitted <==**

The Brownian shocks _Z_ 1 and _Z_ 2 have instantaneous correlation equal to _ϱ_ . 

In this two-tree economy, the equilibrium quantities such as the short-term interest rate, dividend yield, expected return, and asset volatility are determined by a single state variable, namely, the dividend share _st_ = _D_ 1 _t/_ ( _D_ 1 _t_ + _D_ 2 _t_ ). Figure 4 compares the numerical solution produced by the DPI method and the analytical solution of Cochrane et al. (2008) for the four equilibrium quantities mentioned above as a function of the state variable _st_ .[19] As indicated, the high nonlinearities exhibited by these functions suggest that methods based on log linearization may fail to accurately capture these curvatures, resulting in inaccurate numerical solutions. The DPI method, in contrast, has no difficulty in capturing nonlinear dynamics due to its global nature and the flexibility of neural networks. 

We use two measures to assess the accuracy of the numerical solution: (i) the absolute deviation of the numerical solution from the exact one; (ii) the HJB residuals. Figure 5 shows the distribution of our two accuracy measures. To obtain these 

> 19All numerical computations in the paper are done using a NVIDIA A100 GPU. 

29 

Figure 4: Two-tree Economy 

**==> picture [416 x 331] intentionally omitted <==**

**----- Start of picture text -----**<br>
5 DPI<br>Analytical<br>4 . 0<br>4<br>3 . 5<br>3<br>3 . 0<br>2<br>2 . 5<br>1<br>2 . 0<br>0 1 . 5<br>− 1 1 . 0<br>− 2 0 . 5<br>0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0 0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0<br>s s<br>(a) Risk-free Rate (b) Dividend Yield<br>7<br>6 4 . 0<br>5 3 . 5<br>4 3 . 0<br>3 2 . 5<br>2<br>2 . 0<br>1<br>1 . 5<br>0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0 0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0<br>s s<br>(c) Expected Return (d) Volatility<br>(%) (%)<br>Rate Yield<br>Risk-free Dividend<br>(%)<br>Return (%)<br>Volatility<br>Expected<br>**----- End of picture text -----**<br>


_Notes._ The figure shows the plots of the risk-free rate, dividend yield, expected return, and instantaneous volatility as a function of the first tree dividend share. The solid lines correspond to the numerical solutions, and the dashed lines correspond to the analytical solutions evaluated on the random test set. The values of the parameters are as follows: _ρ_ = 0 _._ 04, _γ_ = 1, _ϱ_ = _−_ 0 _._ 5, _µ_ 1 = 0 _._ 02, _µ_ 2 = 0 _._ 03, _σ_ 1 = 0 _._ 2 and _σ_ 2 = 0 _._ 3. We use a neural network to approximate normalized asset prices _V_ = _P ·_ ( _D_ 1 + _D_ 2) _[−][γ]_ . The iteration stops when the average error of the dividend yield is less than 10 _[−]_[5] . 

. 

distributions, we randomly draw 10,000 values for _s_ uniformly from [0 _,_ 1] and compute the value of the two measures for each draw. The panel on the left of Figure 5 shows the distribution of the absolute difference between the numerical and analytical solution for the dividend-yield, _εd_ ( **s** ) = log10 _|d_[numerical] ( **s** ) _− d_[analytical] ( **s** ) _|_ . For conciseness, we only report the accuracy for the dividend yield as the results for the other variables are similar. We find that the average deviation is _−_ 5 _._ 04, with a standard deviation of 0.34, showing that the solution is accurate approximately up to the fifth decimal 

30 

Figure 5: Error Distribution in a Two-tree Economy 

**==> picture [416 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
4 . 0<br>1 . 6<br>3 . 5<br>1 . 4<br>3 . 0<br>1 . 2<br>2 . 5<br>1 . 0<br>2 . 0<br>0 . 8<br>1 . 5 0 . 6<br>1 . 0 0 . 4<br>0 . 5 0 . 2<br>0 . 0 − 6 . 25 − 6 . 00 − 5 . 75 − 5 . 50 − 5 . 25 − 5 . 00 − 4 . 75 − 4 . 50 0 . 0 − 8 − 7 − 6 − 5 − 4 − 3<br>εd εHJB<br>(a) Deviation from the Analytical Solution (b) HJB Residual<br>Frequency Frequency<br>**----- End of picture text -----**<br>


_Notes._ The left panel shows the distribution of the (log10) absolute difference between the numerical and the analytical solution of the dividend yield, while the right panel shows the (log10) HJB residuals for a test set of 10,000 randomly drawn points with _s ∈_ [0 _,_ 1]. The iteration stops when the average error is less than 10 _[−]_[5] . 

place. 

Since _εd_ ( **s** ) requires the knowledge of the exact solution, this measure is restricted to economies for which closed-form solutions are available. For more complex economies where analytical solutions are not available, we consider a second measure of accuracy, namely the HJB residuals. The HJB residuals correspond to the normalized deviations _|_ HJB( **s** _,_ **c** ( **s** )) _|_ from the HJB equation, defined as _εHJB_ ( **s** ) = log10 _V_ ( **s** ) , where HJB( **s** _,_ **c** ( **s** )) is given in Eq.(10).[20] The panel on the right of Figure 5 shows the distribution of the HJB residuals. The distribution has a mean of _−_ 4 _._ 56 and a standard deviation of 0 _._ 56, once again showing that the solution has high accuracy. Combined, these results show that the distribution of HJB residuals is similar to the distribution of the absolute deviation errors, indicating that the two measures of accuracy are quantitatively similar. 

> 20 HJB residuals can be interpreted as the continuous-time analog of the Euler equation errors commonly used in discrete-time models. For a discussion of the use of this metric in continuous-time settings, see Parra-Alvarez (2018). 

31 

**Lucas Orchard.** The curse of dimensionality becomes apparent when we move from the two-tree Lucas economy of Cochrane et al. (2008) to the Lucas orchard economy of Martin (2013). The author generalizes the two-tree economy of Cochrane et al. (2008) by assuming the existence of _N_ trees and by relaxing the log utility assumption on the representative agent’s utility function. Martin (2013) provides semi-analytical expressions for the equilibrium quantities as functions of the _N −_ 1 dividend shares in the economy. However, the integral formulas are subject to a severe curse of dimensionality, which limits the applicability of the analytical results to setups with at most three or four trees. 

To illustrate how the DPI method can alleviate the curse of dimensionality, we conduct the following experiment. Starting from an economy with two trees, we gradually increase the number of identical trees in the economy and solve for the equilibrium using the DPI algorithm. We consider two stopping criteria. First, we stop the iteration when a MSE lower than 10 _[−]_[8] is achieved. Second, we adopt a more stringent accuracy metric and stop the iteration when the 90th percentile of the squared errors is lower than 10 _[−]_[8] . Panel (a) of Figure 6 shows the time in minutes to compute the solution using the two criteria. The figure shows that the DPI method produces accurate solutions for problems with a high-dimensional state space in a timely manner. Moreover, raising the dimensionality of the problem or considering a more stringent accuracy measure do not substantially increase the time-to-solution. For instance, even in an economy with 100 trees, it takes less than a minute for the DPI algorithm to reach an MSE of 10 _[−]_[8] . 

Panel (b) of Figure 6 shows the time-to-solution of the DPI method and the Smolyak method. The Smolyak method is arguably among the most widely used techniques in financial economics to tackle high-dimensional stochastic dynamic models.[21] Hence, 

> 21In recent years, some notable contributions have increased the efficiency and accuracy of the Smolyak methods. See e.g. Judd et al. (2014), Brumm and Scheidegger (2017), Brumm et al. (2022). 

32 

Figure 6: Accuracy and Time-to-Solution in a Lucas Orchard Economy 

**==> picture [324 x 217] intentionally omitted <==**

**----- Start of picture text -----**<br>
Minutes of Training for accuracy < 10 [−] [8]<br>Mean squared errors<br>90th percentile (squared errors)<br>0 . 30<br>0 . 25<br>0 . 20<br>0 . 15<br>0 . 10<br>0 . 05<br>2 20 40 60 80 100<br>Number of Trees<br>Minutes<br>**----- End of picture text -----**<br>


## (a) Time to solution 

**==> picture [324 x 217] intentionally omitted <==**

**----- Start of picture text -----**<br>
Minutes of Training for Accuracy < 10 [−] [3]<br>DPI<br>20 . 0 Smolyak2<br>Smolyak3<br>Smolyak4<br>17 . 5<br>15 . 0<br>12 . 5<br>10 . 0<br>7 . 5<br>5 . 0<br>2 . 5<br>0 . 0<br>2 5 8 10 12 15 20 25 26<br>Number of Trees<br>Minutes<br>**----- End of picture text -----**<br>


## (b) Smolyak methods and DPI algorithm MSEs. 

_Notes._ Panel (a) shows the time-to-solution of the DPI algorithm, measured by the number of minutes required for a given metric to be less than 10 _[−]_[8] . The blue line corresponds to the mean squared errors and the orange line corresponds to the 90th percentile of the squared errors. Panel (b) shows the time-to-solution of the DPI method and the Smolyak methods of orders 2, 3, and 4. The tolerance is set to 10 _[−]_[3] , which is the highest threshold reached by all the Smolyak methods. The parameter values are as follows: _ρ_ = 0 _._ 04, _γ_ = 1, _ϱ_ = 0 _._ 0, _µ_ = 0 _._ 015, and _σ_ = 0 _._ 1. The HJB errors are computed on a random sample of 2[13] points from the state space. 

33 

it is important to compare how our method performs relative to it. We consider the Smolyak method of orders 2, 3, and 4, and we solve for the coefficients using the conjugate gradient method. We set the tolerance for the MSE to 10 _[−]_[3] , the highest threshold reached by all versions of the Smolyak method. The time-to-solution of the different versions of the Smolyak method increases rapidly with the number of trees in the economy, and the computer runs out of memory for orchards with 8, 12, and 26 trees for the methods of order 2, 3, and 4, respectively. In contrast, the DPI method is able to maintain high accuracy with a relatively low time-to-solution for economies with a much larger number of trees. This illustrates the ability of the DPI method to alleviate the curse of dimensionality relative to previously known methods. 

**Economic consequences of large** _N_ **.** We consider next how the equilibrium objects vary the number of trees. We show that when the analysis is restricted to a small number of trees, either due to numerical limitations or for the sake of analytical tractability, important economic channels are overlooked. This leads to significantly different equilibrium outcomes, both quantitatively and qualitatively. 

We illustrate this point by examining the equilibrium objects of a Lucas orchard with _N_ trees for _N ∈{_ 2 _,_ 3 _,_ 5 _,_ 10 _,_ 50 _}_ . The dividend process is the same for all trees, with volatility _σ_ and pairwise correlation _ϱ_ . When _N >_ 2, we need to specify not only the share of the first tree _s_[1] but also the dividend share distribution of the remaining trees ( _s_[2] _, s_[3] _, . . . , s[N]_ ). To represent this high-dimensional object in a two-dimensional graph, we draw 10,000 values of ( _s_[2] _, s_[3] _, . . . , s[N]_ ), after being normalized to add up to one, from a symmetric Dirichlet distribution with concentration parameter _α_ and report equilibrium quantities averaged over these draws in Figure 7.[22] 

When _N_ = 2, we recover the results of Cochrane et al. (2008). In this economy, the dividend yield and the interest rate respond strongly to changes in the share of 

> 22 2 When _α ≈_ 1, the sampled dividend shares ( _st[, s]_[3] _t[, ..., s][N] t_[)][are][relatively][dispersed.][For][larger] values of _α_ , the sampled dividend shares become more concentrated around the center of the simplex, and the draws tend to be similar to each other, consistent with the economy being more diversified. 

34 

the first tree _s_[1] _t_[,][as][shown][in][Panels][(a)][and][(b)][of][Figure][7][.][The][risk][premium][is] positive, and the correlation between asset 1 returns and consumption is large, even as _s_[1] approaches zero, as shown in Panels (c) and (d). Similarly, consumption and return volatilities are also highly sensitive to changes in _s_[1] , as shown in Panels (e) and (f). 

Figure 7 shows that the results change substantially when _N_ is relatively large _and s_[1] is small, an important case largely ignored by the literature. This case is particularly important because, when _N_ = 2, either the economy is diversified and the trees are similar in size (i.e., there is no small asset as _s_[1] _≈ s_[2] _≈_ 0 _._ 5), or the economy has a small asset, but it is extremely underdiversified, with the larger tree being responsible for nearly all consumption. The graphs show that the three-tree economy ( _N_ = 3) analyzed by Martin (2013) experiences similar drawbacks, albeit to a lesser extent. In contrast, when _N_ is large, we can analyze the behavior of a small asset ( _s_[1] _≈_ 0) in an economy that is still reasonably diversified, where no single tree represents the entirety of consumption. 

For example, consider the case where _N_ = 50, and the dividend share of the first risky asset is in the range 0 _< s_[1] _<_ 20%. Note that the dividend yield and interest rate barely move as the dividend share of the first asset _s_[1] changes. The reason is that aggregate consumption volatility is roughly insensitive to this state variable in this region as the other 49 trees still provide enough diversification.[23] In the absence of the effects on aggregate volatility, movements in interest rates and in the dividend yield are muted. In stark contrast, when _N_ = 2, a reduction of _s_[1] from 20% to almost 0% substantially increases consumption volatility, resulting in significantly lower dividend yield and risk-free rate. 

An important economic insight derived from Figure 7 is that when the economy has many trees _and_ the dividend share _s_[1] is relatively small, the behavior of the economy resembles a fully diversified economy (horizontal red line) where consumption 

> 23Naturally, as _s_ 1 approaches 1, all economies behave similarly as the economy becomes concentrated on the first risky asset, regardless of the value of _N_ . 

35 

Figure 7: Equilibrium Quantities 

**==> picture [412 x 497] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 Fully N = 50 FullyDiversified<br>N = 50 Diversified<br>10<br>8 N = 10<br>N = 10<br>8<br>N = 5<br>6 N = 5<br>6<br>4 N = 3<br>N = 3<br>4<br>2 N = 2 αα  = 1 = 3 2 N = 2<br>0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0 0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0<br>s [1] s [1]<br>(a) Dividend Yield (b) Risk-free Rate<br>100<br>N = 50<br>4<br>80 N = 10<br>3 N = 2<br>60<br>2 N = 2<br>40<br>N = 3 N = 3<br>1<br>N = 50 FullyDiversified<br>Fully 20<br>Diversified<br>0<br>0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0 0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0<br>s [1] s [1]<br>(c) Equity Risk Premium (d) Corr( R 1 , dC/C )<br>10 N = 2<br>12<br>9 N = 3<br>8<br>11<br>7 N = 5<br>6 10 NN = 50= 10 FullyDiversified<br>5 N = 10<br>N = 5<br>9<br>4<br>N = 3<br>3 N = 50 8<br>Fully<br>Diversified<br>2 N = 2<br>0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0 0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0<br>s [1] s [1]<br>(e) Consumption Volatility (f) Asset 1 Volatility<br>(%) (%)<br>Yield Rate<br>Dividend Risk-free<br>(%)<br>(%))<br>RiskPremium , dC/CR 1<br>Corr(<br>Equity<br>(%)<br>Volatility (%)<br>Volatility<br>1<br>Asset<br>Consumption<br>**----- End of picture text -----**<br>


_Notes._ We discretize the interval (0 _,_ 1), representing the domain of the dividend share of the first risky asset _s_[1] , into 100 equal parts. For each given point in the grid, we draw 10,000 samples of the remaining _N −_ 1 dividend shares ( _s_[2] _, s_[3] _, ..., s[N]_ ) from a symmetric Dirichlet distribution with parameter _α_ . With 10,000 samples for each point _s_[1] in the grid, we then compute the equilibrium quantities by evaluating the trained neural network model at each point in space ( _s_[1] _, s_[2] _, ..., s[N]_ ) and averaging the result across the samples. We repeat this process for different levels of the concentration parameter _α_ in the interval [1 _,_ 3]. The remaining parameter values are as follows: _ρ_ = 0 _._ 04, _γ_ = 4, _ϱ_ = 0 _._ 04, _µ_ = 0 _._ 02, _σ_ = 0 _._ 1, and _σagg_ = 0 _._ 02. 

36 

is exposed to only an aggregate shock.[24] Moreover, our results provide a quantitative assessment of how _fast_ the equilibrium outcomes converge to this fully diversified benchmark. Even for moderately diversified economies, with _N_ = 5 or _N_ = 10, the market-clearing effects emphasized by Cochrane et al. (2008) get substantially attenuated, as seen, for instance, in panels (c) and (f) of Figure 7. 

Martin (2013) argues that the positive risk premium of a small asset ( _s_[1] _≈_ 0) is due to the high covariance of its valuation ratio with aggregate cash flows. As Figure 7 shows, these effects are greatly attenuated when there is sufficient diversification in the economy (e.g., _N_ = 50) and disappear when the economy is fully diversified. Thus, by lifting the numerical restrictions that had impeded the literature’s ability to analyze the behavior of small firms in well-diversified economies, the DPI method reveals that the positive risk premium of a small asset is a byproduct of a severely underdiversified economy. 

## **3.2 Corporate Finance** 

As our next application, we consider a canonical corporate finance model. Even though the model can be solved using standard numerical techniques, we illustrate how the DPI algorithm’s ability to handle large state spaces can be used by researchers to perform a _global sensitivity analysis_ . This is an important step in showing how different moments in the data are informative about specific parameters in the model in a transparent way.[25] Moreover, by considering a nonconvex optimization problem, we illustrate how the DPI method seamlessly handles severe nonlinearities in the solution, such as multiple kinks. 

> 24In the fully diversified economy the process for consumption is _dCt/Ct_ = _µdt_ + _σaggdZt_ , and dividend _j_ follows the process _dDj,t/Dj,t_ = _µdt_ + _σdZj,t_ , where _dZtdZj,t_ = _ϱ_ . We set _σagg_[2][=] _[ϱσ]_[2] (i.e, the minimum consumption variance in the Lucas orchard as _N →∞_ ), corresponding to the nondiversifiable risk in this economy. 

> 25For a discussion of the role of transparency in structural research, including its connection with sensitivity analysis, see Andrews et al. (2020). 

37 

**Model environment.** We present a simplified version of the model by Hennessy and Whited (2007) that includes costly equity issuance and investment adjustment costs. To simplify the exposition, we abstract from taxes and a corporate debt decision. We assume that there is a firm with operating profits following a standard Cobb-Douglas production function _π_ ( _kt, zt_ ) = _ztkt[α]_[,][with][elasticity] _[α][∈]_[(0] _[,]_[ 1)][.][There][are][two][state] variables that drive operating profits: total factor productivity (TFP hereafter) _zt_ and the capital stock _kt_ . TFP follows an Ornstein-Uhlenbeck process in logs: 

**==> picture [220 x 12] intentionally omitted <==**

Capital accumulates according to _[dk][t]_ = ( _it − δ_ ) _dt_ , where _it_ represents the firm’s _kt_ investment rate and _δ_ is the depreciation rate. Investment is subject to quadratic adjustment costs, Λ( _kt, it_ ) = 0 _._ 5 _χkti_[2] _t_[,][with] _[χ >]_[ 0][.] 

As in Hennessy and Whited (2007), we assume that raising external equity is costly, and equity issuance is subject to the linear cost _λ >_ 0. Since the firm’s operating profits net of investment costs is _Dt[∗]_[=] _[z][t][k] t[α][−]_[(] _[i][t]_[+ 0] _[.]_[5] _[χi]_[2] _t_[)] _[ k][t]_[,][the][firm’s][dividend] policy is given by 

**==> picture [275 x 14] intentionally omitted <==**

Eq.(19) shows that the firm pays a unit cost _λ_ if it decides to issue equity (i.e., if _Dt[∗][<]_[ 0][).] 

Given a discount rate _r >_ 0, the firm’s problem can be written as follows: 

**==> picture [311 x 30] intentionally omitted <==**

subject to Eq.(19), the law of motion of TFP and capital, the initial conditions _k_ 0 = _k_ and _z_ 0 = _z_ , and a vector of model parameters Φ. Notice that, contrary to common practice in the literature, we explicitly state the dependence of the value function 

38 

_V_ ( _k, z_ ; Φ) on the model parameters Φ to emphasize that the parameter choices alter the solution of the model. 

This dynamic corporate finance model helps illustrate different aspects of the DPI algorithm. First, unlike the endowment economy considered in Section 3.1, the dynamics of one of the state variables is endogenous since the investment decision determines capital accumulation. In this case, we need to approximate both the value and policy functions with neural networks. Moreover, while only the policy evaluation step of the DPI method was needed in the Lucas orchard economy, a problem with an endogenous state variable requires both policy evaluation and policy improvement to compute the solution. Second, the cost of issuing equity creates kinks in the policy functions. Because kinks are a ubiquitous feature in a wide class of models with occasionally binding constraints or transaction costs, it is important to assess how the solution method performs in such a case.[26] 

Figure 8 shows the policy functions _D_ ( _k, z_ ) and _i_ ( _k, z_ ) as a function of _k_ for different values of _z_ . The colored lines represent the solution obtained using the DPI method, while the black dashed lines represent the solution obtained using an implicit finite-differences scheme with a very fine grid, which serves as our benchmark. From the graphs, we observe that the solution using the DPI method closely tracks the solution obtained using finite differences. The accuracy of the solution is also demonstrated by the low log10 RMSE of the HJB residuals, which amounts to _−_ 5. 

The high accuracy level of the solution produced by the DPI algorithm is particularly noteworthy due to the presence of kinks in the firm’s optimal dividend policy. As shown in Figure 8, the dividend policy can be divided into three regions. When the firm has a large initial capital stock _k_ , it pays positive dividends. When the initial capital stock is small, the firm issues equity. However, for intermediate levels of capital, 

> 26The fact that the solution has kinks implies that a classical solution to the HJB equation for the firm’s problem in Eq.(20) does not exist and we instead look for a _viscosity solution_ to the HJB. For a discussion of viscosity solutions, see Crandall (1995) and Achdou et al. (2022). 

39 

Figure 8: Optimal Dividend Policy and Investment Rate 

**==> picture [416 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 . 75 1 . 50<br>z =0.87<br>0 . 50 1 . 25 zz =1.00=1.15<br>1 . 00<br>0 . 25<br>0 . 75<br>0 . 00<br>0 . 50<br>− 0 . 25<br>0 . 25<br>− 0 . 50<br>0 . 00<br>− 0 . 75 − 0 . 25<br>− 1 . 00 − 0 . 50<br>− 1 . 25 − 0 . 75<br>5 10 15 20 25 30 35 40 5 10 15 20 25 30 35 40<br>Capital Capital<br>(a) Dividends (b) Investment Rate<br>Rate<br>Dividends<br>Investment<br>**----- End of picture text -----**<br>


_Notes._ The figure shows the plots of the optimal dividend policy and optimal investment rate as a function of the capital stock for different values of TFP. The colored lines (dotted, dash-dotted, and solid lines) represent the solution using the DPI method, and the black dashed lines represent the solution using an upwind finite differences method with 23,001 grid points (451 for capital and 51 for TFP). The RMSE of the HJB residuals for the DPI solution is 2 _._ 0 _×_ 10 _[−]_[5] , computed on a random sample of 8 _,_ 192 _,_ 000 observations (2[14] parallel simulations of size 2 _,_ 000) sampled from the ergodic distribution. The value of the parameters are as follows: _δ_ = 0 _._ 1, _α_ = 0 _._ 55, _λ_ = 0 _._ 059, _θ_ = 0 _._ 26, and _σz_ = 0 _._ 123. The network takes as inputs the states ( _k, z_ ) and the vector of model parameters Φ. The network was trained in approximately 1 hour. 

the firm neither pays dividends nor issues equity, creating _an inaction region_ . The differences in the firm’s payout policy in each region give rise to kinks in the optimal dividend policy function. Nonetheless, these nonlinearities do not pose a challenge for the DPI algorithm, which accurately captures both the region of inaction for dividends and the corresponding kinks. 

**Global sensitivity analysis and universal value functions.** For a given parametrization, the previous model can easily be solved using a standard numerical method such as finite differences. However, since the model’s results might be dependent on the chosen parametrization, we are often interested in the solution for different parameter values to check the robustness of our findings to changes in the parameter space in the context of structural work.[27] Thus, global sensitivity analysis is critical to identify which moments in the data are particularly informative about 

> 27A recent literature emphasizes the importance of sensitivity analysis in the context of structural analysis. See e.g. Andrews et al. (2017), Armstrong and Kolesár (2021), and Catherine et al. (2022). 

40 

each parameter. However, because calibration or structural estimation may require solving the model for a large number of parameter values, sensitivity analysis can become computationally very costly and impractical in many cases. 

To overcome the high computational cost of performing sensitivity analysis or structural estimation, we exploit the ability of the DPI algorithm to handle highdimensional problems and include the model parameters as inputs to the neural network, as suggested by our formulation in Eq.(20). In our experiment, this increases the computational cost only slightly, but once the network is trained, the solution is available for any point in the state and parameter spaces.[28] 

In the literature on deep-reinforcement learning (Schaul et al., 2015), approximators similar to _V_ ( _k, z_ ; Φ) are known as _universal value functions_ (UVFs hereafter).[29] In our experiment, the UVF depends on the state variables ( _k, z_ ) and the vector of parameters Φ = ( _λ, δ, α, θ, σ_ ), for a total of seven variables.[30] The proposed approach allows us to obtain at once the solution for an entire _class_ of models. 

Figure 9 shows the results of the global sensitivity analysis for our version of the Hennessy and Whited model. The figure shows selected moments of the equilibrium variables as a function of the parameters Φ = ( _λ, δ, α, θ, σ_ ). As illustrated, the average profitability is sensitive to _α_ , while the average investment rate is particularly sensitive to _δ_ . Note that the sensitivity of the moments to the parameters varies depending on the region of the parameter space. For example, for low-volatility firms, average equity issuance is relatively insensitive to _σ_ , while for high-volatility firms, equity issuance is highly sensitive to _σ_ . This particular feature of the solution could not be uncovered using a local sensitivity measure, such as the one proposed by Andrews et al. (2017). The authors recommend that a local measure of the sensitivity of estimated parameter values to moments should be reported along with the results of a structural estimation. 

> 28We thank an anonymous referee for pointing out this fact to us. 

> 29See Norets (2012) for an early application of this approach in a discrete-choice setting. 

> 30 To ease exposition and limit the number of results to report, we fix the values of _r_ and _χ_ . It is straightforward to include these parameters and perform sensitivity analysis with respect to them. 

41 

Figure 9: Global Sensitivity Analysis 

**==> picture [524 x 426] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 . 010 0 . 20 0 . 4 0 . 04<br>0 . 50<br>0 . 15 0 . 03<br>0 . 3 0 . 45<br>0 . 005<br>0 . 10 0 . 40 0 . 02<br>0 . 2<br>0 . 000 0 . 05 0 . 35 0 . 01<br>0 . 00 0 . 1 0 . 30 0 . 00<br>0 . 05 0 . 10 0 . 05 0 . 10 0 . 05 0 . 10 0 . 05 0 . 10 0 . 05 0 . 10<br>λ λ λ λ λ<br>0 . 010 0 . 20 0 . 4 0 . 04<br>0 . 50<br>0 . 15 0 . 03<br>0 . 3 0 . 45<br>0 . 005<br>0 . 10 0 . 40 0 . 02<br>0 . 2<br>0 . 000 0 . 05 0 . 35 0 . 01<br>0 . 00 0 . 1 0 . 30 0 . 00<br>0 . 02 0 . 08 0 . 15 0 . 02 0 . 08 0 . 15 0 . 02 0 . 08 0 . 15 0 . 02 0 . 08 0 . 15 0 . 02 0 . 08 0 . 15<br>δ δ δ δ δ<br>0 . 010 0 . 20 0 . 4 0 . 04<br>0 . 50<br>0 . 15 0 . 03<br>0 . 3 0 . 45<br>0 . 005<br>0 . 10 0 . 40 0 . 02<br>0 . 2<br>0 . 000 0 . 05 0 . 35 0 . 01<br>0 . 00 0 . 1 0 . 30 0 . 00<br>0 . 4 0 . 5 0 . 6 0 . 4 0 . 5 0 . 6 0 . 4 0 . 5 0 . 6 0 . 4 0 . 5 0 . 6 0 . 4 0 . 5 0 . 6<br>α α α α α<br>0 . 010 0 . 20 0 . 4 0 . 04<br>0 . 50<br>0 . 15 0 . 03<br>0 . 3 0 . 45<br>0 . 005<br>0 . 10 0 . 40 0 . 02<br>0 . 2<br>0 . 000 0 . 05 0 . 35 0 . 01<br>0 . 00 0 . 1 0 . 30 0 . 00<br>0 . 20 0 . 25 0 . 30 0 . 20 0 . 25 0 . 30 0 . 20 0 . 25 0 . 30 0 . 20 0 . 25 0 . 30 0 . 20 0 . 25 0 . 30<br>θ θ θ θ θ<br>0 . 010 0 . 20 0 . 4 0 . 04<br>0 . 50<br>0 . 15 0 . 03<br>0 . 3 0 . 45<br>0 . 005<br>0 . 10 0 . 40 0 . 02<br>0 . 2<br>0 . 000 0 . 05 0 . 35 0 . 01<br>0 . 00 0 . 1 0 . 30 0 . 00<br>0 . 05 0 . 18 0 . 30 0 . 05 0 . 18 0 . 30 0 . 05 0 . 18 0 . 30 0 . 05 0 . 18 0 . 30 0 . 05 0 . 18 0 . 30<br>σ σ σ σ σ<br>Issuance Rate Autocorr.<br>Profitability<br>Equity Investment Prof. STD(Residual)<br>Issuance Rate Autocorr.<br>Profitability<br>Equity Investment Prof. STD(Residual)<br>Issuance Rate Autocorr.<br>Profitability<br>Equity Investment Prof. STD(Residual)<br>Issuance Rate Autocorr.<br>Profitability<br>Equity Investment Prof. STD(Residual)<br>Issuance Rate Autocorr.<br>Profitability<br>Equity Investment Prof. STD(Residual)<br>**----- End of picture text -----**<br>


_Notes._ The figure shows the plots of the following moments as a function of the parameters: (i) average equity issuance: E[min _{Dt,_ 0 _}_ ], (ii) average investment rate: E[ _it_ ], (iii) average profitability: E[ _pt_ ], _pt ≡ π_ ( _kt, zt_ ) _/kt_ , (iv) annual autocorrelation of profitability: the slope coefficient of the regression _pt_ +1 = _α_ + _βpt_ + _σϵϵt_ +1, and (v) the volatility of future profitability conditional on current profitability: _σϵ_ . The model solution is obtained by approximating value and policy functions by neural networks including the vector of parameters as inputs. For each column, we fix the parameters at the baseline values and then vary each parameter individually. The moments are computed by simulating 2[12] economies in parallel for 2 _,_ 000 periods, after dropping 1 _,_ 000 burn-in periods. The SDE is simulated using the Euler method with a time step of 0.05. 

Figure 10: Moments Scatter Plots 

**==> picture [436 x 117] intentionally omitted <==**

**----- Start of picture text -----**<br>
Equity Issuance ( R [2] = 1 . 00) Investment Rate ( R [2] = 1 . 00) Profitability ( R [2] = 1 . 00) Prof. Autocorr. ( R [2] = 1 . 00) STD(Residual) ( R [2] = 1 . 00)<br>0 . 040 0 . 55<br>0 . 14 0 . 07<br>0 . 035 0 . 40<br>0 . 030 0 . 12 0 . 35 0 . 50 0 . 06<br>0 . 025 0 . 10 0 . 05<br>0 . 30 0 . 45<br>0 . 020 0 . 04<br>0 . 08<br>0 . 015 0 . 25 0 . 40 0 . 03<br>0 . 06<br>0 . 010 0 . 20 0 . 02<br>0 . 005 0 . 04 0 . 15 0 . 35 0 . 01<br>0 . 000 0 . 02 0 . 30 0 . 00<br>0 . 00 0 . 01 0 . 02 0 . 03 0 . 04 0 . 00 0 . 05 0 . 10 0 . 15 0 . 1 0 . 2 0 . 3 0 . 4 0 . 3 0 . 4 0 . 5 0 . 6 0 . 00 0 . 02 0 . 04 0 . 06 0 . 08<br>**----- End of picture text -----**<br>


_Notes._ The figure shows the scatterplots of moments computed using the DPI method, as described in Figure 9, against the solution using an upwind finite-differences method with 23,001 grid points (451 points for capital and 51 points for TFP). For the computation of the model-implied moments using the finite differences solution, we interpolate the points outside the grid with nearest-neighbor interpolation. 

In a sense, the sensitivity analysis we propose is a global version of their measure, as it allows one to assess how parameters affect moments not only in the neighborhood of the estimated parameters but also for parameters far from their estimated values.[31] 

To check the accuracy of the UVF approach, we compute the moments for 100 random draws from the parameter space and compare the solutions produced by a finite-difference method with a fine grid (our proxy for the exact solution) and our UVF approximator. Figure 10 shows the _R_[2] values for a regression comparing the moments computed with the DPI method with those computed with finite differences. The resulting _R_[2] is very close to one for all moments, and the moments computed with the DPI method and finite differences are very similar. 

In summary, this exercise shows that the DPI method can be useful even when the model in question has a small number of state variables. In addition, while we have focused exclusively on the important topic of global sensitivity analysis, it is 

> 31A similar approach to performing a global sensitivity analysis was recently proposed by Scheidegger and Bilionis (2019); Kase et al. (2022); Catherine et al. (2022). Similar to Duarte (2018), Catherine et al. (2022) construct moment networks that produce predicted moments as functions of the model parameters. The authors propose to construct a large dataset of model parameters and their corresponding moments by solving a model tens of thousands of times. Alternatively, one can leverage the DPI method to construct the same dataset by including the parameters as inputs to the network and solving the model only once. 

43 

worth noting that similar methods can be used for structural estimation. For example, Duarte (2018) builds on the methods of this paper to show that UVFs can be used to efficiently estimate structural models. 

## **3.3 Portfolio Choice** 

In this section, we consider a high-dimensional version of the portfolio problem of Campbell and Viceira (1999) with time-varying expected returns. We first demonstrate our method’s ability to provide accurate solutions. Since closed-form solutions are typically not available for these highly nonlinear problems, we propose a new method to test the accuracy of the DPI solution which consists of reverse engineering a portfolio problem with a known solution in a high-dimensional space. We then consider an empirically motivated portfolio problem with multiple risky assets and realistic return dynamics. 

## **3.3.1 Reverse engineering a portfolio problem** 

**Model environment.** Consider the problem of an investor with CRRA utility function who must choose the consumption policy _Ct_ and the fraction of wealth invested in a (single) risky asset _αt_ , for given exogenous processes for the interest rate _rt_ and the risk premium _ξt_ , in order to maximize her expected utility function: 

**==> picture [324 x 32] intentionally omitted <==**

subject to the wealth dynamics 

**==> picture [222 x 13] intentionally omitted <==**

Here, **Z** _t_ is an ( _N_ + 1)-dimensional Brownian motion, and _σ_ **r** is a constant ( _N_ + 1)dimensional (row) vector. The risk-free rate _rt_ = _r_ ( **x** _t_ ) and the risk premium _ξt_ = _ξ_ ( **x** _t_ ) 

44 

are assumed to be time-varying and driven by an _N_ -dimensional state variable **x** _t_ , with dynamics given by 

**==> picture [290 x 13] intentionally omitted <==**

where _µ_ **x** ( **x** _t_ ) is an _N_ -dimensional vector and _σ_ **x** ( **x** _t_ ) is an _N ×_ ( _N_ + 1) matrix. 

The vector **x** _t_ represents state variables that capture return predictability. It can include financial measures such as the dividend-yield, the term spread, the investmentcapital ratio of Cochrane (1991), the consumption-wealth ratio _cay_ of Lettau and Ludvigson (2001), the accounting growth measures of Daniel and Titman (2006), among many others.[32] We are interested in finding the optimal portfolio share _α_ ( **x** _t_ ) and the consumption policy _C_ ( **x** _t_ ), given the dynamics of the predictors **x** _t_ in Eq.(22), the risk-free rate _r_ ( **x** _t_ ), and the risk premium _ξ_ ( **x** _t_ ). 

**Reverse engineering.** Since a closed-form solution to the previous problem is typically not available, we propose to reverse engineer the functions _r_ ( **x** ) and _ξ_ ( **x** ) to achieve any desired solution policies _α_ ( **x** ) and _C_ ( **x** ). We can then use the DPI method with the reverse-engineered functions _r_ ( **x** ) and _ξ_ ( **x** ) to solve this high-dimensional portfolio problem and compare the solution of the algorithm with the known functions _α_ ( **x** ) and _C_ ( **x** ) that were initially specified by the investigator. 

To illustrate the proposed procedure, consider first a simple transformation of the consumption policy _Ct_ that simplifies our exposition. By writing the value function in Eq.(21) as _V_ ( _W,_ **x** ) = _ϕ_ ( **x** ) _[W]_[ 1] _[−][γ]_[where] _[ϕ]_[(] **[x]**[)][is][a][value-function][shifter][to][be] 1 _− γ_[,] determined, the first-order condition implies that _Ct_ = _ϕ_ ( **x** _t_ ) _[−] γ_[1] _Wt_ . Since there is a one-to-one mapping between the consumption policy and the value-function shifter, giving a functional form to the value-function shifter _ϕ_ ( **x** _t_ ) is equivalent to modeling the consumption policy _Ct_ = _C_ ( **x** _t_ ) and vice versa. Moreover, the dynamics of the 

> 32For analyses and reviews of the empirical performance of market return predictors, see Welch and Goyal (2008), Koijen and Van Nieuwerburgh (2011), and Lewellen (2015). 

45 

value-function shifter _ϕt_ can be easily obtained by a simple application of Ito’s lemma: 

**==> picture [145 x 28] intentionally omitted <==**

Suppose now that the functional form of _ϕ_ ( **x** ) and _α_ ( **x** ) are known and set exogenously by the investigator. The functions _ξ_ ( **x** ) and _r_ ( **x** ) can be derived from the investor’s optimality conditions and the investor’s HJB equation, respectively, which yield the following expressions 

**==> picture [440 x 56] intentionally omitted <==**

Thus, the expressions in Eqs.(23) and (24) allow us to obtain the values of _ξ_ ( **x** ) and _r_ ( **x** ) associated with any given value-function shifter _ϕ_ ( **x** ) and portfolio share _α_ ( **x** ). 

We use this procedure to test the ability of the DPI algorithm to produce accurate solutions in high-dimensional portfolio-choice problems. Rather than choosing the functions _ϕ_ and _α_ based on economic considerations, we select functional forms that are known to be challenging for standard methods to approximate. We consider an empirically motivated case below. More specifically, for the value function shifter _ϕ_ ( **x** ), we choose a multivariate version of the Runge function 

**==> picture [274 x 53] intentionally omitted <==**

which is typically used in numerical analysis to illustrate the difficulties of interpolation with polynomials.[33] For the portfolio share, we consider a highly nonlinear function that is capable of generating rich patterns for the relationship between the portfolio 

> 33For a discussion of the Runge function and the corresponding challenges of approximating this function numerically, see Epperson (1987), for example. 

46 

Figure 11: Value-Function Shifter and Portfolio Share 

**==> picture [416 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 . 0 xx −− 11 =0.0=0.1 1 . 0<br>x − 1 =0.2<br>0 . 9 0 . 8<br>0 . 8<br>0 . 6<br>0 . 7<br>0 . 4<br>0 . 6<br>0 . 2<br>0 . 5<br>0 . 0<br>− 0 . 3 − 0 . 2 − 0 . 1 0 . 0 0 . 1 0 . 2 0 . 3 − 0 . 3 − 0 . 2 − 0 . 1 0 . 0 0 . 1 0 . 2 0 . 3<br>x 1 x 1<br>)(shifter φ x )(asset x α<br>risky<br>the<br>of<br>Value-function Share<br>**----- End of picture text -----**<br>


_Notes._ The figure shows the plots of the value-function shifter and the portfolio share as a function of the first predictor, _x_ 1, given the value of the remaining predictors, **x** _−_ 1, and _W_ = 1. The colored lines (dotted, dash-dotted, and solid lines) represent the solution using the DPI method, and the black dashed lines correspond to the exact solution given by Eqs.(25) and (26). The RMSE of the HJB residuals for the DPI solution is 2 _×_ 10 _[−]_[3] , computed on a random sample of 8 _,_ 192 _,_ 000 observations (2[14] parallel simulations of size 2 _,_ 000) sampled from the ergodic distribution. The value of the parameters are as follows: _γ_ = 2, _ρ_ = 0 _._ 04, _µ_ **x** ( **x** ) = _−_ 0 _._ 45 **x** , _σ_ **x** _,i_ ( **x** ) = 0 _._ 1 **e** _i_ , _σ_ **r** = 0 _._ 2 **e** _N_ +1, _N_ = 10. The functions _ξ_ ( **x** ) and _r_ ( **x** ) are given by Eqs.(23) and (24). The network was trained in approximately 1 minute. 

share and a given predictor; an important feature given the variety of predictors proposed in the literature. We model _α_ ( **x** ) as 

**==> picture [278 x 37] intentionally omitted <==**

In our numerical exercise, we set the number of predictors to _N_ = 10 so that it is in the ballpark of the number of predictors in the "kitchen sink" regression of Welch and Goyal (2008). We set _µ_ **x** ( **x** ) = _−_ 0 _._ 45 **x** and _σ_ **x** _,i_ ( **x** ) = 0 _._ 1 **e** _i_ , where _σ_ **x** _,i_ ( **x** ) denotes the _i_ -th row of _σ_ **x** ( **x** ) and **e** _i_ is the ( _N_ + 1)-th dimensional canonical basis vector in the _i_ -th direction. Therefore, the predictors follow uncorrelated Ornstein–Uhlenbeck processes with a volatility of 10% and a half-life of roughly 1.5 years, which is the average persistence of the different predictors reported in Gârleanu and Pedersen (2013).[34] We set _σ_ **r** = 0 _._ 2 _eN_ +1 so that return volatility is 20% and return innovations 

> 34The assumption that the predictors are uncorrelated can be interpreted as an extreme form of 

47 

Figure 12: DPI vs Exact Solution Scatterplots 

**==> picture [416 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Value Function ( R [2] = 1 . 00) Asset Allocation ( R [2] = 1 . 00)<br>1 . 0<br>− 0 . 2<br>0 . 8<br>− 0 . 4<br>0 . 6<br>− 0 . 6 0 . 4<br>− 0 . 8 0 . 2<br>− 1 . 0 0 . 0<br>− 1 . 0 − 0 . 8 − 0 . 6 − 0 . 4 − 0 . 2 0 . 0 0 . 2 0 . 4 0 . 6 0 . 8 1 . 0<br>Exact Solution Exact Solution<br>Solution Solution<br>DPI DPI<br>**----- End of picture text -----**<br>


_Notes._ The figure shows the scatterplots of the value function (left panel) and portfolio share (right panel) computed using the DPI method against the exact solution given by Eqs.(25) and (26). 

are uncorrelated with the predictors. We assume that the risk aversion coefficient is _γ_ = 2 and the time-preference parameter is _ρ_ = 0 _._ 04. 

**Numerical results.** Figure 11 shows the value-function shifter and the portfolio share, respectively, as a function of the first predictor, _x_ 1, for different values of the remaining predictors. The colored lines represent the solution obtained with the DPI method, and the black dashed lines correspond to the exact solution, as given by Eqs.(25) and (26). The approximate solution closely tracks the exact solution, and the log10 RMSE of the HJB residuals is _−_ 3, indicating that the solution is sufficiently accurate. Note that the solutions obtained with the DPI method for the value-function shifter _ϕ_ ( **x** ) and the portfolio share _α_ ( **x** ) do not exhibit the type of oscillations typically found in polynomial approximations of these functions. In addition, the portfolio share _α_ ( **x** ) shows a rich pattern of behavior depending on the value of predictors 2 through 10. The functions can be V-shaped, increasing, or decreasing as a function of _x_ 1 depending on the value of the remaining predictors **x** _−_ 1. Despite this wide range of 

a shrinkage estimator applied to the variance-covariance matrix. For the importance of covariance shrinkage in portfolio optimization, see Ledoit and Wolf (2004) and Pedersen et al. (2021). 

48 

behavior, the DPI method is able to accurately represent all these curves. 

To further assess the accuracy of the solution, we consider a random sample of points drawn from the state space and compare the exact and approximate solutions. Figure 12 shows a scatter plot of the solution obtained using the DPI method against the exact solution. The points line up closely over the 45 _[◦]_ degree line and the _R_[2] of the two regressions are essentially one. 

## **3.3.2 Portfolio Choice with Realistic Dynamics** 

In this final application, we use the DPI algorithm to solve a high-dimensional portfolio choice problem calibrated with realistic asset-pricing dynamics in which the expected returns on different asset classes are driven by several macro-finance variables. 

**Problem description.** We depart from the portfolio problem discussed in Section 3.3.1 in three important dimensions. First, we build on the state-of-the-art affine model of Jiang et al. (2019) to discipline the evolution of expected returns. In particular, we consider a flexible model for the state-price density (SPD) that accurately prices stocks, nominal bonds, and inflation-protected bonds. Second, we assume that the investor has recursive preferences with a risk aversion coefficient _γ_ and an elasticity of intertemporal substitution (EIS) _ψ_ . Third, the investor has access to five risky assets in addition to a risk-free money market account. The vector of risky assets includes stocks, long- and medium-term nominal bonds, and long- and medium-term real bonds. 

Expected returns are driven by a _N ×_ 1 vector of state variables **x** _t ∈_ R _[N]_ . The vector of state variables evolves according to a multivariate Ornstein-Uhlenbeck process: 

**==> picture [273 x 13] intentionally omitted <==**

where Φ _∈_ R _[N][×][N]_ is a matrix of coefficients and _σ_ **x** _∈_ R _[N][×][N]_ is a matrix of loadings 

49 

on the _N ×_ 1 Brownian motion **Z** _t_ . The real risk-free rate _r_ ( **x** _t_ ) and the _N ×_ 1 vector of market prices of risk _**η**_ ( **x** _t_ ) are assumed to be affine functions of **x** _t_ , with _r_ ( **x** _t_ ) = _r_ 0 + _**r**[⊤]_ 1 **[x]** _[t]_[and][the] _**[η]**_[(] **[x]** _[t]_[) =] _**[ η]**_ 0[+] _**[ η]**[⊤]_ 1 **[x]** _[t]_[.] 

**Estimation of the state dynamics.** We assume that there are _N_ = 11 state variables, comprised of the financial and macroeconomic variables described in Table 2. These variables include standard bond and stock market predictors as well as relevant macroeconomic variables. 

Data on the state variables **x** _t_ are sampled in discrete intervals and their process can be estimated by fitting a VAR(1): 

**==> picture [261 x 13] intentionally omitted <==**

where Ψ is a _N × N_ matrix of coefficients, **u** _t_ = **B** _**ϵ** t_ is a _N ×_ 1 vector of shocks, **B** is a _N × N_ lower-triangle matrix of loadings, and _**ϵ** t ∼N_ (0 _, IN_ ). The time-integrated version of the continuous-time process in Eq.(27) implies specific values for Ψ and **B** . We can then recover the continuous-time parameters Φ and _σ_ **x** from the discrete-time VAR by solving an inverse problem in the spirit of Campbell et al. (2004), i.e., finding the continuous-time parameters that when time-integrated deliver the estimated VAR coefficients. Appendix C describes this problem in detail. 

**Estimation of the state-price density.** Given the assumption on the affine structure of _r_ ( **x** ) and _**η**_ ( **x** ), we derive closed-form expressions for bond yields and expected stock returns and then search for the parameters _r_ 0, _**r**_ 1, _**η**_ 0 and _**η**_ 1 to minimize the squared residuals between the model-implied time-integrated values and the corresponding data for 12 time series: one-, two-, five-, ten-, 20-, and 30-year nominal yields, five-, seven-, ten-, 20-, and 30-year real yields, and expected stock returns. Figure 13 shows the model fit for six selected series. Similar results hold 

50 

Table 2: List of State Variables Driving the Expected Returns of Assets 

|**Variable**|**Description**|**Mean**|**S.D.**(%)|
|---|---|---|---|
|_πt_|Log Infation|0.032|2.3|
|_y_$ _t_ (1)<br>_yspr_$ _t_<br>∆_zt_<br>∆_dt_|Log 1-Year Nominal Yield<br>Log 5-Year Minus 1-Year Nominal Yield Spread<br>Log Real GDP Growth<br>Log Stock Dividend-to-GDP Growth|0.043<br>0.006<br>0.030<br>-0.002|3.1<br>0.7<br>2.4<br>6.3|
|_dt_|Log Stock Dividend-to-GDP Level|-0.270|30.5|
|_pdt_<br>∆_τt_<br>_τt_<br>∆_gt_<br>_gt_|Log Stock Price-to-Dividend Ratio<br>Log Tax Revenue-to-GDP Growth<br>Log Tax Revenue-to-GDP Level<br>Log Spending-to-GDP Growth<br>Log Spending-to-GDP Level|3.537<br>0.000<br>-1.739<br>0.006<br>-1.749|42.6<br>5<br>6.5<br>7.6<br>12.9|



_Notes:_ The table shows the list of 11 state variables driving expected returns in our economy, along with their mean and standard deviation. The data are collected from `https://www.publicdebtvaluation.com/data` . 

for the remaining six variables. As illustrated, the model can accurately capture the evolution of nominal and real bonds of different maturities. Moreover, the equity premium implied by the model closely matches the conditional equity premium in the data implied by the VAR. 

Given ( _r_ ( **x** _t_ ) _,_ _**η**_ ( **x** _t_ )) and the state dynamics in Eq.(27), we can derive the 5 _×_ 1 vector of expected excess return _**ξ**_ ( **x** _t_ ) for risky assets and the matrix of loadings on the Brownian shocks _σ_ **R** _∈_ R[5] _[×]_[11] to describe the investor’s investment opportunity set and the dynamics of the investor’s wealth.[35] 

**The investor’s optimization problem.** With the investment opportunity set fully described, we turn to the optimization problem faced by the investor. The agent chooses consumption _Ct_ and portfolio shares _**α** t ∈_ R[5] _[×]_[1] to solve the following optimization problem: 

**==> picture [322 x 30] intentionally omitted <==**

35See Appendix C for a detailed derivation of the model and a thorough discussion of the estimation process for this exercise. 

51 

Figure 13: Time Series of Bond Yields and Equity Expected Returns 

**==> picture [432 x 347] intentionally omitted <==**

**----- Start of picture text -----**<br>
1-yr Nominal Yield 1947-01-01 / 2019-01-01 5-yr Nominal Yield 1947-01-01 / 2019-01-01 10-yr Nominal Yield 1947-01-01 / 2019-01-01<br>14 Data 14 14<br>Model<br>12<br>12 12<br>10<br>10 10<br>8<br>8 8<br>6<br>6<br>6<br>4<br>4<br>4<br>2<br>2<br>0 2<br>1950 1960 1970 1980 1990 2000 2010 2020 1950 1960 1970 1980 1990 2000 2010 2020 1950 1960 1970 1980 1990 2000 2010 2020<br>Equity Return 1947-01-01 / 2019-01-01 5-yr Real Yield 1947-01-01 / 2019-01-01 10-yr Real Yield 1947-01-01 / 2019-01-01<br>50<br>40 8 8<br>30 6 6<br>20 4<br>4<br>10 2<br>2<br>0 0<br>0<br>1950 1960 1970 1980 1990 2000 2010 2020 1950 1960 1970 1980 1990 2000 2010 2020 1950 1960 1970 1980 1990 2000 2010 2020<br>(%)<br>Rate<br>(%)<br>Rate<br>**----- End of picture text -----**<br>


_Notes._ The figure shows the time series for nominal yields, real yields, and equity expected return for the model (solid black line) and the data (dashed blue line). The maturity for the nominal yields are one, five, and ten years. The maturity for the real yields are five and ten years. 

subject to the state dynamics in Eq.(27), the wealth dynamics 

**==> picture [274 x 16] intentionally omitted <==**

the position limits 0 _≤ αj,t ≤_ 1 for _j_ = 1 _, . . . ,_ 5, the natural borrowing limit _Wt ≥_ 0, and initial conditions _W_ 0 = _W_ and **x** 0 = **x** . The preference aggregator is given 1 _−ψ−_ 1 by _f_ ( _C, V_ ) = _ρ_[(] 1[1] _−[−] ψ[γ][−]_[)] _[V]_[1] ((1 _−γ_ ) _CV_ ) 1 _−_ 1 _γ_ � _−_ 1 _,_ where _ρ_ is the time-preference pa�� � rameter. The position limits imply the investor is not allowed to short sell or use leverage. 

52 

Figure 14: Time Series of Expected Returns and Optimal Allocations 

**==> picture [416 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
40 Risk-freeStockMediumMediumLong RealRealNominalBondBondBond 100 Risk-freeStockMediumMediumLongLong RealNominalRealNominalrateBondBondBondBond<br>Long Nominal Bond 80<br>30<br>60<br>20<br>40<br>10<br>20<br>0<br>− 10 0<br>1949 1959 1969 1979 1989 1999 2009 2019 1950 1960 1970 1980 1990 2000 2010 2020<br>Year Year<br>(a) Expected Returns (b) Asset Allocation<br>(%)<br>(%)<br>Returns Weights<br>Expected Portfolio<br>**----- End of picture text -----**<br>


_Notes._ Panel (a) shows the time series of expected returns implied by the model for five asset classes: equities, nominal and real long-term bonds (i.e., ten-year maturity), and nominal and real medium-term bonds (i.e., five-year maturity), for the period 1949–2019. The NBER recession periods are indicated as grey bars. Panel (b) shows the time series of the optimal asset allocation computed using the DPI algorithm for an investor with recursive utility solving the optimization problem in Eq.(29), given the dynamics of expected returns shown in Panel (a) and preferences parameters _ρ_ = 0 _._ 04, _γ_ = 20, and _ψ_ = 0 _._ 5. 

**Optimal allocation.** We use the DPI algorithm to find the optimal consumption and portfolio plans that solve the optimization problem in Eq.(29). Panel (a) of Figure 14 shows the evolution of expected returns for the six asset classes. Expected returns show substantial variability over our sample period and exhibit a strong cyclical component, with large spikes in expected excess returns during recessions. 

Panel (b) of Figure 14 shows the optimal allocation for an investor with a coefficient of risk aversion _γ_ = 20 and EIS _ψ_ = 0 _._ 5.[36] The solution shows that the investor engages in market timing to a great extent. For instance, the investor held a substantial amount of stocks during the 1950s and 1960s, but she was nearly out of the stock market during the early 1970s. Similarly, the optimal solution is essentially to stay away from stocks during the early 2000s, at the height of the Dot-Com Bubble. 

An important feature of the optimal portfolio is the substantial demand for inflationprotected bonds. The holdings of medium- and long-term real bonds are substantial 

> 36Appendix C discusses how the preference parameters impact the optimal allocation. 

53 

during several periods in our sample. Even though inflation-protected bonds were only introduced in the US in the late 1990s, our model enables us to assess what would the optimal holdings of these bonds be if they were available throughout our sample period. 

Figure 14 also shows a rich pattern of substitution between stocks and bonds. For instance, as investors reduce their exposure to stocks in the early 1970s, they substantially increase their holdings of long-term real bonds. In contrast, as investors reduce again their exposure to stocks during the early 2000s, they shift their portfolio mostly to nominal bonds this time. To better understand these substitution patterns, we consider next how the policy functions vary with each state variable in isolation. 

**Policy functions.** Figure 15 shows how the consumption-wealth ratio and the portfolio share of the different assets respond to changes in the state variables. Each line shows the response of an outcome as we vary a given state variable by _±_ 1 standard deviations, while we keep the remaining variables at their average level. 

Panel (a) of Figure 15 shows how the investor’s consumption behavior responds to changes in the state variables. An increase in expected returns, as captured for example by higher short-term interest rates or lower price-dividend ratio, leads to an increase in the consumption-wealth ratio. Hence, the investor saves _less_ when returns are high, consistent with the income effect dominating the substitution effect in savings decision, in line with our assumption of a low EIS ( _ψ_ = 0 _._ 5). 

As expected, the portfolio share of stocks is decreasing in the price-dividend ratio, as a high price-dividend ratio forecasts lower future returns. More interestingly, Panel (b) of Figure 15 shows that the share of stocks on the portfolio also responds to variables typically associated with the bond market, such as the yield spread or the inflation rate. This captures the substitution pattern between stocks and bonds. 

The demand for long-term real bonds is naturally increasing in the inflation rate, 

54 

## Figure 15: Optimal Policy Functions 

**==> picture [416 x 500] intentionally omitted <==**

**----- Start of picture text -----**<br>
6 . 75 πyt [$][(1)] 100<br>6 . 50 yspr ∆∆ zd t [$]<br>dpd 80<br>6 . 25 ∆ τ τ<br>∆ g<br>6 . 00 g 60<br>5 . 75<br>40<br>5 . 50<br>20<br>5 . 25<br>5 . 00 − 1 . 00 − 0 . 75 − 0 . 50 − 0 . 25 0 . 00 0 . 25 0 . 50 0 . 75 1 . 00 − 1 . 00 − 0 . 75 − 0 . 50 − 0 . 25 0 . 00 0 . 25 0 . 50 0 . 75 1 . 00<br>State State<br>(a) Consumption-Wealth Ratio (b) Stock<br>60 80<br>50<br>60<br>40<br>30 40<br>20<br>20<br>10<br>0 0<br>− 1 . 00 − 0 . 75 − 0 . 50 − 0 . 25 0 . 00 0 . 25 0 . 50 0 . 75 1 . 00 − 1 . 00 − 0 . 75 − 0 . 50 − 0 . 25 0 . 00 0 . 25 0 . 50 0 . 75 1 . 00<br>State State<br>(c) Nominal Long-Term Bond (d) Real Long-Term Bond<br>1 . 0<br>25<br>0 . 5 20<br>15<br>0 . 0<br>10<br>− 0 . 5 5<br>0<br>− 1 . 0 − 1 . 00 − 0 . 75 − 0 . 50 − 0 . 25 0 . 00 0 . 25 0 . 50 0 . 75 1 . 00 − 1 . 00 − 0 . 75 − 0 . 50 − 0 . 25 0 . 00 0 . 25 0 . 50 0 . 75 1 . 00<br>State State<br>(e) Nominal Medium-Term Bond (f) Real Medium-Term Bond<br>(%)<br>Ratio (%)<br>Allocation<br>Stock<br>Consumption-Wealth<br>(%)<br>(%)<br>Allocation<br>Allocation<br>Bond<br>Bond<br>Long-Term<br>Long-Term<br>Real<br>Nominal<br>(%)<br>(%)<br>Allocation<br>Allocation<br>Bond<br>Bond<br>Medium-Term<br>Medium-Term<br>Real<br>Nominal<br>**----- End of picture text -----**<br>


_Notes._ The panels show the optimal policies computed with the DPI algorithm as a function of the 11 state variables. The effects on consumption-wealth ratio, stock, nominal long-term bond, real long-term bond, nominal medium-term bond, and real medium-term bond are represented in Panels (a), (b), (c), (d), (e), and (f), respectively. Long-term bonds have ten-year maturity and medium-term bonds mature in five years. The x-axis is measured in standard deviations for each state variable. 

55 

as these bonds are designed to provide inflation protection. For small deviations of inflation from its mean, the investor obtains this protection only from long-term bonds, while for large deviations the investor uses both medium- and long-term bonds. We also find that the demand for inflation-protected bonds is very sensitive to movements in the price-dividend ratio, a standard stock market predictor. Notice this is not a mechanical effect, as the investor could have chosen instead to raise her holdings of short-term bonds or long-term nominal bonds when stocks become less attractive due to a high price-dividend ratio. 

The way the investor reallocates her portfolio is more intricate for changes in the yield spread. An increase in the yield spread leads to a reduction in stock holdings and an initial increase in real long-term bonds. For larger deviations of the yield spread, the investor shifts away from real bonds towards long-term nominal bonds. This behavior leads to highly nonlinear policy functions that are unlikely to be captured by the log-linear approximations commonly used in portfolio problems. Moreover, for the range of parameters we consider, the agent does not invest in the medium-term nominal bond. 

**Portfolio sensitivities.** In our last analysis, we investigate what are the main economic factors driving changes in portfolio allocation. To assess that, for a given asset _j_ , we decompose the change in its weights from time _t_ to _t_ + 1 as: 

**==> picture [218 x 35] intentionally omitted <==**

and define the sensitivity of asset _j_ to state variable _i_ at time _t_ + 1 as: 

**==> picture [302 x 68] intentionally omitted <==**

56 

Table 3: Sensitivities 

||_π_|_y_$ _t_ (1)|_yspr_$ _t_|∆_z_|∆_d_|_d_|_pd_|fscal|
|---|---|---|---|---|---|---|---|---|
|10y Nominal|5.9|6.4|19.6|17.3|11.6|3.1|12.1|24.1|
|10y Real<br>Risk-free|6.6<br>5.6|5.2<br>6.1|18.1<br>21.0|18.9<br>17.3|15.2<br>10.4|2.5<br>3.7|12.3<br>10.3|21.2<br>25.6|
|5y Nominal|5.1|6.7|21.5|18.0|9.4|3.1|9.9|26.3|
|5y Real<br>Stock|4.3<br>10.7|5.9<br>2.9|20.9<br>13.6|18.2<br>18.5|10.1<br>14.7|3.0<br>2.5|11.3<br>21.6|26.3<br>15.5|



_Notes._ The table shows the average sensitivity of the asset allocations as a percentage of wealth with respect to each of the 11 state variables listed in Table 2. The sensitivity of the allocations is computed as in Eq.(30). The column “fiscal” shows the sum of the sensitivities for all fiscal variables. 

By construction, the sum of the sensitivities of an asset allocation with respect to the 11 state variables adds up to one, which allows us to interpret this measure as the relative importance of each state variable for a given asset allocation, at a given time. 

Table 3 shows the sensitivities for all assets averaged over our sample period. Movements in the price-dividend ratio account on average for 22% of the variability in the share invested on stocks, while the yield spread accounts for 14%, inflation 11%, and fiscal variables 15%. Interestingly, all fiscal variables together account for more than 20% of the variability in real and nominal long-term bonds. This is more than the fraction explained by the short-rate or the term spread, commonly used predictors of bond returns. 

Taken together, these results indicate that the optimal portfolio follows a rich pattern that cannot be easily captured by rule-of-thumbs such as a 60 _−_ 40 allocation or simple age-dependent rules. It is important to take into account market conditions as captured by key macroeconomic and financial variables. 

## **4 Conclusion** 

This paper proposes a novel numerical method that alleviates the three curses of dimensionality. The method rests on three pillars. First, it uses deep learning to represent value and policy functions. Second, it combines Ito’s lemma and automatic 

57 

differentiation to compute exact expectations with negligible additional computational cost. Third, it uses a gradient-based version of policy iteration that dispenses rootfinding methods to find the optimal control for a given state. We show that the DPI method has broad applicability in several areas of Finance, such as asset pricing, corporate finance, and portfolio choice, and that it can solve complex large-dimensional problems with highly nonlinear dynamical systems. 

The ability to solve rich high-dimensional problems can be an invaluable tool in economic analysis. We oftentimes are forced to make assumptions that have no clear economic interest but are necessary for the model solution to be feasible. This often makes it hard to determine whether results are due to these auxiliary assumptions or to the economically motivated ones. By significantly expanding the set of models that researchers can solve, or even potentially estimate, our methods enable researchers to focus on models that better capture the rich phenomena that we observe in modern economies, instead of focusing on models that current numerical methods can solve. 

58 

## **References** 

- Achdou, Y., Buera, F. J., Lasry, J.-M., Lions, P.-L., Moll, B., 2014. Partial differential equation models in macroeconomics. Philosophical Transactions of the Royal Society of London A: Mathematical, Physical and Engineering Sciences 372. 

- Achdou, Y., Han, J., Lasry, J.-M., Lions, P.-L., Moll, B., 2022. Income and wealth distribution in macroeconomics: A continuous-time approach. Review of Economic Studies 89, 45–86. 

- Ahn, S., Kaplan, G., Moll, B., Winberry, T., Wolf, C., 2018. When inequality matters for macro and macro matters for inequality. NBER macroeconomics annual 32, 1–75. 

- Andrews, I., Gentzkow, M., Shapiro, J. M., 2017. Measuring the sensitivity of parameter estimates to estimation moments. Quarterly Journal of Economics 132, 1553–1592. 

- Andrews, I., Gentzkow, M., Shapiro, J. M., 2020. Transparency in structural research. Journal of Business & Economic Statistics 38, 711–722. 

- Angrist, J. D., Pischke, J.-S., 2008. Mostly Harmless Econometrics: An Empiricist’s Companion. Princeton University Press. 

- Armstrong, T. B., Kolesár, M., 2021. Sensitivity analysis using approximate moment condition models. Quantitative Economics 12, 77–108. 

- Azinovic, M., Gaegauf, L., Scheidegger, S., 2022. Deep equilibrium nets. International Economic Review 63, 1471–1525. 

- Baird, L., 1995. Residual algorithms: Reinforcement learning with function approximation. In: Prieditis, A., Russell, S. (eds.), _Machine Learning Proceedings 1995_ , Morgan Kaufmann, San Francisco (CA), pp. 30–37. 

- Bali, T. G., Beckmeyer, H., Mörke, M., Weigert, F., 2023. Option return predictability with machine learning and big data. Review of Financial Studies . 

- Baydin, A. G., Pearlmutter, B. A., Radul, A. A., 2015. Automatic differentiation in machine learning: A survey. CoRR abs/1502.05767. 

- Bellman, R., 1957. Dynamic Programming. Princeton University Press, Princeton, NJ, USA, first ed. 

- Bianchi, D., Büchner, M., Tamoni, A., 2021. Bond risk premiums with machine learning. Review of Financial Studies 34, 1046–1089. 

- Bretscher, L., Fernández-Villaverde, J., Scheidegger, S., 2022. Ricardian business cycles. Available at SSRN . 

- Brumm, J., Krause, C., Schaab, A., Scheidegger, S., 2022. Sparse Grids for Dynamic Economic Models. In: Oxford Research Encyclopedia of Economics and Finance. 

59 

- Brumm, J., Scheidegger, S., 2017. Using adaptive sparse grids to solve high-dimensional dynamic models. Econometrica 85, 1575–1612. 

- Brunnermeier, M., Sannikov, Y., 2016. Macro, money, and finance: A continuous-time – 

- approach. Elsevier, vol. 2 of _Handbook of Macroeconomics_ , pp. 1497 1545. 

- Brunnermeier, M. K., Sannikov, Y., 2014. A macroeconomic model with a financial sector. American Economic Review 104, 379–421. 

- Bybee, L., Kelly, B. T., Manela, A., Xiu, D., 2021. Business news and business cycles. Available at SSRN . 

- Campbell, J. Y., Chacko, G., Rodriguez, J., Viceira, L. M., 2004. Strategic asset allocation in a continuous-time var model. Journal of Economic Dynamics and Control 28, 2195–2214. 

- Campbell, J. Y., Viceira, L. M., 1999. Consumption and portfolio decisions when expected returns are time varying. Quarterly Journal of Economics 114, 433–495. 

- Cao, S., Jiang, W., Yang, B., Zhang, A. L., 2023. How to Talk When a Machine Is Listening: Corporate Disclosure in the Age of AI. Review of Financial Studies . 

- Catherine, S., Ebrahimian, M., Sraer, D., Thesmar, D., 2022. Robustness checks in structural analysis. Tech. rep., National Bureau of Economic Research. 

- Cauchy, A., 1847. Méthode générale pour la résolution des systemes d’équations simultanées. Comp. Rend. Sci. Paris 25, 536–538. 

- Chen, H., Didisheim, A., Scheidegger, S., 2021. Deep structural estimation: With an application to option pricing. arXiv preprint arXiv:2102.09209 . 

- Chen, L., Pelger, M., Zhu, J., 2023. Deep learning in asset pricing. Management Science . 

- Cochrane, J. H., 1991. Production-based asset pricing and the link between stock returns and economic fluctuations. Journal of Finance 46, 209–237. 

- Cochrane, J. H., Longstaff, F. A., Santa-Clara, P., 2008. Two trees. Review of Financial Studies 21, 347–385. 

- Crandall, M. G., 1995. Viscosity solutions: A primer. In: _Viscosity Solutions and Applications_ . 

- Cybenko, G., 1989. Approximation by superposition of sigmoidal functions. Mathematics of Control, Signals and Systems 2, 303–314. 

- Daniel, K., Titman, S., 2006. Market reactions to tangible and intangible information. Journal of Finance 61, 1605–1643. 

60 

- Drechsler, I., Savov, A., Schnabl, P., 2018. A model of monetary policy and risk premia. Journal of Finance 73, 317–373. 

- Duarte, V., 2018. Gradient-based structural estimation. Available at SSRN 3166273 . 

- Duarte, V., Duarte, D., Fonseca, J., Montecinos, A., 2020. Benchmarking machinelearning software and hardware for quantitative economics. Journal of Economic Dynamics and Control 111, 103796. 

- Duarte, V., Fonseca, J., Goodman, A. S., Parker, J. A., 2021. Simple allocation rules and optimal portfolio choice over the lifecycle. Tech. rep., National Bureau of Economic Research. 

- Epperson, J. F., 1987. On the runge example. The American Mathematical Monthly 94, 329–341. 

- Fernández-Villaverde, J., Hurtado, S., Nuno, G., 2023. Financial frictions and the wealth distribution. Econometrica 91, 869–901. 

- Fernández-Villaverde, J., Levintal, O., 2018. Solution methods for models with rare disasters. Quantitative Economics 9, 903–944. 

- Folini, D., Kübler, F., Malova, A., Scheidegger, S., 2021. The climate in climate economics. arXiv preprint arXiv:2107.06162 . 

- Fuster, A., Goldsmith-Pinkham, P., Ramadorai, T., Walther, A., 2022. Predictably unequal? the effects of machine learning on credit markets. Journal of Finance 77, 5–47. 

- Gârleanu, N., Pedersen, L. H., 2013. Dynamic trading with predictable returns and transaction costs. Journal of Finance 68, 2309–2340. 

- Goodfellow, I., Bengio, Y., Courville, A., 2016. Deep Learning. MIT Press. 

- Gopalakrishna, G., 2021. Aliens and continuous time economies. Swiss Finance Institute Research Paper . 

- Griewank, A., Walther, A., 2008. Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation. Society for Industrial and Applied Mathematics, USA, second ed. 

- Gu, S., Kelly, B., Xiu, D., 2020. Empirical asset pricing via machine learning. Review of Financial Studies 33, 2223–2273. 

- Han, J., Yang, Y., et al., 2021. Deepham: A global solution method for heterogeneous agent models with aggregate shocks. arXiv preprint arXiv:2112.14377 . 

- Haugh, M. B., Kogan, L., 2004. Pricing american options: A duality approach. Operations Research 52, 258–270. 

61 

- Heess, N., TB, D., Sriram, S., Lemmon, J., Merel, J., Wayne, G., Tassa, Y., Erez, T., Wang, Z., Eslami, S. M. A., Riedmiller, M. A., Silver, D., 2017. Emergence of locomotion behaviours in rich environments. CoRR abs/1707.02286. 

- Hennessy, C. A., Whited, T. M., 2007. How costly is external financing? evidence from a structural estimation. Journal of Finance 62, 1705–1745. 

- Hornik, K., 1991. Approximation capabilities of multilayer feedforward networks. – 

- Neural Networks 4, 251 257. 

- Howard, R. A., 1960. Dynamic Programming and Markov Processes. MIT Press, Cambridge, MA. 

- Jarrett, K., Kavukcuoglu, K., LeCun, Y., et al., 2009. What is the best multistage architecture for object recognition? In: _Computer Vision, 2009 IEEE 12th International Conference on_ , IEEE, pp. 2146–2153. 

- Jiang, Z., Lustig, H., Van Nieuwerburgh, S., Xiaolan, M. Z., 2019. The us public debt valuation puzzle. Tech. rep., National Bureau of Economic Research. 

- Judd, K. L., Maliar, L., Maliar, S., Valero, R., 2014. Smolyak method for solving dynamic economic models: Lagrange interpolation, anisotropic grid and adaptive – 

- domain. Journal of Economic Dynamics and Control 44, 92 123. 

- Kargar, M., 2021. Heterogeneous intermediary asset pricing. Journal of Financial Economics 141, 505–532. 

- Kase, H., Melosi, L., Rottner, M., 2022. Estimating nonlinear heterogeneous agents models with neural networks. CEPR Discussion Paper No. DP17391 . 

- Koijen, R. S., Van Nieuwerburgh, S., 2011. Predictability of returns and cash flows. Annual Review of Financial Economics 3, 467–491. 

- Krizhevsky, A., Sutskever, I., Hinton, G. E., 2012. Imagenet classification with deep convolutional neural networks. In: Pereira, F., Burges, C. J. C., Bottou, L., Weinberger, K. Q. (eds.), _Advances in Neural Information Processing Systems 25_ , Curran Associates, Inc., pp. 1097–1105. 

- Ledoit, O., Wolf, M., 2004. Honey, I shrunk the sample covariance matrix. Journal of Portfolio Management 30, 110. 

- Lettau, M., Ludvigson, S., 2001. Consumption, aggregate wealth, and expected stock returns. Journal of Finance 56, 815–849. 

- Lewellen, J., 2015. The cross-section of expected stock returns. Critical Finance Review 4, 1–44. 

- Li, K., Mai, F., Shen, R., Yan, X., 2021. Measuring corporate culture using machine learning. Review of Financial Studies 34, 3265–3315. 

62 

- Liaw, R., Liang, E., Nishihara, R., Moritz, P., Gonzalez, J. E., Stoica, I., 2018. Tune: A research platform for distributed model selection and training. arXiv preprint arXiv:1807.05118 . 

- Lillicrap, T. P., Hunt, J. J., Pritzel, A., Heess, N., Erez, T., Tassa, Y., Silver, D., Wierstra, D., 2015. Continuous control with deep reinforcement learning. CoRR abs/1509.02971. 

- Ljungqvist, L., Sargent, T., 2000. Recursive Macroeconomic Theory. MIT Press. 

- Longstaff, F. A., Schwartz, E. S., 2001. Valuing American options by simulation: A simple least-squares approach. Review of Financial Studies 14, 113–147. 

- Lucas, R. E., 1978. Asset prices in an exchange economy. Econometrica 46, 1429–1445. 

- Maliar, L., Maliar, S., 2022. Deep learning classification: Modeling discrete labor choice. Journal of Economic Dynamics and Control 135, 104295. 

- Maliar, L., Maliar, S., Winant, P., 2021. Deep learning for solving dynamic economic models. Journal of Monetary Economics 122, 76–101. 

- Martin, I., 2013. The Lucas orchard. Econometrica 81, 55–111. 

- Mnih, V., Kavukcuoglu, K., Silver, D., Rusu, A. A., Veness, J., Bellemare, M. G., Graves, A., Riedmiller, M., Fidjeland, A. K., Ostrovski, G., Petersen, S., Beattie, C., Sadik, A., Antonoglou, I., King, H., Kumaran, D., Wierstra, D., Legg, S., Hassabis, D., 2015. Human-level control through deep reinforcement learning. Nature 518, 529–533. 

- Moreira, A., Savov, A., 2017. The macroeconomics of shadow banking. Journal of Finance 72, 2381–2432. 

- Nagel, S., 2021. Machine learning in asset pricing, vol. 1. Princeton University Press. 

- Norets, A., 2012. Estimation of dynamic discrete choice models using artificial neural network approximations. Econometric Reviews 31, 84–106. 

- Parra-Alvarez, J. C., 2018. A comparison of numerical methods for the solution of continuous-time dsge models. Macroeconomic Dynamics 22, 1555–1583. 

- Pedersen, L. H., Babu, A., Levine, A., 2021. Enhanced portfolio optimization. Financial Analysts Journal 77, 124–151. 

- Piazzesi, M., 2010. Affine term structure models. In: _Handbook of financial econometrics: Tools and Techniques_ , Elsevier, pp. 691–766. 

- Powell, W. B., 2007. Approximate Dynamic Programming: Solving the Curses of Dimensionality (Wiley Series in Probability and Statistics). Wiley-Interscience, New York, NY, USA. 

63 

- Rapin, J., Teytaud, O., 2018. Nevergrad - A gradient-free optimization platform. `https://GitHub.com/FacebookResearch/Nevergrad` . 

- Ross, S. A., 1976. Options and efficiency. Quarterly Journal of Economics 90, 75–89. 

- Rumelhart, D. E., Hinton, G. E., Williams, R. J., 1988. Neurocomputing: Foundations of research. MIT Press, Cambridge, MA, USA, chap. Learning Representations by Back-propagating Errors, pp. 696–699. 

- Sadhwani, A., Giesecke, K., Sirignano, J., 2021. Deep learning for mortgage risk. Journal of Financial Econometrics 19, 313–368. 

- Sauzet, M., 2021. Projection methods via neural networks for continuous-time models. Available at SSRN 3981838 . 

- Schaul, T., Horgan, D., Gregor, K., Silver, D., 2015. Universal value function approximators. In: _International conference on machine learning_ , PMLR, pp. 1312–1320. 

- Scheidegger, S., Bilionis, I., 2019. Machine learning for high-dimensional dynamic stochastic economies. Journal of Computational Science 33, 68–82. 

- Silver, D., Huang, A., Maddison, C. J., Guez, A., Sifre, L., van den Driessche, G., Schrittwieser, J., Antonoglou, I., Panneershelvam, V., Lanctot, M., Dieleman, S., Grewe, D., Nham, J., Kalchbrenner, N., Sutskever, I., Lillicrap, T., Leach, M., Kavukcuoglu, K., Graepel, T., Hassabis, D., 2016. Mastering the game of Go with deep neural networks and tree search. Nature 529, 484–489. 

- Silver, D., Schrittwieser, J., Simonyan, K., Antonoglou, I., Huang, A., Guez, A., Hubert, T., Baker, L., Lai, M., Bolton, A., Chen, Y., Lillicrap, T., Hui, F., Sifre, L., van den Driessche, G., Graepel, T., Hassabis, D., 2017. Mastering the game of Go without human knowledge. Nature 550, 354 EP –. 

- Song, X., Perel, S., Lee, C., Kochanski, G., Golovin, D., 2023. Open source vizier: Distributed infrastructure and API for reliable and flexible blackbox optimization. 

- Stokey, N., Lucas, R., Prescott, E., 1989. Recursive Methods in Economic Dynamics. Harvard University Press. 

- Sutton, R. S., Barto, A. G., 1998. Introduction to Reinforcement Learning. MIT Press, Cambridge, MA, USA, first ed. 

- Wachter, J. A., 2013. Can time-varying risk of rare disasters explain aggregate stock market volatility? Journal of Finance 68, 987–1035. 

- Welch, I., Goyal, A., 2008. A comprehensive look at the empirical performance of equity premium prediction. Review of Financial Studies 21, 1455–1508. 

64 

## **A Proofs** 

_Proof of Proposition 1._ Since the second derivative of _F_ ( _t_ ) is given by 

**==> picture [366 x 72] intentionally omitted <==**

evaluating it at _t_ = 0 gives 

**==> picture [204 x 54] intentionally omitted <==**

which concludes the proof. 

## **B Time-varying Disasters and Epstein-Zin Preferences** 

In this section, we extend the method presented in Section 2 to solve an equilibrium problem where agents have Epstein-Zin preferences and the state variable is driven by a jump-diffusion process. To achieve this goal, we consider the model of Wachter (2013), which has the two aforementioned features and allows the equilibrium quantities to be characterized in closed form. Similar to the analysis of the Lucas orchard economy in Section 3.1, we use the analytical expressions to assess the accuracy of our numerical solution. 

65 

**Model environment.** The economy of Wachter (2013) can be briefly summarized as follows. Aggregate dividends follow the jump-diffusion process of the form 

**==> picture [175 x 27] intentionally omitted <==**

where _Jt_ is a random variable with time-invariant distribution _ν_ , and _Nt_ is a Poisson process with time-varying intensity process _λt_ satisfying a standard Cox–Ingersoll–Ross process 

**==> picture [170 x 16] intentionally omitted <==**

All random variables are assumed to be independent. The representative investor has the continuous-time analog of Epstein-Zin preferences with unit elasticity of intertemporal substitution (EIS); that is, the value function _Vt_ satisfies 

**==> picture [124 x 28] intentionally omitted <==**

**==> picture [286 x 17] intentionally omitted <==**

In this economy, the state variables driving the equilibrium quantities are the agent’s wealth _Wt_ and the time-varying intensity process _λt_ . As shown in Wachter (2013), the investor’s HJB equation is given by 

**==> picture [409 x 50] intentionally omitted <==**

Here, _C_ = _βW_ , and the value function assumes the form 

**==> picture [281 x 31] intentionally omitted <==**

66 

where _I_ ( _λt_ ) = _e[a]_[+] _[bλ][t]_ , with _a_ and _b_ as coefficients given in Wachter (2013). 

**DPI method with jumps.** In the absence of jumps, the HJB equation in Eq.(31) contains no integral and depends only on the partial derivatives of the value function, which can be easily evaluated using the methods described in Section 2.1. In the presence of jumps, however, the HJB equation in Eq.(31) contains an integral, which in principle would require a numerical integration method. Computing this integral can be potentially very costly, making the numerical solution of models with jumps particularly challenging.[37] However, by using simulation methods analogous to the Least-Squares Monte Carlo method (LSMC hereafter) of Longstaff and Schwartz (2001), commonly used to price American options, we can bypass the evaluation of the integral. 

To understand how this variation of the DPI method works, consider the following rewrite of the HJB in Eq.(31): 

**==> picture [317 x 27] intentionally omitted <==**

where 

**==> picture [370 x 27] intentionally omitted <==**

**==> picture [368 x 27] intentionally omitted <==**

The term in Eq.(34) comes from the Brownian shock and can be computed exactly using Proposition 1, as the previous examples in the paper illustrate. The term in Eq.(35) comes from the jump shock and involves an integral that in principle must be approximated, which can be computationally costly. 

> To bypass numerical integration, we simply need to implement two modifications 

> 37See Fernández-Villaverde and Levintal (2018) for a discussion of the challenges of solving models with rare disasters. 

67 

that are surprisingly straightforward, but conceptually powerful: ( _i_ ) for a given minibatch of _I_ samples of the state variable _{λi}[I] i_ =1[, approximate] _[ λ]_[E] � _V_ ( _We[J] , λ_ ) _− V_ ( _W, λ_ )� by a single random realization _λi_ � _V_ ( _Wie[J][i] , λi_ ) _− V_ ( _Wi, λi_ )�, and ( _ii_ ) use the MSE as the loss function in the policy evaluation step. 

The reason why these two seemingly straightforward modifications work is as follows. When using the Policy Evaluation 1 rule in Eq.(17), the HJB residuals are used to construct the continuous-time Bellman target for the regression, as in Eq.(15). For a given realization _Ji_ , the regression target in Eq.(15) becomes 

**==> picture [420 x 51] intentionally omitted <==**

where 

**==> picture [317 x 27] intentionally omitted <==**

However, as it is well known in the statistics and econometrics literature (Angrist and Pischke, 2008), when the MSE is used as the loss function in the regression, minimizing this loss leads to the estimation of the _conditional expectation function_ . Longstaff and Schwartz (2001) leverage this fundamental statistical result to estimate conditional expectations using regressions, and this is precisely what we do here too. Indeed, the minimization of the mean square errors using samples as in Equation 36 produces the conditional expectation 

**==> picture [443 x 60] intentionally omitted <==**

which is identical to the targets we would have used if we could compute the[]] _[i]_ expectation[E] _[J]_[[] _dt[dV]_ exactly. 

68 

The implementation of the policy evaluation in the presence of jumps is summarized in the following pseudo-algorithm: 

**Algorithm 1** Policy evaluation in the presence of jumps 

1: **procedure** PolicyEvaluation( _**θ**[j] V[−]_[1] ) _▷_ Update the value function. 

- 2: Draw _{λ_ 1 _, . . . , λI}_ random points from the state space. 

3: Compute[E] _[B] dt_[[] _[dV]_[]] _[i]_ using Proposition 1 as before. 

- 4: Sample one realization of _Ji_ per sample point. 

5: Construct the vector of targets _Yi[j]_[for][the][points] _[λ][i]_[,][with] _[i]_[ = 1] _[,]_[ 2] _[, ..., I]_[:] 

**==> picture [380 x 30] intentionally omitted <==**

6: Construct the vector of residuals as _e[j] i_[=] _[ V] i[j][−]_[1] _− Yi[j]_[.] 7: Use the SGD algorithm to update _**θ**[j] V_[:] 

**==> picture [176 x 35] intentionally omitted <==**

- 8: **return** _**θ**[j] V_ 

**==> picture [220 x 11] intentionally omitted <==**

**Numerical solution.** Figure 16 shows the analytical solution (dashed black line) for the value-function shifter _I_ ( _λt_ ), and the numerical solution produced by the DPI method (solid blue line). As illustrated, the numerical solution is virtually indistinguishable from the analytical solution. The log RMSE of the HJB residuals is _−_ 5, demonstrating that the DPI method is able to provide an accurate solution to this asset pricing problem in a much more complex environment with time-varying disaster risk and recursive preferences. 

69 

Figure 16: Value Function: Model with Jumps 

**==> picture [378 x 261] intentionally omitted <==**

**----- Start of picture text -----**<br>
DPI<br>Analytical<br>450<br>400<br>350<br>300<br>250<br>0 . 00 0 . 05 0 . 10 0 . 15 0 . 20 0 . 25 0 . 30<br>λ<br>)<br>λ<br>(<br>I<br>**----- End of picture text -----**<br>


_Notes._ The figure shows the value-function shifter _I_ ( _λ_ ) for the solution using the DPI method (red solid line) and the exact solution (black dashed line). Parameter values are as in Wachter (2013). For the network architecture, we use LayerNormMLP with SILU activation with [32 _,_ 32] hidden units. Each iteration is performed on a random batch of size 4,096. The optimizer is Adam with default parameters (learning rate = 10 _[−]_[3] , _β_ 1 = 0 _._ 9, and _β_ 2 = 0 _._ 999). 

## **C The Empirical No-Arbitrage Model** 

In this section, we discuss the estimation of the parameters governing the state dynamics and the parameters from our proposed SPD, which together determine the process for expected returns for the risky asset in the portfolio problem of Section 3.3. 

**Data description.** We collect the data used in Jiang et al. (2019) from the authors website `https://www.publicdebtvaluation.com/data` . The dataset contains annual data on the 11 state variables listed in Table 2, from January 1947 to January 2020. We use this data set to calibrate the dynamics of the state variables that drive asset risk premia. The bond yield data are from the Federal Reserve Economic Data (FRED) 

70 

database. 

**Identifying the vector of state variables.** While the vector of state variables is in principle unobservable, we can recover **x** _t_ from the data if we can observe enough variables that are an affine transformation of the latent variables. Since we assume that the state variables in **x** _t_ are stationary in our model, their empirical counterparts must be stationary as well. Under the assumption that the variables listed in Table 2 are affine functions of **x** _t_ and using the fact that the units of **x** _t_ are not identified, we can simply take those listed variables, after being demeaned, to equal the vector **x** _t_ . 

An important observation is that log GDP, denoted by _zt_ , is not a stationary variable, and as a consequence, it cannot be one of the latent variables. However, we assume that the state variables in **x** _t_ carry information about the expected GDP growth. Specifically, we assume that log GDP satisfies the SDE: 

**==> picture [280 x 15] intentionally omitted <==**

where the expected GDP growth rate _µz_ ( **x** _t_ ) is such that a the time-integrated GDP growth, ∆ _zt_ +1, is a stationary variable and a function of the state variable **x** _t_ . Similarly, the change in the price level (inflation index) is also modeled as an affine function of **x** _t_ . In addition, we assume that the log stock dividend-to-GDP _dt_ , the log tax revenue-to-GDP _τt_ , and the log spending-to-GDP _gt_ are stationary variables and a function of the state variable **x** _t_ . As GDP, dividends, spending, and tax revenues are all non-stationary variables, this assumption captures a set of co-integrating relations between these variables. The fact these variables are stationary implies that we must also include their changes to the VAR, so we have effectively a vector error correction model (VECM). By allowing the change in a variable to depend on its level, we capture mean reversion in the scaled variables. 

71 

## **Step 1: Estimation of the state dynamics.** 

Once the vector of state variables **x** _t_ is identified, the first step of the portfolio-choice exercise with realistic dynamics is to obtain the parameters for the continuous-time counterpart of the VAR system governing the evolution of the state variables. To obtain these parameters, we proceed as follows. 

Consider a _N ×_ 1 vector of state variables **x** _t_ in continuous time that follows an affine diffusion process: 

**==> picture [120 x 12] intentionally omitted <==**

where Φ is a _N × N_ matrix of coefficients, **Z** _t_ is a _N_ -dimensional Brownian motion, and _σ_ **x** is a _N × N_ matrix of risk loadings. 

Our goal is to find the matrices Φ and _σ_ **x** such that the time-integrated process has a given VAR coefficients matrix Ψ and loading matrix **B** , as shown in Eq. (28). Formally, this is a _inverse problem_ and can be solved with standard optimization techniques. We start by deriving closed-form expressions for the discrete-time VAR parameters as a function of Φ and _σ_ **x** (the forward problem). The inverse problem then boils down to solving a system of nonlinear equations. 

From the properties of the Ornstein-Uhlenbeck process, we can write the continuoustime process as: 

**==> picture [162 x 13] intentionally omitted <==**

_t_ +∆ _t_ where **u** _t_ +∆ _t ≡_ exp ( _−_ Φ( _t_ + ∆ _t − s_ )) _σ_ **x** _d_ **Z** _s_ . � _t_ 

Matching the integrated continuous-time process with its discrete-time counterpart, we obtain the following relationship between Φ and Ψ: 

**==> picture [78 x 13] intentionally omitted <==**

72 

Table 4: State Variables Dynamics: _d_ **x** _t_ = _−_ Φ **x** _tdt_ + _σ_ **x** _d_ **Z** _t_ 

||a|e :|tate|raes|yna|cs:|**x**_t_ =_−_|**x**_tt_|_σ_**x**|_t_||
|---|---|---|---|---|---|---|---|---|---|---|---|
||||||Φ|||||||
||_π_|_y_$ _t_ (1)|_yspr_$ _t_|∆_z_|∆_d_|_d_|_pd_|∆_τ_|_τ_|∆_g_|_g_|
|_d_(_π_)|0.60|-0.16|0.67|0.21|0.02|0.01|0.00|-0.23|0.02|0.06|-0.03|
|_d_(_y_$ _t_ (1))|-0.05|0.14|0.04|-0.30|-0.14|0.00|-0.01|0.05|-0.04|-0.03|-0.08|
|_d_(_yspr_$ _t_ )|0.15|-0.02|0.70|0.35|0.06|0.00|0.01|-0.03|0.00|0.02|0.01|
|_d_(∆_z_)|0.10|-1.16|-4.06|0.96|-0.43|-0.10|-0.07|0.02|0.15|-0.02|-0.10|
|_d_(∆_d_)|1.46|1.26|9.76|0.62|1.54|0.30|0.03|0.16|0.91|0.73|-0.28|
|_d_(_d_)|0.37|0.53|2.95|-0.10|-0.48|0.11|0.00|0.18|0.26|0.20|-0.14|
|_d_(_pd_)|4.74|-0.72|-1.28|3.08|0.17|0.10|0.32|-0.29|-0.25|-0.46|0.37|
|_d_(∆_τ_)|1.97|-2.20|0.99|0.59|-0.49|0.01|-0.10|0.34|1.01|-0.13|-0.28|
|_d_(_τ_)|0.77|-0.78|0.80|0.14|-0.15|0.02|-0.04|-0.73|0.46|-0.05|-0.11|
|_d_(∆_g_)|-2.48|1.80|2.41|0.42|1.40|0.01|0.13|-0.61|0.48|0.81|1.13|
|_d_(_g_)|-1.01|0.50|0.16|0.11|0.41|-0.02|0.04|-0.26|0.14|-0.65|0.47|



_σ_ **x** _×_ 100 

||||||_σ_**x**_×_|100||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
||_dZ_1|_dZ_2|_dZ_3|_dZ_4|_dZ_5|_dZ_6|_dZ_7|_dZ_8|_dZ_9|_dZ_10|_dZ_11|
|_d_(_π_)|1.31|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|_d_(_y_$ _t_ (1))|0.21|1.29|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|_d_(_yspr_$ _t_ )|0.10|-0.30|0.52|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|_d_(∆_z_)|0.43|1.27|0.07|3.43|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|_d_(∆_d_)|-2.23|-1.56|1.35|-2.11|8.32|0.00|0.00|0.00|0.00|0.00|0.00|
|_d_(_d_)|-1.15|-1.01|0.04|-1.88|4.38|0.00|0.00|0.00|0.00|0.00|0.00|
|_d_(_pd_)|0.09|1.68|-1.30|-2.49|-3.93|0.00|15.61|0.00|0.00|0.00|0.00|
|_d_(∆_τ_)|0.63|0.26|1.03|4.02|1.95|0.00|0.12|4.32|0.00|0.00|0.00|
|_d_(_τ_)|-0.36|0.16|1.05|1.99|2.16|0.00|0.67|2.84|0.00|0.00|0.00|
|_d_(∆_g_)|-1.46|-2.69|-1.30|-5.71|0.12|0.00|0.89|-0.03|0.00|7.61|0.00|
|_d_(_g_)|0.10|-1.71|-1.60|-3.06|-1.14|0.00|-0.30|-1.02|0.00|4.63|0.00|



The covariance matrix of **u** _t_ +1 is given by 

**==> picture [114 x 30] intentionally omitted <==**

where **A** ( _s_ ) _≡_ exp ( _−_ Φ(1 _− s_ )) _σ_ **x** . This integral can be calculated in closed form: 

**==> picture [352 x 23] intentionally omitted <==**

where _vec_ is the vectorization operation and _⊗_ denotes the Kronecker product. 

Given the closed-form expressions for Ψ and **B** as a function of Φ and _σ_ **x** , we numerically search for the continuous-time parameters to match their discrete-time estimated counterparts. The estimates for Φ and _σ_ **x** are shown in Table 4. 

73 

## **Step 2: Estimation of the SPD.** 

The second step consists of estimating the parameters ( _r_ 0 _,_ **r** 1 _,_ _**η**_ 0 _,_ _**η**_ 1) governing the evolution of the SPD _Mt_ . To accomplish that, we consider a continuous-time noarbitrage model with an affine term structure of interest rates where yields (and consequently spreads) are linear functions of **x** _t_ . Similarly, market prices of risk are also assumed to be linear on **x** _t_ . We first derive the theoretical expressions for the yields and expected stock returns and then estimate ( _r_ 0 _,_ **r** 1 _,_ _**η**_ 0 _,_ _**η**_ 1) by minimizing the squared error between the model’s implied values and their empirical counterparts. 

Our model assumes that the real risk-free rate is given by _r_ ( **x** _t_ ) = _r_ 0 + **r** _[⊤]_ 1 **[x]** _[t]_[,][where] _r_ 0 _∈_ R and **r** 1 _∈_ R _[N][×]_[1] , and market prices of risk are given by _**η**_ ( **x** _t_ ) = _**η**_ 0 + _**η**[⊤]_ 1 **[x]** _[t]_[,] where _**η**_ 0 _∈_ R _[N][×]_[1] corresponds to the unconditional mean of _**η**_ ( **x** _t_ ) and _**η**_ 1 _∈_ R _[N][×][N]_ is the matrix of loadings on the state variable. 

Given the risk-free rate _r_ ( **x** _t_ ) and market prices of risk _**η**_ ( **x** _t_ ), the real SPD _Mt_ satisfies: 

**==> picture [295 x 28] intentionally omitted <==**

The nominal SPD is given by _Mt_[$][=] _[M]_ Π _t[t]_ , where the price level Π _t_ satisfies the diffusion process: 

**==> picture [125 x 28] intentionally omitted <==**

where the expected inflation rate at time _t_ is _π_ ( **x** _t_ ) = _π_ 0 + _**π**[⊤]_ 1 **[x]** _[t]_[.][An][application][of] Ito’s lemma yields the following evolution for the nominal SPD: 

**==> picture [159 x 32] intentionally omitted <==**

where _i_ ( **x** _t_ ) _≡ i_ 0 + _**i**[⊤]_ 1 **[x]** _[t]_[denotes][the][instantaneous][nominal][interest][rate,][with] _[i]_[0][=] _r_ 0 + _π_ 0 _− σ_ Π _[⊤]_[(] _[σ]_[Π][ +] _**[ η]**_ 0[)][,] _**[i]**_[1][=] _**[ r]**_[1][ +] _**[ π]**_[1] _[ −][σ]_ Π _[⊤]_ _**[η]**_ 1[.][The][nominal][market][prices][of][risk][are] _**η**_[$] ( **x** _t_ ) _≡_ _**η**_ ( **x** _t_ ) + _σ_ Π = _**η**_[$] 0[+] _**[ η]**[⊤]_ 1 **[x]** _[t]_[,][where] _**[η]**_[$] 0[=] _**[ η]**_ 0[+] _[ σ]_[Π][.] 

74 

**Affine bond pricing.** Let _P_ ( _h,_ **x** _t_ ) denote the price of a real zero-coupon bond maturing _h_ periods ahead, and _P_[$] ( _h,_ **x** _t_ ) the price of a nominal zero-coupon bond with the same maturity. Let _y_ ( _h,_ **x** _t_ ) = _−h_[1][log] _[ P]_[(] _[h,]_ **[ x]** _[t]_[)][denote][the][yield][on][the][real] bond and _y_[$] ( _h,_ **x** _t_ ) = _−h_[1][log] _[ P]_[ $][(] _[h,]_ **[ x]** _[t]_[)][denote][the][yield][on][the][nominal][bond.][Given] the interest rate and market price of risk are affine functions of a state variable, **x** _t_ follows an affine diffusion under the risk-neutral measure, which yields an affine term structure model (see e.g. Piazzesi 2010). The next proposition characterizes the yields and risk premia as affine functions of the state variable **x** _t_ . 

**Proposition 2** (Bond pricing) **.** _Suppose the vector of state variables follows the dynamics given in Eq._ (27) _and the SPD the dynamics in Eq._ (39) _. Then,_ 

_1. The yield and the risk premium on a real zero-coupon bond with maturity h are given by_ 

**==> picture [315 x 27] intentionally omitted <==**

_where_ 

**==> picture [331 x 61] intentionally omitted <==**

_2. The yield and the risk premium on a nominal zero-coupon bond with maturity h are given by_ 

**==> picture [339 x 28] intentionally omitted <==**

_and ζ_[$] ( _h_ ) _and_ **Υ**[$] ( _h_ ) _follow analogous expressions to ζ_ ( _h_ ) _and_ **Υ** ( _h_ ) _, with i_ 0 _and_ _**i**_ 1 _in the place of r_ 0 _and_ _**r**_ 1 _, respectively, and_ _**η**_[$] 0 _[in][the][place][of]_ _**[η]**_ 0 _[.]_ 

75 

_Proof._ By no arbitrage, the price of a real bond is given by 

**==> picture [118 x 29] intentionally omitted <==**

where the price function _P_ ( _h,_ **x** ) satisfies the PDE: 

**==> picture [367 x 35] intentionally omitted <==**

with the boundary condition _P_ (0 _,_ **x** ) = 1, and _σ_ **x** _,k_ representing the _k_ -th column of _σ_ **x** . We guess and verify that the solution to Eq.(40) is exponentially affine: 

**==> picture [158 x 15] intentionally omitted <==**

with the boundary conditions _ζ_ (0) = 0 and **Υ** (0) = **0** . In this case, the partial derivatives are: 

**==> picture [319 x 25] intentionally omitted <==**

Plugging the partial derivatives into Eq.(40), we obtain 

**==> picture [432 x 33] intentionally omitted <==**

Using the method of undetermined coefficients, it follows that **Υ** ( _h_ ) and _ζ_ ( _h_ ) satisfy the following system of differential equations: 

**==> picture [414 x 51] intentionally omitted <==**

76 

which has the solution given by 

**==> picture [330 x 61] intentionally omitted <==**

Denoting the cumulative return on the bond with maturity _h_ by _R_ ( _h,_ **x** _t_ ), it follows that the instantaneous return is given by 

**==> picture [330 x 61] intentionally omitted <==**

where _rp_ ( _h,_ **x** _t_ ) _≡_ **Υ** ( _h_ ) _[⊤] σ_ **x** _**η**_ ( **x** _t_ ) is the bond risk premium. This concludes the characterization of the equilibrium real bond price and returns. 

The computation of nominal bond price _P_[$] ( _h,_ **x** _t_ ) = E _t_ � _MMt_ $+ _t_[$] _h_ � is carried out analogously by substituting the instantaneous real interest rate _r_ ( **x** _t_ ) and the real market price of risk _**η**_ ( **x** _t_ ) for their nominal counterparts _i_ ( **x** _t_ ) and _**η**_[$] ( **x** _t_ ) in Eq.(40), and by solving the associated fundamental PDE. 

**Stock prices.** We follow Jiang et al. (2019) and assume that the state variables include information on scaled stock prices and that the stock price-dividend ratio is an affine function of **x** _t_ . 

Denote the log stock price divided by GDP by _st_ = _s_ ( **x** _t_ ) = _s_ 0 + **s** _[⊤]_ 1 **[x]** _[t]_[and][let] _[y][t]_ denote log GDP satisfying the SDE: 

**==> picture [122 x 13] intentionally omitted <==**

with expected GPD growth rate given by _µy_ ( **x** _t_ ) = _µy,_ 0 + _**µ**[⊤] y,_ 1 **[x]** _[t]_[and constant Brownian] exposures _σ_ _**y** ∈_ R[1] _[×][N]_ . An application of Ito’s lemma gives the following SDE for the 

77 

log stock price: 

**==> picture [94 x 12] intentionally omitted <==**

**==> picture [252 x 41] intentionally omitted <==**

Thus, the volatility of stock returns _σR[m]_[is][given][by] 

**==> picture [86 x 15] intentionally omitted <==**

The instantaneous expected excess return on stocks follows immediately from the no-arbitrage condition: 

**==> picture [154 x 15] intentionally omitted <==**

Since this instantaneous return is affine in the state **x** _t_ , it can be easily timeintegrated in closed form to produce the 1-year expected stock return. 

With the theoretical expressions for the time series of bond yields and expected stock returns, we minimize the error between the model-implied quantities and their empirical counterpart. In line with Jiang et al. (2019), we assume that the market price of risk for fiscal variables is equal to zero, but we allow fiscal variables to affect the dynamics of the market price of risk for the other shocks. The estimated values for the ( _r_ 0 _,_ **r** 1 _,_ _**η**_ 0 _,_ _**η**_ 1) are shown in Table 5. 

**Preference parameters.** Figure 17 shows the optimal allocation for different combinations of the risk aversion coefficient _γ_ and EIS _ψ_ . The EIS seems to have only a minor impact on the optimal allocation. Reducing the risk aversion coefficient from _γ_ = 20 to _γ_ = 5 increases the portfolio share of stocks and reduces the demand for 

78 

Table 5: Risk-free rate and market price of risk 

_r_ ( **x** _t_ ) = 0 _._ 013 + **r** _[⊤]_ 1 **[x]** _[t][,]_ _**η**_ ( **x** _t_ ) = _**η**_ 0 + _**η**[⊤]_ 1 **[x]** _[t][.]_ 

||||||**r**1||||||
|---|---|---|---|---|---|---|---|---|---|---|
|_π_|_y_$ _t_ (1)|_yspr_$ _t_|∆_z_|∆_d_|_d_|_pd_|∆_τ_|_τ_|∆_g_|_g_|
|-0.28|1.35|0.42|-0.29|0.20|0.08|0.02|0.15|0.12|0.05|-0.07|



||||||**_η_**0||||||
|---|---|---|---|---|---|---|---|---|---|---|
|_dZ_1|_dZ_2|_dZ_3|_dZ_4|_dZ_5|_dZ_6|_dZ_7|_dZ_8|_dZ_9|_dZ_10|_dZ_11|
|0.68|0.00|-1.13|3.83|0.31|0.00|0.86|0.00|0.00|0.00|0.00|



||||||**_η_**1|||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
||_dZ_1|_dZ_2|_dZ_3|_dZ_4|_dZ_5|_dZ_6|_dZ_7|_dZ_8|_dZ_9|_dZ_10|_dZ_11|
|_π_|44.71|0.00|-35.14|0.27|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|_y_$ _t_ (1)|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|_yspr_$ _t_|-21.63|-1.87|-93.97|-33.51|22.78|4.58|0.59|18.85|14.57|3.82|3.67|
|∆_z_|-26.84|-30.77|23.94|-6.02|-80.49|-20.09|-4.97|-36.60|-38.82|-10.62|7.62|
|∆_d_|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|_d_|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|_pd_|-34.40|3.07|-14.90|-21.47|0.26|-2.17|-2.62|0.53|-2.13|1.59|-0.44|
|∆_τ_|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|_τ_|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|∆_g_|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|_g_|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|



inflation-protected bonds. We still observe a substantial amount of market timing, with very low stock holdings in the early 1970s and early 2000s. 

79 

Figure 17: Optimal Allocations 

**==> picture [416 x 331] intentionally omitted <==**

**----- Start of picture text -----**<br>
100 Risk-freeStock rate 100<br>Medium Real Bond<br>Medium Nominal Bond<br>LongLong RealNominalBondBond<br>80 80<br>60 60<br>40 40<br>20 20<br>0 0<br>1950 1960 1970 1980 1990 2000 2010 2020 1950 1960 1970 1980 1990 2000 2010 2020<br>Year Year<br>(a) γ = 20, ψ = 0 . 5 (b) γ = 20, ψ = 1 . 5<br>100 100<br>80 80<br>60 60<br>40 40<br>20 20<br>0 0<br>1950 1960 1970 1980 1990 2000 2010 2020 1950 1960 1970 1980 1990 2000 2010 2020<br>Year Year<br>(c) γ = 5, ψ = 0 . 5 (d) γ = 5, ψ = 1 . 5<br>(%) (%)<br>Weights Weights<br>Portfolio Portfolio<br>(%) (%)<br>Weights Weights<br>Portfolio Portfolio<br>**----- End of picture text -----**<br>


_Notes._ This figure shows the time series of the optimal asset allocation computed using the DPI algorithm for an investor with recursive utility solving the optimization problem in Eq.(29) for different combinations of relative risk aversion _γ_ and elasticity of intertemporal substitution _ψ_ . 

80 

Figure 18: Time Series of Nominal Bond Yields 

**==> picture [432 x 346] intentionally omitted <==**

**----- Start of picture text -----**<br>
1-yr Nominal Yield 1947-01-01 / 2019-01-01 2-yr Nominal Yield 1947-01-01 / 2019-01-01 5-yr Nominal Yield 1947-01-01 / 2019-01-01<br>14 ModelData 14 14<br>12<br>12 12<br>10<br>10 10<br>8<br>8 8<br>6<br>6 6<br>4<br>4<br>4<br>2<br>2<br>2<br>0<br>0<br>1950 1960 1970 1980 1990 2000 2010 2020 1950 1960 1970 1980 1990 2000 2010 2020 1950 1960 1970 1980 1990 2000 2010 2020<br>10-yr Nominal Yield 1947-01-01 / 2019-01-01 20-yr Nominal Yield 1947-01-01 / 2019-01-01 30-yr Nominal Yield 1947-01-01 / 2019-01-01<br>14 14 14<br>12 12 12<br>10 10 10<br>8 8 8<br>6 6 6<br>4 4 4<br>2 2 2<br>1950 1960 1970 1980 1990 2000 2010 2020 1950 1960 1970 1980 1990 2000 2010 2020 1950 1960 1970 1980 1990 2000 2010 2020<br>(%)<br>Rate<br>(%)<br>Rate<br>**----- End of picture text -----**<br>


_Notes._ The figure shows the time series for the nominal yield for the model (solid black line) and the data (dashed blue line). The maturity for the nominal yields are one, two, five, ten, 20, and 30 years, respectively. 

81 

Figure 19: Time Series of Real Bond Yields 

**==> picture [432 x 346] intentionally omitted <==**

**----- Start of picture text -----**<br>
5-yr Real Yield 2000-01-01 / 2019-01-01 7-yr Real Yield 2000-01-01 / 2019-01-01 10-yr Real Yield 2000-01-01 / 2019-01-01<br>Model 3 . 0 3 . 0<br>2 . 5 Data<br>2 . 5 2 . 5<br>2 . 0<br>2 . 0<br>1 . 5 2 . 0<br>1 . 5<br>1 . 0 1 . 5<br>1 . 0<br>0 . 5 1 . 0<br>0 . 5<br>0 . 0 0 . 5<br>0 . 0<br>− 0 . 5<br>0 . 0<br>− 0 . 5<br>− 1 . 0<br>− 1 . 0 − 0 . 5<br>2000 2002 2004 2006 2008 2010 2012 2014 2016 2018 2000 2002 2004 2006 2008 2010 2012 2014 2016 2018 2000 2002 2004 2006 2008 2010 2012 2014 2016 2018<br>20-yr Real Yield 2000-01-01 / 2019-01-01 30-yr Real Yield 2000-01-01 / 2019-01-01<br>3 . 5 3 . 0<br>3 . 0<br>2 . 5<br>2 . 5<br>2 . 0<br>2 . 0<br>1 . 5<br>1 . 5<br>1 . 0 1 . 0<br>0 . 5 0 . 5<br>2000 2002 2004 2006 2008 2010 2012 2014 2016 2018 2000 2002 2004 2006 2008 2010 2012 2014 2016 2018<br>(%)<br>Rate<br>(%)<br>Rate<br>**----- End of picture text -----**<br>


_Notes._ The figure shows the time series for the real yield for the model (solid black line) and the data (dashed blue line). The maturity for the real yields are five, seven, ten, 20, and 30 years, respectively. 

82 

