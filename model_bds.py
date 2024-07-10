import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class PricePredictor:
    def __init__(self):
        self.model = Pipeline(steps=[
            ('preprocessor', self._create_preprocessor()),
            ('regressor', LinearRegression())
        ])

    def _prepare_data(self, data_path):
        df = pd.read_csv(data_path)
        df = df[["area_value", "price_per_m2_final", "district", "city", "type"]]
        df = df.dropna()

        X = df.drop('price_per_m2_final', axis=1)
        y = df['price_per_m2_final']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        return X_train, X_test, y_train, y_test

    def _create_preprocessor(self):
        numeric_features = ['area_value']
        categorical_features = ['district', 'city', 'type']

        numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
        categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])

        return preprocessor

    def train_model(self, data_path):
        X_train, X_test, y_train, y_test = self._prepare_data(data_path)

        self.model.fit(X_train, y_train)

        score = self.model.score(X_test, y_test)
        print(f'R^2 Score: {score}')

    def save_model(self, model_path):
        with open(model_path, 'wb') as file:
            pickle.dump(self.model, file)

if __name__ == "__main__":
    predictor = PricePredictor()
    data_path = "data_bds/all_bds_clean.csv"
    model_path = 'model/model.pkl'
    predictor.train_model(data_path)
    predictor.save_model(model_path)
