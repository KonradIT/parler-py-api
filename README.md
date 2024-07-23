# Parler API interface for Python

![](https://i.imgur.com/uPUw5p1.jpg)

This **UNOFFICIAL** library designed to programatically fetch data from parler.com


## Installation

#### From pypi:

```
pip install parler-api
```

#### Clone and run locally:

If using `pipenv`:

```
pipenv install
pipenv shell
```

If using `pip`:

```
pip install -r requirements.txt
```

## Login + save credentials:

```bash
$ python3 ./scripts/login_helper.py
Parler v3 API Login Helper tool
Please enter your email used to register with Parler
Email: your.email@here.com
DEBUG:parler-py-api:User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36
Magic link: https://api.parler.com/magicLogin/jbZgjMe3V....
All done.
$ 
```
## CLI usage:

```bash
$ python3 ./scripts/simplecli.py --debug=True --config_file=parlerconfig.ini search --term=ukraine
```

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
