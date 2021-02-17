# Parler API interface for Python

![](https://i.imgur.com/CmAmSBF.jpg)

This **UNOFFICIAL** library designed to programatically fetch data from parler.com

# IMPORTANT ANNOUNCEMENT:

~~Parler.com is down, [they got dumped by their cloud host AWS](https://www.buzzfeednews.com/article/johnpaczkowski/amazon-parler-aws) and should they go online again I will update this project accordingly.~~

⇙⇙⇙

Parler is back up, API is the same, update your `JST` and `MST` tokens, the `_ddg` (DDoS guard related?) cookie is not needed.

## Authentication:

You need to create a `.parler.env` file with the following contents:

```
JST=<your browser JST>
MST=<your browser MST>
```

Get them from Inspect element > storage

![](https://i.imgur.com/IP2bimo.png)

## Usage for `parlerctl`:

Can show hashtags, feed

```
usage: parlerctl.py [-h] --show SHOW [--summary]
parlerctl.py: error: the following arguments are required: --show
```

-   profile
-   hashtags
-   ingest

## Installation

If using `pipenv`:

```
pipenv install
pipenv shell
```

If using `pip`:

```
pip install -r requirements.txt
```

## Experiments:

Collected the suggested hashtags for a 9 hour period, [data here](./sampledata/hashtags.csv)

Other experiments available as well.

## Contributing:

Feel free to improve the code, submit your experiments and sample code or fix bugs. Before submitting a PR, run `pep8` linter on your code.

## Donate:

If you found this package useful, [consider donating](https://paypal.me/konradit).

## Disclaimer:

I am in now way affiliated with Parler, it's subsidiaries or any entity related to the company. I am not responsible for what you do with this Python package.

2009/24/EC Art 5:

```
The person having a right to use a copy of a computer program shall be entitled, without the authorisation of the rightholder, to observe, study or test the functioning of the program in order to determine the ideas and principles which underlie any element of the program if he does so while performing any of the acts of loading, displaying, running, transmitting or storing the program which he is entitled to do.
```
