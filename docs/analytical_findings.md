# Steam Market Analytics — Analytical Findings

## 1. Dataset overview

The analysis covers a dataset of **2,927 Steam games**, focusing on pricing, discounts, review activity, genres, and tags.

### Key findings

- **Average game price:** €15.89
- **Median game price:** €10.35
- **Games with review data:** 2,196 (75.03%)
- **Most represented release year:** 2025, with 679 games in the dataset.

### Interpretation

The average game price is higher than the median, indicating a right-skewed price distribution. Relatively expensive games increase the average compared with the price of a typical game. Approximately 75% of the games have review-count data available, while the remaining games require consideration when interpreting popularity-related metrics. The dataset contains the highest number of games released in 2025. However, this reflects the composition of the collected sample rather than the total number of games released on Steam during that year.

### Limitations

The dataset represents a sample of Steam games, not the entire Steam catalog. Therefore, the results should not be generalized to the whole platform without considering the data collection methodology and sampling bias.

## 2. Pricing & discounts

### Key findings

- **Discounted games:** 641
- **Average discount:** 47.85%
- **Average original price:** €19.01
- **Average discounted price:** €9.41
- **Most common discount range:** 26–50%, covering 233 games.

### Interpretation

The average discount of 47.85% indicates that discounted games in the dataset frequently receive substantial price reductions. The 26–50% discount range contains the largest number of discounted games, followed by the 51–75% range, which includes 161 games.
Games discounted by 51–75% have the highest average number of reviews (19,290). However, their median review count is much lower (approximately 2,338). This large difference suggests a strongly right-skewed distribution, where a relatively small number of highly reviewed games substantially increases the average.

### Limitations

The observed relationship between discounts and review counts does not establish causation. Popular games may receive discounts, but discounts cannot be assumed to cause higher popularity.Review counts are also cumulative and may reflect historical popularity rather than activity during a particular discount period.

## 3. Reviews & popularity

### Key findings

- **Games with review data:** 2,196 (75.03% of the dataset).
- **Most common review category:** Very Positive, with 1,034 games.
- **Total reviews in the Very Positive category:** 40,062,197.
- **Most reviewed game:** Counter-Strike 2, with 8,679,136 reviews.
- **Games with fewer than 1,000 reviews:** 848.

### Interpretation

The *Very Positive* category is the most represented review category in the dataset, accounting for approximately 47.1% of games with review-count data. Review activity is highly unevenly distributed across games. Counter-Strike 2 alone accounts for approximately 11.6% of the total recorded reviews (74.5 million), illustrating how a small number of highly popular titles can dominate aggregate popularity metrics. A particularly notable example occurs in 2012, when the average number of reviews per game reaches approximately 883,000. This unusually high value is strongly influenced by Counter-Strike 2, which is assigned to that release year in the dataset. The large differences between average and median review counts across release years further illustrate how extreme values influence the mean.

### Limitations

Review counts measure the volume of user feedback rather than the number of active players, sales, or revenue. The release year represents the date recorded in the dataset and may not always correspond to the release date of the current version of a game. Additionally, review counts are cumulative, meaning that older games have generally had more time to accumulate reviews.

## 4. Genres & tags

### Key findings

- **Most frequently assigned tag:** Simulación, appearing in 740 games.
- **Second most common tag:** Acción, appearing in 604 games.
- **Third most common tag:** Estrategia, appearing in 515 games.
- **Tag with the highest median review count:** Robos, with 239,309 reviews.
- **Dynamic genre analysis:** Within the Rol genre, the most frequent tags are Rol (60 games), Mundo abierto (39 games), and Acción (36 games).

### Interpretation

Simulation, action, and strategy are among the most frequently assigned tags in the analyzed dataset, indicating their strong representation within the collected sample. However, the most common tags are not necessarily associated with the highest median review counts. For example, Robos leads the ranking by median reviews, despite not appearing among the ten most frequently assigned tags.
The interactive genre-based analysis reveals how tag distributions vary within specific genres. For games classified under Rol, tags such as Mundo abierto, Acción, and Multijugador frequently occur alongside the main genre.
These results illustrate the value of analyzing both tag frequency and review-based popularity metrics rather than relying on a single measure.

### Limitations

Games can have multiple tags and belong to multiple genres. Consequently, counts across tags and genres overlap and should not be summed to estimate the total number of unique games.
A high median review count for a tag does not necessarily imply that the tag causes greater popularity. Additionally, tags assigned to relatively few games may produce unstable statistics.
The analysis reflects the composition of the collected dataset rather than the complete Steam catalog.

## 5. Overall conclusions & limitations

### Overall conclusions

The Steam Market Analytics project provides insights into game pricing, discounts, review activity, genres, and tags based on a dataset of 2,927 games.

The analysis highlights several important findings:

- **Price distribution:** The average game price exceeds the median, indicating that higher-priced titles influence the overall average.
- **Discount patterns:** Discounts are common within the analyzed sample, with the 26–50% range containing the largest number of discounted games.
- **Review concentration:** A relatively small number of highly reviewed games significantly influences aggregate review statistics.
- **Average vs. median:** Large differences between these measures highlight the importance of robust statistics when analyzing highly skewed distributions.
- **Genre and tag analysis:** Frequently assigned tags do not necessarily correspond to those with the highest median review counts.

### Data limitations

The analysis has several important limitations:

- **Sampling bias:** The dataset is a sample of Steam games and may not represent the entire platform.
- **Missing review data:** Approximately 25% of games do not have review-count data available.
- **Cumulative reviews:** Review counts reflect accumulated activity rather than sales, revenue, or current player engagement.
- **Multiple categories:** A game can belong to multiple genres and have multiple tags, resulting in overlapping category counts.
- **Temporal limitations:** Prices and discounts represent the state captured during data collection and may change over time.
- **Data quality:** Release dates and category labels depend on the quality and consistency of the source dataset.

### Final remarks

The project demonstrates an end-to-end data analytics workflow involving data exploration, transformation, relational data modeling, SQL analysis, and interactive visualization in Power BI.

The findings provide descriptive insights into the collected data while acknowledging the methodological limitations that affect interpretation and generalization.