import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler,StandardScaler,MaxAbsScaler, RobustScaler
from statsmodels.tsa.stattools import adfuller as ADF
from sklearn.model_selection import train_test_split
#import pymrmr
from sklearn.feature_selection import f_regression
import math
import operator
import sqlite3
from ._utils.dataframe import read_pandas
from typing import Union,List,Dict,Optional,Any
import json

columnsDate = ["Time","TIME","time","Datetime","datetime","DATETİME","TARİH",
                       "Tarih","tarih","timestamp","TIMESTAMP","Timestamp","date","Date","DATE"]


def check_string_values(df, columns):
    for column in columns:
        has_string_or_nan = df[column].apply(lambda x: isinstance(x, str) or np.isnan(x)).any()
        if has_string_or_nan:
            error_messages = [
                f"String or NaN value found in column '{column}' at index {index}."
                for index, value in df[column].iteritems() if
                isinstance(value, str) or (np.isnan(value) or pd.isna(value))
            ]
            raise ValueError("\n".join(error_messages))

class HandleException(Exception):
    messages = {
        'generic': 'A generic error occurred.',
        'generic_value_error': 'Invalid type of value provided.',
        'integer_value_error': 'The value must be type of Integer (int).',
        'list_value_error': 'The value must be type of List (list).',
        'float_value_error': 'The value must be type of Float (float).',
        'string_value_error': 'The value must be type of String (string).',
        'boolean_value_error': 'The  value must be type of Boolean (bool).',
        'file_not_found': 'File not found.',
        'permission_error': 'Permission denied.',
        'index_error': 'Index out of range.',
        'key_error': 'Key not found.',
        'type_error': 'Invalid data type.',

        # Add more error messages as needed
    }

    def __init__(self, error_type='generic', error_message=""):
        self.error_type = error_type
        self.message = self.messages.get(error_type, self.messages['generic'])+' '+error_message
        super().__init__(self.message)



class dataPrepration:

    def __init__(self):
        self.dataFrame = False
        self.col       = False
        #self.dataFrame = self.__datatimeinsert()
        #self.dataFrame = self.insertFirstcolumn(col=self.col)

    def read_data(self, path,delimiter=None) -> pd.DataFrame:
        dataFrame = read_pandas(path,delimiter=delimiter)
        return dataFrame
