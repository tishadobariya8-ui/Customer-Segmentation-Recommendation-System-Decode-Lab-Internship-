import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Load Dataset
df = pd.read_csv("data/customers.csv")

print("First 5 Records:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nMissing Values:")
print(df.isnull().sum())

# Features for clustering
X = df[["Annual Income (k$)", "Spending Score (1-100)"]]

print("\nFeatures Used:")
print(X.head())

wcss = []

for i in range(1, 11):
    kmeans = KMeans(
        n_clusters=i,
        init="k-means++",
        random_state=42
    )

    kmeans.fit(X)

    wcss.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss, marker="o")

plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")

plt.grid(True)

plt.savefig("elbow_method.png")
plt.show()

print("\nElbow graph saved!")

# Create KMeans Model
kmeans = KMeans(
    n_clusters=5,
    init="k-means++",
    random_state=42
)

# Fit Model
y_kmeans = kmeans.fit_predict(X)

# Add cluster labels to dataset
df["Cluster"] = y_kmeans

print("\nFirst 10 Customers with Cluster:")
print(
    df[
        [
            "CustomerID",
            "Annual Income (k$)",
            "Spending Score (1-100)",
            "Cluster"
        ]
    ].head(10)
)

plt.figure(figsize=(10, 7))

plt.scatter(
    X.iloc[:, 0],
    X.iloc[:, 1],
    c=y_kmeans
)

plt.scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    s=200,
    marker="X"
)

plt.title("Customer Segments")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score")

plt.savefig("customer_clusters.png")
plt.show()

print("\nCustomer Cluster Graph Saved!")

print("\nCustomers in Each Cluster:")
print(df["Cluster"].value_counts().sort_index())

print("\nCluster Summary:")

cluster_summary = df.groupby("Cluster")[
    ["Annual Income (k$)", "Spending Score (1-100)"]
].mean()

print(cluster_summary)

print("\nCustomer Recommendations:")

recommendations = {
    0: "Popular Products, Loyalty Rewards",
    1: "Luxury Products, VIP Membership",
    2: "Trending Products, Special Promotions",
    3: "Personalized Marketing, Premium Product Bundles",
    4: "Discount Coupons, Budget-Friendly Products"
}

for cluster, recommendation in recommendations.items():
    print(f"\nCluster {cluster}")
    print("Recommendation:", recommendation)

print(f"\nTotal Customers Analyzed: {len(df)}")

print("\nEnter Customer Details")

income = float(input("Enter Annual Income (k$): "))
spending = float(input("Enter Spending Score (1-100): "))

new_customer = pd.DataFrame(
    [[income, spending]],
    columns=["Annual Income (k$)", "Spending Score (1-100)"]
)

cluster = kmeans.predict(new_customer)[0]

print(f"\nCustomer belongs to Cluster {cluster}")

print("\nRecommended Items:")
print(recommendations[cluster])

print("\nProject Completed Successfully!")
