class ModelViolations:

    def __init__(self):
        self.content = [func for func in dir(ModelViolations) if callable(getattr(ModelViolations, func))]
        self.content = [func for func in self.content if not func.startswith("__")]

    def collinearity(self):
        collinearity = "- does not influence SSE and hence the usfulness of the model\n" \
                       "- but interpretation of the rgression coefficient becomes harder\n" \
                       "- the values of t-tests are biased towards zero\n" \
                       "- providing the individual significances may be hard\n"
        solutions = "\nWhat can be done?\n" \
                    "- possible action: remove a perpetrating variable from the model or transform them into linearly independnt components\n" \
                    "- if caused by squared or interaction terms, the problem can occasionally be solved by switching to \033[1mcenterd\033[0m variables\n" \
                    "  (if it is possible), that is, using (Xk - X̄k)^2 instead of (Xk)^2"
        print(collinearity)
        print(solutions)

    def nonlinearity(self):
        print("\nConsequences of linearity -> model and estimates are incorrect")
        print("""\nThe existance of non-lineraity can be tested as follows:
        -  estimate the original model
        -  create the cvariable of the accompanying predictions ŷ (= fitted values)
        - extend the original model by including the square of the prediction (for exampl, witch coefficient γ):
                ->  Model:  E(Y) = β₀ + β₁⋅x₁ + ... + βₖ⋅xₖ+ γŷ²
        - estimate this new model
        - apply \033[1;3mt-test:\033[0m  H₀: γ = 0 (linearity)  H₁: y ≠ 0 (non-linearity)
        """)

    def heteroskedacity(self):
        print("""\n\033[1mConsequences:\033[0m
        -  a common σₑ does not exist;
        -  thre exists better unbiased estimators than the LS-estimator
        -  conclusions of statistical procedures assuming homoscedasticity (i.e., based on common σₑ) cannot be trusted
        """)
        print("""\nThe existence of heteroskedasticity can be detected as followed:
        - studying the \033[1msquared residuals \033[0m e₁², ..., eₙ²:
        - test the \033[1musefulness\033[0m of either one of the auxiliary models
                (1)  Model:  E(ε²) = γ₀ + γ₁⋅x₁ + ... + γₖ⋅xₖ
                (2)  Model:  E(ε²|x₁, x₂) = γ₀ + γ₁⋅x₁² + y₂⋅x₂² + x₁⋅x₂
        -> usefulness of model indicates the presence of heteroskedasticity
        -  possible solution:  weighted least squares estimation, that is, standardizing data so that errors become homoskedastic
        """)
        print("""\nR:
        d$residuals_squared = results$residuals^2
        summary(lm(residuals_squared ~ GROWTH_pop + Dtime, d))
        """)

    def non_normality(self):
        print("""\n\033[1mConsequences:\033[0m
        -  the LS estimators are generally not normally distributed
        -  the LS estimators are not optimal anymore
        -  the statistical conclusion thus cannot be trusted
        -  however, these problems are \033[1less serious for large sample sizes\033[0m
        """)
        print("""\nWhat can be done?
        -  a perfect remedy does not exist;
        -  occasionally it helps to use log(Y) instead of Y
        -  one can rely on the large sample results if data contain sufficiently many observations
        """)

        print("""\nChi-square goodness of fit:
        stdres <- results$residuals/summary(results)$sigma
        boundaries <- qnorm((0:6)/6)
        resid_classes <- cut(stdres, boundaries)
        table(resid_classes)
        chisq.test(table(resid_classes))
        qchisq(0.95, 1)     df = k - m - 1
        """)

        print("""\n\033[1mKolmogorov-Smirnov test:\033[0m
        """)

        print("""\n\033[1mShapiro-Wilk test:""")

    def first_order_autocorrelation(self):
        print("""Dependenca of the error terms
        -  often occurs in the case of time series data
        -  first-order autocorrelation: \033[3meₜ\033[0m and \033[3meₜ₊₁\033[0m are correlated
        """)

        print("""\n\033Durbin-Watson statistic:\033[0m
        -> estimates a linear function of the correlation in the regression residuals:
                                          
                                          ∑(eₜ - eₜ₋₁)² for t=1 to t=n
        if R₁ denotes corr(eₜ, eₜ₋₁),  D = ----------------------------  ≈  2(1 - R₁) for large n
                                             ∑eₜ² for t=1 to t=n
        
        - D can only take values in the range [0, 4];
        - if it is close to 2: indicates no first order autocorrelation
        - if it is close to 0: indicates positive first-order autocorrelation
        - if it is close to 4: indicates negative first-order autocorrelation
        """)
        print("""\n\033[1mThe use of an auxiliary AR(1) model to test the first-order auttocorelation:\033[0m
                AR{1):  εₜ = γ₀ + ρ⋅eₜ₋₁ + vₜ,   with E(vₜ) = 0
        -  H : ρ = 0  ->  there is \033[1no\033[0m first-order autocorrelation
        -  H : ρ ≠ 0  ->  there \033[1mis\033[0m first-ordr autocorrelation
        -  H : ρ > 0  ->  \033[1mpositive\033[0m first-order autocorrelation
        -  H : ρ < 0  ->  \033[1mnegative\033[0m first-order autocorrelation
    -> test = t-test""")


