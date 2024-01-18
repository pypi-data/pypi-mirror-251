from sklearn.utils import check_array
from hpelm import ELM as Elm

# References Code
# https://github.com/akusok/hpelm/blob/master/hpelm/elm.py

class ELM:
    def __init__(self, object):
        """

        Parameters
        ----------
        object

        func (string): type of neurons: "lin" for linear, "sigm" or "tanh" for non-linear,
                "rbf_l1", "rbf_l2" or "rbf_linf" for radial basis function neurons.

        mss :'V'/'CV'/'LOO' (sting, choose one): model structure selection: select optimal number of neurons using
        a validation set ('V'), cross-validation ('CV') or Leave-One-Out ('LOO')
        'OP' (string, use with 'V'/'CV'/'LOO'): choose best neurons instead of random ones, training takes longer;
        equivalent to L1-regularization
        'c'/'wc'/'ml'/'r' (string, choose one): train ELM for classification ('c'), classification with weighted
        classes ('wc'), multi-label classification ('ml') with several correct classes per data sample, or
        regression ('r') without any classification. In classification, number of `outputs` is the number
        of classes; correct class(es) for each sample has value 1 and incorrect classes have 0.
        Overwrites parameters given an ELM initialization time.
        """

        self.m_info = object
        #self.n_hidden = self.m_info["n_hidden"]
        #if "activation" not in self.m_info.keys():
        #    self.activation = "lin"
        #else:
        #    self.activation = self.m_info["activation"]
        if "bias" not in self.m_info.keys():
            self.bias = 1
        else:
            self.bias = self.m_info["bias"]

        if "mss" not in self.m_info.keys():
            self.mss = "LOO"
        else:
            self.mss = self.m_info["mss"]

    def add_noron(self,unit, act):
        return elm.add_neurons(unit,act)

    def fit(self, X, y):
        global elm
        X = check_array(X)
        y = check_array(y)
        if "Batchsize" not in self.m_info.keys():
            self.Bsize = X.shape[0] / self.bias + 1
        else:
            self.Bsize = self.m_info["Batchsize"]
        elm = Elm(X.shape[1], y.reshape(-1, 1).shape[1], batch=self.Bsize)
        for i,j in zip(self.m_info["unit"],self.m_info["activation"]):
            elm.add_neurons(i, j)
        #elm.add_neurons(20, "sigm")
        #elm.add_neurons(self.n_hidden, self.activation)
        elm.train(X, y,self.mss)

    def predict(self, X):
        X = check_array(X)
        y_pred = elm.predict(X)
        return y_pred