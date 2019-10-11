import sys
from bs4 import BeautifulSoup
import pandas as pd
import requests


def get_box_office_hits():
    """top ten box office winners"""
    top_ten_url = "https://en.wikipedia.org/wiki/{}_in_film"
    dfs = []
    for i in range(2010, 2020):
        html = pd.read_html(top_ten_url.format(i))
        top_ten = [i for i, h in enumerate(html) if h.shape == (11, 4)].pop()
        df = html[top_ten]
        df.columns = df.iloc[0]
        df = df.drop(0)
        df["year"] = i
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    df.columns = [c.lower() for c in df.columns]
    return df[["title", "year"]]


def get_oscar_nods():
    """academy award best picture nominees"""
    html = pd.read_html("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture")
    the_2010s = html[11]
    the_2010s.columns = ["title", "producers", "junk"]
    the_2010s["is_year"] = the_2010s["title"].apply(
        lambda x: x[:4] in [str(y) for y in range(2010, 2020)]
    )
    the_2010s["year"] = the_2010s["title"].apply(
        lambda x: x[:4] if x[:4] in [str(y) for y in range(2010, 2020)] else pd.np.nan
    )
    the_2010s["year"] = the_2010s["year"].fillna(method="ffill")
    the_2010s = the_2010s.loc[
        (~the_2010s["is_year"]) & (~the_2010s["year"].isna()), ["title", "year"]
    ]
    return the_2010s


def extract_rt_ratings(url):
    r = requests.get(f"https://www.rottentomatoes.com/m/{url}")
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text)
    ratings_html = soup.find_all("span", {"class": "mop-ratings-wrap__percentage"})
    ratings = [r.text.strip().replace("%", "") for r in ratings_html]
    return ratings


def build_movie_df():
    """Puts together a dataframe of top box office hits and
    Academy Award Nominated movies with scores from RottenTomatoes."""
    top_ten_box_office_hits = get_box_office_hits()
    top_ten_box_office_hits["type"] = "top_ten_box_office_hit"
    oscar_nominations = get_oscar_nods()
    oscar_nominations["type"] = "oscar_nomination"
    # combine
    movies = pd.concat([top_ten_box_office_hits, oscar_nominations], ignore_index=True)
    # combine titles in both
    both = movies.title[movies.title.duplicated()]
    movies.loc[movies.title.isin(both), "type"] = "both"
    movies = movies.drop_duplicates().reset_index()
    # clean up title so can pass to http request
    movies["url_title"] = movies.title.apply(
        lambda x: x.lower()
        .replace(" ", "_")
        .replace(":", "")
        .replace("-", "")
        .replace(".", "")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace("&", "and")
        .replace("'", "")
        .replace(":", "")
        .replace("–", "")
        .replace("__", "_")
    )
    # fetch ratings from RT
    movie_ratings = {}
    for idx, row in movies.iterrows():
        rating = extract_rt_ratings(row["url_title"])
        if rating is None or len(rating) < 2:
            url = f"{row['url_title']}_{row['year']}"
            rating = extract_rt_ratings(url)
        movie_ratings[row["url_title"]] = rating
    # add ratings to df
    movies["ratings"] = movies.url_title.map(movie_ratings)
    # check number of ratings for errors
    movies['num_ratings'] = movies.ratings.apply(lambda x: len(x) if x else 0)
    movies.loc[movies.num_ratings < 2, "ratings"] = None
    # split ratings by critic vs audience
    movies["critics_score"] = movies.ratings.apply(lambda x: x[0] if x else None)
    movies["audience_score"] = movies.ratings.apply(lambda x: x[1] if x else None)
    return movies.drop(columns=["url_title", "ratings", "num_ratings"])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        outputfilename = sys.argv[1]
        if not outputfilename.endswith(".csv"):
            print("Output file must end in .csv")
            raise NameError
    else:
        outputfilename = "movies_2010s.csv"
    movies = build_movie_df()
    movies.to_csv(outputfilename, index=False)
