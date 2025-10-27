import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
try:
    from IPython.display import display
except Exception:
    # Fallback for non-notebook environments
    def display(x): 
        print(x)

def perform_eda(df, target_column=None):
    '''
    This function performs the EDA for the different datasets using the same parameters.
    1. Dataset Overview
    2. Shape
    3. Missing values
    4. Duplicated values
    5. Boxplots, one per numeric feature
    6. Unique values per column, including an all unique check
    7. Features types
    8. Descriptive analytics
    9. Target variable distribution, when the target_column parameter is used
    10. Histograms for numeric features
    11. Categorical features count
    12. Correlation heatmap
    '''
    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(include='object').columns
    
    print("Dataset Overview:")
    display(df.head())
    
    print("Shape:", df.shape)
    
    print("Missing Values:")
    display(df.isnull().sum())

    print("Duplicated Rows (beyond first):", int(df.duplicated().sum()))

    # Show all rows that belong to duplicate groups including a sample
    dups_all = df[df.duplicated(keep=False)].copy()

    if dups_all.empty:
        print("No duplicate rows found.")
    else:
        # Sorting so identical rows appear together
        dups_all = dups_all.sort_values(list(df.columns))
        print("All rows in duplicate groups (showing first 10):")
        display(dups_all.head(10))

    # Exact rows and how many times
    #     dup_patterns = (
    #         dups_all.groupby(list(df.columns), dropna=False)
    #                 .size().reset_index(name="count")
    #                 .sort_values("count", ascending=False)
    #     )
    #     print("Duplicate patterns:")
    #     display(dup_patterns)

    # Boxplots, one per numeric feature
    if len(num_cols):
        print("Boxplots for Numeric Features (overall):")
        cols = list(num_cols)
        n = len(cols); n_per_row = 3
        n_rows = int(np.ceil(n / n_per_row))

        fig, axes = plt.subplots(n_rows, n_per_row, figsize=(6*n_per_row, 4*n_rows))
        axes = np.atleast_1d(axes).ravel()

        for i, col in enumerate(cols):
            ax = axes[i]
            s = pd.to_numeric(df[col], errors="coerce")
            sns.boxplot(x=s, ax=ax, orient="h")
            ax.set_title(col)
            ax.set_xlabel(col)

        # Hide unused subplots
        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)
        # for ax in axes[n:]:
        #     ax.set_visible(False)

        plt.tight_layout()
        plt.show()

    # Boxplots by target class if target is provided
    if target_column and target_column in df.columns and len(num_cols):
        print(f"Boxplots by Target Class: {target_column}")
        for col in num_cols:
            plt.figure(figsize=(6, 4))
            sns.boxplot(data=df, x=target_column, y=col)
            plt.title(f"{col} by {target_column}")
            plt.tight_layout()
            plt.show()

    
    print("Unique Values Per Column:")
    unique_counts = df.nunique()
    unique_df = pd.DataFrame({
        'unique_count': unique_counts,
        'all_unique_flag': unique_counts == len(df)
    })
    display(unique_df)
    
    all_unique_cols = unique_df[unique_df['all_unique_flag']].index.tolist()
    if all_unique_cols:
        print("Columns with all unique values (possible IDs, consider dropping):")
        print(all_unique_cols)

    print("Feature Types:")
    display(df.dtypes.value_counts())

    print("Descriptive Statistics:")
    display(df.describe(include='all'))

    if target_column:
        print("Target Distribution:")
        display(df[target_column].value_counts(normalize=True))
        sns.countplot(x=target_column, data=df)
        plt.title("Target Class Distribution")
        plt.show()

    if len(num_cols):
        print("Numeric Feature Histograms with Normal Curve:")
        cols = list(num_cols)
        n = len(cols)
        n_per_row = 3
        n_rows = int(np.ceil(n / n_per_row))

        fig, axes = plt.subplots(n_rows, n_per_row, figsize=(6*n_per_row, 4*n_rows))
        axes = np.atleast_1d(axes).ravel()

        for i, col in enumerate(cols):
            ax = axes[i]
            s = pd.to_numeric(df[col], errors="coerce").dropna()
            if s.empty:
                ax.set_visible(False)
                continue

            # Histogram 
            ax.hist(s, bins=20, density=True, alpha=0.6, edgecolor="black")

            # Fit curve
            mu = s.mean()
            sigma = s.std(ddof=1)

            # Overlay normal curve 
            if np.isfinite(mu) and np.isfinite(sigma) and sigma > 0:
                x_min, x_max = s.min(), s.max()
                x = np.linspace(x_min, x_max, 200)
                pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
                ax.plot(x, pdf, linewidth=2)
                subtitle = f"μ={mu:.2f}, σ={sigma:.2f}"
            else:
                subtitle = "σ=0 (no spread) — normal curve skipped"

            ax.set_title(f"{col}  |  {subtitle}")
            ax.set_xlabel(col)
            ax.set_ylabel("Density")

    # Hiding any unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.show()
    # if len(num_cols):
    #     print("Numeric Feature Histograms:")
    #     df[num_cols].hist(bins=20, figsize=(15, 10))
    #     plt.suptitle("Histograms of Numerical Features")
    #     plt.show()
    
    # Pairplot for numeric features
    if len(num_cols) >= 2:
        print("Pairplot:")
        try:
            if target_column and target_column in df.columns:
                sns.pairplot(df, vars=num_cols, hue=target_column, corner=True, diag_kind="hist")
            else:
                sns.pairplot(df, vars=num_cols, corner=True, diag_kind="hist")
            plt.show()
        except Exception as e:
            print(f"Pairplot skipped: {e}")
    if len(cat_cols):
        print("Categorical Feature Counts:")
        for col in cat_cols:
            plt.figure(figsize=(8, 3))
            sns.countplot(y=col, data=df, order=df[col].value_counts().index)
            plt.title(f"Distribution of {col}")
            plt.tight_layout()
            plt.show()

    if len(num_cols) >= 2:
        print("Correlation Heatmap:")
        plt.figure(figsize=(12, 8))
        sns.heatmap(df[num_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Between Numeric Features")
        plt.show()