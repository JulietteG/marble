# MARBLE: Musical Artist Recommendations Based on Lyrical Evidence

This project is host of GitHub: [https://github.com/JulietteG/marble](https://github.com/JulietteG/marble).

## Dependencies

MARBLE makes use of the following Python packages:

- `beatifulsoup4`, `requests` for scraping lyrics
- `nltk` for linguistic analysis
- `numpy`, `scipy`, `scikit-learn` for machine learning infrastructure

All of the aforementioned packages (with the exception of scikit-learn, as explained below) can be installed using `pip`. For your convenience, we have added a `requirements.txt` file so that:

```
pip install -r requirements.txt
```

installs the necessary dependencies (and the correct versions thereof).

MARBLE uses `sklearn.neural_network.MLPClassifier`. For now, this unfortunately requires installing the most recent development version of sci-kit learn. Instructions follow in the subsequent section.

### Installing scikit-learn development version

Start by cloning [https://github.com/scikit-learn/scikit-learn.git](https://github.com/scikit-learn/scikit-learn.git)

```
git clone https://github.com/scikit-learn/scikit-learn.git
```

In order to build scikit-learn, you'll need to install Cython, as via:

```
pip install cython
```

In the newly downloaded `scikit-learn` directory, install scikit-learn via the following instructions (as taken from [https://github.com/scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn)).

To install in your home directory, use

```
python setup.py install --user
```

To install for all users on Unix/Linux:

```
python setup.py build
sudo python setup.py install
```

For more detailed installation instructions,
see the web page [http://scikit-learn.org/stable/install.html](http://scikit-learn.org/stable/install.html).

### Downloading the Data

All lyrics have already been downloaded, saved in the `data/lyrics/` folder, and split into `train/` and `test/` samples, with a test size of 40%.

The `unique_artist.txt` file mapping artist names to ids has been downloaded and saved in the `data/sim/` directory.

Therefore, the only file you must download is `data/sim/artist_similarity.db`, which is ~ 330MB. `artist_similarity.db` can be downloaded from [http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset](http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset) or directly via the the link [http://www.ee.columbia.edu/~thierry/artist_similarity.db](http://www.ee.columbia.edu/~thierry/artist_similarity.db).

## Usage

The complete and final model sources from `mlp.py`. To run:

```
./mlp.py <train|test> [options]
```

where "train" will run the training program and "test" will run the testing program. Note that model files must exist for the training program to run run.

The command-line options are:

```
  -h, --help            show this help message and exit
  -v, --verbose         print status messages to stdout
  -a MAX_ARTISTS, --artists=MAX_ARTISTS
                        number of artists to run
  -c CONF, --conf=CONF  location of the mlp json config file, specifying model
                        parameters
```

The `-a` option can be useful to only run on a random subset of artists. The `-c` option specifies the config file, which defaults to `conf.json`.

For example, to train then test on the complete set of train and complete set of test artists, the following two commands are run:

```
$ ./mlp.py train
$ ./mlp.py test
```

The two alternative (old) models can also still be run and evaluated:

```
$ ./kmeans.py train
```

runs the KMeans algorithm and

```
$ ./em.py train
```

runs the supervised E/M algorithm.

Note that neither KMeans, nor E/M have implemented `test` methods.

## Sample Output

### MLP Training 

After suppressing a few minor warnings, running `$ ./mlp.py train` yields the following output:

```
mode = train
Using parameters from conf.json:
{u'em': {u'iter': 10, u'metric': u'manhattan', u'neighbors': 100},
 u'kmeans': {u'num_clusters': 100},
 u'lyrics_root': {u'test': u'data/lyrics/test',
                  u'train': u'data/lyrics/train'},
 u'mlp': {u'hidden_layer_sizes': [100],
          u'max_iter': 1000,
          u'metric': u'manhattan',
          u'neighbors': 100},
 u'paths': {u'counts': u'counts',
            u'dir': u'var/',
            u'mlp': u'mlp',
            u'pca': u'pca',
            u'scaler': u'scaler'},
 u'pca': 100,
 u'sim_root': {u'artist_similarity.db': u'data/sim/artist_similarity.db',
               u'unique_artists.txt': u'data/sim/unique_artists.txt'}}
Loading artists..............................
Loading similarity database...
Extracting features...
Principal component analysis... explained_variance = 0.99299086836
Scaling the feature vectors...
Training Multi-layer Perceptron classifier...
Calculating MLP Predictions...
Calculating statistics...
	Precision: 11449 / 11461 = 0.998952970945
	Recall: 11449 / 13302 = 0.860697639453
	F-score: 0.924686023503
```

### MLP Testing

Running `$ ./mlpy. test` yields:

```
Using parameters from conf.json:
{u'em': {u'iter': 10, u'metric': u'manhattan', u'neighbors': 100},
 u'kmeans': {u'num_clusters': 100},
 u'lyrics_root': {u'test': u'data/lyrics/test',
                  u'train': u'data/lyrics/train'},
 u'mlp': {u'hidden_layer_sizes': [100],
          u'max_iter': 1000,
          u'metric': u'manhattan',
          u'neighbors': 100},
 u'paths': {u'counts': u'counts',
            u'dir': u'var/',
            u'mlp': u'mlp',
            u'pca': u'pca',
            u'scaler': u'scaler'},
 u'pca': 100,
 u'sim_root': {u'artist_similarity.db': u'data/sim/artist_similarity.db',
               u'unique_artists.txt': u'data/sim/unique_artists.txt'}}
Loading artists.....................
Loading similarity database...
Extracting features...
Principal component analysis... explained_variance = 0.99299086836
Scaling the feature vectors...
Calculating statistics...
	Precision: 824 / 97500 = 0.00845128205128
	Recall: 824 / 6042 = 0.136378682555
	F-score: 0.0159162465473
```

## Structure

The default structure is as follows:

```
.
├── README.md
├── conf.json
├── data
│   ├── lyrics
│   │   ├── test
│   │   └── train
│   └── sim
│       ├── artist_similarity.db
│       └── unique_artists.txt
├── em.py
├── features.py
├── kmeans.py
├── main.py
├── marble.py
├── mlp.py
├── models
│   ├── __init__.py
│   ├── artist.py
│   └── song.py
├── play
│   ├── regex.py
│   ├── syllabify.py
│   └── wordnet.py
├── requirements.txt
├── scrape
│   ├── azlyrics_scrape.py
│   └── lyrics_scrape.py
├── similarity.py
├── stats.py
├── util
│   ├── __init__.py
│   ├── mexceptions.py
│   ├── progress.py
│   ├── split.py
│   └── verify.py
└── var

10 directories, 26 files
```

The purpose of the directories is as follows:

- the `data/lyrics/` directory contains lyrics on which the model runs, as divided into `train/` and `test/` directories
- the `data/sim/` directory contains the `artist_similarity.db` and `unique_artist.txt` files used to extract gold standard similarity relationships
- the `models/` directory contains simple `Artist` and `Song` class definitions for representing artists and songs in memory
- the `play/` directory contains some trivial scripts used to test feature implementations
- the `scrape/` directory contains the scrapers used to download lyrics
- the `util/` directory contains a few utility scripts
- the `var/` directory is, by default, where the models are saved after training and loaded from in testing

Diving into the contents of each file:

| filename | class | purpose |
|----------|-------|---------|
| `conf.json` | | the default configuration parameters for the models proposed |
| `em.py` | `EMMarble` | definition of the old E/M supervised learning model |
| `features.py` | `FeatureExtractor` | manages the extraction of all features |
| `kmeans.py` | `KMeansMarble` | definition of the old KMeans unsupervised learning model |
| `main.py` | | provides the main method used to parse command-line arguments for all Marble subclasses. |
| `marble. py` | `Marble` | superclass to manage dataset processing |
| `mlp.py` | `MLPMarble` | definition of the MLP supervised learning model |
| `scrape/azlyrics_scrape.py` | | attempts (but fails) to scrape azlyrics.com |
| `scrape/lyrics_scrape.py` | | successfully scrapes lyrics.com |
| `similarity.py` | `Similarity` | manages the loading of the gold standard similarity labels |
| `stats.py` | | calculate basic statistics on the dataset |
| `util/mexceptions.py` | `NoArtistWithNameError` | a custom exception class |
| `util/progress.py` | | quick utility to print progress |
| `util/split.py` | | quick utility to split the dataset into train / test samples |
| `util/verify.py` | | quick helper method to verify that conf paths exist |

