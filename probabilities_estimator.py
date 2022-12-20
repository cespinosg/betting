import json

import scipy.optimize as opt


class ProbabilityEstimator:
    '''
    Estimates the probability of the results based on the odds.
    '''

    def __init__(self, odds):
        self.odds = odds
        self._validate_odds()
        self._estimate_probability()
        self._estimate_expected()
        self._estimate_variance()

    def _validate_odds(self):
        '''
        Checks if the given odds has the correct format.
        '''
        if 'home' not in self.odds:
            raise RuntimeError('The given data does not have the home odd.')
        if 'draw' not in self.odds:
            raise RuntimeError('The given data does not have the draw odd.')
        if 'away' not in self.odds:
            raise RuntimeError('The given data does not have the away odd.')

    def _estimate_probability(self):
        '''
        Estimates the probability with the power method.
        https://medium.com/geekculture/how-to-compute-football-implied-probability-from-bookmakers-odds-bbb33ccf7c1d
        '''
        home = 1/self.odds['home']
        draw = 1/self.odds['draw']
        away = 1/self.odds['away']
        func = lambda k: (1-(home**k+draw**k+away**k))**2
        k = opt.golden(func)
        self.probability = {
            'home': home**k,
            'draw': draw**k,
            'away': away**k,
            }

    def _estimate_expected(self):
        '''
        Estimates the expected return of each bet.
        '''
        self.expected = {}
        for k in self.probability.keys():
            self.expected[k] = self.probability[k]*self.odds[k]

    def _estimate_variance(self):
        '''
        Estimates the variance of the binomial distribution.
        https://en.wikipedia.org/wiki/Binomial_distribution
        '''
        self.variance = {}
        for k in self.probability.keys():
            p = self.probability[k]
            self.variance[k] = p*(1-p)

    def print_probabilites(self):
        '''
        Prints the probability.
        '''
        print('\nProbabilities')
        self._print_dict(self.probability)

    def print_expected_gains(self):
        '''
        Prints the expected gains.
        '''
        print('\nExpected gains')
        self._print_dict(self.expected)

    def print_variances(self):
        '''
        Prints the variances.
        '''
        print('\nVariances')
        self._print_dict(self.variance)

    def _print_dict(self, data):
        '''
        Prints the given data.
        '''
        print(json.dumps(data, indent=4))


if __name__ == '__main__':
    odds = {
        'home': 8.50,
        'draw': 5.00,
        'away': 1.37,
        }
    estimator = ProbabilityEstimator(odds)
    estimator.print_probabilites()
    estimator.print_expected_gains()
    estimator.print_variances()
