# Parler API interface for Python

![](https://i.imgur.com/uPUw5p1.jpg)

This **UNOFFICIAL** library designed to programatically fetch data from parler.com

# IMPORTANT ANNOUNCEMENT:

~~This library supports the new (as of 2022-02-06) Parler `open-api` / logged-in endpoints. Both logged in and guest modes are supported.~~

**Show is back on!** Now this library supports the *even newer* (as of 2022-10-21) Parler `/v0/` and `/v0/public` endpoints. Same caveats, both logged in and guest modes are supported

# To do list:

- [X] Implement unfinished authed functions
- [ ] Rework experiments
- [ ] Have a github action (several!) to archive posts, run analysises, etc..
- [ ] Testing, testing
- [X] Publish to pypi

## Authentication:

There are two modes of using the API. **Authenticated** and **Guest**.

Authentication is done by initializing the `Parler` class, importing `Parler.with_auth` and initializing an `AuthSession` with your credentials.

```python
from Parler import with_auth as authed

au = authed.AuthSession(debug=False)
au.is_logged_in # ==> False
au.login(
	identifier=os.getenv("email"),
	password=os.getenv("password")
)

au.is_logged_in # ==> True
```

Here is a chart of how the functions are "loginwalled" or not.

| Function           | Description                                                                            | API Type needed |
|--------------------|----------------------------------------------------------------------------------------|-----------------|
| `.profile()`       | Get information from a specified username                                              | Guest           |
| `.discover_feed()` | Get discovery feed from initial page (kinda like suggested posts for first time users) | Guest           |
| `.user_feed()`     | Get Parleys and echoes from a specified username                                       | Guest           |
| `.trending()`      | Get trending posts (today / top)                                                       | Guest           |
| `.feed()`          | Get feed                                                                               | Authenticated   |
| `.users()`         | Search for users                                                                       | Authenticated   |
| `.hashtags()`      | Search for hashtags                                                                    | Authenticated   |
| `.following()`     | Get following profiles from specified username                                         | Authenticated   |
| `.comments()`      | Get comments from a specified post ID                                                  | Authenticated   |
| `.follow_user()`   | Follow a specified username                                                            | Authenticated   |

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
