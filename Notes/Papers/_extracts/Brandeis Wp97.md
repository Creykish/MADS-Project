# Brandeis Wp97

**Source:** Brandeis_WP97.pdf

---

**==> picture [540 x 172] intentionally omitted <==**

## _YOLO: Mortality Beliefs and Household Finance Puzzles_ 

_Rawley Z. Heimer, Federal Reserve Bank of Cleveland Kristian Ove R. Myrseth, University of St. Andrews Raphael S. Schoenle. Brandeis University_ 

**Workin Pa er Series g p** 

2015| 97 

## YOLO: Mortality Beliefs and Household Finance Puzzles 

Rawley Z. Heimer, Kristian Ove R. Myrseth, and Raphael S. Schoenle _[∗]_ 

## **Abstract** 

_Subjective_ mortality beliefs affect pre- and post-retirement consumption and savings decisions, as well as portfolio allocation. New survey evidence shows that individuals overestimate their mortality at short horizons and survival rate at long horizons. For example, a 28 year old male with a 99.4% chance of surviving beyond 5 years believes he will do so with 92.8% probability. A 68 year old with a 71.4% probability of living to 78, believes he has a 82.4% chance of living that long. The formation of these beliefs across age cohorts can be attributed to overweighting the most salient causes-of-death, which change over the life-cycle. This bias matters empirically: Survival expectations correlate with heterogeneity in financial education and investment behavior. Embedded in a run-of-the-mill life-cycle model, these beliefs cause the young to under-save (they have 10% less saved upon retirement) and retirees to not fully draw down their assets (they consume 12% less during retirement). In addition, for reasonable levels of risktolerance, the required excess rate of return on equity is in line with historical averages once subjective beliefs are accounted for. 

> _∗_ Heimer is at the Federal Reserve Bank of Cleveland, Myrseth is at University of St. Andrews, and Schoenle is at Brandeis University. Heimer can be contacted at: rawley.heimer@researchfed.org. The authors are grateful for the research assistance of Timothy Stehulak, and to David Love for generously providing us with his Matlab programs. They thank Stephen Cecchetti, Tony Cookson, Daniel Hamermesh, Simon Gilchrist, Zoran Ivkovich, Olivia Mitchell, John Mondragon, Jim Poterba, Klaus Schmidt and participants at Fed - Cleveland, Colorado - Boulder, Drexel, IIES, Riksbank, Cesifo Area Conference in Behavioral Economics, Cleveland Fed Household Finance Conference, the Northern Finance Association, and the Quadrant Asset Management Conference for helpful comments and suggestions. The views in this article do not necessarily reflect those of the Federal Reserve Bank of Cleveland or the Board of Governors. 

## **1 Introduction** 

Individuals often have distorted views of low probability events and few events in life happen less frequently than death. Yet visions of our own mortality can have important economic consequences. For example, sharks are responsible for an average of just one U.S. death per year (cows kill around 20 people on average), but according to a headline in the August 29, 2015 edition of the L.A. Times, “La Jolla beach closed after shark sighting.” Meanwhile, in a survey conducted by Prudential Financial, Inc., the results of which were presented in a commercial aired during Super Bowl 47, 400 people were asked to list the age of the oldest person they know. The average answer exceeded 90 years old. Clearly, this means that we are living longer and that you should contact Prudential today. 

Motivated by recent efforts to use survey elicited beliefs to understand discrepancies between classical economic models and real outcomes,[1] we measure subjective mortality beliefs and consider their consequences across multiple economic fields that are connected by a common foundation - the inter-temporal nature of household decision-making. We find that these elicited beliefs jointly bring us closer to understanding why some young people undersave towards retirement (Skinner (2007)), retirees do not fully draw down their assets (Poterba et al. (2011)), and the required equity-premium has historically been high (Mehra and Prescott (1985)). The reason we study this mechanism is that subjective lifeexpectancies have direct bearing on what is among the equations most studied by the discipline, the intertemporal trade-off between consumption today and the discounted present value of future consumption streams: 

**==> picture [204 x 19] intentionally omitted <==**

> 1These efforts have been applied to the recent housing boom (Soo (2015) and Bricker et al. (2015)), historical asset prices (Greenwood and Shleifer (2014)), or the difficulty implementing monetary policy (Coibion et al. (2015)). 

1 

The discount factor ( _β_ ) and the utility function’s curvature ( _ρ_ ) have been studied countless times. Yet, despite no indication that subjective mortality beliefs (E [ _s_ ]) are any less meaningful, they have received comparatively little attention. The dearth of research is all the more striking considering that practitioners widely use these beliefs to advertise financial products and to develop long-run financial plans. 

Using new survey evidence that builds a comprehensive picture of survival beliefs over the entire life-cycle, we find that the subjective life-expectancy (SLE) distribution is heavytailed in comparison to actuarial tables provided by the Social Security Administration (SSA).[23] That is, young individuals believe their chances of survival beyond the next few years are lower than that predicted by actuarial data (as much as 7 ppt underestimation), while respondents beyond the age of retirement believe there is a reasonable chance of surviving to extreme old age (as much as 10 ppt overestimation of surviving at least an additional ten years). These expectation errors correspond to salient, cohort-specific stereotypes of cause-of-death (Bordalo et al. (2012) and Bordalo et al. (2014)). Young people associate death with near-term rare events (e.g. plane crashes), the probability of which they overweight. As people age, these rare events take a cognitive backseat to thoughts of health and the normal course of aging. Since the average person who survives to old age has comparatively better health than cohort members to have previously died, long-term survival is perceived to be more likely than it is on average. 

These errors in subjective survival beliefs matter for key aspects of financial decisionmaking. Using off-the-shelf questions from commonly cited household surveys (e.g. the Survey of Consumer Finances), large subjective survival belief errors are associated with a greater propensity to not save or even an over-reliance on credit cards on a month-tomonth basis. Similarly, increased (decreased) expectation errors are associated with an 

> 2Manski (2004) argues for the importance of subjective expectations of significant life events, elicited from survey responses. 

> 3Jarnebrant and Myrseth (2013) finds evidence of a similar distribution. 

2 

increase (decrease) in the perceived likelihood of using one’s savings more quickly, even after accounting for the respondent’s age. These same expectation errors are associated with lower levels of financial literacy and a decreased tendency to describe oneself as having investment experience. Our findings hold even after accounting for income, demographic, and educational differences, as well as after providing some respondents with information on survival rates from actuarial tables. 

We embed these subjective beliefs into the simplest form of a dynamic life-cycle model with pre-cautionary savings, the solution to which furthers our understanding of seemingly disconnected empirical regularities. First, some argue that there is under-saving for retirement that can not fully be explained by income heterogeneity (Skinner (2007)). Our elicited subjective beliefs suggest that individuals are too pessimistic about short-term survival rates, causing them to undersave by about 10 percent relative to our benchmark model calibrated to actuarial data. Second, a distinct body of research finds that retirees do not fully draw down their assets, even after accounting for different bequest motives (Poterba et al. (2011)). Owing to retirees’ overestimation of long-term survival rates, individuals consume 12 percent less during retirement. This mechanism is independent from any income differences that may exist upon reaching retirement. 

A related challenge for models of consumption and savings decisions is for the underlying framework to jointly describe portfolio choice decisions and asset prices.[4] The introduction of our survey-based, subjective mortality beliefs enhance our understanding of the high levels of the historical equity premium (Mehra and Prescott (1985)). We use GMM to estimate the return on the risky-asset required to achieve certainty-equivalent levels of wealth-accumulation under our benchmark calibration with actuarial survival rates. The return premium has to increase by as much as a factor of three, even with reasonable levels 

> 4A few pieces of literature notice the disconnect between models of lifetime consumption and savings, and asset prices. For example, Addoum et al. (2014). 

3 

of risk tolerance, as low as two. To understand this result in this partial equilibrium setting, the required return on equity has to be sufficiently high to compensate individuals for their overestimation of the likelihood of extreme consumption declines (i.e. death). Hence, our explanation is in the spirit of the literature on rare events (Rietz (1988) and Barro (2005)). As a consequence, our findings build a bridge between two strands of literature without requiring any modifications to the basic framework. 

This paper’s primary contribution is to expand the predictive power of the canonical life-cycle framework – including the domain of asset prices – simply by feeding it new data on subjective survival beliefs. There have been a number of excellent efforts to explain empirical regularities in the literature on consumption and savings decisions. For instance, they employ precautionary savings as a mechanism (Gourinchas and Parker (2002) and Lusardi (1998)), self-control problems (O’Donoghue and Rabin (1999)), and hyperbolic discounting (Laibson (1997)). However, “there is little sharp evidence” that these preferences affect the household balance sheet (Zinman (2014)). To better understand why many retirees do not consume all of their assets, some have studied bequest motives (Bernheim et al. (1985) and Hurd (1989)), as well as their interaction with wealth inequality (Nardi and Yang (2015)) and health (Lockwood (2014)). The advantage of our approach, relative to this literature, is that our findings can reconcile what appears to be contradictory behavior at opposite ends of the life-cycle. 

Our paper also segues with research on probability weighting. It is well-documented that individuals place too much weight on low-likelihood events, a literature which began in part because of Lichtenstein et al. (1979)’s findings that people overestimate the frequency of rare causes of death. Probability weighting has been applied to seminal theories such as Cumulative Prospect Theory (Tversky and Kahneman (1992)), which in turn has been shown to have important consequences for asset prices (Barberis and Huang (2008)) and portfolio choice (Polkovnichenko (2005)). Related to these studies is a literature on tail 

4 

