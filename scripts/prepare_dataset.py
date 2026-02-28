import pandas as pd
import os

# Load original dataset
file_path = "marketing_sample_for_walmart_com-walmart_com_product_review__20200701_20201231__5k_data.tsv"

df = pd.read_csv(file_path, sep="\t")

print("Original Columns:")
print(df.columns)

# Create clean dataframe
clean_df = pd.DataFrame()

# Map correct columns
clean_df["name"] = df["Product Name"]
clean_df["brand"] = df["Product Brand"]
clean_df["category"] = df["Product Category"]
clean_df["description"] = df["Product Description"]
clean_df["image_url"] = df["Product Image Url"]

# Convert numeric safely FIRST
clean_df["rating"] = pd.to_numeric(df["Product Rating"], errors="coerce")
clean_df["review_count"] = pd.to_numeric(df["Product Reviews Count"], errors="coerce")

# Fill text columns with empty string
text_columns = ["name", "brand", "category", "description", "image_url"]
clean_df[text_columns] = clean_df[text_columns].fillna("")

# Fill numeric columns with 0
clean_df["rating"] = clean_df["rating"].fillna(0)
clean_df["review_count"] = clean_df["review_count"].fillna(0)

# Remove duplicates
clean_df.drop_duplicates(subset=["name"], inplace=True)

# Optional limit
clean_df = clean_df.head(2000)

# Create data folder
os.makedirs("data", exist_ok=True)

# Save clean CSV
clean_df.to_csv("data/products.csv", index=False)

print("Clean products.csv created successfully!")