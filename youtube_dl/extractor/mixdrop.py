# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from .openload import PhantomJSwrapper


class MixDropIE(InfoExtractor):
    _VALID_URL = r'https?://mixdrop\.co/[ef]/(?P<id>[a-z0-9]+)'
    _TEST = {
        'url': 'https://mixdrop.co/e/qll48gm3tn6q74',
        'info_dict': {
            'id': 'qll48gm3tn6q74',
            'title': 'md5:64aa9a55fd58249a26902e82091d8e18',
            'ext': 'mp4',
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(
            'https://mixdrop.co/e/%s' % video_id, video_id)

        code = self._search_regex(
            r';\n(?P<code>eval\(.+\))',
            webpage, 'code')

        phantom = PhantomJSwrapper(self, required_version='2.0')
        data = phantom.eval('''
            MDCore = {}
            %s;
            return MDCore
        ''' % code, video_id, parse_json=True, note='Deobfuscating')

        title = self._search_regex(
            r'<a href="/f/[a-z0-9]+" target="_blank">(?P<title>.+)</a>',
            webpage, 'title', group='title')

        return {
            'id': video_id,
            'title': title,
            'formats': [{
                'url': 'https:' + data.get('wurl'),
                'ext': 'mp4',
                'http_headers': {
                    'accept': '*/*',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'range': 'bytes=0-',
                    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'video',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'sec-gpc': '1',
                    'referrer': 'https://mixdrop.co/'
                }
            }],
            'thumbnail': 'https:' + data.get('poster'),
        }