events and their contribution to asset prices, but only recently have scholars considered the ex ante beliefs of these rare events (Gao and Song (2015)). Perhaps the most striking market-based evidence that probability overweighting contributes to biased survival beliefs, and that these beliefs meaningfully affect economic decisions, comes from research showing that many individuals purchase too much insurance against unlikely events (Sydnor (2010) and Bhargava et al. (2015)). 

Finally, we contribute to an emergent literature on the measurement and implications of subjective expectations (Christelis et al. (2015)), with a particular interest in mortality beliefs (Hamermesh (1985)). Empirical studies confirm our findings among the retired using the Health and Retirement Survey (Bisetti (2015)), while Puri and Robinson (2007) use the Survey of Consumer Finances to provide initial evidence of the connection between life expectancy beliefs and economic decision-making. Our paper also complements a literature, which interprets evidence of subjective life expectancies through the lens of life-cycle models. Some consider survival ambiguity (Groneck et al. (2013)), while other studies are focused on respondents older than 50 or even the oldest old (Gan et al. (2005) and Wu et al. (2014)). The calibrations therefore do not fully account for the younger years of life, a crucial period for asset accumulation. Another distinguishing feature relative to this literature is that our paper considers the cognitive factors that lead to these distorted mortality beliefs. Doing – – so helps us develop a unified understanding salient cause-of-death as to why errors in subjective life-expectancies differ across survival horizons and over the life-cycle. 

This paper is organized as follows. Section 2 provides survey evidence on subjective lifeexpectancies, while Section 3 demonstrates their connection to household financial behavior. Section 4 describes our life-cycle model. Section 5 presents the solution to the model and describes its findings on consumption, savings, and investment over the life-cycle. Concluding thoughts are provided in Section 6. 

5 

## **2 Survey Evidence on Subjective Life Expectancies** 

We are not the first to ask respondents about their subjective life expectancies. This is an important feature of canonical household datasets, namely the Survey of Consumer Finances (SCF) and the Health and Retirement Survey (HRS). 

Our work differs from these surveys in several key dimensions. While the SCF only asks for the age at which respondents expect to die, guided by theory, our survey asks respondents for their survival rates on a year-by-year basis. The HRS also asks for conditional survival rates, but our survey does so for a comprehensive set of ages. We make these modifications in order to better connect to theoretical treatments of these expectations. 

## **2.1 Survey Description** 

We used an online survey to measure mortality beliefs. The survey was programmed into the Qualtrics Research Suite. We contracted Qualtrics Panels to provide us with a panel of 400 respondents, screened according to national residency and age. All respondents were required to be US residents, and they were to be evenly distributed across the following five age categories: 28, 38, 48, 58, and 68. We further requested an even gender distribution sample-wide. 

The survey asked respondents to indicate their survival likelihood, either for one-, two-, five-, or ten-year horizons from the day of taking the survey. The questions were formulated so as to be as clear as possible to respondents, and they were framed in terms of survival, rather than death, as the latter tends to engender stronger beliefs in mortality (Payne et al. (2013)). Respondents were also asked to indicate their expected longevity, in a manner not unlike that of the SCF. Following questions about expected longevity and survival likelihood, alike, respondents were asked to indicate their degree of confidence in their answers. 

6 

– – The belief elicitation was followed by questions in the order given that probed respondents’ thought processes with respect to financial preferences (SCF), financial literacy (Lusardi and Mitchell (2011)), and numeracy (Cokely et al. (2012)). The survey also collects demographics, which are described in Table 1. Respondents are roughly evenly distributed between 28, 38, 48, 58, and 68 year olds. About half are female and half are married. Higher levels of household income are underrepresented, and so are the fraction of respondents without a high school education. Further details about the survey are given in an online Appendix. 

## **2.2 Survey Results** 

There are stark differences between actuarial tables and subjective beliefs about survival. Results from the entire sample are presented in Figure 1, which plots average subjective survival beliefs by current age and survival horizon. The average respondent is 5 to 10 percentage points more pessimistic about her survival than that predicted by actuarial tables. For instance, a 28 year old with a 99.9 percent chance of survival to 29, believes he will do so with only 94.6 percent probability. These effects are persistent as the respondent ages. The effect reverses at older ages: the average 68 year old believes his likelihood of surviving to 78 is 85.8 percent, but the data predicts it is 75.3 percent. 

These findings are robust to a number of relevant data trimmings. At younger ages, males and females have similar SLEs (Figure 2). Only at age 68 do men and women have noticeably different beliefs. 68 year old men and women both underestimate their short-run survival odds, whereas women have a greater overestimation of their 5 and 10 year survival probability than men (around 5 percentage points more). 

Errors in subjective survival beliefs are unlikely to be caused by poor numerical literacy. Figure 3 presents SLEs partitioned by the respondent’s ability to answer basic questions re- 

7 

lated to probabilities.[5] Respondents still underestimate their survival rates at short horizons. However, for some ages (28, 38, and 48), the expectation error is smaller, roughly cut in half. Even numerically literate respondents overestimate their long-run survival probability when they are 68 years old. 

The most notable source of heterogeneity comes when we ask whether respondents feel confident in their beliefs about their subjective probability of survival. Figure 4 sorts subjects as being above or below the median level of confidence in their responses. Those above the median tend to have accurate responses of their short-run survival rates. On the other hand, confident respondents are the source of overestimation in long-run survival rates. 

Remarkably, respondents are unaffected by the administration of an information primer prior to taking the survey. The primer specifically provides mortality statistics and so it would be reasonable for respondents to base their beliefs on the provided data. According to Figure 5, they do not. Similarly, the survey asks some respondents to give their 1, 2, 5, and 10 year survival horizons, consecutively and on the same page. Doing so may help respondents calibrate their answers to the ranking of different survival horizons. Figure 6 provides evidence that this treatment does not have a consistent impact on SLEs. 

## **2.3 Heterogeneity of Subjective Survival Beliefs** 

To gauge the extent of these expectations errors, we calculate the following statistic: 

**==> picture [270 x 13] intentionally omitted <==**

> 5Figure 3 calls a respondent numerically literate if they can correctly answer the following question: “Imagine that we roll a fair, six-sided die 1,000 times. Out of 1,000 rolls, how many times do you think the die would come up even (2, 4, or 6)?” However, the effects are similar when other related questions on numerical literacy are used to partition the data. 

8 

where _t_ is the respondent _i_ ’s age and _l_ = _{_ 1 _,_ 2 _,_ 5 _,_ 10 _}_ . The expectations operator _E_ [ _·_ ] indicates _i_ ’s subjective beliefs about her survival to at least _t_ + _l_ , while _Pr_ [ _·_ ] are the survival rates indicated by the SSA actuarial tables. 

The survival belief errors are large, as evidenced by Figure 7, which presents a series of histograms for _exp.errori_ . The histograms are separated by the different survival horizons asked of respondents: one, two, five, and ten years. When the survival horizon is one (two) years the median error is 2 (3) years and the 25th percentile is 9 (14). As we increase the survival horizon to five (ten) years, the expectation error becomes more uniformly distributed. The median error is 6 (9) years, while the 25th percentile is 25 (19) years. 

## **2.4 How do Mortality Beliefs Form?** 

Why do many people have beliefs about their own mortality that differ from statistical life-expectancies, even respondents who are provided data about projected longevity? We propose a simple framework for understanding these cognitive errors. Using an availability heuristic, individuals have stereotypes about the cause-of-death at different ages over the life-cycle. Young people are thought to die because of unintended injury or other unnatural causes. Unnatural causes-of-death are thought to occur more often than they do, because individuals overweight unlikely events. Meanwhile, failing health causes death among the elderly. Older respondents are optimistic about their longterm survival, because the average respondent is of comparatively better health than other members of their cohort to have perished. 

We provide evidence to support these mechanisms by asking respondents to tell us how they weight different causes-of-death when forming their survival beliefs. First, we show that rare events play an over-sized role in the belief formation process. Respondents place roughly half as much weight on unnatural causes, such as physical violence, as they do 

9 

medical conditions or the normal course of aging (Table 2). Yet unnatural causes account for roughly just a twentieth of all deaths according to statistics from the Centers for Disease Control and Prevention. Second, respondent age plays a prominent role in determining these subjective weights (Table 3). Using regression analysis, older individuals (58 and 68 year olds) place around ten points, on a scale of 0 - 100, more weight on normal mortality risk, diet, and medical conditions than do 28 year olds. They also tend to place about five less points weight on rare events such as natural disasters and freak events. These results hold even after controlling for factors such as numerical ability and education. 

## **3 Do Mortality Beliefs Affect Household Finances?** 

Before studying the aggregate implications of SLEs, we ask whether survival beliefs matter for the decision-making process. This section presents preliminary, but direct evidence that subjective life-expectancies are closely linked to personal feelings about savings, investing, planning, and risk-tolerance. 

To test how subjective life-expectancies relate to savings decisions, we employ the following multinomial logistic model:[6] 

**==> picture [340 x 13] intentionally omitted <==**

where _f_ ( _k, i_ ) is a prediction of the probability that observation _i_ has outcome _k_ . The coefficient _β_ 1 _k_ captures the effect of _exp.error_ on the likelihood of choosing _k_ .[7] The matrix 

> 6A multinomial logit model is an appropriate specification to estimate the effect of errors in subjective beliefs on various aspects of financial decision-making. The dependent variables we are interested in have more than two categorical response options. The multinomial logit models impose the constraint that the alternative responses are mutually exclusive and exhaustive. The multinomial logit flexibly allows the model to have different slope coefficients and intercepts within each outcome category, a feature that is useful for presenting our findings graphically. We find similar results using ordered logit models (when appropriate). 

