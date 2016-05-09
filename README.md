# MARBLE: Musical Artist Recommendations Based on Lyrical Evidence

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

MARBLE uses `sklearn.neural_network.MLPClassifier`. For now, this unfortunately requires installing the most recent development version of sci-kit learn. Instructions following in the subsequent section.

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

## Usage

The complete and final model sources from `mlp.py`. To run:

```
./mlp.py <train|test> [options]
```

where "train" will run the training program and "test" will run the testing program. Not that model files must exist for the training program to run run.

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

## Structure

The default directory structure is as follows:

```
.
├── data
├── lyrics
├── models
├── play
├── scrape
├── util
└── var
```

- the `data/` directory contains the `artist_similarity.db` and `unique_artist.txt` files used to extract gold standard similarity relationships
- the `lyrics/` directory contains lyrics on which the model runs, as divided into `train/` and `test/` directories
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
| `marble. py` | `Marble` | superclass to manage dataset processing |
| `mlp.py` | `MLPMarble` | definition of the MLP supervised learning model |
| `scrape/azlyrics_scrape.py` | | attempts (but fails) to scrape azlyrics.com |
| `scrape/lyrics_scrape.py` | | successfully scrapes lyrics.com |
| `similarity.py` | `Similarity` | manages the loading of the gold standard similarity labels |
| `stats.py` | | calculate basic statistics on the dataset |
| `util/mexceptions.py` | `NoArtistWithNameError` | a custom exception class |
| `util/progress.py` | | quick utility to print progress |
| `util/split.py` | | quick utility to split the dataset into train / test samples |

