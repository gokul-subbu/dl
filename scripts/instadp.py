import argparse
import re
import sys
import requests


def fetchDP(username):
    url = f'https://www.instagram.com/{username}/?__a=1'
    r = requests.get(url)
    if r.ok:
        data = r.json()
        return data['graphql']['user']['profile_pic_url_hd']
    else:
        print('😥😥😥😥😥 Cannot find user ID')
        sys.exit()


def main():
    parser = argparse.ArgumentParser(
        description='Download any users Instagram display picture/profile picture in full quality')

    parser.add_argument('username', action='store', help='username of the Instagram user')

    args = parser.parse_args()

    username = args.username

    file_url = fetchDP(username)
    fname = username + '.jpg'

    r = requests.get(file_url, stream=True)
    if r.ok:
        with open(fname, 'wb') as f:
            f.write(r.content)
            print(f'✔ Downloaded: {fname}')
    else:
        print('😘😘😘😘😘😘😘 Cannot make connection to download image')


if __name__ == "__main__":
    main()