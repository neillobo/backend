import pandas as pd
import numpy as np
import pylab as pl

from scipy.stats.stats import pearsonr

df = pd.read_csv("beer_reviews.csv")

# calculate relationships between the most popular beers, based on # of reviews
beers = df['beer_beerid'].value_counts().keys()[:100]

#calculate everything for real production
#beers = df['beer_beerid'].value_counts().keys()[:3000]


def get_beer_reviews(beer, common_users):
    mask = (df.review_profilename.isin(common_users)) & (df.beer_beerid==beer)
    reviews = df[mask].sort('review_profilename')
    reviews = reviews[reviews.review_profilename.duplicated()==False]
    return reviews

features = ['review_overall', 'review_aroma', 'review_palate', 'review_taste']
with open('beer_distances.csv', 'w') as outfile:
    outfile.write('beer1_id,beer2_id,' + ','.join(features) + '\n')
    for beer1_index, beer1 in enumerate(beers):
        print "%d/%d" % (beer1_index, len(beers)-1)

        beer_1_reviewers = df[df.beer_beerid==beer1].review_profilename.unique()
        for beer2_index in range(len(beers)-1, beer1_index+1, -1):
            beer2 = beers[beer2_index]

            beer_2_reviewers = df[df.beer_beerid==beer2].review_profilename.unique()
            common_reviewers = set(beer_1_reviewers).intersection(beer_2_reviewers)

            beer_1_reviews = get_beer_reviews(beer1, common_reviewers)
            beer_2_reviews = get_beer_reviews(beer2, common_reviewers)

            line = [beer1, beer2]
            for feature in features:
                # the pearson function returns the pearson correlation between 2 data sets,
                # as well as the probability that the correlation arose randomly
                correlation, probability = pearsonr(beer_1_reviews[feature], beer_2_reviews[feature])
                # save correlation only if it is probabilistically significant
                score = correlation if probability < .50 else 0.0
                line.append(score)

            # convert all the elements to a string, then join with commas
            outfile.write(','.join(map(str, line)) + '\n')

            if beer2_index % (len(beers)/10) == 0:
                print "  %d/%d" % (beer2_index, len(beers)-1-beer1_index)

with open('beer_beerid.csv', 'w') as outfile:
    outfile.write('beer_id,beer_name,image_url' + '\n')
    for beer_id in beers:
        beer_name = df[df.beer_beerid==beer_id].beer_name.value_counts().keys()[0]
        image_url = 'http://cdn.beeradvocate.com/im/beers/%d.jpg' % (beer_id)
        line = map(str, [beer_id, beer_name, image_url])
        outfile.write(','.join(line) + '\n')