> 7We Winsorize exp.error at the 5 percent level in the upper bound. 

10 

_Xi_ includes _i_ ’s age and gender, a categorical adjustment for the survival horizon, as well as an indicator if _i_ was asked to consecutively provide her subjective beliefs about the four different survival horizons. The matrix also include an indicator if _i_ correctly answers our numeracy test, which implies the results account for any differences in numerical ability. In all instances, we cluster standard errors to allow for correlated residuals across the four survival horizons. 

Figure 8 presents the estimated effect of survival belief expectation errors on savings plans. Although _expect.errori_ has a lower bound of zero, a useful way to gauge the magnitude of its impact is to note that a 15 percentage point increase is roughly equal to a one standard deviation increase. The estimates of Equation 1 suggest that increasing the expectation error from zero to 20 increases probability of using savings “any time now” from around 14 to 20 percent. The slope is positive, but less steep when respondents plan to use their savings in the medium term. On the other hand, an equivalent increase in expectation error reduces from 45 to 30 percent the probability of using savings at least ten years from now. 

The second piece of evidence that SLEs are linked to personal decisions comes from estimates of how much respondents save per month. Respondents that claim to spend all of their income or even rely on credit cards to spend more than they earn, are more likely to do so when their subjective beliefs are misaligned with the actuarial data. For instance, increasing the expectation error from zero to 20 percentage points is associated with a 4 percentage point increased likelihood of spending all income monthly (from 23 to 27 percent). An inverse relation of similar magnitude is found between increased _exp.error_ and the decreased probability of saving at least 25 percent of _i_ ’s monthly income. Figure 9 summarizes these results. 

Survival expectation errors are also associated with investing experience or acumen, as well as risk-tolerance using key survey questions borrowed from the SCF. Figure 10 presents evidence of the former. Again using a zero to 20 percentage point increase in subjective 

11 

survival expectation error as a metric, the likelihood of describing oneself as very (somewhat) inexperienced increases by 5 (4) percentage points, from 25 (24) percent likelihood to 30 (28). On the other hand, the likelihood the respondent is a somewhat (very) experienced investor falls from 38 (6) to 30 (4) percent. 

These same expectation errors exhibit a U-shaped relation to surveyed risk-tolerance. According to Figure 11 and using the same magnitude change in _exp.error_ , the probability of not taking any financial risks increases by about 10 percentage points from 15 to 25 percent. The likelihood also increases (from 5 to 10 percent) when the respondent takes substantial financial risks. On the other hand, as _exp.error_ decreases, so does the propensity to take average or above average financial risk. 

Our final test shows that increased bias in subjective mortality beliefs correlates with lower levels of financial literacy (Table 4). Evidence comes from estimates of the following regression estimated using OLS: 

_fin.liti_ = _β_ 0 + _β_ 1 _· exp.errori_ + _β · Xi_ + _εi_ 

where _fin.liti_ is equal to one if _i_ answers two of three financial literacy questions correctly. The coefficient estimate on _exp.error_ is around equal to -0.006 after controlling for education, income, or survival horizon (all specifications), or even consecutive questions (column 2), respondent gender (column 3), and the respondent’s confidence in their beliefs (column 4). The coefficient is economically significant: A one standard deviation in _exp.error_ is associated with as much as a 10 percentage point decrease in the likelihood of being financially literate. 

12 

## **4 Modeling the Life Cycle and Subjective Beliefs** 

This section presents our modeling framework, a canonical dynamic life-cycle model. We highlight in this framework how SLEs impact the maximization problem as they enter the effective discount rate: while the first component of the effective discount rate is given by the constant rate of time preference, the second component is given by subjective transition probabilities. This connects our model directly to our empirical strategy where me measure these transition probabilities. We calibrate the model using standard parameters. The next section shows the dramatic effect that calibration to actual subjective transition probabilities has for consumption, portfolio choices and asset pricing puzzles in a canonical life-cycle model. 

## **4.1 Model Setup** 

Our framework exactly follows the model of Love (2013). As such, agents live in discrete time t, where _t_ = 0 _,_ 1 _,_ 2 _,_ 3 _, ...Tretire, ..., T_ and _Tretire_ denotes the date of retirement. Agents choose to maximize their expected discounted stream of utility by choosing current period consumption, as well as what share of income to allocate to either a risky or risk-free asset. Recursively, their problem can be written as follows: 

**==> picture [441 x 19] intentionally omitted <==**

where _Ct_ denotes consumption in period _t_ , _φt_ the share of wealth allocated to the risky asset, _Pt_ permanent income, _Xt_ cash on hand, _Bt_ ( _Xt_ ) a bequest motive, _β_ the rate of time preference and _st_ the subjective probability that individuals attach to transitioning to the next period conditional on having reached the current period. Cash on hand evolves as follows: 

**==> picture [137 x 13] intentionally omitted <==**

13 

where the gross rate of return on the portfolio is the weighted return of the risky and the risk free asset, that is, _Rt_ = _φtRt[r]_[+ (1] _[ −][φ][t]_[)] _[R][f][.]_ 

The process for income _Yt_ is given by permanent income _Pt−_ 1, an adjustment for the age-earnings profile _Gt_ , a shock _Nt_ following a log-normal distribution and a transitory shock Θ _t_ . This specification is due to Carroll (2011). Thus, we have that: 

**==> picture [87 x 11] intentionally omitted <==**

and permanent income transitions according to: 

**==> picture [75 x 12] intentionally omitted <==**

We parameterize the utility function by choosing _u_ ( _C_ ) = _C_[1] _[−][ρ] /_ (1 _− ρ_ ), and the bequest function by choosing _B_ ( _X_ ) = _b_ ( _X/b_ )[(1] _[−][ρ]_[)] _/_ (1 _− ρ_ ) _._ The curvature of the utility function is prescribed by _ρ_ , with this parameter often called the coefficient of relative risk aversion. We solve the problem numerically using the method of endogenous grid-points as described in Carroll (2011) and Love (2013).[8] 

We emphasize that subjective beliefs play an important role in this framework. Individual agents make their consumption and portfolio choices today using their subjective beliefs about their transitions to the next period. These beliefs multiplicatively enter the maximization problem through the effective period discount rate, that is, through _βst_ . Thus, while the first component of the effective discount rate is given by _β_ , the constant rate of time preference, the second component is exactly given by subjective transition probabilities. 

All that we are doing in this paper is to highlight that optimal decision rules are determined by subjective transition probabilities. In particular, we solve for these decision rules without having to assume any kinds of bounded rationality, such as hyperbolic discounting implemented by Laibson (1997). We thus extend the pioneering work by Hamermesh (1985), 

8 We are extremely grateful to David Love for sharing his set of codes with us. 

14 

– by showing in a standard lifecycle model how important these subjective beliefs carefully mapped out in the data – can be for perfectly rational, optimizing agents, and how they can potentially address several empirical challenges to the model. 

## **4.2 Calibration** 

We calibrate our model to two specifications: one for comparison, one to show the effect of subjective beliefs, which can be further differentiated to yield additional comparisons. Our calibration for comparison purposes implements a canonical life-cycle model. This calibration is consistent with Love (2013) and we follow his parameter choices exactly except that we do not allow for an explicit bequest motive. Our subjective belief specification is identical to the comparison specification with one important difference: we now use subjective survival probabilities from our survey instead of statisticial mortality data. 

This difference in transition probabilities reflects the most important difference to the standard calibrations in the life-cycle literature because subjective beliefs affect the effective discount factor. Our main subjective belief calibration uses the subjective transition probabilities in Figure 1: on average, individuals who are between 28 and 38 years old believe that they are approximately 50 times less likely to live to the next period than statistical mortatility data indicate. The comparison uses data from the 2007 Social Security Administration Period Life Tables. We set _β_ , the rate of time preference, which is the other component of the effective discount factor, to be 0.98 in both specifications. 

The other key parameter choices reflect typical values chosen in the life-cycle literature. While we refer the reader to Tables 1 and 2 in Love (2013) for details, we highlight our choices of several key parameter values, especially those relevant for the asset pricing aspect of our analysis. We thus set the risk-free rate to 2 percent, the excess return to 4 percent and the standard deviation of the risky asset to 18 percent. The excess return is somewhat lower 

15 

than found by Campbell and Viceira (2002), which is needed so that households do not end up at a corner solution of investing 100 percent into the risky asset. This is helped by a high risk aversion parameter of 5. Following Love (2013) and Carroll and Samwick (1997), we use 1970-2007 PSID data to calibrate the income process. While there are potentially many interesting aspects to the life cycle coming from family composition and marital status, we calibrate the income process for college graduates only who live in a married household but without additional dependents. We allow for a non-zero correlation between permanent income and excess returns during the working life, but set the correlation to zero during retirement. 

## **5 Life-cycle Model with Mortality Beliefs, Results** 

This section shows the dramatic impact that introducing subjective beliefs into a run-ofthe-mill lifecycle model can have. First, we find that young individuals overconsume and undersave relative to what is optimal in a benchmark based on statistical transition probabilities. Second, we find that retirees consume less than would be optimal. This holds true even when we abstract from wealth differences due to undersaving when young. Third, we find that subjective transition probabilities bring us closer to observed levels of the return on equity over the risk-free rate given reasonable degrees of risk aversion – while we continue to match undersaving of the young. 

