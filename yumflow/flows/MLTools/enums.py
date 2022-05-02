from enum import Enum


class Activation_function(Enum):
    RELU_FUNCTION = 'relu_function'
    SIGMOID_FUNCTION = 'sigmoid_function'
    SOFT_MAX = 'soft_max'
    TANH = 'tanh'


class Weight(Enum):
    Conv = 'conv'
    Linear = 'linear'


class Loss_fn(Enum):
    CROSS_ENTROPY = 'cross_entropy'
    MEAN_ABSOLUTE_ERROR = 'mean_absolute_error'
    MEAN_SQUARE_ERROR = 'mean_square_error'
    NEGATIVE_LIKELIHOOD = 'negative_likelihood'

class Optimizer(Enum):
    SGD = 'SGD'
    ADAM = 'adam'
