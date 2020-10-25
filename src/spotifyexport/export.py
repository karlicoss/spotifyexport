#!/usr/bin/env python3
import argparse
import json
from functools import lru_cache
import sys
from typing import List

import spotipy # type: ignore[import]

from .exporthelpers import logging_helper
from .exporthelpers.export_helper import Json


logger = logging_helper.logger('spotifyexport')


def _cleanup(j: Json) -> Json:
    '''
    Clean up irrelevant (hopefully?) stuff from the data.
    '''
    # NOTE: for now not used.. maybe make it an optional cmdline flag?
    artists = j['track']['album']['artists'] + j['track']['artists']
    for k in ('external_urls', ):
        for a in artists:
            del a[k]
    for k in ('available_markets', 'images', 'external_urls', 'href', 'uri', 'release_date_precision'):
        del j['track']['album'][k]
    for k in ('available_markets', 'preview_url', 'external_ids', 'external_urls', 'href', 'uri'):
        del j['track'][k]
    return j


def as_list(api_method) -> List[Json]:
    results: List[Json] = []
    while True:
        offset = len(results)
        cres = api_method(limit=50, offset=offset)
        chunk = cres['items']
        total = cres['total']
        logger.debug('%s: collected: %d/%d', api_method, len(results), total)
        if len(results) >= total:
            break
        results.extend(chunk)
        # todo log?
    return results


class Exporter:
    SCOPE = 'playlist-read-private,user-library-read,user-read-recently-played'

    def __init__(self, **kwargs) -> None:
        kw = {
            'scope'       : self.SCOPE,
            'open_browser': False,
        }
        kw.update(kwargs)
        auth = spotipy.oauth2.SpotifyOAuth(**kw)
        self.api = spotipy.Spotify(auth_manager=auth)

    def export_json(self) -> Json:
        playlists = as_list(self.api.current_user_playlists)
        for p in playlists:
            pid = p['id']
            p['tracks'] = as_list(lambda *args, **kwargs: self.api.playlist_items(*args, playlist_id=pid, **kwargs))
        # todo cleanup stuff??
        return dict(
            saved_tracks=as_list(self.api.current_user_saved_tracks),
            saved_albums=as_list(self.api.current_user_saved_albums),
            saved_shows =as_list(self.api.current_user_saved_shows),
            # NOTE: seems that only supports the most recent 50
            # https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played
            recently_played=self.api.current_user_recently_played(limit=50)['items'],
            playlists   =playlists,
        )


def get_json(**params):
    return Exporter(**params).export_json()


def main() -> None:
    p = make_parser()
    args = p.parse_args()

    params = args.params
    dumper = args.dumper
    j = get_json(**params)
    js = json.dumps(j, ensure_ascii=False, indent=1)
    dumper(js)


def make_parser():
    from .exporthelpers.export_helper import setup_parser, Parser
    p = Parser('Export your personal Spotify data: playlists, saved tracks/albums/shows, etc. as JSON.')
    setup_parser(
        parser=p,
        params=[
            'client_id'    ,
            'client_secret',
            'redirect_uri' ,
            'cache_path'   ,
        ]
    )
    return p


if __name__ == "__main__":
    main()


# todo https://stackoverflow.com/a/30557896 in case of too may requests