#
    def load_sql( self,query:str,path:str):
        con = sqlite3.connect(path)
        dataFrame = pd.read_sql(query,con=con)
        return dataFrame

    def _date_check(self,dataFrame : pd.DataFrame):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        if dataFrame.index.name in columnsDate:
            dataFrame = dataFrame.reset_index()
            dcol = list(set(dataFrame.columns.tolist()).intersection(columnsDate))[0]
            dataFrame[dcol] = pd.to_datetime(dataFrame[dcol])
        elif len(list(set(dataFrame.columns.tolist()).intersection(columnsDate))) > 0:
            dcol = list(set(dataFrame.columns.tolist()).intersection(columnsDate))[0]
            dataFrame[dcol] = pd.to_datetime(dataFrame[dcol])

        return dataFrame,dcol

    def _datatimeinsert(self, dataFrame:pd.DataFrame ) -> pd.DataFrame:
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        dataFrame,dcol = self._date_check()
        try:
            dataFrame[dcol] = dataFrame[dcol].astype('datetime64[ns]')
            dataFrame.index = dataFrame[dcol]
            del dataFrame[dcol]
        except: pass
        return dataFrame

    def _insertFirstcolumn(self , col : str , dataFrame : pd.DataFrame):

        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        dataFrame = dataFrame.sort_index()
        first_column = dataFrame.pop(col)
        dataFrame.insert(0, col, first_column)
        return dataFrame

    def trainingFordate_range(self, dt1 : str, dt2 : str, dataFrame : pd.DataFrame):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        try:
            dataFrame = self._datatimeinsert().sort_index()
        except:pass
        return dataFrame[(dataFrame.index > dt1) & (dataFrame.index < dt2)]


    def train_test_split(self, dataFrame : pd.DataFrame, target=None, test_size=None, tX=None, tY=None,
                         train_size=None,
                         random_state=None,
                         shuffle=True,
                         stratify=None,
                         ):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        try:
            Y = dataFrame.loc[:, [target]].values
            X = dataFrame.loc[:, dataFrame.columns != target].values
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, train_size=train_size,
                                                                random_state=random_state, shuffle=shuffle,
                                                                stratify=stratify)
        except:
            X_train, X_test, y_train, y_test = train_test_split(tX, tY, test_size=test_size, train_size=train_size,
                                                                random_state=random_state, shuffle=shuffle,
                                                                stratify=stratify)

        print("X_train shape :", X_train.shape)
        print("X_test shape  :", X_test.shape)
        print("Y_train shape :", y_train.shape)
        print("Y test shape  :", y_test.shape)
        return X_train, X_test, y_train, y_test

    def clean_dataset(self,df:pd.DataFrame):
        assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
        df.dropna(inplace=True)
        indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
        return df[indices_to_keep].astype(np.float64)

    def split( X_data , y_data , test_split : int  ):
        # Splitting the data into train and test
        X_train= X_data[:-test_split]
        X_test= X_data[-test_split:]
        y_train=y_data[:-test_split]
        y_test=y_data[-test_split:]

        print("X_train shape :", X_train.shape)
        print("X_test shape  :", X_test.shape)
        print("Y_train shape :", y_train.shape)
        print("Y test shape  :", y_test.shape)

        return X_train , X_test , y_train , y_test

    def diff( self , col : str  ,dataFrame : pd.DataFrame) :
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        values = dataFrame[col].diff()
        return values

    def gauss_Filter(self, dataFrame : pd.DataFrame, col : str, sigma =0.3, ):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        values = pd.Series(gaussian_filter(dataFrame[col], sigma=sigma),
                                                           index=dataFrame.index).astype(float)
        return values

    def moving_average(self,dataFrame : pd.DataFrame, col : str, window : int =3):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        values = dataFrame[col].rolling(window=window).mean().dropna()
        return values

    def exponential_Smoothing(self, col : str, dataFrame : pd.DataFrame):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        values = sm.tsa.ExponentialSmoothing(dataFrame[col],
                                                                 trend='add',
                                                                 seasonal_periods=4).fit().fittedvalues.shift(1)
        return values

    def rolling_mean_diff(self,dataFrame : pd.DataFrame, col : str, window : int =3 ):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        rolling_mean = dataFrame.rolling(window=window).mean()
        values = rolling_mean[col] - rolling_mean[col].shift().dropna()
        return values

    def circ(self,dataFrame : pd.DataFrame,dateColumn : str):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        hours_in_week = 7 * 24
        #dataFrame,dcol            = self._date_check()
        dataFrame[dateColumn] = pd.to_datetime(dataFrame[dateColumn])
        dataFrame['CircHourX']    = dataFrame[dateColumn].apply(lambda x: np.cos(x.hour / 24 * 2 * np.pi))
        dataFrame['CircHourY']    = dataFrame[dateColumn].apply(lambda x: np.sin(x.hour / 24 * 2 * np.pi))
        dataFrame['CircWeekdayX'] = dataFrame[dateColumn].apply(lambda x: np.cos(x.weekday() * 24 + x.hour / hours_in_week * 2 * np.pi))
        dataFrame['CircWeekdayY'] = dataFrame[dateColumn].apply(lambda x: np.sin(x.weekday() * 24 + x.hour / hours_in_week * 2 * np.pi))
        dataFrame['CircDayX']     = dataFrame[dateColumn].apply(lambda x: np.cos(x.day * 24 + x.hour / x.daysinmonth * 2 * np.pi))
        dataFrame['CircDayY']     = dataFrame[dateColumn].apply(lambda x: np.sin(x.day * 24 + x.hour / x.daysinmonth * 2 * np.pi))
        dataFrame['CircMonthX']   = dataFrame[dateColumn].apply(lambda x: np.cos(x.dayofyear / 365 * 2 * np.pi))
        dataFrame['CircMonthY']   = dataFrame[dateColumn].apply(lambda x: np.sin(x.dayofyear / 365 * 2 * np.pi))
        dataFrame = dataFrame.set_index(dateColumn)
        return dataFrame

    def generate_time_lags(self,dataFrame : pd.DataFrame, col : str, n_lags : int = False, th : float=False, firstN : int =False):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        def glag(df, columns, n_lags: int):
            df_L = df.copy()
            df_L = df_L[[columns]]
            for n in range(1, n_lags + 1):
                df_L[f"lag{n}"] = df_L[columns].shift(n)
            return pd.concat([df, df_L.iloc[:, 1:]], axis=1).dropna()

        dict_ = {'Lag': [],
                 'Autocor': []}

        for lag in range(1, int(np.sqrt(dataFrame.shape[0]))):
            shift = dataFrame[col].autocorr(lag)
            dict_['Lag'].append(lag)
            dict_['Autocor'].append(shift)
        autocorr_df = pd.DataFrame(dict_)
        autocorr_df = autocorr_df.sort_values("Autocor", ascending=False).reset_index(drop=True)

        if bool(n_lags) is True:
            return glag(dataFrame, col, n_lags).dropna()

        elif bool(th) is True:
            autocorr_df = autocorr_df[autocorr_df.Autocor > th]
            if autocorr_df.__len__() > 0:
                lags = ["lag" + str(x) for x in autocorr_df.Lag.tolist()]
                df_c = dataFrame.copy()
                df_c = glag(df_c, col, autocorr_df.Lag.max())
                return pd.concat([dataFrame, df_c.loc[:, lags]], axis=1).dropna()
            else:
                raise ValueError(f'No value above {th} was found.')

        elif bool(firstN) is True:
            autocorr_df = autocorr_df[:firstN]
            lags = ["lag" + str(x) for x in autocorr_df.Lag.tolist()]
            df_c = dataFrame.copy()
            df_c = glag(df_c, col, autocorr_df.Lag.max())
            return pd.concat([dataFrame, df_c.loc[:, lags]], axis=1).dropna()
        else:
            pass

    def adf_test(self, dataFrame : pd.DataFrame, columns : list =[]):

        if len(columns) == 0:
            raise  TypeError("adf_test() missing 1 required positional argument: columns")

        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        dataFrame = dataFrame.dropna()
        for col in columns:
            print(f'Augmented Dickey-Fuller Test: {col}')
            result = ADF(dataFrame[col], autolag='AIC')

            labels = ['ADF test statistic', 'p-value', '# lags used', '# observations']
            out = pd.Series(result[0:4], index=labels)

            for key, val in result[4].items():
                out[f'critical value ({key})'] = val
            print(out.to_string())

            if result[1] <= 0.05:
                print("Strong evidence against the null hypothesis")
                print("Reject the null hypothesis")
                print("Data has no unit root and is stationary")
            else:
                print("Weak evidence against the null hypothesis")
                print("Fail to reject the null hypothesis"),
                print("Data has a unit root and is non-stationary")

    def date_transform(self,dateColumn : str , dataFrame : pd.DataFrame):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        #dataFrame, dcol = self._date_check(dataFrame=dataFrame)

        if bool(dataFrame.index.name):
            dataFrame = dataFrame.reset_index()
        try:
            dataFrame[dateColumn] = pd.to_datetime(dataFrame[dateColumn],dayfirst=True)
        except:
            dataFrame[dateColumn] = pd.to_datetime(dataFrame[dateColumn])
        dataFrame['Year']       = dataFrame[dateColumn].dt.year
        dataFrame['Month']      = dataFrame[dateColumn].dt.month
        dataFrame['Day']        = dataFrame[dateColumn].dt.day
        try:
            dataFrame['WeekofYear'] = dataFrame[dateColumn].dt.weekofyear
        except:
            dataFrame['WeekofYear'] = dataFrame[dateColumn].apply(lambda x: x.isocalendar()[1])
        dataFrame['DayofWeek']  = dataFrame[dateColumn].dt.weekday
        dataFrame['Hour']       = dataFrame[dateColumn].dt.hour
        try:
            dataFrame[dateColumn] = dataFrame[dateColumn].astype('datetime64[ns]')
            dataFrame.index = dataFrame[dateColumn]
            del dataFrame[dateColumn]
        except:
            pass

        return dataFrame

    #def mRMR(self, dataFrame = None, method="MIQ", n_features=3):
