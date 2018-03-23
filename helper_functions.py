# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Handle table-like data and matrices
import numpy as np
import pandas as pd

# Modelling Algorithms
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier , GradientBoostingClassifier

# Error Handling
from sklearn.exceptions import NotFittedError

# Modelling Helpers
from sklearn.preprocessing import Imputer , Normalizer , scale
from sklearn.cross_validation import train_test_split , StratifiedKFold

# Visualisation
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# Configure visualisations
mpl.style.use( 'ggplot' )
sns.set_style( 'white' )
pylab.rcParams[ 'figure.figsize' ] = 8 , 6

def plot_histograms( df , variables , n_rows , n_cols ):
    fig = plt.figure( figsize = ( 16 , 12 ) )
    for i, var_name in enumerate( variables ):
        ax=fig.add_subplot( n_rows , n_cols , i+1 )
        df[ var_name ].hist( bins=10 , ax=ax )
        ax.set_title( 'Skew: ' + str( round( float( df[ var_name ].skew() ) , ) ) ) # + ' ' + var_name ) #var_name+" Distribution")
        ax.set_xticklabels( [] , visible=False )
        ax.set_yticklabels( [] , visible=False )
    fig.tight_layout()  # Improves appearance a bit.
    plt.show()

def plot_distribution( df , var , target , **kwargs ):
    row = kwargs.get( 'row' , None )
    col = kwargs.get( 'col' , None )
    facet = sns.FacetGrid( df , hue=target , aspect=4 , row = row , col = col )
    facet.map( sns.kdeplot , var , shade= True )
    facet.set( xlim=( 0 , df[ var ].max() ) )
    facet.add_legend()

def plot_categories( df , cat , target , **kwargs ):
    row = kwargs.get( 'row' , None )
    col = kwargs.get( 'col' , None )
    facet = sns.FacetGrid( df , row = row , col = col )
    facet.map( sns.barplot , cat , target )
    facet.add_legend()

def plot_correlation_map( df ):
    corr = df.corr()
    _ , ax = plt.subplots( figsize =( 12 , 10 ) )
    cmap = sns.diverging_palette( 220 , 10 , as_cmap = True )
    _ = sns.heatmap(
        corr, 
        cmap = cmap,
        square=True, 
        cbar_kws={ 'shrink' : .9 }, 
        ax=ax, 
        annot = True, 
        annot_kws = { 'fontsize' : 12 }
    )

def describe_more( df ):
    var = [] ; l = [] ; t = []
    for x in df:
        var.append( x )
        l.append( len( pd.value_counts( df[ x ] ) ) )
        t.append( df[ x ].dtypes )
    levels = pd.DataFrame( { 'Variable' : var , 'Levels' : l , 'Datatype' : t } )
    levels.sort_values( by = 'Levels' , inplace = True )
    return levels

def plot_variable_importance( X , y ):
    tree = DecisionTreeClassifier( random_state = 99 )
    tree.fit( X , y )
    plot_model_var_imp( tree , X , y )
    
def plot_model_var_imp( model , X , y ):
    imp = pd.DataFrame( 
        model.feature_importances_  , 
        columns = [ 'Importance' ] , 
        index = X.columns 
    )
    imp = imp.sort_values( [ 'Importance' ] , ascending = True )
    imp[ : 10 ].plot( kind = 'barh' )
    print (model.score( X , y ))
    

    
def plot_partial_dependence( model , X , y , features, grid_resolution=100):
    
    try:
        model.predict(X.sample(1))
    except NotFittedError as e:
        print('You need to fit the model, please go to step 4.2.')
        return
        
    if len(features) == 1:

        @np.vectorize
        def parDep(x):

            X_sample = X.sample(500)
            X_sample[features[0]] = x
            z = np.mean(model.predict(X_sample))

            return(z)
        
        x = np.linspace(min(X[features[0]]),max(X[features[0]]), grid_resolution)
        z = parDep(x)

        plt.figure(figsize=(8,6))
        plt.plot(x,z)
        plt.xlabel(features[0])
        plt.ylabel('probability of survival')
        plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
        plt.show()
    
    elif len(features) == 2:

            @np.vectorize
            def parDep(x, y):

                X_sample = X.sample(250)
                X_sample[features[0]] = x
                X_sample[features[1]] = y
                z = np.mean(model.predict(X_sample))

                return(z)
            
            x = np.linspace(min(X[features[0]]),max(X[features[0]]),grid_resolution)
            y = np.linspace(min(X[features[1]]),max(X[features[1]]),grid_resolution)
            XX, YY = np.meshgrid(x, y)

            ZZ = parDep(XX, YY)

            fig = plt.figure(figsize=(8,6))
            ax = Axes3D(fig)
            surf = ax.plot_surface(XX, YY, ZZ, cmap=plt.cm.Spectral)
            ax.set_xlabel(features[0])
            ax.set_ylabel(features[1])
            ax.set_zlabel('probability of survival')
            plt.show()
 