First, we find that the introduction of subjective beliefs into a canonical life-cycle model has qualitatively and quantitatively large effects on consumption, savings and asset allocations of the young. Since this period is crucial for asset accumulation for retirement, we view the large effects during this period as our main result. What do we find exactly? During much of their working life, individuals substantially over-consume, relative to what our benchmark specification based on statistical probabilities implies. Between ages 28 and 

16 

58, people on average consume 25 percent more based on their subjective beliefs than what they should based on statistical transition probabilities. This is equivalent to $5000 per year. 

The intuition for this result lies of course in the lower than statistical, subjective transition probabilities: due to these beliefs, people discount the future more and prefer present-term consumption. This is what the change of the effective discount factor implies. Unlike other work in the life-cycle literature such as Laibson (1997), we do not require any behavioral assumptions to obtain our results. We show the result for consumption in the top left panel of Figure 12. 

At the same time, a result of such large over-consumption is that people have less income to save and accumulate fewer assets when they are young. Their savings rate and total accumulated assets are below those implied by our canonical comparison model between ages 28 and 58. Then, as people approach retirement, we find that their consumption stays essentially flat. In particular, this means that their savings go up starting at age 58 since the income profile we calibrate to implies rising incomes until retirement. In fact, savings leading up to retirement are slightly higher than in the canonical model. 

Second, an important finding is what happens during retirement: Strikingly, throughout retirement, people save more compared to the canonical model while they consume relatively less. Because they want to smooth consumption but cannot relie on a large asset base, this is an intuitive result. Interestingly, people have an approximately constant savings profile during retirement. They save on average $17,500 per year. These results can be seen from the top right panel and the bottom left panel of Figure 12. 

To what extent are the heavy right tails in subjective beliefs at old age responsible for higher savings during retirement? We investigate this by comparing only the choices of retirees, either under subjective or statistical transition probabilities, while giving individuals exactly the same amount of assets at age 65. That is, we simulate a truncated version of the life-cycle model. We find that subjective transition probabilities still generate a pattern of 

17 

oversaving and underconsumption during retirement, relative to a benchmark of statistical transition probabilities (Figure 13). This finding shows that not only a lower asset base at the start of retirement but again, subjective beliefs are crucial determinants of savings and consumption decisions. Our results agree with the findings of old age and subjective life expectancies in Wu et al. (2014). 

## **5.1 Robustness** 

Our results are robust to a number of alternative parametrization, as well as alternative sets of subjective transition probabilities. Figure 14 presents evidence of the latter. The most notable differences are for subjects that have confidence in their answers to the subjective lifeexpectancy questions. For these individuals, the life-cycle model predicts overconsumption when young by an even greater amount. This leads to increased under-accumulation of wealth. 

The results are insensitive to alternative discount factors (Figure 15). When _β_ is increased, overconsumption of the young increases and wealth accumulation falls, implying an interaction between the discount factor and SLEs. When the coefficient of relative risk-aversion is changed from our preferred parametrization ( _ρ_ = 5), the model produces additional overconsumption for both increases and decreases in _ρ_ (Figure 16). These differences are owing to changes in how individuals allocate their savings between the risky and risk-less asset. Lastly, we find little change in our results when we incorporate a bequest motive into the model (Figure 17). 

## **5.2 Subjective Beliefs and Asset Returns** 

Finally, our results relate to the asset pricing and finance literature, specifically the wellstudied relation between the risk aversion and the difference between the returns on a risky 

18 

and risk-less asset (Mehra and Prescott (1985)). As Siegel and Thaler (1997) summarize, an additively separable utility function with constant relative risk-aversion can be reduced to a single linear equation. The equation sets the equity premium (the return on the risky asset minus the risk-free rate) equal to the covariance between consumption and asset prices scaled by a single parameter, the coefficient of relative risk-aversion, _ρ_ . Given what the data says about returns and consumption over time, the equation implies a value of _ρ_ = 30. However, _ρ_ = 30 also suggests that one would concede 49 percent of their wealth just to avoid a coin-flip gamble that would either double or half their existing wealth. Hence, the relationship is difficult to reconcile with observed risk-tolerance and is therefore deemed a puzzle. 

There is evidence of a connection between mortality beliefs and the high levels of the equity premium. Figure 19 plots average wealth accumulation over the life-cycle for – different levels of risk-tolerance, the equity premium, and two different survival functions the actuarial data and the survey-elicited subjective belief distribution. We highlight the time-series of wealth accumulation calibrated to the actuarial survival data and with an equity premium of 4 (with the risk-free rate set equal to[1] _/β_ = 1 _._ 02, the return on equity equals 6). This time-series is the welfare-maximizing set of outcomes over the life-cycle for a perfectly calibrated individual given these parameter values. In other words, it serves as our benchmark. 

In comparison, we estimate the wealth-accumulation time-series using SLEs and vary the level of equity premium. When _ρ_ = 2, the model solution using SLEs requires an equity premium close to 8 to come close to achieving benchmark levels of wealth. When _ρ_ = 4, the required equity premium falls to around 6. For greater levels of _ρ_ , specifically 10 and 20 in Figure 19, the consumer is invariant to the different levels of equity premium, and is seemingly equally well-off under the subjective and actuarial survival functions. 

19 

... 

A more formal treatment, which uses GMM to estimate the return on equity, provides further evidence that these survival beliefs affect the required returns to holding equity. To estimate _R[r]_ , we search for the parameter value that minimizes the following objective function: 

**==> picture [224 x 35] intentionally omitted <==**

where _X_ is a vector that includes the time-series of cash-on-hand at each age, _t_ , of _i_ ’s life using the model solution with actuarial transition probabilities. The vector, _X_[�] , is cash-onhand when the individual has SLEs. We estimate _R[r]_ holding constant different values of _ρ_ and _β_ . The counterfactual exercise determines what the required excess return on equity would have had to have been to achieve equivalent levels of lifetime wealth accumulation when the individual has subjective mortality beliefs. 

Estimates of _R[r]_ show that individuals require higher levels of equity returns to compensate them for having mortality beliefs that differ from actuarial data (Figure 20). The figure presents the estimated _R[r]_ for _ρ_ ranging from 1 to 10 and _β_ from 0.9 to 1. The top left graph presents the required return on equity needed to achieve an equivalent level of wealth accumulation as an individual without mistaken survival beliefs who receives an equity premium of 0.01. The top right is for an equity premium of 0.02, bottom left has 0.03, and the bottom right has 0.04. 

The estimated equity premium increases under all of these different parameterizations when the representative agent has SLEs. The effect is often large. For instance, when we use _β_ = 0 _._ 98 and _ρ_ = 2, _R[r]_ increases from 1 percent to around 10 percent when the individual goes from making decisions using actuarial data to their own subjective beliefs. Generally, the effect of these beliefs on the required return on equity lessens as _β_ decreases away from one. The effect on the equity premium has a concave relation to _ρ_ . 

20 

An appealing way to understand this relationship is to argue not that the return on equity is too high, but that historical bond returns are too low (Weil (1989)). This argument highlights the rate of time-preference, and draws into question whether observed asset (bond) returns are a reasonable reflection of the model-implied risk-free rate. Our subjective life-expectancies contribute to this line of inquiry, because they interact multiplicatively with the discount factor. Even in our more conservative estimates of SLEs, we show that with a transition probability of around 0.95, the weight put on the discounted stream of future consumption falls relative to today’s consumption. This implies that the latent risk-free rate is actually much higher than is the case when only _β_ is used to discount. This upward adjustment to the risk-free rate lessens the differential between it and historical equity returns, which would be more consistent with lower levels of _ρ_ . Another way to view this result is to note that there is room for an even greater divide between equity returns and[1] _/β_ once an adjustment has been made for subjective survival beliefs.[9] 

## **6 Conclusion** 

This paper presents new findings on subjective survival beliefs over the life-cycle. Young people tend to overestimate their mortality risk while older individuals believe they will survive longer than actuarial data expect. We embed these survival beliefs into a canonical dynamic life-cycle model with portfolio choice. Without any modifications to the standard model and using the literature’s preferred parametrization, the application of elicited survival beliefs better align the model with notable features of data aggregates. Namely, our estimates produce under-saving while young and under-consumption while old. They also 

> 9Our explanation bears similarity – either mechanically or in spirit – to a few other popular theories for the high return on equity. These theories include excessive pessimism (optimism) over expansions (contractions) (Cecchetti et al. (2000)), low-probability or tail events (Rietz (1988)), and pessimism and doubt over the growth rate of consumption (Abel (2002)). Our paper is perhaps most closely aligned with the latter explanation, because it also generates a reduction in the risk-free rate. 

21 

allow the model’s solution to feature accurate levels of elicited risk-tolerance and the historical equity premium. In sum, simply incorporating more accurate data on subjective beliefs, substantially improves the performance of the standard framework in a number of seemingly unrelated yet critical dimensions. 

As a final consideration, we speculate on the origins of subjective beliefs that are poorly aligned with actuarial life-expectancies. The survey asks how respondents develop expectations of their own mortality. When developing their own survival beliefs, the average respondent places about half as much weight on unlikely occurrences such as natural disasters and animal attacks as they do on the natural course of aging and medical conditions (Table 3). If that is indeed so, it is important that we fully consider how beliefs diverge from true probability distributions, because as this paper shows, there are important consequences. 

22 

## **References** 

- Abel, A. B. (2002). An exploration of the effects of pessimism and doubt on asset returns. _Journal of Economic Dynamics and Control_ , 26(7-8):1075–1092. 

- Addoum, J. M., Delikouras, S., and Korniotis, G. (2014). License to spend: ConsumptionIncome sensitivity and portfolio choice. _working paper_ . 

