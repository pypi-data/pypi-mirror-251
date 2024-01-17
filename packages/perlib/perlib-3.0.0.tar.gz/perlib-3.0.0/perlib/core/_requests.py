class m_info(object):
    """
    Desired parameters for machine learning algorithms  ( ALL machine learnin algorithms )
    """

    def __init__(self,
                 y=None,
                 modelname      : str   = "SVR",
                 scaler         : str   = "minmax",
                 testsize       : float = 0.2,
                 shuffle        : bool  = True,
                 metric         : str   = "mape",
                 modelparams            = None,
                 auto                   = False,

                 ):
        self.y = y
        self.modelname = modelname
        self.modelparams = modelparams
        self.testsize = testsize
        self.scaler = scaler
        self.shuffle = shuffle
        self.auto = auto
        self.metric              = metric

class aR_info(object):

    """
    Desired parameters for statistical learning algorithms  ( ARIMA , SARIMA )
    """
    def __init__(self,
                 modelname             : str  = "arima",
                 max_p                 : int  = 5,
                 max_d                 : int  = 2,
                 max_q                 : int  = 5,
                 max_P                 : int  = 2,
                 max_D                 : int  = 2,
                 max_Q                 : int  = 2,
                 s                     : int  = 12,
                 forecastNumber        : int  = 24,
                 metric                : str  = "mape",
                 forecastingStartDate  : int  = False
                 ):
        self.modelname           = modelname
        self.max_p               = max_p
        self.max_d               = max_d
        self.max_q               = max_q
        self.max_P               = max_P
        self.max_D               = max_D
        self.max_Q               = max_Q
        self.s                   = s
        self.forecastNumber       = forecastNumber
        self.forecastingStartDate = forecastingStartDate
        self.metric              = metric

class req_info(object):
    """

    modelname (str) : Desired parameters for deep learning algorithms  ( LSTNET,LSTM,BILSTM,CONVLSTM,RNN,TCN )

    lookback (int): Number of time steps to look back in the input sequence.

    epoch (int)            : Number of training epochs.

    batch_size (int)       : Batch size for training.

    learning_rate (float)  : Learning rate for the optimizer.

    optimizer (str)        : Name of the optimizer to be used. ( 'adam', 'sgd', 'rmsprop','adagrad','adadelta','adamax','nadam','ftrl')

    scaler   (str)         : Data scaling object.

    metric (str)           : Evaluation metric to be used.

    forecastNumber (int)   : Number of steps ahead to forecast.

    targetCol (str)        : Index of the target column in the input data.

    layers (dict): List containing the number of units in each hidden layer.

    forecastingStartDate (str): Start date for forecasting.


    Example :

    {

    "unit": [150,100,50],

    "activation": ["tanh","tanh","tanh"],

    "dropout": [0.2,0.2,0.2]

    }


    LstNet params :
    CNNFilters:   Number of output filters in the CNN layer Default : 100 If set to 0, the CNN layer will be omitted

    CNNKernel:    CNN filter size that will be (CNNKernel, number of multivariate timeseries) Default : 6

    GRUUnits:     Number of hidden states in the GRU layer Default : 100

    SkipGRUUnits: Number of hidden states in the SkipGRU layer Default : 5

    skip:         Number of timeseries to skip. 0 => do not add Skip GRU layer Default : 24

    dropout:      Dropout frequency Default : 0.2

    highway:      Number of timeseries values to consider for the linear layer (AR layer) Default : 24

    Example :

    {

  "CNNFilters": 100,

  "CNNKernel": 6,

  "GRUUnits": 50,

  "skip": 24

    }
    """

    def __init__(self,
                 modelname             : str  = "lstm",
                 lookback              : int  = 24,
                 epoch                 : int  = 2,
                 batch_size            : int  = 200,
                 learning_rate         : float= 0.001,
                 optimizer             : str  = "adam",
                 loss                  : str  = "mse",
                 scaler                : str  = "standard",
                 metric                : str  = "mape",
                 forecastNumber        : int  = 24,
                 targetCol             : str  = None,
                 layers                : dict = None,
                 forecastingStartDate  : str  = False
                 ) :

        self.modelname            = modelname
        self.metric               = metric
        self.loss                 = loss
        self.layers               = layers
        self.learning_rate        = learning_rate
        self.optimizer            = optimizer
        self.lookback             = lookback
        self.epoch                = epoch
        self.batch_size           = batch_size
        self.scaler               = scaler
        self.forecastingStartDate = forecastingStartDate
        self.forecastNumber       = forecastNumber
        self.targetCol            = targetCol