class ChiSquare:

    def __init__(self):
        self.content = [func for func in dir(ModelViolations) if callable(getattr(ModelViolations, func))]
        self.content = [func for func in self.content if not func.startswith("__")]


    def common_concepts(self):
        print("""\nCommon Concepts:
        -  \033[3mDistributional assumption H₀:  \033[0m possible outcomes for X or (X, Y) are divided into k classes 1, ..., k with probabilities pᵢ = P(X in class i)
        -  \033[3mData of size n under H₀\033[0m:  \033[1mexpected frequencies\033[0m e₁, ..., eₖ
           are calculated by eᵢ = npᵢ
        -  \033[3mRandom sample\033[0m:  using data on X or on (X, Y), the \033[1msample frequencies\033[0m N₁, ..., Nₖ are determined.
        -  the deviations N₁ - e₁, ..., Nₖ - eₖ enter the test statistic:
                ->  G =  ∑ ((N₁ - e₁)² / e₁) for i=1 to i=k
        -  under H₀ and for n large enough, G follows χ²-distribution, the \033[1m chi-square distribution\033[0m with v degrees of freedom
        -  number of degrees of freedom (v) differs per each test, but since ∑ ((N₁ - e₁) = 0, v is at most k-1
        """)

    def goodness_of_fit(self):
        print("""\nThe case of complete specification:
        \033[1mCentral question\033[0m: is the distribution of X equal to a certain distribution that is \033[1mcompletely specified\033[0m
        -  Testing problem:  H₀:  X does have the given distribution
                             H₁:  X does not have the given distribution
        -  Test procedure:   the possible outcomes of X are divided into k classes. For the test statistic, the sample frequencies N₁, ..., Nₖ are compared with the expected frequencies e₁, ..., eₖ \033[1m if H₀ is valid \033[0m by means of G
        -  Test statistic G has the following property:
            ->  H₀ is true and e₁ ≥ 5 for all i = 1, ..., k  => G ~ χ²ₖ₋₁
            """)
        print("""\nTest:
        (i)     H₀:  X does have the completely given distribution
                H₁:  X does not have the completely specified distribution
        (ii)    test statistic: G = ∑ ((N₁ - e₁)² / e₁) for i=1 to i=k
        (iii)   calculate \033[1;3mvalue\033[0m
        (iv)    calculate rejection region/p-value
        (v)     reject/fail to reject H₀
        
        requirement:  n so large that all e₁ ≥ 5
        """)

        print("""\n\nThe case of incomplete specification:
              -  \033[1mCentral question\033[0m: is the \033[1mtype of\033[0m the distribution of X equal to a certain prescribed \033[1m type of\033[0m distributions
              -  \033[3mSpecial case\033[0m: Is the distribution of X normal N(μ. σ²)
              -  the 'incomplete specification' test is the same as the 'complete specification' test that belongs to the \033[1mbest fitting\033[0m distribution; but \033[1mm\033[0m unknown parameters estimated -> \033[1mm\033[0m degrees of freedom lost.
              
              If testing X ~  N(μ. σ²):
              -  estimate m unknown parameters μ and/or σ²
              -  critical values can be approximated by thos of χ²ₖ₋ₘ₋₁
              -  create k intervals / classes; the k expected frequencies under H₀ become random variables E₁, ..., Eₖ since they depend on the estimators of the parameters""")

    def multinomial_experiment(self):
        print("""\nA multinomial experiment with parameters p₁, p₂, ..., pₖ is a random expriment that
        -  consists of a series of n independent and identical repetitions (called trials) of an experiment
        -  has k possible outcomes 1, 2, ..., k (called 'classes' or 'cells')
        -  has probabilities of outcomes p₁, p₂, ..., pₖ
        -  example:  survey answers about the safety and quality of the Dutch amusement parks with
                        n = 355 trials  (355 respondents)
                        k = 2 for FirstTime (2 possible outcomes) with p₁ = coming for the first time and p₂ = 1 - p₁
                        k = 8 for Education (8 possible outcomes after classification) with p₁, ..., p₈ = probabilities of different education levels
        
        -  Test:
        (i)     H₀:  X does have the \033[1min\033[0mcompletely given distribution
                H₁:  X does not have the \033[1min\033[0mcompletely specified distribution
        (ii)    test statistic: G = ∑ ((N₁ - E₁)² / E₁) for i=1 to i=k
        (iii)   a) estimate the m parameters under H₀
                b) determine the realised expected frequencies e₁, ..., eₖ under H₀
                c) calculate value
        (iv)    calculate rejection region/p-value
        (v)     reject/fail to reject H₀
        \033[1mrequirement\033[0m: n is so large that all e₁ ≥ 5
        
        Example:
            X = sample(1:6, 10000)
            chisq.test(table(X))
            qchisq(0.95, 5)
        
            d)  which cell has the largest contribution to the \033[1mval\033[0m?
                chisq.test(table(X))$observed - chisq.test(table(X))$expected
        """)

    def examples(self):
        print("""\n""")


