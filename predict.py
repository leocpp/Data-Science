import pickle
import numpy as np
import pandas as pd
import category_encoders as ce
import itertools
# import warnings
import requests
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor
from sportsreference.nba.roster import Roster, Player
from sportsreference.nba.player import AbstractPlayer
from sportsreference.nba.teams import Teams
from sklearn.metrics import r2_score, mean_squared_error


teams = Teams()
teamabbs = []
squadnames = []
for team in teams:
    teamabbs.append(team.abbreviation)
for abb in teamabbs:
    squad = Roster(abb, slim=True)
    squaddict = squad.players
    squadnames.append(list(squaddict.values()))
mergednames = list(itertools.chain.from_iterable(squadnames))

rawpast = pd.read_csv("https://raw.githubusercontent.com/Build-Week-NBA-Longevity-Predictor/Data-Science/master/1976_to_2015_Draftees_edit2.csv")
rawpast = rawpast[rawpast['Yrs'] != 0]
past = rawpast[~rawpast['Player'].isin(mergednames)]

train, val = train_test_split(past, train_size=0.80, test_size=0.20,
                              random_state=42)


def organize(X):
    X = X.copy()
    # Let's name some features that we don't need, Duplicates and Meaningless
    # and a few that would bleed into our model , Obvious
    duplicates = ['Win.Share', 'Unnamed: 0', 'Executive']
    meaningless = ['Draft_Yr', 'first_year', 'second_year', 'third_year',
                   'fourth_year', 'fifth_year']
    obvious = ['PTS', 'TRB', 'AST', 'Minutes.Played', 'Games', 'VORP']

    # Now let's do a cosmetic change to College
    X['College'] = X['College'].replace('0', 'None')

    # And we'll make Tenure(days) from the Tenure feature
    X['Tenure(days)'] = X['Tenure'].map(lambda x: str(x)[:-24]).astype('int64')

    # We'll add Tenure to duplicates
    duplicates = duplicates + ['Tenure']

    # Now let's drop the features we don't need
    todrop = duplicates + meaningless + obvious
    X = X.drop(columns=todrop)

    return X


train = organize(train)
val = organize(val)
# Now let's arrange x matrix and y vector
target = 'Yrs'
xtrain = train.drop(columns=target)
xval = val.drop(columns=target)
ytrain = train[target]
yval = val[target]

feats = train.drop(columns=[target]).columns.tolist()
# We'll drop some more features that won't match up with the API we use
# We'll also drom some more (post analysis) noisy features
todrop = {'Player', 'All_NBA', 'All.Star', 'College', 'Pk', 'Exec_ID',
          'Exec_draft_exp', 'attend_college', 'Tenure(days)'}
feats = [e for e in feats if e not in todrop]


def rmse(ytrue, ypred):
    return np.sqrt(mean_squared_error(ytrue, ypred))


# First we'll use the average NBA career length of 5 yrs
avgyrs = 5
ybase = np.full_like(yval, avgyrs)
## print('The Average Career of an NBA player is 5 Years')
## print(f"Baseline RMSE: {rmse(yval, ybase)}")

# Now let's use XGBoost
# We've already Optimized our Hyperparamaters
xgbpipeline = make_pipeline(
    ce.OrdinalEncoder(),
    XGBRegressor(n_estimators=586, max_depth=7, n_jobs=-1,random_state=42)
)
xgbpipeline.fit(xtrain[feats],ytrain)

# Now let's pickle our pipeline
pickle.dump(xgbpipeline, open('xgbpipe.pkl', 'wb'))
        # warnings.simplefilter(action='ignore', category=FutureWarning)
        # encoder = ce.OrdinalEncoder()
        # xtrainencoded = encoder.fit_transform(xtrain[feats])
        # xvalencoded = encoder.transform(xval[feats])
        # eval_set = [(xtrainencoded, ytrain),
        #             (xvalencoded, yval)]
        # xgbreg = XGBRegressor(n_estimators=586, max_depth=7, n_jobs=-1)
        # xgbreg.fit(xtrainencoded, ytrain,
        #            eval_set=eval_set, eval_metric='rmse', early_stopping_rounds=50)
        # ypred = xgbreg.predict(xvalencoded)  # We can check this agains yval

        # # Now let's pickle our model
        # pickle.dump(xgbreg, open('model.pkl', 'wb'))

# Now let's get the csv of current players
nbads = pd.read_csv('nbads.csv')
# Now we'll set up a test player, Ben Simmons (nbads index 213)
chkdata = nbads[nbads['Player'] == 'Ben Simmons']
        # xtestencoded = encoder.transform(chkdata.drop(columns=['Player', 'VORP']))

# Now let's load the model to find the result
##xgbpipe = pickle.load(open('xgbpipe.pkl', 'rb'))
        # model = pickle.load(open('model.pkl', 'rb'))
##print('Predicted longevity of chosen player:', xgbpipe.predict(chkdata[feats]))

# Now let's find a comparable historic player
def comparrison(chkdata):
    Xpast = past[feats]
    coder = ce.OrdinalEncoder()
    Xencoded = coder.fit_transform(Xpast)
    chkcoded = coder.transform(chkdata[feats])
    nghbr = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(Xencoded)
    distance, idx = nghbr.kneighbors(chkcoded)
    finfeats = feats + ['Player', 'Yrs']
    comppast = past[finfeats]
    compplayer = comppast.iloc[idx[0]]
    compresult = compplayer[['Player', 'Yrs']]
    return compresult


print('A Comparable Historical Player is:', comparrison(chkdata))
