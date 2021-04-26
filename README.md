# An intelligent sentiment proxy analysis system for estimating price changes in financial markets

Final Year Project

## Todo

- To Implement
  - sentiment error given limited sample size
  - Python packages install
  
- Results Evaluation
  - (pos sent vs neg sent) ratio vs returns + error
  - volume vs returns - volume indicated change, change indicates sentiment
  - correlation between magnitude of returns
  - correlation error, pvalue, etc.
  - Display all values then narrow down to statistically significant values
  - bring up receiver/sender bias - feedback loop
  - economic policy uncertainty index
  - 0 point motion
  - bachelier
  - statistical estimation
  - naive trader vs informed trader
  - demand vs supply
  - statistically significant >90%
  - diffentiate between correlation and causation, causation has to be stastically significant
  - Panel Regression?
  - Fashions
  - How many std devs in sentiment for 1 std dev in price
  - negative words are important < 2,3 %, otherwise lie, if high negative sentiment, important news
  - Define:
    - LexisNexis articles and their types
    - Gamestop - quote? ordinary company pos->neg->pos return
    - Correlation
    - Vector Autoregression
    - sentiment proxy
    - proxy
    - efficient market hypothesis
    - pearson correlation
- Discussion and Conclusion
  - Qualitative -> Quantitative -> Market Dynamics (description -> correlation -> causation/dependence)
  - What have I learnt? nlp, financial concepts, econometrics, behavioural psychology
  - created system that is more than the sum of its parts
- Background
  - research papers
- Nomenclature
- Abstract
- Ackowledgments
- Bibliography
  - Papers read
  - Paper from slides
  - Papers given by Khurshid
  - Tetlock?
- Appendix
- Declaration
- Spell Check
- Proof Read

- reference:
  - given structure
  - structure picked
  - everything
  - definitions
  - datacamp.com for ml models
  - lexisnexis.com
  - iexcloud.com
  - gamestop.com
  - where I found gamestop info

FIXME
- vector autoregression in design and implementation
- outline var steps in implementation
  lag length selection -> unit root test (stationary test) -> VAR -> causality
  - step 1 - lag selection
    The asterisks below indicate the best (that is, minimized) values
    of the respective information criteria, AIC = Akaike criterion,
    BIC = Schwarz Bayesian criterion and HQC = Hannan-Quinn criterion.
    lag = 18 picked by AIC

  - step 2 - unit root test
    stationarity test run on all vars
    stationarity test
    1 day return - p with constant = 1.778e-020, p < 0.1 -> unconditional
    pos neg ratio - p with constant = 8.259e-018, p < 0.1 -> unconditional

  - step 3 - var
    all endogenous vars
    var
    1 day return - p = 5.98e-28, p < 0.1 -> causation
    pos neg ratio - p = 0.005381, p < 0.1 -> causation

- news source improvement: e.g. the importants of non standard media, such as social media
- comparison between source types and even specific sources, e.g. newspaper vs social media, twitter vs facebook