class Instruction8:

    def __init__(self):
        self.content = [func for func in dir(ModelViolations) if callable(getattr(ModelViolations, func))]
        self.content = [func for func in self.content if not func.startswith("__")]

        print("""\n\nExercise 24.18:
        In estimation, stock returns often assumed normally distributed.
        Y = 'returns of the stock of Peugeot in 2005-2007'
        Use α = 0.05
        
        a)  Create a histogram of the returns:
        
                library('foreign')
                d <- read.spss('Xrc24-18.sav', to.data.frame = TRUE)
                hist <- hist(d$Return, freq=FALSE, breaks = 30)
                curve(dnorm(x, mean = mean(d$Return), sd=sd(d$Return)), add=TRUE col='blue')
                
        b)  Check that the returns follow the standard normal distribution of the returns assuming the classification (-∞, -1], (-1, -0.5], (-.5, 0], (0, 0.5], (0.5, 1], (1, ∞) under the standard normal density.
            ->  The data deviate from the standard normal as shown by the test pro edure
            
                r <- d$Return
                probs <- pnorm( (-1.0, -0.5, 0, 0.5, 1.0, Inf))-pnorm( (-Inf, -1.0, -0.5, 0, 0.5, 1.0))
                classaslt <- cut(r, (-Inf, -1.0, -0.5, 0, 0.5, 1.0, Inf))
                chisq.test(table( lassalt), p = probs)
            
                Chi squared test for given probabilities:
                data:  table(classalt)
                X-squared = 20.353, df = 5, p=value = 0.001073
                
                - H₀:  returns follow N(0,1) vs H₁:  returns do not follow N(0,1)
                - G =  ∑ ((N₁ - e₁)² / e₁) for k=1 to k=6
                - value g = 20.353
                - p-value = 0.001073 
                - since p < α -> Reject H₀, returns do not follow the standard normal distribution
            
        c)  Check the \033[1mnormality\033[0m of the returns assuming the classification (-∞, -1], (-1, -0.5], (-0.5, 0], (0, 0.5], (0.5, 1], (1, ∞) under the standard normal density.
            ->  Data have to be normalized First by subtracting the (unknown) mean and dividing by the standard deviation before performing the test. Note that the p-value in the computer output cannot be used now
            
                r <- (d$Return - mean(d$Return)) / sd(d$Return)
                probs <- pnorm( (-1.0, -0.5, 0, 0.5, 1.0, Inf))-pnorm( (-Inf, -1.0, -0.5, 0, 0.5, 1.0))
                classalt <- cut(r, (-Inf, -1.0, -0.5, 0, 0.5, 1.0, Inf))
                chisq.test(table(classalt), p = probs)
                
                Chi-squared test for given probabilities:
                data:  table(classalt)
                X-squared = 11.665, df = 5, p-value = 0.03967
                > qchisq(0.95, 3)       -> df = k - m - i,  k = 6,  estimating μ and σ² -> m = 2
                [1] 7.814728
                
                -  H₀:  returns follow N(μ,σ²))  vs  H₁:  returns do not follow N(μ,σ²)
                -  G =  ∑ ((N₁ - E₁)² / E₁) for k=1 to k=6
                -  value g = 11.665
                -  rejection region:  g ≥ χ²₀.₀₁,₆₋₂₋₁ = χ²₀.₀₁,₃ = 7.8147
                -  since value 11.665 > 7,8147, reject H₀, data are not normally distributed
        
        
        d)  Repeating the steps in point (c) while omitting the most extreme outlier from computation of the standard deviation:
                r <- (d$Return - mean(d$Return)) / sd(d$Return[abs(d$Return)<10℄)
            
        e)  How would you create six intervals such that they have all equal expected probability?
            ->  to create 6 intervals with equal probability, use function \033[3mqnorm()\033[0m.
                
                r <- (d$Return - mean(d$Return)) / sd(d$Return[abs(d$Return)<10])
                classalt <- cut(r, qnorm((0:6)/6))
                chisq.test(table(classalt))
        """)

        print("""\nExercise 24.16:
        
        A midterm exam on statistics was taken by students from three courses: business
        administration (BA), international business (IB) and business studies (BS). This
        midterm consisted of ten multiple-choice questions; the grades (scale 1- 10) are in
        the file Xrc24-16.sav.
        
        The aim of the present study is to find out whether the dummy variable Y = `Passes
        the midterm’ has a common distribution over the three populations. Here, ‘pass’
        means that the grade is at least 6.
        
        a)  Investigate this problem by assuming that the grades in the dataset come from
            three random samples, one from each of the three populations. Take 0.01 as
            significance level.
            
            (i)     -  H₀:  has a common distribution for BA, BS and IB  
                    -  H₁:  Y does not have a common distribution for BA, BS and iB
            This is a homogeneity problem (category 4) with 6 cells
            
            (ii)    Test statistic (Chi square test): G = ∑ ((N₁ - e₁)² / e₁) for i=1 to i=k
            (iii)   Val = 51.661    ->  d$Pass = d$Grade >= 6
                                        chisq.test(table(d$Pass, d$Education))
                                        qchisq(0.99,2)
            
            c)  Which population especially contributes to the val of part (a)?
                test_results <- chisq.test(table(d$Pass, d$Education))
                answer <- test_results$observed - test_results$expected""")

