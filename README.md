MARBLE uses `sklearn.neural_network.MLPClassifier`. For now, this requires installing the most recent development version of sci-kit learn. 

## Installing sci-kit learn

Start by cloning [https://github.com/scikit-learn/scikit-learn.git](https://github.com/scikit-learn/scikit-learn.git)

```
git clone https://github.com/scikit-learn/scikit-learn.git
```

In the newly downloaded `scikit-learn` directory, install scikit-learn via the following instructions (as taken from [https://github.com/scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn)).

To install in your home directory, use

```
python setup.py install --user
```

To install for all users on Unix/Linux::

```
python setup.py build
sudo python setup.py install
```

For more detailed installation instructions,
see the web page [http://scikit-learn.org/stable/install.html](http://scikit-learn.org/stable/install.html).
