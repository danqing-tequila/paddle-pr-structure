import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler, KBinsDiscretizer
from sklearn.decomposition import PCA

# 假设有一个DataFrame数据df

# 1. 数据预处理举例：时间戳拆分，缺失值填补，异常值处理
def preprocess_data(df):
    # 时间戳拆分
    if 'timestamp' in df.columns:
        df['year'] = pd.to_datetime(df['timestamp']).dt.year
        df['month'] = pd.to_datetime(df['timestamp']).dt.month
        df['day'] = pd.to_datetime(df['timestamp']).dt.day
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour

    # 缺失值填充（数值型用中位数）
    for col in df.select_dtypes(include=[np.number]).columns:
        median = df[col].median()
        df[col].fillna(median, inplace=True)

    # 处理异常值（简单Example: clip到上下1%和99%分位）
    for col in df.select_dtypes(include=[np.number]).columns:
        low = df[col].quantile(0.01)
        high = df[col].quantile(0.99)
        df[col] = df[col].clip(lower=low, upper=high)

    return df

# 2. 类别变量处理：独热编码 (One-Hot)
def encode_categorical(df, categorical_cols):
    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    transformed = ohe.fit_transform(df[categorical_cols])
    ohe_df = pd.DataFrame(transformed, columns=ohe.get_feature_names_out(categorical_cols))
    df = df.drop(columns=categorical_cols).reset_index(drop=True)
    df = pd.concat([df, ohe_df], axis=1)
    return df

# 3. 数值变量处理：分箱和标准化
def process_numeric(df, numeric_cols):
    # 分箱
    kbins = KBinsDiscretizer(n_bins=5, encode='onehot-dense', strategy='quantile')
    binned = kbins.fit_transform(df[numeric_cols])
    binned_df = pd.DataFrame(binned, columns=[f"{col}_bin{i}" for col in numeric_cols for i in range(binned.shape[1]//len(numeric_cols))])

    # 标准化（针对原数值列）
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[numeric_cols])
    scaled_df = pd.DataFrame(scaled, columns=[f"{col}_scaled" for col in numeric_cols])

    df = df.drop(columns=numeric_cols).reset_index(drop=True)
    df = pd.concat([df, binned_df, scaled_df], axis=1)
    return df

# 4. 交叉特征构造：两个类别变量生成组合特征
def cross_features(df, col1, col2):
    cross_col = df[col1].astype(str) + "_" + df[col2].astype(str)
    df[f"{col1}_{col2}_cross"] = cross_col
    return df

# 5. 特征选择和降维示例（PCA降维）
def reduce_features(df, n_components=5):
    pca = PCA(n_components=n_components)
    reduced = pca.fit_transform(df)
    reduced_df = pd.DataFrame(reduced, columns=[f"PCA_{i+1}" for i in range(n_components)])
    return reduced_df

# 6. 关键词归类示例（规则匹配+词典映射）
keywords_map = {
    '类别A': ['关键词1', '关键词2', '关键词3'],
    '类别B': ['关键词4', '关键词5']
}

def categorize_text(text):
    text = text.lower()
    for category, keywords in keywords_map.items():
        for kw in keywords:
            if kw in text:
                return category
    return '其他'

# 示例使用
if __name__ == '__main__':
    df = pd.DataFrame({
        'timestamp': ['2023-01-01 12:00:00', '2023-06-15 08:30:00'],
        'cat1': ['A', 'B'],
        'cat2': ['X', 'Y'],
        'num1': [1.5, 2.3],
        'num2': [100, 150],
        'text': ['这是关键词1的案例', '包含关键词5内容']
    })

    df = preprocess_data(df)
    df = encode_categorical(df, ['cat1', 'cat2'])
    df = process_numeric(df, ['num1', 'num2'])
    df = cross_features(df, 'cat1', 'cat2')

    # 用PCA简化所有数值和编码列（不含文本）
    numeric_features = df.select_dtypes(include=[np.number])
    pca_df = reduce_features(numeric_features)

    # 把PCA结果与原文本合并
    df = df.reset_index(drop=True)
    df = pd.concat([df[['text']], pca_df], axis=1)

    # 多关键词归类示例
    df['category'] = df['text'].apply(categorize_text)

    print(df)
