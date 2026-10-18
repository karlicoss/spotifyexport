

Export your personal Spotify data: playlists, saved tracks/albums/shows, etc. as JSON.

<!-- Keep this separator: Quarto otherwise moves the generated preamble below the following heading. -->

# Setting up

1.  The easiest way is `pip3 install --user git+https://github.com/karlicoss/spotifyexport`.

    Alternatively, clone the repository and run `pip3 install --editable .`.

2.  To use the API, you need to create a new app on [Spotify for Developers](https://developer.spotify.com/dashboard/applications)

    For `redirect_uri`: you can pick pretty much anything, e.g. `https://github.com`. After that you’ll get `client_id` and `client_secret`.

3.  On the first script run, you’ll be prompted to approve the script access.

    Once approved, the token is saved to `cache_path` (will be created if doesn’t exist). After that you won’t need to enter the password again as long as you pass the same `cache_path`.

# Exporting

Usage:

**Recommended**: create `secrets.py` keeping your API parameters, e.g.:

    client_id = "CLIENT_ID"
    client_secret = "CLIENT_SECRET"
    redirect_uri = "REDIRECT_URI"
    cache_path = "CACHE_PATH"

After that, use:

    python3 -m spotifyexport.export --secrets /path/to/secrets.py

That way you type less and have control over where you keep your plaintext secrets.

**Alternatively**, you can pass parameters directly, e.g.

    python3 -m spotifyexport.export --client_id <client_id> --client_secret <client_secret> --redirect_uri <redirect_uri> --cache_path <cache_path>

However, this is verbose and prone to leaking your keys/tokens/passwords in shell history.

I **highly** recommend checking exported files at least once just to make sure they contain everything you expect from your export.
If they don’t, please feel free to ask or raise an issue!

# API limitations

- you might want to do a [GDPR export](https://www.spotify.com/uk/privacy/#privacy-center-control-section) in addition, just in case

- [“Recently played”](https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played) API endpoint **only returns the 50 most recent tracks**, which makes it kind of useless unless you export the data every hour or so.

  If you care about them, might be a good idea to connect Spotify to Last.FM.

  GPDR export has more tracks, but also seems incomplete (e.g. my data is missing first few years).

# Using the data

## TODO need to implement the data access bit

# Updating README

This README is generated from a ‘literate’ Quarto [README.qmd](README.qmd) via the following command:

`tox -e quarto`

If you want to correct something, feel free to simply update `README.md` though, I can reconcile the changes next time I regenerate it.