- Barberis, N. and Huang, M. (2008). Stocks as lotteries: The implications of probability weighting for security prices. _American Economic Review_ , 98(5):2066–2100. 

- Barro, R. J. (2005). Rare events and the equity premium. Working Paper 11310, National Bureau of Economic Research. 

- Bernheim, B. D., Shleifer, A., and Summers, L. H. (1985). The strategic bequest motive. _Journal of Political Economy_ , 93(6):pp. 1045–1076. 

- Bhargava, S., Loewenstein, G., and Sydnor, J. (2015). Do individuals make sensible health insurance decisions? evidence from a menu with dominated options. Working Paper 21160, National Bureau of Economic Research. 

- Bisetti, E. (2015). Do the elderly save too much? _working paper_ . 

- Bordalo, P., Gennaioli, N., and Shleifer, A. (2012). Salience theory of choice under risk. _The Quarterly Journal of Economics_ , 127(3):1243–1285. 

- Bordalo, P., Gennaioli, N., and Shleifer, A. (2014). Stereotypes. Working Paper 20106, National Bureau of Economic Research. 

- Bricker, J., Krimmel, J., and Sahm, C. (2015). ’house prices can’t fall’: Do beliefs affect consumer spending and borrowing cycles? _presentation slides NBER Summer Institute_ . 

- Campbell, J. Y. and Viceira, L. M. (2002). _Strategic Asset Allocation: Portfolio Choice for Long-Term Investors_ . Number 9780198296942. Oxford University Press. 

- Carroll, C. D. (2011). Theoretical foundations of buffer stock saving. CFS Working Paper Series 2011/15, Center for Financial Studies (CFS). 

- Carroll, C. D. and Samwick, A. A. (1997). The nature of precautionary wealth. _Journal of Monetary Economics_ , 40(1):41–71. 

- Cecchetti, S. G., Lam, P., and Mark, N. C. (2000). Asset pricing with distorted beliefs: Are equity returns too good to be true? _American Economic Review_ , 90(4):787–805. 

- Christelis, D., Georgarakos, D., Jappelli, T., and van Rooij, M. (2015). Consumption uncertainty and precautionary saving. _working paper_ . 

23 

- Coibion, O., Gorodnichenko, Y., and Kumar, S. (2015). How do firms form their expectations? new survey evidence. Working Paper 21092, National Bureau of Economic Research. 

- Cokely, E. T., Galesic, M., Schulz, E., Ghazal, S., and Garcia-Retamero, R. (2012). Measuring risk literacy: The berlin numeracy test. _Judgment and Decision Making_ , 7(1):25–47. 

- Gan, L., Hurd, M. D., and McFadden, D. L. (2005). Individual Subjective Survival Curves. In _Analyses in the Economics of Aging_ , NBER Chapters, pages 377–412. National Bureau of Economic Research, Inc. 

- Gao, G. and Song, Z. (2015). Rare disaster concerns everywhere. _working paper_ . 

- Gourinchas, P.-O. and Parker, J. A. (2002). Consumption over the life cycle. _Econometrica_ , 70(1):pp. 47–89. 

- Greenwood, R. and Shleifer, A. (2014). Expectations of returns and expected returns. _Review of Financial Studies_ , 27(3):714–746. 

- Groneck, M., Ludwig, A., and Zimper, A. (2013). A Life-Cycle Model with Ambiguous Survival Beliefs. MEA discussion paper series 13270, Munich Center for the Economics of Aging (MEA) at the Max Planck Institute for Social Law and Social Policy. 

- Hamermesh, D. S. (1985). Expectations, Life Expectancy, and Economic Behavior. _The Quarterly Journal of Economics_ , 100(2):389–408. 

- Hurd, M. D. (1989). Mortality risk and bequests. _Econometrica_ , 57(4):779–813. 

- Jarnebrant, P. and Myrseth, K. O. R. (2013). Mortality beliefs distorted: Magnifying the risk of dying young. _ESMT Working Paper No 13-03_ . 

- Laibson, D. (1997). Golden Eggs and Hyperbolic Discounting. _The Quarterly Journal of Economics_ , 112(2):443–77. 

- Lichtenstein, S., Slovic, P., Fischhoff, B., Layman, M., and Combs, B. (1979). Judged frequency of lethal events. _Journal of Experimental Psychology: Human Learning and Memory_ , 4(6):551–578. 

- Lockwood, L. M. (2014). Incidental bequests: Bequest motives and the choice to self-insure late-life risks. NBER Working Papers 20745, National Bureau of Economic Research, Inc. 

- Love, D. A. (2013). Optimal Rules of Thumb for Consumption and Portfolio Choice. _Economic Journal_ , 123:932–961. 

- Lusardi, A. (1998). On the Importance of the Precautionary Saving Motive. _American Economic Review_ , 88(2):449–53. 

- Lusardi, A. and Mitchell, O. S. (2011). Financial literacy around the world: An overview. _Journal of Pension Economics and Finance_ , 10:497–508. 

24 

- Mehra, R. and Prescott, E. C. (1985). The equity premium: A puzzle. _Journal of Monetary Economics_ , 15(2):145–161. 

- Nardi, M. D. and Yang, F. (2015). Wealth Inequality, Family Background, and Estate Taxation. NBER Working Papers 21047, National Bureau of Economic Research, Inc. 

- O’Donoghue, T. and Rabin, M. (1999). Doing it now or later. _American Economic Review_ , 89(1):103–124. 

- Payne, J. W., Sagara, N., Shu, S. B., Appelt, K. C., and Johnson, E. J. (2013). Life expectation: A constructed belief? evidence of a live to or die by framing effect. _Journal of Risk and Uncertainty_ , 46(1):27–50. 

- Polkovnichenko, V. (2005). Household portfolio diversification: A case for rank-dependent preferences. _Review of Financial Studies_ , 18(4):1467–1502. 

- Poterba, J. M., Venti, S. F., and Wise, D. A. (2011). The Drawdown of Personal Retirement Assets. NBER Working Papers 16675, National Bureau of Economic Research, Inc. 

- Puri, M. and Robinson, D. T. (2007). Optimism and economic choice. _Journal of Financial Economics_ , 86(1):71–99. 

- Rietz, T. A. (1988). The equity risk premium a solution. _Journal of Monetary Economics_ , – 

- 22(1):117 131. 

- Siegel, J. J. and Thaler, R. H. (1997). Anomalies: The equity premium puzzle. _Journal of Economic Perspectives_ , 11(1):191–200. 

- Skinner, J. (2007). Are you sure you’re saving enough for retirement? _Journal of Economic Perspectives_ , 21(3):59–80. 

- Soo, C. K. (2015). Quantifying animal spirits: News media and sentiment in the housing market. _working paper_ . 

- Sydnor, J. (2010). (over)insuring modest risks. _American Economic Journal: Applied Economics_ , 2(4):177–99. 

- Tversky, A. and Kahneman, D. (1992). Advances in prospect theory: Cumulative representation of uncertainty. _Journal of Risk and Uncertainty_ , 5(4):297–323. 

- Weil, P. (1989). The equity premium puzzle and the risk-free rate puzzle. _Journal of Monetary Economics_ , 24(3):401–421. 

- Wu, S., Stevens, R., and Thorp, S. (2014). Die young or live long: Modeling subjective survival probabilities. _working paper_ . 

- Zinman, J. (2014). Consumer credit: Too much or too little (or just right)? _The Journal of_ – 

- _Legal Studies_ , 43(S2):S209 S237. 

25 

Table 1: **Survey Respondent Characteristics Description:** This table presents data on the characteristics of participants in the survey administered by Qualtrics. 

||pct.|pct.|pct.|
|---|---|---|---|
||_age_<br>28<br>17.4<br>38<br>19.3<br>48<br>21.6<br>58<br>23.0<br>68<br>18.8<br>_gender_<br>female<br>49.3<br>male<br>50.7<br>_have_<br>_children_<br>no<br>34.7<br>yes<br>65.3|_civil_<br>_status_<br>single<br>24.6<br>partner (not co-habitating)<br>0.8<br>partner (co-habiting)<br>9.5<br>married<br>52.9<br>divorced<br>8.7<br>widowed<br>3.4<br>_education_<br>primary school<br>3.1<br>high school<br>23.4<br>college, no degree<br>30.8<br>bachelor’s degree<br>31.9<br>master’s degree<br>8.8<br>doctorate<br>2.0|_gross_<br>_hh_<br>_income_<br>less than $10k<br>3.7<br>$10k - $20k<br>8.4<br>$20k - $35k<br>17.4<br>$35k - $50k<br>18.8<br>$50k - $100k<br>38.8<br>$100k - $200k<br>11.5<br>greater than $200k<br>1.4|
||||_N_ = 357|



26 

Table 2: **Risk Factors and the Formation of Mortality Beliefs Description:** This table presents data on the factors respondents use to judge their own survival probabilities. They are asked to rate each factor on a scale of 0 to 100 (the weights do not have to sum to one). 

|“When you assessed your survival likelihood, to what extent did you place weight on the|“When you assessed your survival likelihood, to what extent did you place weight on the|“When you assessed your survival likelihood, to what extent did you place weight on the|“When you assessed your survival likelihood, to what extent did you place weight on the|
|---|---|---|---|
|following risk factors?” (scale of 0 to 100)||||
|variable|mean|median|std dev|
|The natural course of life and aging (“normal risk”)|74.5|80|23.5|
|Medical conditions (e.g., cancer and heart disease)|69.4|78|26.4|
|Dietary habits (e.g. unhealthy foods)|62.3|69|28.2|
|Trafc accidents (e.g., car crash)|45.3|50|29.8|
|Physical violence (e.g., murder)|35.3|20|32.3|
|Natural disasters (e.g., earth quakes)|34.7|23|31.5|
|Animal attacks (e.g., shark attacks)|25.6|9|31.3|
|Risky lifestyle (e.g., base jumping)|28.3|10|33.3|
|“Freak events” (e.g., choking on your food)|32.7|23|30.8|
||||_N_ = 357|



