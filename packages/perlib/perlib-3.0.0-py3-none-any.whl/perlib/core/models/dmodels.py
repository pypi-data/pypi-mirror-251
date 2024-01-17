import tensorflow as tf
from keras.optimizers import (Adam,SGD,RMSprop,Adadelta,Adamax,Adagrad,Nadam,Ftrl)
from tcn import TCN
from ..req_utils import *

class models():
    def __init__(self,
                 req_info,
                 pool_size = 1,
                 kernel_size = 3,
                 filters = 64,
                 show=True
                 ):

        self.req_info    = req_info
        self.input_shape = (24,1)
        self.model_multi = tf.keras.models.Sequential()
        self.pool_size = pool_size
        self.kernel_size = kernel_size
        self.filters = filters
        self.show = show
        if self.req_info.targetCol is None:
            check(False)
        if bool(self.req_info.metric):
            evaluate(self.req_info.metric)
        if self.req_info.modelname == "lstnet":
            check_D_modelname(self.req_info.layers,self.req_info.modelname)
        check_layer(self.req_info.layers,self.req_info)
        check_scaler(self.req_info.scaler)


    def layers(self,unit:int,activation:str,return_sequences=True,
               input_shape=None,filters=None,kernel_size = None):

        if self.req_info.modelname.lower() == "lstm":
            return tf.keras.layers.LSTM(units=unit,input_shape=self.input_shape,
                                        activation=activation,
                                        return_sequences=return_sequences)
        elif self.req_info.modelname.lower() == "bilstm":
            return tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units=unit,input_shape=self.input_shape,
                                        activation=activation,
                                        return_sequences=return_sequences))
        elif self.req_info.modelname.lower() == "convlstm":
             return tf.keras.layers.Conv1D(filters=self.filters,
                                       kernel_size= self.kernel_size,
                                       input_shape=self.input_shape,
                                       activation=activation)
        elif self.req_info.modelname.lower() == "tcn":
            return TCN(unit,input_shape=self.input_shape,
                                        activation=activation,
                                        return_sequences=return_sequences)
        elif self.req_info.modelname.lower() == "rnn":
            return tf.keras.layers.SimpleRNN(units=unit, input_shape=self.input_shape,
                                        activation=activation,
                                        return_sequences=return_sequences)


    def losses_(self, loss_: str = 'mse', from_logits: bool = False):

        """Selects a loss function from TensorFlow Keras losses.

           This method takes a string argument that specifies the name of the loss function
           and an optional boolean argument that indicates whether the predictions are logits
           or probabilities. It returns a loss function object that can be used to compute
           the error between the true and predicted values.

           Parameters:
           loss_ (str): The name of the loss function. It should be one of the following:
               - 'mse': Mean squared error
               - 'mae': Mean absolute error
               - 'mape': Mean absolute percentage error
               - 'msle': Mean squared logarithmic error
               - 'cosine_similarity': Cosine similarity
               - 'logcosh': Logarithm of the hyperbolic cosine of the prediction error
               - 'huber': Huber loss
               - 'hinge': Hinge loss for "maximum-margin" classification
               - 'squared_hinge': Squared hinge loss
               - 'categorical_hinge': Categorical hinge loss
               - 'binary_crossentropy': Binary cross-entropy
               - 'categorical_crossentropy': Categorical cross-entropy
               - 'sparse_categorical_crossentropy': Sparse categorical cross-entropy
               - 'poisson': Poisson loss
               - 'kl_divergence': Kullback-Leibler divergence
           from_logits (bool): Whether the predictions are logits or probabilities. Default is False.

           Returns:
           A loss function object from TensorFlow Keras losses.

           Raises:
           ValueError: If the loss_ argument is not a valid loss function name.
           """


        if loss_.lower() == 'mse':
            loss = tf.keras.losses.MeanSquaredError()
        elif loss_.lower() == 'mae':
            loss = tf.keras.losses.MeanAbsoluteError()
        elif loss_.lower() == 'mape':
            loss = tf.keras.losses.MeanAbsolutePercentageError()
        elif loss_.lower() == 'msle':
            loss = tf.keras.losses.MeanSquaredLogarithmicError()
        elif loss_.lower() == 'cosine_similarity':
            loss = tf.keras.losses.CosineSimilarity()
        elif loss_.lower() == 'logcosh':
            loss = tf.keras.losses.LogCosh()
        elif loss_.lower() == 'huber':
            loss = tf.keras.losses.Huber()
        elif loss_.lower() == 'hinge':
            loss = tf.keras.losses.Hinge()
        elif loss_.lower() == 'squared_hinge':
            loss = tf.keras.losses.SquaredHinge()
        elif loss_.lower() == 'categorical_hinge':
            loss = tf.keras.losses.CategoricalHinge()
        elif loss_.lower() == 'binary_crossentropy':
            loss = tf.keras.losses.BinaryCrossentropy(from_logits=from_logits)
        elif loss_.lower() == 'categorical_crossentropy':
            loss = tf.keras.losses.CategoricalCrossentropy(from_logits=from_logits)
        elif loss_.lower() == 'sparse_categorical_crossentropy':
            loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=from_logits)
        elif loss_.lower() == 'poisson':
            loss = tf.keras.losses.Poisson()
        elif loss_.lower() == 'kl_divergence':
            loss = tf.keras.losses.KLDivergence()
        else:
            raise ValueError("Unsupported loss")
        return loss

    def metrics_(self, metric_: str = 'acc', from_logits: bool = False):

        """Selects a metric function from TensorFlow Keras metrics.

           This method takes a string argument that specifies the name of the metric function
           and an optional boolean argument that indicates whether the predictions are logits
           or probabilities. It returns a metric function object that can be used to evaluate
           the performance of the model.

           Parameters:
           metric_ (str): The name of the metric function. It should be one of the following:
               - 'acc': Accuracy
               - 'binary_acc': Binary accuracy
               - 'categorical_acc': Categorical accuracy
               - 'sparse_categorical_acc': Sparse categorical accuracy
               - 'top_k_categorical_acc': Top k categorical accuracy
               - 'sparse_top_k_categorical_acc': Sparse top k categorical accuracy
               - 'mse': Mean squared error
               - 'rmse': Root mean squared error
               - 'mae': Mean absolute error
               - 'mape': Mean absolute percentage error
               - 'msle': Mean squared logarithmic error
               - 'cosine_similarity': Cosine similarity
               - 'logcosh_error': Logarithm of the hyperbolic cosine of the prediction error
               - 'auc': Area under the curve
               - 'precision': Precision
               - 'recall': Recall
               - 'true_positives': True positives
               - 'true_negatives': True negatives
               - 'false_positives': False positives
               - 'false_negatives': False negatives
               - 'precision_at_recall': Precision at recall
               - 'sensitivity_at_specificity': Sensitivity at specificity
               - 'specificity_at_sensitivity': Specificity at sensitivity
               - 'mean_iou': Mean intersection-over-union
               - 'hinge': Hinge loss for "maximum-margin" classification
               - 'squared_hinge': Squared hinge loss
               - 'categorical_hinge': Categorical hinge loss
               - 'binary_crossentropy': Binary cross-entropy
               - 'categorical_crossentropy': Categorical cross-entropy
               - 'sparse_categorical_crossentropy': Sparse categorical cross-entropy
               - 'poisson': Poisson loss
               - 'kl_divergence': Kullback-Leibler divergence
           from_logits (bool): Whether the predictions are logits or probabilities. Default is False.

           Returns:
           A metric function object from TensorFlow Keras metrics.

           Raises:
           ValueError: If the metric_ argument is not a valid metric function name.

           """
        if metric_.lower() == 'acc':
            metric = tf.keras.metrics.Accuracy()
        elif metric_.lower() == 'binary_acc':
            metric = tf.keras.metrics.BinaryAccuracy()
        elif metric_.lower() == 'categorical_acc':
            metric = tf.keras.metrics.CategoricalAccuracy()
        elif metric_.lower() == 'sparse_categorical_acc':
            metric = tf.keras.metrics.SparseCategoricalAccuracy()
        elif metric_.lower() == 'top_k_categorical_acc':
            metric = tf.keras.metrics.TopKCategoricalAccuracy()
        elif metric_.lower() == 'sparse_top_k_categorical_acc':
            metric = tf.keras.metrics.SparseTopKCategoricalAccuracy()
        elif metric_.lower() == 'mse':
            metric = tf.keras.metrics.MeanSquaredError()
        elif metric_.lower() == 'rmse':
            metric = tf.keras.metrics.RootMeanSquaredError()
        elif metric_.lower() == 'mae':
            metric = tf.keras.metrics.MeanAbsoluteError()
        elif metric_.lower() == 'mape':
            metric = tf.keras.metrics.MeanAbsolutePercentageError()
        elif metric_.lower() == 'msle':
            metric = tf.keras.metrics.MeanSquaredLogarithmicError()
        elif metric_.lower() == 'cosine_similarity':
            metric = tf.keras.metrics.CosineSimilarity()
        elif metric_.lower() == 'logcosh_error':
            metric = tf.keras.metrics.LogCoshError()
        elif metric_.lower() == 'auc':
            metric = tf.keras.metrics.AUC()
        elif metric_.lower() == 'precision':
            metric = tf.keras.metrics.Precision()
        elif metric_.lower() == 'recall':
            metric = tf.keras.metrics.Recall()
        elif metric_.lower() == 'true_positives':
            metric = tf.keras.metrics.TruePositives()
        elif metric_.lower() == 'true_negatives':
            metric = tf.keras.metrics.TrueNegatives()
        elif metric_.lower() == 'false_positives':
            metric = tf.keras.metrics.FalsePositives()
        elif metric_.lower() == 'false_negatives':
            metric = tf.keras.metrics.FalseNegatives()
        elif metric_.lower() == 'precision_at_recall':
            metric = tf.keras.metrics.PrecisionAtRecall()
        elif metric_.lower() == 'sensitivity_at_specificity':
            metric = tf.keras.metrics.SensitivityAtSpecificity()
        elif metric_.lower() == 'specificity_at_sensitivity':
            metric = tf.keras.metrics.SpecificityAtSensitivity()
        elif metric_.lower() == 'mean_iou':
            metric = tf.keras.metrics.MeanIoU()
        elif metric_.lower() == 'hinge':
            metric = tf.keras.metrics.Hinge()
        elif metric_.lower() == 'squared_hinge':
            metric = tf.keras.metrics.SquaredHinge()
        elif metric_.lower() == 'categorical_hinge':
            metric = tf.keras.metrics.CategoricalHinge()
        elif metric_.lower() == 'binary_crossentropy':
            metric = tf.keras.metrics.BinaryCrossentropy(from_logits=from_logits)
        elif metric_.lower() == 'categorical_crossentropy':
            metric = tf.keras.metrics.CategoricalCrossentropy(from_logits=from_logits)
        elif metric_.lower() == 'sparse_categorical_crossentropy':
            metric = tf.keras.metrics.SparseCategoricalCrossentropy(from_logits=from_logits)
        elif metric_.lower() == 'poisson':
            metric = tf.keras.metrics.Poisson()
        elif metric_.lower() == 'kl_divergence':
            metric = tf.keras.metrics.KLDivergence()
        else:
            raise ValueError("Unsupported metric")
        return metric

    def optimizers_(self, opt_: str = 'adam', learning_rate: float = 0.001):
        if opt_.lower() == 'sgd':
            opt = SGD(learning_rate=learning_rate)
        elif opt_.lower() == 'adam':
            opt = Adam(learning_rate=learning_rate)
        elif opt_.lower() == 'rmsprop':
            opt = RMSprop(learning_rate=learning_rate)
        elif opt_.lower() == 'adagrad':
            opt = Adagrad(learning_rate=learning_rate)
        elif opt_.lower() == 'adadelta':
            opt = Adadelta(learning_rate=learning_rate)
        elif opt_.lower() == 'adamax':
            opt = Adamax(learning_rate=learning_rate)
        elif opt_.lower() == 'nadam':
            opt = Nadam(learning_rate=learning_rate)
        elif opt_.lower() == 'ftrl':
            opt = Ftrl(learning_rate=learning_rate)
        else:
            raise ValueError("Unsupported optimizer")
        return opt
    def layer(self, tuple, index, len):
        if index == 0:
            self.model_multi.add(
                self.layers(tuple[0],kernel_size=self.kernel_size,filters=self.filters, activation=tuple[1])),
            if self.req_info.modelname.lower() == "convlstm":
                self.model_multi.add(tf.keras.layers.MaxPool1D(pool_size=1))
            self.model_multi.add(tf.keras.layers.Dropout(tuple[2])),
        elif index == len - 1:
            if self.req_info.modelname.lower() == "convlstm":
                self.model_multi.add(tf.keras.layers.LSTM(tuple[0], activation=tuple[1], return_sequences=False)),
            else:
                self.model_multi.add(self.layers(tuple[0], activation=tuple[1],input_shape=None,filters=None,
                                                         kernel_size=None,
                                                         return_sequences=False)),
            self.model_multi.add(tf.keras.layers.Dropout(tuple[2])),
            self.model_multi.add(tf.keras.layers.Dense(units=1)),
        else:
            if self.req_info.modelname.lower() == "convlstm":
                self.model_multi.add(tf.keras.layers.LSTM(tuple[0], activation=tuple[1], return_sequences=True)),
            else:
                self.model_multi.add(self.layers(tuple[0],kernel_size=None,filters=None, activation=tuple[1],input_shape=None)),
            self.model_multi.add(tf.keras.layers.Dropout(tuple[2])),

        opt = self.optimizers_(opt_=self.req_info.optimizer, learning_rate=self.req_info.learning_rate)
        loss_ = self.losses_(loss_=self.req_info.loss)
        #metrics_ = self.losses_(loss_=self.req_info.train_metrics)
        self.model_multi.compile(optimizer=opt,loss=loss_)
        return self.model_multi

    def set_inputShape(self,input_shape):
        self.input_shape = input_shape

    def build_model(self):
        if self.req_info.layers is None:
            units = [150, 100, 50]
            activations = ["tanh", "tanh", "tanh"]
            dropouts = [0.2, 0.2, 0.2]
        else:
            units = [x for x in self.req_info.layers.values()][0]
            activations = [x for x in self.req_info.layers.values()][1]
            dropouts = [x for x in self.req_info.layers.values()][2]
        for i in range(len(units)):
            self.model_multi = self.layer([list(zip(units, activations, dropouts))][0][i], i, len(units))
        if self.show:
            try:
                self.model_multi.summary()
            except:pass
        return self.model_multi
