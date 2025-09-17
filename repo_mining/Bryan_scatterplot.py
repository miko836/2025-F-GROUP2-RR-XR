import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import hashlib

# === Input CSV path ===
INPUT_CSV = r"C:\Users\pc\source\repos\2025-F-GROUP2-RR-XR-1\2025-F-GROUP2-RR-XR\data\file_rootbeer_authors.csv"

def author_to_color(author, cmap="tab10"):
    """Map author to a stable color index."""
    hash_val = int(hashlib.md5(author.encode()).hexdigest(), 16)
    return hash_val % 10  # colormap index

def main():
    # Load CSV
    df = pd.read_csv(INPUT_CSV)

    # Convert commit date → week number (numeric for plotting)
    df["week_num"] = pd.to_datetime(df["Date"]).dt.isocalendar().week
    df["year"] = pd.to_datetime(df["Date"]).dt.year
    df["weeks"] = (df["year"] - df["year"].min()) * 52 + df["week_num"]

    # Map files to integer indices
    file_to_idx = {f: i for i, f in enumerate(df["Filename"].unique())}
    df["file_idx"] = df["Filename"].map(file_to_idx)

    # Prepare arrays
    x = df["file_idx"].to_numpy()
    y = df["weeks"].to_numpy()
    c = df["Author"].map(lambda a: author_to_color(a)).to_numpy()

    # Scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, c=c, s=80, cmap="tab10")

    plt.xlabel("file")
    plt.ylabel("weeks")
    plt.title("File Touches by Authors Over Time")

    plt.show()

if __name__ == "__main__":
    main()