27 

## Table 3: **What Risk Factors Matter for Subjective Beliefs?** 

**Description:** This table presents estimates of the following regression estimated using OLS: _risk.factori_ = _β_ 0 + _β_ 1 _· exp.errori_ + _β · Xi_ + _εi_ . The dependent variable, _risk.factor_ , is equal to the weight respondent _i_ places on the corresponding risk factor divided by the sum of the weights _i_ places on all nine risk factors. The independent variable is _exp.errori_ = _abs_ ( _Eit_ [ _surv_ ( _t_ + _l_ )] _− Prit_ [ _surv_ ( _t_ + _l_ )]), where _t_ is the respondent _i_ ’s age and _l_ = _{_ 1 _,_ 2 _,_ 5 _,_ 10 _}_ . The ommitted category for respondent age is 28 years old. Standard errors clustered by age are in parentheses. 

|parentheses.||||||||||
|---|---|---|---|---|---|---|---|---|---|
||(1)|(2)|(3)|(4)|(5)|(6)|(7)|(8)|(9)|
|risk factor weight share|natural aging|medical|diet|trafc accident|violence|natur. disaster|animal attack|risky lifestyle|freak events|
|expectation error (Z)|-2.776|0.362|-1.065|0.227|0.870|0.495|0.540|0.483|0.863|
||(0.74)|(0.62)|(0.28)|(0.22)|(0.19)|(0.38)|(0.27)|(0.22)|(0.37)|
|age = 38|5.469|0.0634|0.818|-2.026|-1.502|-0.996|-0.725|-0.622|-0.478|
||(0.44)|(0.18)|(0.18)|(0.068)|(0.14)|(0.075)|(0.10)|(0.13)|(0.15)|
|age = 48|3.237|0.760|2.055|-1.355|-0.542|-1.009|-1.051|-1.894|-0.201|
||(0.43)|(0.32)|(0.20)|(0.13)|(0.24)|(0.086)|(0.10)|(0.21)|(0.13)|
|age = 58|3.327|3.344|2.704|-2.104|-1.495|-1.742|-1.617|-1.637|-0.781|
||(0.33)|(0.40)|(0.23)|(0.12)|(0.19)|(0.064)|(0.11)|(0.20)|(0.14)|
|age = 68|3.053|1.021|3.956|-1.539|-0.721|-1.124|-1.493|-1.489|-1.664|
||(0.62)|(0.28)|(0.22)|(0.13)|(0.23)|(0.14)|(0.15)|(0.25)|(0.17)|
|consecutive questions|x|x|x|x|x|x|x|x|x|
|education|x|x|x|x|x|x|x|x|x|
|numeracy|x|x|x|x|x|x|x|x|x|
|_N_|357|357|357|357|357|357|357|357|357|
|_R_2|0.078|0.016|0.048|0.016|0.015|0.027|0.027|0.036|0.028|



Standard errors in parentheses 

28 

## Table 4: **Mortality Beliefs and Financial Literacy** 

**Description:** This table presents results from estimating the following regression estimated using OLS: _fin.liti_ = _β_ 0 + _β_ 1 _· exp.errori_ + _β · Xi_ + _εi_ . The dependent variable, _fin.lit_ , is equal to one if the respondent answers two of three financial literacy questions correctly. These questions assess the respondent’s understanding of diversification, inflation, and compound interest, and they are described in the appendix. The independent variable is _exp.errori_ = _abs_ ( _Eit_ [ _surv_ ( _t_ + _l_ )] _− Prit_ [ _surv_ ( _t_ + _l_ )]), where _t_ is the respondent _i_ ’s age and _l_ = _{_ 1 _,_ 2 _,_ 5 _,_ 10 _}_ . The committed category for respondent age is 28 years old. Standard errors clustered by age are in parentheses. 

|rentheses.|||||
|---|---|---|---|---|
|fnancial literacy indicator|(1)|(2)|(3)|(4)|
|mortality belief exp. error|-0.00586|-0.00595|-0.00595|-0.00518|
||(0.0016)|(0.0017)|(0.0015)|(0.0016)|
|age = 38|0.0226|0.0244|0.0238|0.0227|
||(0.0084)|(0.0075)|(0.0081|(0.0084)|
|age = 48|0.187|0.191|0.180|0.186|
||(0.012)|(0.0078)|(0.013)|(0.012)|
|age = 58|0.204|0.209|0.196|0.207|
||(0.012)|(0.0081)|(0.013)|(0.012)|
|age = 68|0.249|0.256|0.228|0.251|
||(0.012)|(0.0096)|(0.039)|(0.012)|
|consecutive questions||-0.0595|||
|||(0.093)|||
|male|||0.0503||
||||(0.088)||
|confdent||||0.0519|
|||||(0.067)|
|constant|0.0631|0.656|0.613|0.597|
||(0.041)|(0.074)|(0.058)|(0.066)|
|education|x|x|x|x|
|income|x|x|x|x|
|survival horizon|x|x|x|x|
|_N_|357|357|357|357|
|_R_2|0.062|0.061|0.062|0.062|



29 

Figure 1: **Subjective Life-expectancy vs. Actuarial Data Description:** The figure compares stated survival beliefs (“subjective E(survival)”) against actuarial probabilities (“pr(survival)”) from statistical life tables provided by the social security administration. We sample respondents age 28, 38, 48, 58, and 68, and ask them the probability that they will survive beyond 1, 2, 5, and 10 years. We ask an equal number of respondents (one-fifth each) about survival beyond 1 year, 2 year, 5 year, 10 year, and all horizons jointly. 

**==> picture [469 x 342] intentionally omitted <==**

**----- Start of picture text -----**<br>
All respondents<br>30 40 50 60 70 80<br>survive at least to age<br>mean pr(transition)<br>fitted pr(transition)<br>95% CI<br>20<br>10<br>0<br>−10<br>−20<br>subjective E(survival) − pr(survival), (ppt)<br>**----- End of picture text -----**<br>


30 

Figure 2: **Gender Differences in Subjective Life-expectancy Description:** The description is the same as Figure 1, except the data is divided by gender. 

**==> picture [469 x 342] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gender differences in subjective survival probabilities?<br>30 40 50 60 70 80<br>survive at least to age<br>Male Female<br>fitted pr(transition) fitted pr(transition)<br>95% CI 95% CI<br>20<br>10<br>0<br>−10<br>−20<br>subjective E(survival) − pr(survival), (ppt)<br>**----- End of picture text -----**<br>


31 

Figure 3: **Survival Beliefs when Respondents are Numerically Literate Description:** The description is the same as Figure 1, except the data is divided by whether the respondent correctly answers questions related to their numerical ability. 

**==> picture [469 x 341] intentionally omitted <==**

**----- Start of picture text -----**<br>
Can subjects correctly answer numeracy questions?<br>30 40 50 60 70 80<br>survive at least to age<br>Yes No<br>fitted pr(transition) fitted pr(transition)<br>95% CI 95% CI<br>20<br>10<br>0<br>−10<br>−20<br>subjective E(survival) − pr(survival), (ppt)<br>**----- End of picture text -----**<br>


32 

Figure 4: **Survival Beliefs when Respondents are Confident in Their Answers Description:** The description is the same as Figure 1, except the data is divided by being above or below the median level of in one’s beliefs about their survival. 

**==> picture [469 x 341] intentionally omitted <==**

**----- Start of picture text -----**<br>
Are subjects confident in their responses?<br>30 40 50 60 70 80<br>survive at least to age<br>Yes No<br>fitted pr(transition) fitted pr(transition)<br>95% CI 95% CI<br>20<br>10<br>0<br>−10<br>−20<br>subjective E(survival) − pr(survival), (ppt)<br>**----- End of picture text -----**<br>


33 

Figure 5: **Survival Beliefs when Respondents are Given an Information Treatment Description:** The description is the same as Figure 1, except the data is divided by whether or not respondents were given an information primer that gives detail about the population survival statistics. 

**==> picture [469 x 342] intentionally omitted <==**

**----- Start of picture text -----**<br>
Did subjects receive info about survival probabilities?<br>30 40 50 60 70 80<br>survive at least to age<br>Yes No<br>fitted pr(transition) fitted pr(transition)<br>95% CI 95% CI<br>20<br>10<br>0<br>−10<br>−20<br>subjective E(survival) − pr(survival), (ppt)<br>**----- End of picture text -----**<br>


34 

## Figure 6: **Survival Beliefs when Respondents are Asked Consecutive Survival Horizons** 

**Description:** The description is the same as Figure 1, except the data is divided by whether or not respondents are asked their beliefs over the full set of horizons (1, 2, 5, and 10 years) consecutively and on the same page. All other respondents were only asked to provide their beliefs about one of the four survival horizons. 

**==> picture [469 x 342] intentionally omitted <==**

**----- Start of picture text -----**<br>
Are subjects asked about consecutive survival horizons?<br>30 40 50 60 70 80<br>survive at least to age<br>Yes No<br>fitted pr(transition) fitted pr(transition)<br>95% CI 95% CI<br>20<br>10<br>0<br>−10<br>−20<br>subjective E(survival) − pr(survival), (ppt)<br>**----- End of picture text -----**<br>


35 

## Figure 7: **Expectation Errors in Survival Beliefs** 

**Description:** The figure presents the distribution of the following statistic: 

_exp.errori_ = _abs_ ( _Eit_ [ _surv_ ( _t_ + _l_ )] _− Prit_ [ _surv_ ( _t_ + _l_ )]) 

where _t_ is the respondent _i_ ’s age and _l_ = _{_ 1 _,_ 2 _,_ 5 _,_ 10 _}_ . The expectations operator _E_ [ _·_ ] indicates _i_ ’s subjective beliefs about her survival to at least _t_ + _l_ , while _Pr_ [ _·_ ] are the survival rates indicated by the SSA actuarial tables. 

**==> picture [469 x 341] intentionally omitted <==**

**----- Start of picture text -----**<br>
Expectation errors in subjective beliefs<br>1 year horizon 2 year horizon<br>0 20 40 60 80 0 20 40 60 80<br>absolute error in survival expecations (pp) absolute error in survival expecations (pp)<br>5 year horizon 10 year horizon<br>0 20 40 60 80 0 20 40 60 80<br>absolute error in survival expecations (pp) absolute error in survival expecations (pp)<br>.25 .25<br>.2 .2<br>.15 .15<br>Density .1 Density .1<br>.05 .05<br>0 0<br>.25 .25<br>.2 .2<br>.15 .15<br>Density .1 Density .1<br>.05 .05<br>0 0<br>**----- End of picture text -----**<br>


36 

## Figure 8: **Mortality Beliefs and Savings Plans** 

**Description:** The figure presents the predictions from the following multinomial logistic model: 

**==> picture [181 x 12] intentionally omitted <==**

where _f_ ( _k, i_ ) is a prediction of the probability that observation _i_ has outcome _k_ . The dependent variable is the survey question: “When do you expect to use most of the money you are now accumulating in your investments or savings?” The set of possible answers are: 1) “At any time now...so a high level of liquidity is important”, 2) “Probably in the future...2-5 years from now”, 3) “In 6-10 years”, and 4) “Probably at least 10 years from now.” The coefficient _β_ 1 _k_ captures the effect of _exp.error_ on the the likelihood of choosing _k_ . The matrix _Xi_ includes _i_ ’s age and gender, a categorical adjustment for the survival horizon, as well as an indicator if _i_ was asked to consecutively provide her subjective beliefs about the four different survival horizons. The matrix also include an indicator if _i_ correctly answers our numeracy test, which implies the results account for any differences in numerical ability. In all instances, we cluster standard errors to allow for correlated residuals across the four survival horizons. 