class Week10:

    def __init__(self):
        self.content = [func for func in dir(ModelViolations) if callable(getattr(ModelViolations, func))]
        self.content = [func for func in self.content if not func.startswith("__")]


    def smoothing_techniques(self):
        moving_averages = """\nMoving averages:
        moving average = (Yt1 + Yt2 + Yt3)/3
        
        ->  Smoothing a time series by the way of a moving average has the
            drawback that the MA has missing values at the start and at the end.
            Use the moving average of k prior observations or ...
        
        R:
            # Create moving average (over 5 time periods)
            x = embed(d$Investment, 5)
            mav_5 = apply(x, 1, mean)
            plot(mav_5, type="l")
            
            # or use library forecast
            library("forecast")
            plot(ma(d$Investment,5), type="l")
        """

        exponential_smoothing = """\nExponential smoothing:
        fix a constant w (the smoothing constant) with 0 < w < 1
        the exponentially smoothed series s1. s2, ..., sn with smoothing constant w is defined as follows:
            s1 = y1
            sₜ = w*yₜ + (1-w)*sₜ₋₁
        The smoothed series is initialised by the choice s1 = y1.
        The smoothed value:
            sₜ = w*yₜ + w(1-w)yₜ₋₁ + w(1-w)²yₜ₋₂
        """
        models = """\nModels with only trend:
            Model:  Yₜ = β₀ + β₁*t + β₂*t² + β₃*t³ + εₜ,    fora all t = 1, 2, ..., n\n\nModels with a trend and seasonal-dummies:
            Model 1:  Yₜ = β₀ + β₁*t + β₂*t² + β₃*t³ + Dummies for seasonal εₜ\n\nAutoregressive models:
            first-order autoregressive model:    Yₜ = β₀ + β₁*Yₜ₋₁ + εₜ
            second-order autoregressive model:    Yₜ = β₀ + β₁*Yₜ₋₁ + β₂*Yₜ₋₂ + εₜ
            pth-order autoregressive model:      ₜ   Yₜ = β₀ + β₁*Yₜ₋₁ + β₂*Yₜ₋₂ + ... + βₚ*Yₜ₋ₚ + εₜ
            """
        print(moving_averages, exponential_smoothing, models)

    def instrumental_variables(self):
        iv = """\nInstrumental variables:
        -   an instrumental variable (IV) such that cov(V, ε) = 0, while cov(V,X) ≠ 0
        -   apply \033[1mtwo-stage least-squares regression (TSLS)\033[0m:
            
            Stage 1:    regress X on V using data (x1, v1), ..., (vn, xn)
                        and create the predictions x̂₁, ..., x̂ₙ
                        
            Stage 2:    regress Y on X̂ using the data (x̂₁, y₁), ..., (x̂ₙ, yₙ)
            """

    def binary_choice(self):
        print("""\nBinary Choice model:
        Let Y be 0-1. 
        The basic assumption E(Y| x1, x2, xk) = b0 + b1*x1 + ... + bk*xk turns into
                            P(Y = 1 |x1, ..., xk) = ...
        but the right-hand side does not have to belong to the interval [0,1]
        trick:  use an increasing function F to map it
            P(Y = 1 | x1, ..., xk) = F(b0 + b1*x1 + ... + bx*xk)
            P(Y = 0 | x1, ..., xk) = 1 - F(...)
        disadvantage:   in general, the coefficient beta_i cannot be interpreted
        in terms of a unit increase of xi under a ceteris paribus
        condition
        
        Example:
            Study how the probability that a university student spent some time
            at a foreign university during his or her studies (Y = 1 if yes) differs
            across 10 European countries. Use α = 0.05.
        
            a)  Write down the basic assumption of the model.
                    the basic assumption is P(Y = 1|dAustria, ... , dUnitKing) = Λ(β0 +β1*dAustria + ... +β9*dUnitKing), 
                    or simply P (Y = 1) = Λ(β0+β1*dAustria + ... + β9*dUnitKing)
                    
            b + c)  1.  Estimate the model and report -2 ln L
                    2.  Is the model significant at a = 0.05
                    
                    To test the model usefulness at 5% signicanan e level, we estimate the model and perform the LR test (the residual deviance −2 ln L = 15418 
                    below). Computation can be done manually based on the regression output or using the anova ommand:
                    
                        > summary(glm(Y ~ dAustria + dFrance + dFinland + dGermany + dItaly + ... + dUnitKing, data=d, family=binomial(link='logit'))
                        > logit0= glm(Y ~ 1, data=d, family=binomial(link='logit'))
                        > logit = glm(Y ~ dAustria + dFran e + dFinland + dGermany + dItaly + dNorway + dSpain + dSwitzerland + dUnitKing, data=d, family=binomial(link='logit'))
                        > anova(logit0, logit, test='Chisq')
                        
                        Resid. Df Resid. Dev Df Devian e Pr(>Chi)
                     1      12854 15930
                     2      12845 15418       9 512.17 < 2.2e-16
                     
                    -  H0: β1 = β2 = ... = β9 = 0
                    -  H1 : β1 = 0 and / or ... and / or β9 6 = 0
                    -  LR = −2(ln LR − ln LC ) ∼ χ²₉
                    -  value = −(15930 − 15418) = 512.17
                    -   rejection region = χ²₀.₀₅,₁₂₈₄₅

            d)  Which variables are individually significant at 5% level?
                    Looking at the individual p-values in the above output, all dummy variables
                    except for dAustria are signicant at 5% level
            
            e)  Predict the probability that a Dutch student spends some time
                at a foreign university and his answer to the questions ‘Have
                you spent some time at a foreign university?’.
                
                > logit$fitted.values[1]
                # or #
                > exp(-0.23767) / (1+exp(-0.23767))
                
                [1] 0.4408602
                
                The probability obtained b elow indi ates that the ma jority of students do
                not have some 'foreign' experience and expected answer is thus 'No'.
                
            f)  Is it possible to use the linear regression model instead?
                
                In this special case, when all explanatory variables are dummy variables, the
                linear regression will provide the same results since E(Y |Dummy = 1) − E(Y |Dummy = 0) = P (Y = 1|Dummy = 1) − P (Y = 1|Dummy = 0)""")

    def tutorial6(self):
        print("""\nFormulate the basic assumption of a linear regression model with a first-order linear
        trend and a seasonal component; take the fourth quarter as a base level. Estimate
        this model and interpret the estimates. Investigate whether there is a problem
        regarding autocorrelation using an auxiliary AR(1) model
        
        Model 1: yₜ = β₀ + β₁*t + β₂*DQ₁ + β₃*DQ₂ + β₄*DQ₃ + εₜ     E(εₜ) = 0
            
            d$F_Quarter = factor(d$Quarter)
            d$F_Quarter = relevel(d$F_Quarter, "4")
            results = lm(Investment ~ T + F_Quarter, data=d)
            summary(results)
        """)

