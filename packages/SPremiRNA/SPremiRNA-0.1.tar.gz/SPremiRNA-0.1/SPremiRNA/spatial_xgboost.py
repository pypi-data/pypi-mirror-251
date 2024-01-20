import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor

import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
from time import time



# 使用 StandardScaler 进行 z-score 标准化
def standard(mrna, mirna):
    scaler = MinMaxScaler()
    mrna_scale = scaler.fit_transform(mrna)

    # # 使用 StandardScaler 进行 z-score 标准化
    scaler = MinMaxScaler()
    mirna_scale = scaler.fit_transform(mirna)

    mrna = pd.DataFrame(mrna_scale, columns=mrna.columns)
    mirna = pd.DataFrame(mirna_scale, columns=mirna.columns)
    return mrna, mirna


# 划分训练集和测试集
def SplitData(mrna, mirna, split_size):
    x_train, x_test, y_train, y_test = train_test_split(mrna, mirna, test_size=split_size)
    return x_train, x_test, y_train, y_test


def Build_Model(lr, n_estimators=100, max_depth=3):
    other_params = {'learning_rate': lr, 'n_estimators': n_estimators, 'max_depth': max_depth, 'min_child_weight': 1,
                    'seed': 0,
                    'subsample': 0.3, 'colsample_bytree': 0.3, 'gamma': 0, 'reg_alpha': 1, 'reg_lambda': 1}

    # 建立XGBoost模型
    model = XGBRegressor(**other_params, tree_method="hist", device="cuda")
    return model


def Train_Model(model, x_train, y_train,x_test,y_test,cancer,outdir):
    t0 = time()
    # 训练模型
    model.fit(x_train, y_train)
    print(f"XGBoost fit done in {(time() - t0):.3f}s")
    y_ = model.predict(x_train)
    Fit_visual(y_train, y_, outdir,type="Train", cancer_type=cancer, color="lightblue")

    # 使用模型进行预测
    predictions = model.predict(x_test)
    Fit_visual(y_test, predictions, outdir,type="Test", cancer_type=cancer, color="lightgreen")
    # r2_score_xgb = r2_score(y_test, predictions)
    # print(f"XGBoost r^2 on test data : {r2_score_xgb:.3f}")


"""
输出观测值和模型预测值之间的拟合曲线,即拟合模型
决定系数R2，有拟合曲线公式，有1:1线
注意：R2、RMSE是预测和实测计算的，即原来的反演或预测模型的值。拟合曲线模型是预测和实测重新计算的拟合曲线。
"""


def Fit_visual(true, predict, outdir,type,cancer_type, color):
    # x: 是观测值; y: 是模型预测值
    x = true.values.flatten()
    y = predict.flatten()

    fig, ax = plt.subplots(figsize=(7, 7), dpi=300)
    # 绘制1:1对角线，linewidth线的粗细，ls线的格式，c线的颜色，
    ax.plot((0, 1), (0, 1), linewidth=1, transform=ax.transAxes, ls='--', c='k', label="1:1 line", alpha=0.5)
    # 绘制点，'o'点的形状，点的颜色，markersize点的大小
    ax.plot(x, y, 'o', c=color, markersize=1)

    # polyfit(x, y, 1)，1代表线性拟合
    # parameter返回的是线性拟合线的斜率和截距
    parameter = np.polyfit(x, y, 1)
    f = np.poly1d(parameter)
    ax.plot(x, f(x), 'r-', lw=1)

    # 计算决定系数R
    r2 = r2_score(x, y)
    print(r2)

    # 那个框框的设置
    bbox = dict(boxstyle="round", fc='1', alpha=0.)
    bbox = bbox
    # 在图上安放R2和拟合曲线公式，0.05和0.87是位置偏移量，自己调试
    plt.text(0.05, 0.87, "$R^2=%.2f$\n$y=%.2fx+%.2f$" % ((r2), parameter[0], parameter[1]),
             transform=ax.transAxes, size=7, bbox=bbox)

    # 横轴的设置
    ax.set_xlabel('True values', fontsize=7)
    ax.set_ylabel("Predicted values", fontsize=7)

    # 设置图片title
    ax.tick_params(labelsize=7)
    ax.set_title("%s %s True Values vs Predictions" % (cancer_type, type), fontsize=7)

    x_major_locator = MultipleLocator(1)
    ax.xaxis.set_major_locator(x_major_locator)
    y_major_locator = MultipleLocator(1)
    ax.yaxis.set_major_locator(y_major_locator)
    # 坐标轴
    ax.set(xlim=(0, 1.2), ylim=(0, 1.2))

    plt.savefig(outdir+ "%s %s True vs Pre.jpg" % (cancer_type, type))
    plt.show()