**==> picture [469 x 341] intentionally omitted <==**

**----- Start of picture text -----**<br>
When do you expect to use your savings?<br>Pr(use savings any time now) Pr(use savings in 2 − 5 years)<br>0 10 20 0 10 20<br>absolute error in survival expectations (pp) absolute error in survival expectations (pp)<br>Pr(use savings in 6 − 10 years) Pr(use savings > 10 years from now)<br>0 10 20 0 10 20<br>absolute error in survival expectations (pp) absolute error in survival expectations (pp)<br>.4<br>.2<br>.18 .35<br>.16 .3<br>.14 .25<br>.12 .2<br>.5<br>.18<br>.45<br>.17<br>.16 .4<br>.15 .35<br>.14 .3<br>.13 .25<br>**----- End of picture text -----**<br>


37 

## Figure 9: **Mortality Beliefs and Rule-of-thumb Savings** 

**Description:** The description of this figure is the same as Figure 8. Except, the dependent variable is the survey question: “How much of your monthly income do you save? (choose the closest answer from the following)”, with the following set of possible responses: 1) “I spend more money than I earn. I often use credit cards or other loans to supplement my monthly income”, 2) “I save around 25% of my monthly income”, 3) “I save around 10% of my monthly income”, 4) “I spend all of my income each month”, or 5) “I save at least 50% of my monthly income.” 

**==> picture [469 x 341] intentionally omitted <==**

**----- Start of picture text -----**<br>
How much of your monthly income do you save?<br>Pr(spend more than earn, rely on credit) Pr(spend all of my income) Pr(save ~10% of monthly income)<br>0 10 20 0 10 20 0 10 20<br>absolute error in survival expectations (pp) absolute error in survival expectations (pp) absolute error in survival expectations (pp)<br>Pr(save ~25% of monthly income) Pr(save at least 50%)<br>0 10 20 0 10 20<br>absolute error in survival expectations (pp) absolute error in survival expectations (pp)<br>.08 .3 .48<br>.46<br>.06<br>.44<br>.25<br>.42<br>.04<br>.4<br>.2<br>.02 .38<br>.12<br>.24<br>.1<br>.22<br>.2 .08<br>.18 .06<br>.16 .04<br>.14 .02<br>**----- End of picture text -----**<br>


38 

Figure 10: **Mortality Beliefs and Experience Investing Description:** The description of this figure is the same as Figure 8. Except, the dependent variable is the survey question: “When it comes to investing in stocks, bonds, mutual funds, or real estate, I would describe myself as”, with the following set of possible responses: 1) “Very inexperienced”, 2) “Somewhat inexperienced”, 3) “Experienced”, 4) “Somewhat experienced”, or 5) “Very experienced.” 

**==> picture [432 x 17] intentionally omitted <==**

**----- Start of picture text -----**<br>
When it comes to investing, how do you describe yourself?<br>**----- End of picture text -----**<br>


**==> picture [469 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
Pr(very inexperienced) Pr(somewhat inexperienced) Pr(experienced)<br>0 10 20 0 10 20 0 10 20<br>absolute error in survival expectations (pp) absolute error in survival expectations (pp) absolute error in survival expectations (pp)<br>Pr(somewhat experienced) Pr(very experienced)<br>0 10 20 0 10 20<br>absolute error in survival expectations (pp) absolute error in survival expectations (pp)<br>.35 .3<br>.1<br>.28<br>.3 .09<br>.26<br>.08<br>.24<br>.25<br>.07<br>.22<br>.2 .2 .06<br>.45<br>.07<br>.4 .06<br>.35 .05<br>.3 .04<br>.25 .03<br>**----- End of picture text -----**<br>


39 

## Figure 11: **Mortality Beliefs and Risk-tolerance** 

**Description:** The description of this figure is the same as Figure 8. Except, the dependent variable is the survey question: “Which of the following statements on this page comes closest to the amount of financial risk that you are willing to take when you save to make investments?”, with the following set of possible responses: 1) “Take substantial financial risk expecting to earn substantial returns”, 2) “Take above average financial risks expecting to earn above average returns”, 3) “Take average financial risks expecting to earn average returns”, or 4) “Not willing to take any financial risks.” 

**==> picture [469 x 341] intentionally omitted <==**

**----- Start of picture text -----**<br>
What amount of financial risk are you willing to take?<br>Pr(not willing to take any financial risks) Pr(take average fiancial risk)<br>0 10 20 0 10 20<br>absolute error in survival expectations (pp) absolute error in survival expectations (pp)<br>Pr(take above average financial risk) Pr(take substantial financial risk)<br>0 10 20 0 10 20<br>absolute error in survival expectations (pp) absolute error in survival expectations (pp)<br>.55<br>.25<br>.5<br>.2<br>.45<br>.15<br>.4<br>.1 .35<br>.3<br>.1<br>.28 .08<br>.06<br>.26<br>.04<br>.24<br>.02<br>**----- End of picture text -----**<br>


40 

Figure 12: **Life-Cycle Results: Subjective vs. Actual Life-Expectancies Description:** This figure presents the solution to the life-cycle outlined in Section 4. The line “SSA” takes the survival rates from the Social Security Administration. The dotted line, “Subj. Pr(Surv)”, are model estimates using survey elicited subjective survival beliefs. 

**==> picture [469 x 290] intentionally omitted <==**

**----- Start of picture text -----**<br>
× 10 [4] Consumption × 10 [4] Savings<br>6 6<br>SSA<br>5 Subj Pr(Surv) 5<br>4<br>4<br>3<br>3<br>2<br>2 1 SSA<br>Subj Pr(Surv)<br>1 0<br>20 40 60 80 100 20 40 60 80 100<br>Age Age<br>× 10 [5] Cash on hand Share of risky assets<br>5 1<br>SSA<br>0.9<br>4 Subj Pr(Surv)<br>0.8<br>3 0.7<br>2 0.6<br>0.5<br>1 SSA<br>0.4<br>Subj Pr(Surv)<br>0 0.3<br>20 40 60 80 100 20 40 60 80 100<br>Age Age<br>$ $<br>$<br>Portfolio weight<br>**----- End of picture text -----**<br>


41 

## Figure 13: **Savings and Consumption into Retirement** 

**Description:** This figure presents the solution to the life-cycle outlined in Section 4. The model is solved using survey-elicited subjective survival beliefs. We allow the representative consumer to arrive at retirement (age 65) with $525,000 accumulate wealth, which is roughly the median household in 2008, excluding housing equity and including Social Security income. We also allow consumers to plan as though they will live until 120. 