class Week11:

    def __init__(self):
        self.content = [func for func in dir(ModelViolations) if callable(getattr(ModelViolations, func))]
        self.content = [func for func in self.content if not func.startswith("__")]

    def endegeneity_test(self):
        wu_hausmann = """\nWu-hausman augmented regression test:
        -   As in first stage of 2SLS, regress possibly endegenoug variable X1 on instrumental variable s V and exegonous variables:
                X1 = γ0 + γ1*V + V*γ1 + V2*γ2 + ... + Xk*γk + u
            but save now the regression residuals û
        -   Next, augment the original regression model by û:
                Y = b0 + b0*X1 + ... + bk*Xk + û*a + ε
        -   Test by t-test (or F-test in case of multiple enodgenous variables)
            H0:  a = 0  (basic assumption is not violated, X1 exogenous)
            h1:  a != 0 (basic assumption is violated, X1 endogenous)
            """
        print(wu_hausmann)

    def tutorial7(self):
        print("""\n\nExercise 22.9:
        We study, for the euro area, the relationship between economic quarterly 
        growth 𝑌 and quarterly unit labor costs 𝑋 Both variables are measured as a percentage with 
        respect to one year before. It is suspected that 𝑌 tends to decrease as 𝑋 increases. To check 
        that conjecture, 𝑌 is regressed on 𝑋 on the basis of quarterly data of the European Central 
        Bank for the period 1996Q1 – 2007Q2; see Xrc22-09.sav. Since the two variables 𝑋 and 𝑌 influence 
        each other, we may not expect that 𝑐𝑜𝑣(𝜖, 𝑋) will be 0 when using the usual linear regression model 
        for the equation:       𝑌 = 𝛽0 + 𝛽1𝑋 + 𝜖
        
        Below, we will compare the results of an ordinary regression and a two-
        stage regression with instrumental variable 𝑉 = ‘unit labor costs in the
        \033[1mprevious quarter\033[0m’ for 𝑋.
        
        a)  Use ordinary linear regression to find estimates for 𝛽0 and 𝛽1. Write down the
            equation of the linear regression line and the coefficient of determination. Is 𝛽1
            significantly negative (use 𝛼 = 0.05)?
            
            > ordinary <- lm(GDPGrowth ~ UnitLabCosts, data=d)
            > summary(ordinary)
            
                𝑦 = 3.2709 − 0.8770 𝑋       𝑟^2 = 0.4995
                
                (i)     H0:  b1 ≥ 0     vs     H1:  b1 < 0
                (ii)    T = B1 / S_B1
                etc.
                
        b)  Answer the same questions in the case of two-stage regression with 𝑉 as instrumental variable for 𝑋
                
                X   =   UnitLabCost
                V   =   UnitLabCost of previous period, i.e. lag(UnitLabCost, 1)
                First stage regression:     X = 𝛽0 + 𝛽1*𝑉 + 𝑢    𝐸(𝑢, 𝑉) = 0
                Second stage regression:    𝑌 = 𝛽0 + 𝛽1*X̂ + 𝜖    𝐸(𝜖, X̂) = 0
                
                # Use AER package with ivreg command: CORRECT standard errors
                > aer_results <- ivreg(GDPGrowth ~ UnitLabCosts | Lag_UnitLabCosts, data=d_iv)
                > aer_results <- ivreg(Dependent ~ Independent | Instrumental, data=data)
                > summary(aer_results)
        
        c)  What do you think about the requirement in part (b) that 𝑐𝑜𝑣 𝜖, 𝑉 = 0? Do you think that first-order autocorrelation of the error terms may be a problem?
                the lagged version of a variable is generally a good instrumental variable since it
                might be correlated with the past economic shocks eₜ₋₁, but the past is
                uncorrelated with the present economic shocks eₜ. This can be violated if the errors
                are first-order autocorrelated since eₜ and eₜ₋₁ are correlated and thus eₜ and V
                can be correlated
        
        d)  Formally test whether the unit labor costs 𝑋 are endogeneous (use 𝛼 = 0.05).
                We save the residuals  from the first stage regression:
                > first_stage <- lm(UnitLabCosts ~ Lag_UnitLabCosts, data=d_iv)
                > d_iv$u_hat <- first_stage$residuals
                
                # Auxiliary regression for endogeneity test
                > aux_results = lm(GDPGrowth ~ UnitLabCosts + u_hat, data=d_iv)
                > summary(aux_results)
        
a)  Assumption logit model:
        𝑃(𝐷𝑆 = 1|𝐷𝐹,𝐴𝐺𝐸,𝐸𝐷𝑈,𝑊𝐴𝐺𝐸,𝐻𝑂𝑈𝑅𝑆,𝑁𝐾𝐼𝐷𝑆) = Λ(𝑤) = eʷ / 1+eʷ, with w = b0 + b1*DF + b2*AGE + ... 
        
b)  predict mode:
        >   results_logit = glm(DS ~ DF + AGE + EDU + WAGE + HOURS + NKIDS, data=d, family=binomial(link='logit'))
        
        >   table(d$DS, as.double(results_logit$fitted.values > 0.5), dnn=c("Observed","Predicted"))
            ->  Percentage correctly classified: 100 ∗ (223+28) / 300 = 83.66%

c)  Is the model useful? Test at 1% significance level.
        (i)     H0: b1 = 𝛽2 = ... = 𝛽6 = 0      vs  01:     𝛽1 ≠ 0 𝑎𝑛𝑑/𝑜𝑟 ... 𝛽6 ≠ 0
        (ii)    Test statistic: 𝐿𝑅 = −2(ln 𝐿𝑅 − ln 𝐿𝐶) ∼ 𝜒²𝑘
        
        >   results_logit = glm(DS ~ DF + AGE + EDU + WAGE + HOURS + NKIDS, data=d, family=binomial(link='logit'))
        >   logit0 = glm(DS ~ 1, data=d, family=binomial(link='logit'))
        >   anova(logit0, results_logit, test="Chisq")
        """)

