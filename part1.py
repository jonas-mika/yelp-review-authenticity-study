# part1.py
# simple queries 

# imports
import pyspark as spark
import pyspark.sql.functions as func     

def question1(bs):
  """
  Analyze business.json to find the total number
  of reviews for all businesses. The output
  should be in the form of a Spark DataFrame with
  one value representing the count.
  """
  bs.agg(func.sum('review_count')).show()

def question2(bs):
  """
  Analyze business.json to find all businesses
  that have received 5 stars and that have been
  reviewed by 1000 or more users. The output
  should be in the form of DataFrame of 
  (name, stars, review count)
  """
  bs.filter(bs.stars==5)\
    .filter(bs.review_count >= 1000)\
    .select('name', 'stars', 'review_count')\
    .show()

def question3(us):
  """
  Analyze user.json to find the influencers who
  have written more than 1000 reviews. The output
  should be in the form of DataFrame of user id.
  """
  influencers = us.filter(us.review_count > 1000)\
                  .select('user_id')
  return influencers

def question4(rs, bs, inf):
  """
  Analyze review.json, business.json, and a view
  created from your answer to Q3 to find the
  businesses that have been reviewed by more than
  5 influencer users.
  """
  # filter out review made by influencers
  inf_rev = rs.join(inf, ["user_id"], 'leftsemi')

  # find the distinct no of influencer users per business_id
  ans = inf_rev\
          .groupBy('business_id')\
          .agg(func.countDistinct('user_id')\
          .alias('inf_count'))

  # filter for businesses having more than 5 reviews
  ans.filter(ans.inf_count > 5).show()

def question5(rs, us):
  """
  Analyze review.json and user.json to find an
  ordered list of users based on the average star
  counts they have given in all their reviews.
  """
  us.join(rs, on='user_id')\
    .groupBy(['user_id', 'name'])\
    .agg(func.mean('stars').alias('average_rating'))\
    .sort(func.desc('average_rating'), func.asc('name'))\
    .show()
  