**==> picture [468 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
4.2 × 10 [4] Consumption, Beq = 0 3.5 × 10 [4] Savings, Beq = 0 6 × 10 [5] Cash on hand, Beq = 0<br>SSA<br>4 3 Subj Pr(Surv) 5<br>3.8 2.5 4<br>3.6 2 3<br>3.4 SSA 1.5 2 SSA<br>Subj Pr(Surv) Subj Pr(Surv)<br>3.2 1 1<br>65 70 75 80 85 90 95 65 70 75 80 85 90 95 65 70 75 80 85 90 95<br>Age Age Age<br>4.2 × 10 [4] Consumption, Beq = 1 3.5 × 10 [4] Savings, Beq = 1 5.5 × 10 [5] Cash on hand, Beq = 1<br>4 3 SSASubj Pr(Surv) 5<br>4.5<br>3.8 2.5 4<br>3.5<br>3.6 2 3<br>2.5<br>3.4 SSASubj Pr(Surv) 1.5 2 SSASubj Pr(Surv)<br>3.2 1 1.5<br>65 70 75 80 85 90 95 65 70 75 80 85 90 95 65 70 75 80 85 90 95<br>Age Age Age<br>$ $ $<br>$ $ $<br>**----- End of picture text -----**<br>


42 

Figure 14: **Robustness to Different Subjective Beliefs Description:** This figure presents the solution to the life-cycle outlined in Section 4. The model is solved using different sets of survey-elicited subjective survival beliefs, as described in Section 14. 

**==> picture [468 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
6 × 10 [4] Consumption 6 × 10 [4] Savings<br>Subj Pr(Surv)<br>Overconfident 5<br>5 Numerical lit<br>Cons questions 4<br>4 3<br>3 2<br>1 Subj Pr(Surv)<br>2 Overconfident<br>0 Numerical lit<br>Cons questions<br>1 -1<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>5 × 10 [5] Cash on hand 1 Share of risky assets<br>Subj Pr(Surv)<br>Overconfident<br>4 Numerical lit 0.8<br>Cons questions<br>3 0.6<br>2 0.4<br>Subj Pr(Surv)<br>1 0.2 Overconfident<br>Numerical lit<br>Cons questions<br>0 0<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>$ $<br>$<br>Portfolio weight<br>**----- End of picture text -----**<br>


43 

Figure 15: **Subjective Survival Beliefs and Different Discount Factors Description:** This figure presents the solution to the life-cycle outlined in Section 4. The model is solved using survey-elicited subjective survival beliefs. 

**==> picture [468 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
4.5 × 10 [4] Consumption 6 × 10 [4] Savings<br>Beta =1<br>4 Beta =0.99Beta =0.98 5<br>Beta =0.97<br>3.5 Beta =0.9<br>4<br>3<br>3<br>2.5 Beta =1<br>Beta =0.99<br>2 2 Beta =0.98Beta =0.97<br>Beta =0.9<br>1.5 1<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>3 × 10 [5] Cash on hand 1 Share of risky assets<br>Beta =1<br>2.5 Beta =0.99 0.9<br>Beta =0.98<br>Beta =0.97<br>2 Beta =0.9 0.8<br>1.5 0.7<br>1 0.6 Beta =1<br>Beta =0.99<br>Beta =0.98<br>0.5 0.5 Beta =0.97<br>Beta =0.9<br>0 0.4<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>$ $<br>$<br>Portfolio weight<br>**----- End of picture text -----**<br>


44 

Figure 16: **Subjective Survival Beliefs and Different Levels of Risk-tolerance Description:** This figure presents the solution to the life-cycle outlined in Section 4. The model is solved using survey-elicited subjective survival beliefs. 

**==> picture [468 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
6 × 10 [4] Consumption 6 × 10 [4] Savings<br>CRRA =1<br>CRRA =3 5<br>5 CRRA =5<br>CRRA =10 4<br>4 3<br>3 2<br>1 CRRA =1<br>2 CRRA =3<br>0 CRRA =5<br>CRRA =10<br>1 -1<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>5 × 10 [5] Cash on hand 1 Share of risky assets<br>CRRA =1<br>CRRA =3<br>4 CRRA =5 0.8<br>CRRA =10<br>3 0.6<br>2 0.4<br>CRRA =1<br>1 0.2 CRRA =3<br>CRRA =5<br>CRRA =10<br>0 0<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>$ $<br>$<br>Portfolio weight<br>**----- End of picture text -----**<br>


45 

Figure 17: **Subjective Survival Beliefs and Bequests Description:** This figure presents the solution to the life-cycle outlined in Section 4. The model is solved using survey-elicited subjective survival beliefs. The model includes a bequest motive when Bequest = 1. 

**==> picture [468 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
4.5 × 10 [4] Consumption 6 × 10 [4] Savings<br>4 Bequest =0Bequest =1 5<br>3.5<br>3 4<br>2.5 3<br>2<br>2<br>1.5 Bequest =0<br>Bequest =1<br>1 1<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>3 × 10 [5] Cash on hand 1 Share of risky assets<br>Bequest =0 0.9<br>2.5 Bequest =1<br>0.8<br>2<br>0.7<br>1.5 0.6<br>0.5<br>1<br>0.4<br>0.5 0.3 Bequest =0Bequest =1<br>0 0.2<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>$ $<br>$<br>Portfolio weight<br>**----- End of picture text -----**<br>


46 

Figure 18: **Subjective Survival Beliefs and Different Levels of Education Description:** This figure presents the solution to the life-cycle outlined in Section 4. The model is solved using survey-elicited subjective survival beliefs. Education 1, 2, and 3 is no degree, highschool, and college graduate, respectively. 

**==> picture [468 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
4.5 × 10 [4] Consumption 6 × 10 [4] Savings<br>Edu =1<br>4 Edu =2 5<br>Edu =3<br>4<br>3.5<br>3<br>3<br>2<br>2.5<br>1<br>Edu =1<br>2 0 Edu =2<br>Edu =3<br>1.5 -1<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>3 × 10 [5] Cash on hand 1 Share of risky assets<br>Edu =1<br>2.5 Edu =2 0.9<br>Edu =3<br>2 0.8<br>1.5 0.7<br>1 0.6<br>Edu =1<br>0.5 0.5 Edu =2<br>Edu =3<br>0 0.4<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>$ $<br>$<br>Portfolio weight<br>**----- End of picture text -----**<br>


47 

## Figure 19: **Wealth Accumulation with Subjective Survival Beliefs and Different Levels of Equity Premium** 

**Description:** This figure presents the solution to the life-cycle model outlined in Section 4. The model is solved using actuarial probabilities from the Social Security Administration (SSA). All other lines come from model solutions using the subjective survival beliefs in the Qualtrics survey, while employing different levels of the equity premium. 

**==> picture [468 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 × 10 [5] Cash on hand, CRRA =2 5 × 10 [5] Cash on hand, CRRA =5<br>SSA SSA<br>2.5 ePrem =0.01ePrem =0.02 4 ePrem =0.01ePrem =0.02<br>ePrem =0.04 ePrem =0.04<br>2 ePrem =0.08 ePrem =0.08<br>3<br>1.5<br>2<br>1<br>0.5 1<br>0 0<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>6 × 10 [5] Cash on hand, CRRA =10 8 × 10 [5] Cash on hand, CRRA =20<br>5 SSAePrem =0.01 7 SSAePrem =0.01<br>ePrem =0.02ePrem =0.04 6 ePrem =0.02ePrem =0.04<br>4 ePrem =0.08 5 ePrem =0.08<br>3 4<br>3<br>2<br>2<br>1<br>1<br>0 0<br>20 30 40 50 60 70 80 90 100 20 30 40 50 60 70 80 90 100<br>Age Age<br>$ $<br>$ $<br>**----- End of picture text -----**<br>


48 

Figure 20: **Estimated Equity Premium with Subjective Mortality Beliefs Description:** This figure presents estimated values of the excess return on equity. Estimates come from targeting life-time wealth accumulation in a life-cycle model with actuarial survival probabilites under different discount factors, levels of risk tolerance, and baseline return on equity (from top right to bottom left, 0.01, 0.02, 0.03, and 0.04). We estimate the required return on equity to match this wealth accumulation when the average consumer has subjective life-expectancies, while holding constant the consumer’s decision rules. These results can be thought of as the required return on equity needed to compensate individuals for the bias in their beliefs. 

**==> picture [200 x 430] intentionally omitted <==**

**----- Start of picture text -----**<br>
50%<br>40%<br>30%<br>20%<br>10%<br> 0%<br>0.9<br>0.92<br>10<br>0.94 8<br>0.96 6<br>4<br>0.98<br>2<br>1 0<br>Rate of Time Preference<br>Coefficient of Relative Risk Aversion<br>10<br>9<br>8<br>7<br>6<br>5<br>4 1<br>3 0.98<br>10 0.96<br>8 6 0.94<br>4 0.92<br>2<br>0 0.9<br>Rate of Time Preference<br>Coefficient of Relative Risk Aversion<br>Equity Premium Subjective Beliefs<br>Equity Premium Subjective Beliefs<br>**----- End of picture text -----**<br>


**==> picture [199 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
16%<br>14%<br>12%<br>10%<br> 8%<br> 6%<br> 4%<br> 2%<br>10 1<br>8 0.98<br>6 0.96<br>4 0.94<br>2 0.92<br>0 0.9<br>Rate of Time Preference<br>Coefficient of Relative Risk Aversion<br>Equity Premium Subjective Beliefs<br>**----- End of picture text -----**<br>


**==> picture [198 x 149] intentionally omitted <==**

**----- Start of picture text -----**<br>
11%<br>10%<br> 9%<br> 8%<br> 7%<br>1<br> 6% 0.98<br> 5% 0.96<br>0.94<br> 4% 0.92<br>10 9 8 7 6 5 4 3 2 Rate of Time Preference1 0.9<br>Coefficient of Relative Risk Aversion<br>Equity Premium Subjective Beliefs<br>**----- End of picture text -----**<br>


49 

