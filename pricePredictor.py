# The predictor then gathers the output from the previous to sections 
# and uses a machine learning model in order to create a prediction for the market.
# I am originally considering it to be a simply up/down predictor, however,
# there is room for expansion, in the sense of predicting the size of the shift,
# as well as determining what timeframe it may be done in.
# This is a classification problem, therefore the scope of models that may be used is limited.
# The one suggested in most papers I have read about the topic is the kNN classifier, however,
# I will explore and compare various options such as logistic regression, decision trees, etc.

# input: [{date, active, negative, passive, positive, political, strong, weak, sentiment, topic}] - today price
# output: price direction - future price

from priceGatherer import getPrices
from sentimentExtractor import getArticleSentimentByDate

sentiment = getArticleSentimentByDate()
for i in range(len(sentiment)):
    print(sentiment[i])
# prices = getPrices()
# for i in range(len(prices)):
#     print(prices[i])