class TestStats:

    def __init__(self):
        self.content = [func for func in dir(ModelViolations) if callable(getattr(ModelViolations, func))]
        self.content = [func for func in self.content if not func.startswith("__")]

    def simple_model(self):

        print("\nY = β₀ + β₁*x₁ + ... + βₖ*xₖ + ε,  with E(ε|x₁,...,xₖ) = 0 "
              "\nβ₁  =  σₓ,ᵧ / σ²ₓ")

    def interval(self):
        print("\nL = B₁ - tₐ/₂;ₙ₋₂"
              "\nU = B₁ + tₐ/₂;ₙ₋₂")

    def t_test(self):
        print("\nT = (B₁ - b)/S₈₁ ≈ N(0,1)")

    def coef_of_determination(self):
        print("\nr² = SSR/SST  =  1 - SSE/SST"
              "\nr²-adj = 1 - (SSE/(n - (k-1))) / (SST/(n-1))"
              "\n-> The adjusted r² is importance only for the building of the model.")

    def f_test(self):
        print("""\nUsefulness of model:
        model is useless    ->      H0: β₁ = ... = βₖ = 0
        model is useful     ->      H1: atleast one of β₁,...,βₖ != 0
        
                 (SST-SSE)/k           SSR/k
        F   =   -------------   =   ------------  
                SSE/(n - (k-1))     SSE/(n-(k-1))
        """)

    def anova(self):
        print("\nComplete model: E(Y) = β₀ + β₁*x₁ + ... + β₉*x₉ + β₉₊₁*x₉₊₁ + ... + βₖ*xₖ"
              "\nReduced model:  E(Y) = β₀ + β₁*x₁ + ... + β₉*x₉"
              "\nH0:  x₉₊₁, ..., xₖ are jointly useless     <=>      β₉₊₁ = ... = βₖ"
              "\nH1:  x₉₊₁, ..., xₖ are jointly usful       <=>     at least one of β₉₊₁,...,βₖ != 0")
        print("""
                (SSEᶜ- SSEᵣ)/(k-g)
        F   =   ---------------
                SSEᶜ/(n-(k+1))
        """)

    def logit(self):
        print("""\nBinary Choice model:
        Let Y be 0-1. 
        The basic assumption E(Y| x1, x2, xk) = b0 + b1*x1 + ... + bk*xk turns into
                            P(Y = 1 |x1, ..., xk) = ...
        but the right-hand side does not have to belong to the interval [0,1]
        trick:  use an increasing function F to map it
            P(Y = 1 | x1, ..., xk) = F(b0 + b1*x1 + ... + bx*xk)
            P(Y = 0 | x1, ..., xk) = 1 - F(...)
        disadvantage:   in general, the coefficient beta_i cannot be interpreted
        in terms of a unit increase of xi under a ceteris paribus
        condition
                
        Is the model useful? Test at 5% significance level.
        (i)     H0: b1 = 𝛽2 = ... = 𝛽6 = 0      vs  01:     𝛽1 ≠ 0 𝑎𝑛𝑑/𝑜𝑟 ... 𝛽6 ≠ 0
        (ii)    Test statistic: 𝐿𝑅 = −2(ln 𝐿𝑅 − ln 𝐿𝐶) ∼ 𝜒²𝑘
        
        >   results_logit = glm(DS ~ DF + AGE + EDU + WAGE + HOURS + NKIDS, data=d, family=binomial(link='logit'))
        >   logit0 = glm(DS ~ 1, data=d, family=binomial(link='logit'))
        >   anova(logit0, results_logit, test='Chisq')""")

    def instrumental_variables(self):
        iv = """\nInstrumental variables:
           -   an instrumental variable (IV) such that cov(V, ε) = 0, while cov(V,X) ≠ 0
           -   apply \033[1mtwo-stage least-squares regression (TSLS)\033[0m:

               Stage 1:    regress X on V using data (x1, v1), ..., (vn, xn)
                           and create the predictions x̂₁, ..., x̂ₙ

               Stage 2:    regress Y on X̂ using the data (x̂₁, y₁), ..., (x̂ₙ, yₙ)
               """
        print(iv)


    def exam(self):
        print("""\nPredict new value:
        xp = data.frame(oil = 122.20, duty = 0.6545)
        predict(ls2,xp,interval="confidence",level=0.90)\n\nPlots:
        # RESIDUALS vs PREDICTED VALUES:
        plot(predict(ls2), residuals(ls2))
        abline(0,0)\n\nAR(1) Model:
        d_ar <- data.frame( embed( d$oil, 2) )
        ls4 <- lm(X1~ X2, d_ar)
        summary(ls4)
        
        # 90% CONFIDENCE INTERVAL FOR THE AUTOREGRESSIVE PARAMETER:
        confint(ls4, "X2", 0.90)\n\nEndegeneity problem:
        
        # 5) REGRESSION MODEL WITH: rent ~ part_pub, pctlihtc, pctprj, pctrehab, pctvch 
        # DESCRIBE the ENDOGENEITY PROBLEM
        # Family Income (for example) --- OMITTED VARIABLE BIAS
        
        # EXTRA must satisfy 2 CONDITIONS: 
        # 1- RELEVANCET for (part_pub) and
        # 2- EXOGENOUS for (RENT)
        
        # FIRST STAGE ESTIMATION PROCEDURE: instruments + 4 exogenous (control variables)
        First_S <- lm(part_pub ~ extra + pctlihtc + pctprj + pctrehab + pctvch, d)
        summary(First_S)
        # Pvalue(t)= 0.0017 -- THE VARIABLE AND THE OVERALL MODEL IS USEFUL ---
        # RELEVANCE IS MET 
        
        # predicted value for the SECOND STAGE REGRESSION MODEL:
        d$part_pubhat = predict(First_S, d)
        
        ############################################################
        # 6) MANUAL SECOND STAGE:
        
        Second_S <- lm(rent ~ part_pubhat + pctlihtc + pctprj + pctrehab + pctvch, d)
        summary(Second_S)
        # POSITIVE SIGN IS EXPECTED --- argument
        # seems highly significant (even if with wrong SE() )
        # We are using WRONG SE, so ALL the inferential RESULTS ARE biased.
        
        ############################################################
        # 7) EXTEND THE MODEL OF THE FIRST STAGE REGRESSIONE BY USING 5 MORE INSTRUMENTS:
        # the variable BOYS + 4 dummies based on HDEDUC
        
        d$hdeduc = as.factor(d$hdeduc)
        d$hdeduc = relevel(d$hdeduc, ref="4") 
        
        # FIRST STAGE 2.0:
        First_S2 <- lm(part_pub ~ extra + boys + hdeduc +
                    pctlihtc + pctprj + pctrehab + pctvch, d)
        summary(First_S2)
        
        # TO TEST THE USEFULNESS OF THE EXTENDED MODEL wrt the First_S, we must compute 
        # a Partial F-test between the 2 first stages:
        anova(First_S,First_S2)
        # F-value = 16.86
        # pvalue = 0.0000
        # REJECT THE NULL IN FAVOUR OF THE ALTERNATIVE: THE SECOND MODEL IS USEFUL AND 
        # THESE OTHER 2 INSTRUMENTS ARE RELEVANT VARIABLES AND CAN BE USED IN THE 2SLS.
        
        # IS BOYS USEFUL?
        summary(First_S2)
        # The variable boys is statistically NOT SIGNIFICANT, SO IT MIGHT NOT BE RELEVANT
        # to explain part_pub, especially because we already have EXTRA. DESPITE THIS,
        # the previous F-test of joint significance told us that it might be an important
        # determinant, so we might would like to keep it.
        
        ############################################################
        # 8) TEST FOR INDEPENDECE OF 2 VARIABLES: boys and hdeduc
        
        # Observed frequencies: N_i
            table(d$boys, d$hdeduc)
        
        ?chisq.test
        # Chi-square TEST of INDEPENDENCE:
            chisq.test(d$boys, d$hdeduc)
        # G = 6.6118
        # pvalue = 0.579
        # DO NOT REJECT THE NULL: THE 2 VARIABLES ARE INDEPENDENT!
        
        # How many degrees of freedom?
        # r= 3-1 = 2
        # c= 5-1 = 4
        # DF = (2)(4) = 8
            qchisq(0.99, 8)   # 20.090
        
        # VALIDITY OF THE TEST: Is the condition, E_i > 5, RESPECTED?
            chisq.test(d$boys, d$hdeduc)$observed
            chisq.test(d$boys, d$hdeduc)$expected    # YES IT IS
        """)



