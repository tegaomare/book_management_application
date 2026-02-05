import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.domain.book import Book
from typing import List


class BookAnalyticsService:

    def df_from_books(self, books: List[Book]) -> pd.DataFrame:
        records = [b.to_dict() for b in books]
        df = pd.DataFrame(records)
        return df

    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        # basic cleaning: ensure numeric types and fill missing values sensibly
        df = df.copy()
        num_cols = [
            "publication_year",
            "page_count",
            "average_rating",
            "ratings_count",
            "price_usd",
            "sales_millions",
        ]
        for c in num_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        df["genre"] = df.get("genre")
        df["available"] = df.get("available").fillna(True)
        return df

    def average_price(self, books: List[Book]) -> float:
        df = self.df_from_books(books)
        df = self.clean_df(df)
        return float(df["price_usd"].mean())

    def top_rated(self, books: List[Book], min_ratings: int = 1000, limit: int = 10):
        df = self.df_from_books(books)
        df = self.clean_df(df)
        filt = df["ratings_count"] >= min_ratings
        res = df.loc[filt].sort_values("average_rating", ascending=False).head(limit)
        return res.to_dict(orient="records")

    def value_scores(self, books: List[Book]) -> dict:
        df = self.df_from_books(books)
        df = self.clean_df(df)
        # score = rating * log1p(ratings_count) / price_usd
        df = df[
            (df["average_rating"].notna())
            & (df["ratings_count"].notna())
            & (df["price_usd"].notna())
        ]
        df["score"] = (df["average_rating"] * np.log1p(df["ratings_count"])) / df[
            "price_usd"
        ]
        return dict(zip(df["book_id"], df["score"].astype(float)))

    def bayesian_weighted_by_genre(
        self, books: List[Book], m: int = 50
    ) -> pd.DataFrame:
        df = self.df_from_books(books)
        df = self.clean_df(df)
        # compute mean rating per genre and median ratings_count per genre
        grouped = (
            df.groupby("genre")
            .agg(
                mean_average_rating=("average_rating", "mean"),
                median_ratings_count=("ratings_count", "median"),
            )
            .reset_index()
        )
        global_mean = df["average_rating"].mean()
        grouped["weighted_rating"] = (
            grouped["median_ratings_count"] / (grouped["median_ratings_count"] + m)
        ) * grouped["mean_average_rating"] + (
            m / (grouped["median_ratings_count"] + m)
        ) * global_mean
        return grouped.sort_values("weighted_rating", ascending=False)

    def genre_count_chart(
        self, books: List[Book], out_path: str = "genre_counts.png"
    ) -> str:
        df = self.df_from_books(books)
        df = self.clean_df(df)
        counts = df["genre"].value_counts()
        plt.figure(figsize=(8, 6))
        counts.plot(kind="bar")
        plt.title("Books per Genre")
        plt.xlabel("Genre")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path

    def genre_rating_chart(
        self, books: List[Book], out_path: str = "genre_ratings.png"
    ) -> str:
        df = self.df_from_books(books)
        df = self.clean_df(df)
        grouped = (
            df.groupby("genre")["average_rating"].mean().sort_values(ascending=False)
        )
        plt.figure(figsize=(8, 6))
        grouped.plot(kind="bar")
        plt.title("Average Rating by Genre")
        plt.xlabel("Genre")
        plt.ylabel("Average Rating")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path

    def scatter_price_rating(
        self, books: List[Book], out_path: str = "price_vs_rating.png"
    ) -> str:
        df = self.df_from_books(books)
        df = self.clean_df(df)
        df = df.dropna(subset=["price_usd", "average_rating"])
        plt.figure(figsize=(8, 6))
        plt.scatter(df["price_usd"], df["average_rating"], alpha=0.6)
        plt.title("Price vs Average Rating")
        plt.xlabel("Price (USD)")
        plt.ylabel("Average Rating")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path

    def line_books_by_year(
        self, books: List[Book], out_path: str = "books_by_year.png"
    ) -> str:
        df = self.df_from_books(books)
        df = self.clean_df(df)
        df = df.dropna(subset=["publication_year"])
        counts = df["publication_year"].value_counts().sort_index()
        plt.figure(figsize=(10, 5))
        counts.plot(kind="line")
        plt.title("Books Released by Year")
        plt.xlabel("Year")
        plt.ylabel("Number of Books")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path

    def pie_checked_in_vs_available(
        self, books: List[Book], out_path: str = "availability_pie.png"
    ) -> str:
        df = self.df_from_books(books)
        df = self.clean_df(df)
        status = df["available"].value_counts()
        plt.figure(figsize=(6, 6))
        status.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Available vs Checked Out")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path
