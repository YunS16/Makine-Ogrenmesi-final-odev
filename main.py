import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# 1) oku
df = pd.read_csv("Smart Home Dataset.csv", low_memory=False)

# 2) time temizle 
df["time"] = pd.to_numeric(df["time"], errors="coerce")
df = df.dropna(subset=["time"])

# 3) datetime + hour
df["datetime"] = pd.to_datetime(df["time"], unit="s", utc=True)
df["hour"] = df["datetime"].dt.hour

# 4) numeric kolonlar
weather_columns = [
    "temperature", "humidity", "visibility", "windSpeed", "pressure",
    "cloudCover", "windBearing", "dewPoint", "precipProbability"
]
for col in weather_columns + ["use [kW]"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# sadece gerçekten lazım olanlarda NaN at
df = df.dropna(subset=["use [kW]", "temperature", "humidity", "windSpeed", "summary"])

# 5) label encode (summary)
le = LabelEncoder()
df["summary_encoded"] = le.fit_transform(df["summary"].astype(str))

# 6) pivot baseline (saat/sıcaklık/nem/rüzgar)
pivot_hour = df.pivot_table(index="hour", values="use [kW]", aggfunc="mean")
pivot_hour.columns = ["hourAvg"]

pivot_temp = df.pivot_table(index="temperature", values="use [kW]", aggfunc="mean")
pivot_temp.columns = ["temperatureAvg"]

pivot_humid = df.pivot_table(index="humidity", values="use [kW]", aggfunc="mean")
pivot_humid.columns = ["humidityAvg"]

pivot_wind = df.pivot_table(index="windSpeed", values="use [kW]", aggfunc="mean")
pivot_wind.columns = ["windSpeedAvg"]

df = df.merge(pivot_hour, on="hour", how="left")
df = df.merge(pivot_temp, on="temperature", how="left")
df = df.merge(pivot_humid, on="humidity", how="left")
df = df.merge(pivot_wind, on="windSpeed", how="left")

# 7) hedef: tüketim ortalamanın üstü mü? (0/1)
y = (df["use [kW]"] > df["use [kW]"].mean()).astype(int)

# 8) features
features = [
    "hour", "summary_encoded",
    "temperature", "humidity", "visibility", "windSpeed",
    "pressure", "cloudCover", "windBearing", "dewPoint", "precipProbability",
    "hourAvg", "temperatureAvg", "humidityAvg", "windSpeedAvg"
]

X = df[features].fillna(0)

# 9) scale
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 10) split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 11) modeller
models = {
    "Logistic Regression": LogisticRegression(max_iter=7000),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Random Forest": RandomForestClassifier(n_estimators=120, random_state=42),
}

for name, model in models.items():
    print(f"\n{name} eğitiliyor...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Sonuç: %{acc*100:.2f}")
    print(classification_report(y_test, y_pred))

# 12) feature importance (RF)
rf_model = models["Random Forest"]
fi_df = pd.DataFrame({
    "Feature": features,
    "Importance": rf_model.feature_importances_
}).sort_values(by="Importance", ascending=False)

plt.figure(figsize=(12, 8))
sns.barplot(x="Importance", y="Feature", data=fi_df)
plt.title("Feature Importance Scores")
plt.tight_layout()
plt.savefig("ImportanceG.png", dpi=250)
plt.show()

# 13) pivotları da kaydet (
pivot_hour.to_csv("pivot_hour.csv")
pivot_temp.to_csv("pivot_temperature.csv")
pivot_humid.to_csv("pivot_humidity.csv")
pivot_wind.to_csv("pivot_windspeed.csv")

print("\nBasarili")
