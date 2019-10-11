# Movie Rating Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt
import pyplot_themes
import seaborn as sns
%matplotlib inline
```


```python
pyplot_themes.theme_ucberkeley()
blue_yellow = pyplot_themes.palettes.UCBerkeley.primary_colors[::2]
```


## Comparing Critics and Audience Scores on Rotten Tomatoes

I _feel like_ I've noticed that audience scores tend to be higher for movies that are fun to watch, while critics scores tend to be higher for movies that are challenging to watch. I also _feel like_ more fun to watch movies end up doing better at the box office while more challenging movies end up getting more acclaim come awards season. Even better than _feeling_ this way, I can compare the scores from RottenTomatoes pretty easily.

I started by extracting the list of top box office hits and Academy Award Best Picture nominations for the 2010s decade from Wikipedia. I then tried to extract the Tomamoter (critic) and Audience scores from rottentomatoes.com using a _"url-friendly"_ version of the title. For example, the film _La La Land_ would be tried as `la_la_land`. If that didn't work, I would then try adding the year to the title like `la_la_land_2016`. One of these two options usually worked. I looked into the others that did not match easily, but decided there was no good way to automate them so filled in by hand.


```python
movies = pd.read_csv("movies_2010s.csv")
```


```python
movies.sample(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>year</th>
      <th>type</th>
      <th>critics_score</th>
      <th>audience_score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>6</th>
      <td>Iron Man 2</td>
      <td>2010</td>
      <td>top_ten_box_office_hit</td>
      <td>73</td>
      <td>71</td>
    </tr>
    <tr>
      <th>159</th>
      <td>Call Me by Your Name</td>
      <td>2017</td>
      <td>oscar_nomination</td>
      <td>95</td>
      <td>86</td>
    </tr>
    <tr>
      <th>38</th>
      <td>Man of Steel</td>
      <td>2013</td>
      <td>top_ten_box_office_hit</td>
      <td>56</td>
      <td>75</td>
    </tr>
    <tr>
      <th>17</th>
      <td>The Hangover Part II</td>
      <td>2011</td>
      <td>top_ten_box_office_hit</td>
      <td>33</td>
      <td>52</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Toy Story 3</td>
      <td>2010</td>
      <td>both</td>
      <td>98</td>
      <td>89</td>
    </tr>
    <tr>
      <th>85</th>
      <td>Bohemian Rhapsody</td>
      <td>2018</td>
      <td>both</td>
      <td>61</td>
      <td>86</td>
    </tr>
    <tr>
      <th>107</th>
      <td>Winter's Bone</td>
      <td>2010</td>
      <td>oscar_nomination</td>
      <td>94</td>
      <td>76</td>
    </tr>
    <tr>
      <th>56</th>
      <td>Inside Out</td>
      <td>2015</td>
      <td>top_ten_box_office_hit</td>
      <td>98</td>
      <td>89</td>
    </tr>
    <tr>
      <th>92</th>
      <td>Spider-Man: Far From Home</td>
      <td>2019</td>
      <td>top_ten_box_office_hit</td>
      <td>90</td>
      <td>95</td>
    </tr>
    <tr>
      <th>35</th>
      <td>Fast &amp; Furious 6</td>
      <td>2013</td>
      <td>top_ten_box_office_hit</td>
      <td>70</td>
      <td>84</td>
    </tr>
  </tbody>
</table>
</div>




```python
print(
    f"There are {movies.shape[0]} movies in this dataset,",
    f"but {movies[['critics_score', 'audience_score']].isna().sum()[0]} of them don't have their scores.",
    sep = "\n",
)
```

    There are 173 movies in this dataset,
    but 0 of them don't have their scores.



```python
movies.plot(
    x="year",
    y=["critics_score", "audience_score"], 
    style=".",
    color=blue_yellow,
)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f7577e64b00>




![svg](movie_rating_analysis_files/movie_rating_analysis_6_1.svg)


There does seem to be a bit of disagreement, but I can't tell right away much it differs.


```python
sns.lmplot(data=movies, x="critics_score", y="audience_score")
```

    /home/rucy/anaconda3/lib/python3.7/site-packages/scipy/stats/stats.py:1713: FutureWarning: Using a non-tuple sequence for multidimensional indexing is deprecated; use `arr[tuple(seq)]` instead of `arr[seq]`. In the future this will be interpreted as an array index, `arr[np.array(seq)]`, which will result either in an error or a different result.
      return np.add.reduce(sorted[indexer] * weights, axis=axis) / sumval





    <seaborn.axisgrid.FacetGrid at 0x7f757066e908>




![svg](movie_rating_analysis_files/movie_rating_analysis_8_2.svg)


I guess we see that usually the scores don't differ too much actually for these types of movies, though there clearly are some bigger debates when one side really loves a movie.


```python
sns.lmplot(data=movies, x="year", y="critics_score", hue="type")
```

    /home/rucy/anaconda3/lib/python3.7/site-packages/scipy/stats/stats.py:1713: FutureWarning: Using a non-tuple sequence for multidimensional indexing is deprecated; use `arr[tuple(seq)]` instead of `arr[seq]`. In the future this will be interpreted as an array index, `arr[np.array(seq)]`, which will result either in an error or a different result.
      return np.add.reduce(sorted[indexer] * weights, axis=axis) / sumval





    <seaborn.axisgrid.FacetGrid at 0x7f7578544588>




![svg](movie_rating_analysis_files/movie_rating_analysis_10_2.svg)


Interestingly, we see here that critics seem to be liking the movies made for mass audiences more over the past 10 years.


```python
sns.lmplot(data=movies, x="year", y="audience_score", hue="type")
```




    <seaborn.axisgrid.FacetGrid at 0x7f7578acbe80>




![svg](movie_rating_analysis_files/movie_rating_analysis_12_1.svg)


Also interestingly, we see that audiences seem to actually be liking the box office hit films more and more, while disliking the Academy Award nominated films.


```python

```
