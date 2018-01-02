import argparse
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

def parser():
    """Argument Parser"""
    argparser = argparse.ArgumentParser('telbot.py')
    argparser.add_argument('--username', help='Spotify Username', required=True)
    argparser.add_argument('--scope', help='Scope', required=False)
    argparser.add_argument('--debug', help='Enable Debug Logging...' , action='store_true')
    return argparser.parse_args()

if __name__ == "__main__":
    args = parser()
    username = args.username
    scope = args.scope
    client_credentials_manager = SpotifyClientCredentials(client_id='c61d66e13fcf4210aca7056025ea6274',client_secret='2e4e008bb8344aaf9cb807deb4aa528a')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    print sp.user('me')
    #token = util.prompt_for_user_token(username, scope)

#playlists = sp.user_playlists('stamatiou.antonis')
