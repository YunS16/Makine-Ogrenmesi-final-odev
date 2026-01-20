import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 1) oku
df = pd.read_csv("Smart Home Dataset.csv", low_memory=False)

# 2) time -> hour
df["time"] = pd.to_numeric(df["time"], errors="coerce")
df.dropna(subset=["time"], inplace=True)

df["dt"] = pd.to_datetime(df["time"], unit="s")
df["hour"] = df["dt"].dt.hour

# 3) lazım olan kolonları sayısal yap
for c in ["use [kW]", "temperature", "humidity", "windSpeed", "pressure"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df.dropna(subset=["use [kW]", "temperature", "humidity", "windSpeed", "pressure", "summary"], inplace=True)

# 4) summary encode
le = LabelEncoder()
df["summary_enc"] = le.fit_transform(df["summary"].astype(str))

# 5) PIVOT 1: saat bazlı normal tüketim
p_hour = df.pivot_table(values="use [kW]", index="hour", aggfunc="mean")
p_hour.columns = ["base_hour"]
df = df.merge(p_hour, on="hour", how="left")

# 6) PIVOT 2: sıcaklık bazlı normal tüketim
p_temp = df.pivot_table(values="use [kW]", index="temperature", aggfunc="mean")
p_temp.columns = ["base_temp"]
df = df.merge(p_temp, on="temperature", how="left")

# 7) hedef 0/1 (ortalamanın üstü mü?)
y = (df["use [kW]"] > df["use [kW]"].mean()).astype(int)

# 8) X
features = ["hour", "temperature", "humidity", "windSpeed", "pressure", "summary_enc", "base_hour", "base_temp"]
X = df[features].fillna(0)

# 9) split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 10) Random Forest 
rf = RandomForestClassifier(n_estimators=120, random_state=42)
rf.fit(X_train, y_train)
rf_acc = accuracy_score(y_test, rf.predict(X_test))

# 11) KNN 
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_s, y_train)
knn_acc = accuracy_score(y_test, knn.predict(X_test_s))


print(f"{'Model':<15} | {'Accuracy':<10}")
print("-" * 30)
print(f"{'RandomForest':<15} | {rf_acc*100:<10.2f}")
print(f"{'KNN':<15} | {knn_acc*100:<10.2f}")

print("\n Bitti .RandomForest bu denemede KNN'den biraz daha iyi çikti.")

