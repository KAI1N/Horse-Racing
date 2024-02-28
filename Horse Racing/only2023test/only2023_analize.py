from sklearn.model_selection import train_test_split
import lightgbm as lgb
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

data=pd.read_csv('2023_processed_data.csv')
features = ['length','out_length','age','e_weight','h_weight','weight_change','小雨','小雪','晴','曇','雨','雪','ダ','芝','不良','稍重','良','重','右','左','直','セ','牝','牡']
target = 'odds'

data['length'] = data['length'].astype(int)
data['age'] = data['age'].astype(int)
data['e_weight'] = data['e_weight'].astype(float)
data['h_weight'] = data['h_weight'].astype(float)
data['weight_change'] = data['weight_change'].astype(float)
data['odds'] = data['odds'].astype(float)
# 指定された特徴量とターゲット変数でデータフレームをフィルタリング
data=data.dropna()
X = data[features]
y = data[target]

# データセットの分割（訓練セット80%、テストセット20%）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LightGBM用のデータセットを作成
train_data = lgb.Dataset(X_train, label=y_train, categorical_feature=features)
test_data = lgb.Dataset(X_test, label=y_test, categorical_feature=features, reference=train_data)

# LightGBMのパラメータ
params = {
    'objective': 'regression',
    'metric': 'rmse',
    'boosting_type': 'gbdt',
    'learning_rate': 0.1,
    'num_leaves': 31,
    'max_depth': -1,
    'min_child_samples': 20,
    'max_bin': 255,
    'subsample': 0.6,
    'subsample_freq': 1,
    'colsample_bytree': 0.7,
    'min_child_weight': 0.001,
    'subsample_for_bin': 200000,
    'min_split_gain': 0,
    'reg_alpha': 0,
    'reg_lambda': 0,
    'nthread': -1,
    'verbose': 0,
}

# モデルの訓練
gbm = lgb.train(params,
                train_data,
                valid_sets=[test_data],
                num_boost_round=1000,
                categorical_feature=features)

# テストデータでの予測
y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)

y_test=y_test.dropna()
# 評価指標の計算
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)  # RMSEはMSEの平方根
r2 = r2_score(y_test, y_pred)

# 評価指標の表示
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R²): {r2:.2f}")