#
    #    """
    #    First parameter is a pandas DataFrame (http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) containing the input dataset, discretised as defined in the original paper (for ref. see http://home.penglab.com/proj/mRMR/). The rows of the dataset are the different samples. The first column is the classification (target) variable for each sample. The remaining columns are the different variables (features) which may be selected by the algorithm. (see “Sample Data Sets” at http://home.penglab.com/proj/mRMR/ to download sample dataset to test this algorithm). IMPORTANT: the column names (feature names) should be of type string;
    #    Second parameter is a string which defines the internal Feature Selection method to use (defined in the original paper): possible values are “MIQ” or “MID”;
    #    Third parameter is an integer which defines the number of features that should be selected by the algorithm.
#
    #    """
    #    if isinstance(dataFrame, pd.DataFrame):
    #        self.dataFrame = dataFrame
    #    return pymrmr.mRMR(self.dataFrame, method, n_features)

    def likelihood(self, targetcol : str, dataFrame : pd.DataFrame, n_features:int = 4):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        columns = []
        for col in dataFrame.columns:
            for col2 in columnsDate:
                if col.endswith(col2) or col.startswith(col2):
                    columns.append(col)
        dataFrame = dataFrame.drop(columns=columns, axis=1)
        from ..forecaster import preprocess
        columns = dataFrame.columns
        dataFrame = preprocess.encode_cat(dataFrame=dataFrame)

        remove_column = []
        for col in columns:
            column = dataFrame.loc[:, dataFrame.columns.str.startswith(col)].select_dtypes(
                "object").columns.tolist()
            if len(column) != 0:
                remove_column.extend(column)
        dataFrame = dataFrame.drop(remove_column, axis=1)
        dataFrame = preprocess.auto(dataFrame=dataFrame)
        Xn = dataFrame.loc[:,dataFrame.columns != targetcol].values
        yn = dataFrame.loc[:,dataFrame.columns == targetcol].values
        scX = MinMaxScaler(feature_range=(0, 1))
        scY = MinMaxScaler(feature_range=(0, 1))
        X = scX.fit_transform(Xn)
        y = scY.fit_transform(yn.reshape(-1, 1))
        X_train, X_test, y_train, y_test = self.train_test_split(dataFrame=dataFrame,tX=X, tY=y, test_size=24, random_state=42)
        f_val, p_val = f_regression(X_train, y_train)
        f_val_dict = {}
        p_val_dict = {}
        for i in range(len(f_val)):
            if math.isnan(f_val[i]):
                f_val[i] = 0.0
            f_val_dict[i] = f_val[i]
            if math.isnan(p_val[i]):
                p_val[i] = 0.0
            p_val_dict[i] = p_val[i]

        sorted_f = sorted(f_val_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_p = sorted(p_val_dict.items(), key=operator.itemgetter(1), reverse=True)

        feature_indexs = []

        for i in range(0, n_features):
            feature_indexs.append(sorted_f[i][0])

        return dataFrame.iloc[:, 1:].iloc[:, feature_indexs].columns.tolist()

    def plb( self, col : str,  period : int , timelag : int,dataFrame:pd.DataFrame ):

        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")

        """
        df      : DataFrame
        col     : Columns
        period  : Period Number
        timelag : Lookback

        """
        dict = {"Values": [],
                "lag": []}
        for i in range(1, period + 1):
            dict["Values"].append(np.tile(dataFrame[:-timelag].iloc[-i * timelag][col], (dataFrame.shape[0], 1))[0])
            dict["lag"].append(i)
        data_l = pd.DataFrame(dict["Values"]).T
        data_l.columns = dict["lag"]
        dataFrame = pd.concat([dataFrame, data_l], axis=1)
        dataFrame.loc[:, dict["lag"]] = dataFrame.loc[:, dict["lag"]].ffill()
        return dataFrame

    def normalizeZeroValues(self,columns : str ,dataFrame : pd.DataFrame):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")


        columnsDate = ['Year', 'Month', 'Day', 'WeekofYear', 'DayofWeek', 'Hour', columns]
        for col in dataFrame.loc[:, (dataFrame == 0).any()].columns.tolist():
            if col not in columnsDate:
                dataFrame.loc[dataFrame[col] < 1, col] = np.nan
                dataFrame = dataFrame.groupby(dataFrame.index.date).transform(lambda x: x.fillna(x.mean()))
        return dataFrame


    def get_scaler(self,scaler):
        scalers = {
            "minmax": MinMaxScaler(),
            "standard": StandardScaler(),
            "maxabs": MaxAbsScaler(),
            "robust": RobustScaler(),
        }
        return scalers.get(scaler.lower())

    def inf_clean(self,dataFrame = None):
        if not isinstance(dataFrame, pd.DataFrame):
            raise ValueError("Must be dataframe.")
        return dataFrame.replace([np.inf, -np.inf], 0, inplace=True)


    def multivariate_data_create_dataset(self, dataset, target, start = 0 , window = 24, horizon = 1,end=None):
        X = []
        y = []
        start = start + window
        if end is None:
            end = len(dataset) - horizon
        for i in range(start, end):
            indices = range(i - window, i)
            X.append(dataset[indices])
            indicey = range(i + 1, i + 1 + horizon)
            y.append(target[indicey])
        X_data,y_data =  np.array(X), np.array(y)
        print('trainX shape == {}.'.format(X_data.shape))
        print('trainY shape == {}.'.format(y_data.shape))

        return X_data, y_data

    def unvariate_data_create_dataset(self, dataset, start=0, window = 24, horizon = 1,end = None):
        dataX = []
        dataY = []

        start = start + window
        if end is None:
          end = len(dataset) - horizon
        for i in range(start, end):
          indicesx = range(i-window, i)
          dataX.append(np.reshape(dataset[indicesx], (window, 1)))
          indicesy = range(i,i+horizon)
          dataY.append(dataset[indicesy])

        return np.array(dataX), np.array(dataY)


    def replace(self, to_replace, value, columns=None) -> pd.DataFrame:
        """
        Parameters:
            to_replace : numeric, str, list-like, dict, or None
                The value(s) to be replaced. It can be a single value, a list of values, a dictionary, or None.
                If None, the function will replace all occurrences of 'to_replace' with 'value' throughout the DataFrame.
            value : scalar, list-like, dict, or None
                The value(s) to replace 'to_replace' with. If 'to_replace' is a single value, 'value' can be a single value
                or a list of values of the same length. If 'to_replace' is a list-like or a dictionary, 'value' should also
                be a list-like or a dictionary with the same length (or matching keys in the case of a dictionary).
                If None, the function will replace 'to_replace' with NaN.
            columns : str or list-like, default None
                The column name(s) or index label(s) where the replacement should be performed. If None, the replacement
                will be applied to all columns in the DataFrame.

        Returns:
            pd.DataFrame
                A new DataFrame with the specified values replaced. If 'columns' is specified, only the selected columns
                will be replaced, otherwise, all columns will be replaced.
                The original DataFrame remains unchanged if 'columns' is None, otherwise, the selected columns will be modified.
        """
        replaced_df = self.dataFrame.copy()
        if columns is None:
            replaced_df.replace(to_replace=to_replace, value=value, inplace=True)
        else:
            replaced_df[columns] = replaced_df[columns].replace(to_replace=to_replace, value=value)
        return replaced_df


    def duplicated(self, columns: str = None) -> pd.DataFrame:
        """
        Parameters:
            columns : str or list-like, default None
                The column name(s) or index label(s) to consider for identifying duplicates.
                If None, all columns will be considered.

        Returns:
            pd.DataFrame
                A DataFrame indicating which rows are duplicates. If 'columns' is specified, the duplicates are checked
                based on the selected columns, otherwise, duplicates are checked across all columns.
        """
        if columns is None:
            return self.dataFrame.duplicated()
        else:
            return self.dataFrame[columns].duplicated()


    def join_dataframes(self, dataFrame: pd.DataFrame, index_col: str) -> pd.DataFrame:
        """
        Performs a join operation on two DataFrames based on the specified index column.
        Args:
            df1 (pd.DataFrame): The first DataFrame.
            df2 (pd.DataFrame): The second DataFrame.
            index_col (str): The index column to perform the join operation on.
        Returns:
            pd.DataFrame: The joined DataFrame.
        """
        return  self.dataFrame.set_index(index_col).join(dataFrame.set_index(index_col))

    def concatenateDataframes(self, dataFrame: pd.DataFrame, axis: int = 0, join: str = 'outer',
                              ignore_index: bool = True) -> pd.DataFrame:
        """
        Concatenates two Pandas DataFrames vertically (along the rows).

        Args:
            df1 (pd.DataFrame): First DataFrame.
            df2 (pd.DataFrame): Second DataFrame.
            axis (int, optional): Axis along which the DataFrames will be concatenated. Default is 0 (rows).
            join (str, optional): Type of join to perform if there are overlapping columns.
                Default is 'outer'. Possible values: {'outer', 'inner'}
            ignore_index (bool, optional): If True, ignore the original index values and reset the index of the concatenated DataFrame.
                Default is True.

        Returns:
            pd.DataFrame: Concatenated DataFrame.
        """
        concatenated_df = pd.concat([self.dataFrame, dataFrame], axis=axis, join=join, ignore_index=ignore_index)
        return concatenated_df

    def replaceSpaceWithUnderscoreInColumns(self) -> pd.DataFrame:

        """
        Replaces spaces in Column Names with "_" Edits
        Returns:
            pd.DataFrame
                A new list of column names with spaces replaced by underscores. The original DataFrame remains unchanged.
        """
        dataFrame.columns = [x.replace(" ", "_") for x in self.dataFrame.columns]
        return dataFrame

    def renameColumn(self, oldColumnName, newColumnName) -> pd.DataFrame:
        """
        Parameters:
            oldColumnName : str
                The current name of the column that needs to be renamed.
            newColumnName : str
                The new name to be assigned to the column.

        Returns:
            pd.DataFrame
                A new DataFrame with the column name renamed. The original DataFrame remains unchanged.
        """
        renamed_df = self.dataFrame.copy()
        renamed_df.rename(columns={oldColumnName: newColumnName}, inplace=True)
        return renamed_df

    def dublicateColumn(self, column: str) -> pd.DataFrame:
        """
        Creates a Duplicate of the Given Column
        Input: column (str) - The name of the column to be duplicated
        Output: pd.DataFrame - A new DataFrame with the duplicated column
        """
        colList = [x for x in self.dataFrame.columns if column in x]
        if column.rfind("_") == -1:
            colNumber = []
            colUnderscore = []
            for i in colList:
                if column + "_" in i:
                    colUnderscore.append(i)

            for i in colUnderscore:
                try:
                    idx = i.rfind("_")
                    number = int(i[idx + 1:])
                    colNumber.append(number)
                except:
                    pass
            if len(colNumber) > 0:
                self.dataFrame[column + "_" + str(max(colNumber) + 1)] = self.dataFrame[column]
                return self.dataFrame
            else:
                self.dataFrame[column + "_" + "2"] = self.dataFrame[column]
                return self.dataFrame
        else:
            colNumber = []
            for i in colList:
                if column in i:

                    try:
                        idx = i.rfind("_")
                        number = int(i[idx + 1:])
                        colNumber.append(number)
                    except:
                        pass
                else:
                    self.dataFrame[column + "_" + "2"] = self.dataFrame[column]
                    return self.dataFrame
            if len(colNumber) > 0:
                self.dataFrame[column + "_" + str(max(colNumber) + 1)] = self.dataFrame[column]
                return self.dataFrame
            else:
                self.dataFrame[column + "_" + "2"] = self.dataFrame[column]
                return self.dataFrame

    def dublicateScalarColumnWithAction(self, column: str, action: str = "exp") -> pd.DataFrame:
        """
        Creates a Duplicate of the Given Scalar Column Based on the Selected Action
        Inputs:
            column (str): The name of the scalar column to be duplicated.
            action (str): The selected action to be applied to the duplicated column. Options: 'abs', 'exp', 'floor'.
        Output: pd.DataFrame - A new DataFrame with the duplicated column based on the selected action.
		Examples : table.dublicateScalarColumnWithAction(column="USD_max",action="exp")
        """
        tempDataframe = self.dataFrame.copy()
        try:
            colList = [x for x in tempDataframe.columns if column in x]
            if column.rfind("_") == -1:
                colNumber = []
                colUnderscore = []
                for i in colList:
                    if column + "_" in i:
                        colUnderscore.append(i)

                for i in colUnderscore:
                    try:
                        idx = i.rfind("_")
                        number = int(i[idx + 1:])
                        colNumber.append(number)
                    except:
                        pass
                if len(colNumber) > 0:
                    if action == "abs":
                        tempDataframe[column + "_abs_" + str(max(colNumber) + 1)] = tempDataframe[column].abs()
                        return tempDataframe
                    elif action == "exp":
                        tempDataframe[column + "_exp_" + str(max(colNumber) + 1)] = tempDataframe[column].apply(
                            np.exp)
                        return tempDataframe
                    elif action == "floor":
                        tempDataframe[column + "_floor_" + str(max(colNumber) + 1)] = tempDataframe[column].apply(
                            np.floor)
                        return tempDataframe
                    else:
                        print("You can only choose abs, exp or floor")
                else:
                    if action == "abs":
                        tempDataframe[column + "_abs_" + "2"] = tempDataframe[column].abs()
                        return tempDataframe
                    elif action == "exp":
                        tempDataframe[column + "_exp_" + "2"] = tempDataframe[column].apply(np.exp)
                        return tempDataframe
                    elif action == "floor":
                        tempDataframe[column + "_floor_" + "2"] = tempDataframe[column].apply(np.floor)
                        return tempDataframe
                    else:
                        print("You can only choose abs, exp or floor")

            else:
                colNumber = []
                for i in colList:
                    if column in i:
                        try:
                            idx = i.rfind("_")
                            number = int(i[idx + 1:])
                            colNumber.append(number)
                        except:
                            pass

                if len(colNumber) > 0:
                    if action == "abs":
                        tempDataframe[column + "_abs_" + str(max(colNumber) + 1)] = tempDataframe[column].abs()
                        return tempDataframe
                    elif action == "exp":
                        tempDataframe[column + "_exp_" + str(max(colNumber) + 1)] = tempDataframe[column].apply(
                            np.exp)
                        return tempDataframe
                    elif action == "floor":
                        tempDataframe[column + "_floor_" + str(max(colNumber) + 1)] = tempDataframe[column].apply(
                            np.floor)
                        return tempDataframe
                    else:
                        print("You can only choose abs, exp or floor")
                else:
                    if action == "abs":
                        tempDataframe[column + "_abs_" + "2"] = tempDataframe[column].abs()
                        return tempDataframe
                    elif action == "exp":
                        tempDataframe[column + "_exp_" + "2"] = tempDataframe[column].apply(np.exp)
                        return tempDataframe
                    elif action == "floor":
                        tempDataframe[column + "_floor_" + "2"] = tempDataframe[column].apply(np.floor)
                        return tempDataframe
                    else:
                        print("You can only choose abs, exp or floor")

        except TypeError:
            print("Column Type Must Be Scalar")

    def dublicateStringColumnWithAction(self, column: str, action: str = "l") -> pd.DataFrame:
        """
        Creates a Duplicate of the Given String Column Based on the Selected Action
        Inputs:
            column (str): The name of the string column to be duplicated.
            action (str): The selected action to be applied to the duplicated column. Options: 'l' (toLower), 'u' (toUpper).
        Output: pd.DataFrame - A new DataFrame with the duplicated column based on the selected action.
	    Examples : table.dataFrame["String_value"]="aaaa"
				   table.dublicateStringColumnWithAction(column="String_value",action="u")
        """
        try:
            colList = [x for x in self.dataFrame.columns if column in x]
            if column.rfind("_") == -1:
                colNumber = []
                colUnderscore = []
                for i in colList:
                    if column + "_" in i:
                        colUnderscore.append(i)

                for i in colUnderscore:
                    try:
                        idx = i.rfind("_")
                        number = int(i[idx + 1:])
                        colNumber.append(number)
                    except:
                        pass
                if len(colNumber) > 0:
                    if action == "l":
                        self.dataFrame[column + "_lower_case_" + str(max(colNumber) + 1)] = self.dataFrame[
                            column].str.lower()
                        return self.dataFrame
                    elif action == "u":
                        self.dataFrame[column + "_upper_case_" + str(max(colNumber) + 1)] = self.dataFrame[
                            column].str.upper()
                        return self.dataFrame
                    else:
                        print("You can only choose l or u ( l = toLower, u = toUpper )")
                else:
                    if action == "l":
                        self.dataFrame[column + "_lower_case_" + "2"] = self.dataFrame[column].str.lower()
                        return self.dataFrame
                    elif action == "u":
                        self.dataFrame[column + "_upper_case_" + "2"] = self.dataFrame[column].str.upper()
                        return self.dataFrame

                    else:
                        print("You can only choose l or u ( l = toLower, u = toUpper )")

            else:
                colNumber = []
                for i in colList:
                    if column in i:
                        try:
                            idx = i.rfind("_")
                            number = int(i[idx + 1:])
                            colNumber.append(number)
                        except:
                            pass

                if len(colNumber) > 0:
                    if action == "l":
                        self.dataFrame[column + "_lower_case_" + str(max(colNumber) + 1)] = self.dataFrame[
                            column].str.lower()
                        return self.dataFrame
                    elif action == "u":
                        self.dataFrame[column + "_upper_case_" + str(max(colNumber) + 1)] = self.dataFrame[
                            column].str.upper()
                        return self.dataFrame
                    else:
                        print("You can choose only abs, exp or floor")
                else:
                    if action == "l":
                        self.dataFrame[column + "_lower_case_" + "2"] = self.dataFrame[column].str.lower()
                        return self.dataFrame
                    elif action == "u":
                        self.dataFrame[column + "_upper_case_" + "2"] = self.dataFrame[column].str.upper()
                        return self.dataFrame
                    else:
                        print("You can only choose  l or u ( l = toLower, u = toUpper )")

        except TypeError:
            print("Column Type Must Be Scalar")

    def apply(self, function_string: str, columns: str = None) -> pd.DataFrame:
        """
            Applies a custom function to the specified columns of the DataFrame.
            Inputs:
                function_string (str): A string representation of the function to be applied. The function should take a single argument 'x'.
                columns (list or None): Optional. A list of column names to apply the function to. If None, the function will be applied to all columns.
            Output:
                pd.DataFrame: A new DataFrame with the applied function results.

			Examples : apply(columns=["Salecount", "Net"],function_string="x**2")
        """
        func = eval(f"lambda x: {function_string}")
        dataFrame = self.dataFrame.copy()
        dataFrame[columns] = dataFrame[columns].apply(func)
        return dataFrame

    def dropColumns(self, columns: str = None) -> pd.DataFrame:
        """
            Drops the selected columns from the DataFrame.
            Inputs:
                columns (list or None): Optional. A list of column names to be dropped. If None, a ValueError will be raised.
            Output:
                pd.DataFrame: The modified DataFrame after dropping the specified columns.
        """
        #Removes selected columns from the datatable
        if columns is not None:
            return self.dataFrame.drop(columns=columns)
        else:
            raise HandleException(error_type="missing_value",
                                  error_message="Missing columns. Please provide column names to be dropped.")

    def orderData(self, columns: str, asc=None) -> pd.DataFrame:
        """
        Orders the DataFrame by multiple columns.
        Input:
            columns (list): The columns to order the DataFrame by.
            asc (list, optional): The sorting direction for each column. If None, default to ascending order.
        Output:
            pd.DataFrame: The ordered DataFrame.
        """
        if asc is not None:
            if len(asc) != len(columns):
                raise HandleException(error_type="length_mismatch",
                                      error_message="asc and columns need to be same length.")
        else:
            asc = [True] * len(columns)
        return self.dataFrame.sort_values(by=columns, ascending=asc)

    def query(self, expr: str) -> pd.DataFrame:
        """
        Filters the DataFrame based on the specified query expression.
        Input:
            expr (str): The query expression to filter the DataFrame.
        Output:
            pd.DataFrame: The filtered DataFrame.

	    Examples =  query(expr="Year>2019 &  Net>5000")
        """
        renamed_df = self.dataFrame.copy()
        renamed_df = renamed_df.query(expr).dropna()
        return renamed_df

    def dynamic_join(self, dataFrame: pd.DataFrame, join_cols: list) -> pd.DataFrame:
        """
        Performs dynamic join operations between two DataFrames based on the specified join columns.
        Args:
            dataFrame (pd.DataFrame): The second DataFrame.
            join_cols (list): The list of join columns to perform the join operations on.
        Returns:
            pd.DataFrame: The merged DataFrame.
        """
        for col in join_cols:
            merged_df = dataFrame.join(self.dataFrame.set_index([col]), on=[col])
        return merged_df


    def getTimeRelated(self):
        def is_date(string):
            try:
                pd.to_datetime(string)
                return True
            except ValueError:
                return False

        time_columns = []
        for column in self.dataFrame.columns:
            if self.dataFrame[column].dtype == object:
                non_null_values = self.dataFrame[column].dropna()
                if non_null_values.sample(frac=0.01, random_state=42).apply(
                        is_date).mean() > 0.9:  # Adjust the threshold as needed
                    time_columns.append(column)

        return time_columns



    def getStatistics(self,columns : Union[list]) -> json:
        """
        Computes descriptive statistics for the specified columns.
        Parameters:
            columns (list): A list of column names to compute statistics for.
        Returns:
            dict: A dictionary containing the computed statistics for each column.
        """
        data = dict()
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)

        if not isinstance(columns,list):
            raise HandleException(error_type="list_value_error")

        else:
            try:
                check_string_values(self.dataFrame[columns], columns)
            except:
                logger.error(" String or NaN value found in column ")
                #columns = self.dataFrame.select_dtypes(include="number")
            for col in columns:
                column_stats={}
                column_stats["Mean"] = self.getMean([col])
                column_stats["Std"] = self.getStd([col])
                column_stats["Median"] = self.getMedian([col])
                column_stats["Kurtosis"] = self.getKurtosis([col])
                column_stats["Skewnes"] = self.getSkewness([col])
                column_stats["Q1"] = self.getQ1([col])
                column_stats["Q2"] = self.getQ2([col])
                column_stats["Q3"] = self.getQ3([col])
                data[col]=column_stats
            return  data


    def checkNullColumns(self,columns) -> Any:
        """
        Checks if there are any null values in the specified columns.
        Parameters:
            columns (list): A list of column names to check for null values.
        Returns:
            Any: True if there are null values, False otherwise.
        """
        return self.dataFrame[columns].apply(lambda x: x.isnull().any())

    def getNullsInColumns(self, columns) -> pd.DataFrame:
        """
        Retrieves the null values in the specified columns.
        Parameters:
            columns (list): A list of column names to retrieve null values.
        Returns:
            pd.DataFrame: A DataFrame containing True for null values and False for non-null values in the specified columns.
        """
        return self.dataFrame[columns].apply(lambda x: x.isnull())


    def groupByOperations(self,group_cols, agg_cols):
        """
        Groups a DataFrame based on specified columns and performs operations on selected columns.

        Parameters:
        - group_cols: list - A list of column names to group by.
        - agg_cols: dict - A dictionary specifying the columns to perform operations on and the operations to apply.
        'sum','mean','median','min','max','count','std','var','prod','first','last','size','idxmax','idxmin','nunique',
        'cumsum','cumprod','describe','quantile','skew','kurt','sem','mode','any','all','mad','pct_change','diff','rank',
        'cov','corr','zscore'
        Example: {'Column1': ['sum', 'mean'], 'Column2': 'max'}

        Returns:
        - grouped_df: DataFrame - The resulting DataFrame after the groupby and aggregation operations.

        Example :
        data = {
            'Group1': ['A', 'A', 'B', 'B', 'A', 'B'],
            'Group2': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
            'Column1': [10, 20, 30, 40, 50, 60],
            'Column2': [100, 200, 300, 400, 500, 600]
        }
        df = pd.DataFrame(data)

        # Perform the grouping operation
        group_cols = ['Group1', 'Group2']
        agg_cols = {'Column1': ['sum', 'mean'], 'Column2': 'max'}

        grouped_df = groupby_operations(df, group_cols, agg_cols)
        print(grouped_df)
        """

        grouped_df = self.dataFrame.groupby(group_cols).agg(agg_cols)

        if isinstance(grouped_df.columns, pd.MultiIndex):
            grouped_df.columns = [f'{col}_{op}' for col, op in grouped_df.columns]
        else:
            grouped_df.columns = [f'{col}_{agg_cols[col]}' if col in agg_cols else col for col in grouped_df.columns]

        grouped_df.reset_index(inplace=True)
        return grouped_df

    def getCov(self, columns) -> pd.DataFrame:
        """
        Computes the covariance matrix for the specified columns.
        Parameters:
            columns (list): A list of column names to compute the covariance matrix.
        Returns:
            pd.DataFrame: The covariance matrix of the specified columns.
        """
        return self.dataFrame[columns].cov()

    def getSampleByNumber(self, n: int, columns, weights=None, replace=False)-> pd.DataFrame:
        """
        Retrieves a random sample of rows from the DataFrame by specifying the number of samples.
        Parameters:
            n (int): The number of samples to retrieve.
            columns (list): A list of column names to include in the sample.
            weights (array-like, optional): An optional array of weights associated with each row. Default is None.
            replace (bool, optional): Whether sampling is done with replacement. Default is False.
        Returns:
            pd.DataFrame: A random sample of rows from the DataFrame.
        """
        if weights is not None:
            if len(weights) != len(self[self.dataFrame.columns[0]]):
                raise HandleException(error_type="generic_value_error",error_message="Weight array must be the same length with dataframe rows number.")
        return self.dataFrame[columns].sample(n=n, weights=weights, replace=replace)

    def getSampleWithFrac(self, frac, columns, weights=None, replace=False)-> pd.DataFrame:
        """
        Retrieves a random sample of rows from the DataFrame by specifying the fraction of samples.
        Parameters:
            frac (float): The fraction of samples to retrieve. Should be between 0 and 1.
            columns (list): A list of column names to include in the sample.
            weights (array-like, optional): An optional array of weights associated with each row. Default is None.
            replace (bool, optional): Whether sampling is done with replacement. Default is False.
        Returns:
            pd.DataFrame: A random sample of rows from the DataFrame.
        """
        if weights is not None:
            if len(weights) != len(self.dataFrame[self.dataFrame.columns[0]]):
                raise HandleException(error_type="generic_value_error",error_message="Weight array must be the same length with dataframe rows number.")
        return self.dataFrame[columns].sample(frac=frac, weights=weights, replace=replace)

    def findValues(self, values: Union[int, List[int]], columns) -> Union[Dict[str, List[int]], None]:
        """
        Finds the indices of specified values in the specified columns.
        Parameters:
            values (int or list): The value or values to find.
            columns (list): A list of column names to search for the values.
        Returns:
            dict or None: A dictionary mapping each column name to a list of indices where the values are found.
        """
        if isinstance(values, int):
            values = [values]
        indices = {col: self.dataFrame[self.dataFrame[col].eq(values[0])].index.tolist() for col in columns}
        return indices

    ####test edilecek. #####
    def filterValue(self, columns: List[str], value, action="equal") -> pd.DataFrame:
        """
        Filters the DataFrame based on specified column(s) and value(s) using a comparison action.
        Parameters:
            columns (list): A list of column names to filter.
            value: The value to compare against.
            action (str, optional): The comparison action to perform. Options: 'equal', 'in', 'notEqual'. Default is 'equal'.
        Returns:
            pd.DataFrame: The filtered DataFrame based on the specified conditions.
        """
        if isinstance(value, int):
            return self._filterValueForScalar(value, columns, action)
        elif isinstance(value, str):
            return self._filterValueForString(columns, value, action)
        else:
            raise ValueError("Invalid value type. Must be int or str.")

    def _filterValueForScalar(self, value: int, columns: List[str], action="==") -> pd.DataFrame:
        """
        Filters the DataFrame based on specified column(s) and scalar value(s) using a comparison action.
        Parameters:
            value (int): The scalar value to compare against.
            columns (list): A list of column names to filter.
            action (str, optional): The comparison action to perform. Default is '=='.
        Returns:
            pd.DataFrame: The filtered DataFrame based on the specified conditions.
        """
        if isinstance(columns, str):
            columns = [columns]
        value = str(value)
        query_str = " & ".join(f"{col} {action} {value}" for col in columns)
        return self.dataFrame.query(query_str)

    def _filterValueForString(self, columns: List[str], value: str, action="equal") -> pd.DataFrame:
        """
        Filters the DataFrame based on specified column(s) and string value(s) using a comparison action.
        Parameters:
            columns (list): A list of column names to filter.
            value (str): The string value to compare against.
            action (str, optional): The comparison action to perform. Options: 'equal', 'in', 'notEqual'. Default is 'equal'.
        Returns:
            pd.DataFrame: The filtered DataFrame based on the specified conditions.
        """
        if action == "equal":
            return self.dataFrame[self.dataFrame[columns].apply(lambda x: x == value).any(axis=1)]
        elif action == "in":
            return self.dataFrame[self.dataFrame[columns].apply(lambda x: x.str.contains(value, na=False)).any(axis=1)]
        elif action == "notEqual":
            return self.dataFrame[self.dataFrame[columns].apply(lambda x: x != value).any(axis=1)]
        else:
            raise ValueError("Invalid action. Must be 'equal', 'in', or 'notEqual'.")







