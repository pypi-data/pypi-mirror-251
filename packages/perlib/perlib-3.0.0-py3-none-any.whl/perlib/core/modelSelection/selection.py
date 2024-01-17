import pandas as pd
import numpy as np
import statsmodels.api as sm
import re
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from perlib.forecaster import preprocess

class ModelSelection:
    def __init__(self, data):
        self.data = data
        self.num_samples, self.num_features = self.data.shape
        self.features = self.data.columns
        self.feature_types = self.analyze_data()

    def analyze_data(self):
        feature_types = {}

        for feature in self.features:
            feature_type = self.determine_feature_type(feature)
            feature_types[feature] = feature_type

        return feature_types

    def is_categorical_feature(self, feature):
        sample_values = self.data[feature].head(100)
        string_values = [value for value in sample_values if isinstance(value, str)]
        if len(string_values) >= 90:
            return True
        return False

    def is_numeric_feature(self, feature):
        dtype = self.data[feature].dtype

        try:
            if np.issubdtype(dtype, np.number):
                return True
        except:pass

        valid_dtypes = [np.int_, np.float_, np.int32, np.int64, np.float32, np.float64]
        if dtype in valid_dtypes:
            return True

        return False

    def is_text_feature(self, feature):
        sample_values = self.data[feature].head(100)
        text_values = [value for value in sample_values if isinstance(value, str) and len(value.split()) > 2]
        return len(text_values) >= 10

    def determine_feature_type(self, feature):
        if self.is_time_series_feature(feature):
            return "time_series"
        elif self.is_categorical_feature(feature):
            return "categorical"
        elif self.is_numeric_feature(feature):
            return "numeric"
        elif self.is_text_feature(feature):
            return "text"
        else:
            return "unknown"

    def is_time_series_feature(self, feature):
        time_formats = [
            r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",  # yyyy-mm-dd hh:mm:ss
            r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}",  # mm-dd-yyyy hh:mm:ss
            r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}",        # yyyy-mm-dd hh:mm
            r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}",        # mm-dd-yyyy hh:mm
            r"\d{4}-\d{2}-\d{2}",                    # yyyy-mm-dd
            r"\d{2}-\d{2}-\d{4}",                    # mm-dd-yyyy
            r"\d{2}:\d{2}:\d{2}",                    # hh:mm:ss
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",  # ISO 8601 format
        ]

        values = self.data[feature].head(100)
        if any(re.match(pattern, str(value)) for pattern in time_formats for value in values):
            return True
        return False

    def apply_dimensionality_reduction(self, X, y=None):
        num_samples, num_features = X.shape

        pca = PCA(n_components=num_features)
        pca_X = pca.fit_transform(X)
        explained_variance_ratio_pca = pca.explained_variance_ratio_

        if y is not None:
            lda = LinearDiscriminantAnalysis(n_components=min(num_samples, num_features))
            lda_X = lda.fit_transform(X, y)
            explained_variance_ratio_lda = lda.explained_variance_ratio_
        else:
            lda_X = None
            explained_variance_ratio_lda = None

        return pca_X, explained_variance_ratio_pca, lda_X, explained_variance_ratio_lda

    def analyze_dimensionality_reduction(self, pca_explained_variance, lda_explained_variance):
        results = []

        if pca_explained_variance is not None:
            if sum(pca_explained_variance) < 0.95:
                results.append("PCA may be recommended (95% of variance not explained).")

        if lda_explained_variance is not None:
            if sum(lda_explained_variance) < 0.95:
                results.append("LDA application may be recommended (95% of variance not explained).")

        if len(results) == 0:
            return "Size reduction is not recommended."


    def is_seasonal(self ):

        self.data['mean'] = self.data.mean(axis=1)
        decomposition = sm.tsa.seasonal_decompose(self.data['mean'], model='additive')
        if decomposition.seasonal.abs().mean() < 0.01:
            return 'Seasonality not detected'
        else:
            return 'Seasonality detected'

    def is_symmetric_data(self):
        correlation_matrix = self.data.corr()
        is_symmetric = (correlation_matrix == correlation_matrix.T).all().all()

        return is_symmetric

    def has_spatial_temporal_patterns(self):
        # Mekansal ve zamansal desen analizi yapın
        # Örnek olarak basit bir desen analizi yapılıyor
        # Bu fonksiyonu istediğiniz şekilde daha kapsamlı hale getirebilirsiniz

        # Örnek: Verinin ilk ve son yarısını iki parçaya ayırın
        half1 = self.data.iloc[:self.num_samples // 2]
        half2 = self.data.iloc[self.num_samples // 2:]

        # Basit bir desen analizi, ilk yarı verisinin ortalamasını alın ve ikinci yarıdaki değerlerle karşılaştırın
        pattern_detected = (half2.mean() > half1.mean()).all()

        return pattern_detected

    def has_irregular_heterogeneous_data(self):
        # Düzensiz ve heterojen veri analizi yapın
        # Örnek olarak basit bir analiz yapılıyor
        # Bu fonksiyonu istediğiniz şekilde daha kapsamlı hale getirebilirsiniz

        # Örnek: Verinin standart sapması düşükse (homojen) veya veri aralığı büyükse (heterojen) öneri yapın
        std_threshold = 0.5  # Düşük standart sapma için eşik değeri
        range_threshold = 1000  # Büyük veri aralığı için eşik değeri

        std = self.data.std()
        data_range = self.data.max() - self.data.min()

        is_irregular_heterogeneous = (std < std_threshold).any() or (data_range > range_threshold).any()

        return is_irregular_heterogeneous


    def analyze_stationarity_autocorrelation(self):

        adf_results = []
        for feature in self.data.columns:
            adf_result = sm.tsa.adfuller(self.data[feature])
            adf_results.append((feature, adf_result[1]))
        non_stationary_features = [feature for feature, p_value in adf_results if p_value > 0.05]

        autocorrelation_results = []
        for feature in self.data.columns:
            autocorrelation = sm.tsa.acf(self.data[feature])
            significant_lags = sum(1 for lag in range(1, len(autocorrelation)) if autocorrelation[lag] > 0.2)
            autocorrelation_results.append((feature, significant_lags))
        high_autocorrelation_features = [feature for feature, lags in autocorrelation_results if lags > 0]
        return non_stationary_features, high_autocorrelation_features


    def analyze_algorithm_feasibility(self, algorithm_name, time_series_column):

        if algorithm_name == "LSTM":
            if self.num_samples >= 1000:
                return True, "Suitable dataset size, LSTM can be used."
            else:
                return False, "Insufficient dataset size, LSTM is not recommended."
        elif algorithm_name == "LSTNET":
            if self.num_samples >= 5000:
                return True, "If the dataset size is appropriate, LSTNet can be used."
            else:
                return False, "Insufficient dataset size, LSTNet is not recommended."
        elif algorithm_name == "TCN":
            if time_series_column.__len__() != 0:
                return True, "There are temporal dependencies, TCN can be used."
            else:
                return False, "No temporal dependencies, TCN is not recommended."
        elif algorithm_name == "BILSTM":
            if self.is_symmetric_data():
                return True, "Data symmetric, BILSTM is available."
            else:
                return False, "Data is not symmetric, BILSTM is not recommended."
        elif algorithm_name == "CONVLSTM":
            if self.has_spatial_temporal_patterns():
                return True, "There are spatial and temporal patterns, CONVLSTM can be used."
            else:
                return False, "No spatial and temporal patterns, CONVLSTM is not recommended."
        elif algorithm_name == "XGBoost":
            if self.has_irregular_heterogeneous_data():
                return True, "If you have irregular and heterogeneous data, XGBoost can be used."
            else:
                return False, "No irregular and heterogeneous data, XGBoost is not recommended."
        elif algorithm_name == "ARIMA":
            if time_series_column.__len__() != 0:
                non_stationary_features, high_autocorrelation_features = self.analyze_stationarity_autocorrelation()
                if time_series_column[0] in non_stationary_features:
                    return f"Data is not static, {algorithm_name} is not recommended."
                elif time_series_column[0] in high_autocorrelation_features:
                    return False, f"High autocorrelation detected, {algorithm_name} is not recommended."
                else:
                    return True, f"If the data are stationary and autocorrelation properties are appropriate, {algorithm_name} can be used."
        elif algorithm_name in ["SARIMA", "PROPHET"]:
            if time_series_column.__len__() != 0:
                if self.is_seasonal():
                    return True, f"Seasonality detected, {algorithm_name} can be used."
                else:
                    return False, f"Seasonality not detected, {algorithm_name} is not recommended."
            else:
                return False, f"No time series data found, {algorithm_name} is not recommended."
        else:
            return False, "The specified algorithm was not found."


    def select_model(self):

        selected_models = []

        feature_types = self.analyze_data()

        if not feature_types:
            return "Data type could not be determined."

        numeric_features = [feature for feature, feature_type in feature_types.items() if feature_type == "numeric"]
        categorical_features = [feature for feature, feature_type in feature_types.items() if feature_type == "categorical"]
        text_features = [feature for feature, feature_type in feature_types.items() if feature_type == "text"]
        time_series_column = [feature for feature, feature_type in feature_types.items() if feature_type == "time_series"]

        # mevsimsellik durumu için
        if time_series_column.__len__() > 0:
            self.data[time_series_column] = self.data[time_series_column].apply(lambda x: pd.to_datetime(x))
            self.data = self.data.set_index(time_series_column)

        pca_X, pca_explained_variance, lda_X, lda_explained_variance = self.apply_dimensionality_reduction(self.data)
        dimensionality_reduction_results = self.analyze_dimensionality_reduction(pca_explained_variance, lda_explained_variance)

        time_series_models = {
            "ARIMA": 5,
            "SARIMA": 4,
            "PROPHET": 3,
            "LSTM": 2,
            "LSTNET": 1,
            "TCN": 2,
            "BILSTM": 3,
            "CONVLSTM": 1,
            "XGBoost": 4
        }

        classification_models = [
            "Logistic Regression",
            "Decision Trees",
            "Random Forest",
            "Gradient Boosting",
            "XGBoost",
            "LightGBM",
            "Support Vector Machines (SVM)",
            "K-Nearest Neighbors (KNN)",
            "Naive Bayes",
            "Neural Networks"
        ]

        regression_models = [
            "Linear Regression",
            "Ridge Regression",
            "Lasso Regression",
            "Random Forest Regression",
            "Gradient Boosting Regression",
            "XGBoost Regression",
            "LightGBM Regression",
            "Support Vector Regression (SVR)",
            "K-Nearest Neighbors (KNN)",
        ]

        text_analysis_models = [
            "CNN (Convolutional Neural Network)",
            "RNN (Recurrent Neural Network)",
            "LSTM (Long Short-Term Memory)",
            "Transformer",
            "BERT (Bidirectional Encoder Representations from Transformers)",
            "GPT (Generative Pre-trained Transformer)"
        ]

        other_models = [
            "Clustering Models",
            "Dimensionality Reduction (PCA, t-SNE)",
            "Ensemble Models",
            "Recommendation Systems",
            "Anomaly Detection Models"
        ]

        algorithm_results = []
        for algorithm in time_series_models:
            algorithm_feasibility = self.analyze_algorithm_feasibility(algorithm, time_series_column)
            if algorithm_feasibility != None:
                if algorithm_feasibility[0]:
                    algorithm_results.append((algorithm, algorithm_feasibility[0],algorithm_feasibility[1]))
                else:
                    algorithm_results.append((algorithm, algorithm_feasibility[0],algorithm_feasibility[1]))

        algorithm_results = sorted(algorithm_results, key=lambda x: x[1], reverse=True)
        # Algoritma sonuçlarını popülerlik sırasına ve kullanılabilirlik durumuna göre sıralayın

        # Diğer model analizlerini burada yapın ve algorithm_results listesine ekleyin
        # ...

        selected_models.extend([(x[0], x[2]) for x in algorithm_results])

        #if time_series_column and numeric_features:
        #    selected_models.extend(time_series_models)
#
        #if time_series_column and categorical_features:
        #    selected_models.extend(time_series_models)
#
        #if numeric_features:
        #    selected_models.extend(regression_models)
#
        #if categorical_features:
        #    selected_models.extend(classification_models)

        if text_features:
            selected_models.extend(text_analysis_models)

        # Diğer durumları ve özellikleri buraya ekleyebilirsiniz
        if not selected_models:
            selected_models = ["General Situation"]

        print("\nDimension Reduction Analysis:",dimensionality_reduction_results)
        print("\nSelected Models:")
        for idx, model in enumerate(selected_models, start=1):
            print(f"{idx}. {model}")