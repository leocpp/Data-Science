# First let's import
# Let's do our imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import pandas_profiling
import category_encoders as ce
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor, plot_importance
from sklearn.metrics import r2_score, mean_squared_error
from .nba import NBAPlayer

%matplotlib inline

rawpast = pd.read_csv("https://raw.githubusercontent.com/Build-Week-NBA-Longevity-Predictor/Data-Science/master/1976_to_2015_Draftees_edit2.csv")
# Now we're going to get rid of the observations with 0 years, as those rows are inherently useless to us
rawpast = rawpast[rawpast['Yrs'] != 0]

trainval, test = train_test_split(rawpast, train_size=0.85, test_size=0.15, random_state=42)
train, val = train_test_split(trainval, train_size=0.80, test_size=0.20, random_state=42)

# With the information we get from the pandas profiler we can now organize our data
def organize(X):
    X = X.copy()
    # Let's name some features that we don't need, Duplicates and Meaningless
    # and a few that would bleed into our model , Obvious
    duplicates = ['Win.Share', 'Unnamed: 0', 'Executive']
    meaningless = ['Draft_Yr', 'first_year', 'second_year', 'third_year', 'fourth_year', 'fifth_year']
    obvious = ['PTS', 'TRB', 'AST', 'Minutes.Played', 'Games' ]
    
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
test = organize(test)

# Now let's arrange x matrix and y vector
target = 'Yrs'
xtrain = train.drop(columns=target)
xval = val.drop(columns=target)
xtest = test.drop(columns=target)

ytrain = train[target]
yval = val[target]
ytest = test[target]

feats = train.drop(columns=[target]).columns.tolist()

# We'll drop some more features that won't match up with the API we useor it adds noise to the model
todrop = {'Player', 'All_NBA', 'All.Star', 'College', 'Pk', 'Exec_ID', 'Exec_draft_exp', 'attend_college', 'Tenure(days)'}
feats = [e for e in feats if e not in todrop]


def rmse(ytrue, ypred):
    return np.sqrt(mean_squared_error(ytrue, ypred))


# Now let's use XGBoost
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

encoder = ce.OrdinalEncoder()
xtrainencoded = encoder.fit_transform(xtrain[feats])
xvalencoded = encoder.transform(xval[feats])
eval_set = [(xtrainencoded, ytrain),
            (xvalencoded, yval)]

model = XGBRegressor(n_estimators=732, maxdepth=4 n_jobs=-1)
model.fit(xtrainencoded, ytrain, 
          eval_set=eval_set, eval_metric='rmse', early_stopping_rounds=50)




def predict_longevity(model, req_ref_id):
    req_player = NBAPlayer.query.filter(NBAPlayer.ref_id == req_ref_id).one