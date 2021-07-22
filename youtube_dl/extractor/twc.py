# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from .openload import PhantomJSwrapper


class TWCIE(InfoExtractor):
    IE_NAME='The Watch Cartoon Online'
    BASE_URL = 'https://www.thewatchcartoononline.tv'
    _VALID_URL = r'https?://(www\.)?thewatchcartoononline\.tv/(?P<id>[a-z0-9-]+)'
    _TEST = {
        'url': 'https://www.thewatchcartoononline.tv/young-robin-hood-episode-1-the-wild-boar-of-sherwood',
        'info_dict': {
            'id': 'young-robin-hood-episode-1-the-wild-boar-of-sherwood',
            'title': 'md5:21cac98ed9d84ba4485cc038f4830c3a',
            'ext': 'mp4',
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage('https://thewatchcartoononline.tv/%s' % video_id, video_id)

        obfu = self._search_regex(
            r'<script>(?P<obfu>.+decodeURIComponent.+)</script>',
            webpage, 'obfu')

        phantom = PhantomJSwrapper(self, required_version='2.0')
        iframe_url = phantom.eval('''
          %s;
          return document.getElementsByTagName('iframe')[0].src
        ''' % obfu, video_id, note='Deobfuscating')

        iframe = self._download_webpage(self.BASE_URL + iframe_url, video_id, headers={
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          'cache-control': 'no-cache',
          'pragma': 'no-cache',
          'sec-fetch-dest': 'iframe',
          'sec-fetch-mode': 'navigate',
          'sec-fetch-site': 'same-origin',
          'upgrade-insecure-requests': '1',
          'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
          'referrer': 'https://www.thewatchcartoononline.tv/anime/',
        })

        api = self._search_regex(
            r'getJSON\(\"(?P<url>[/a-z0-9-.?=A-Z%&]+)\"',
            iframe, 'url')

        json = self._download_json(self.BASE_URL + api, video_id, headers={
          'accept': 'application/json, text/javascript, */*; q=0.01',
          'cache-control': 'no-cache',
          'pragma': 'no-cache',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'x-requested-with': 'XMLHttpRequest',
          'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
          'referrer': self.BASE_URL + api,
        })

        formats = []

        headers = {
          'accept': '*/*',
          'cache-control': 'no-cache',
          'pragma': 'no-cache',
          'range': 'bytes=0-',
          'sec-fetch-dest': 'video',
          'sec-fetch-mode': 'no-cors',
          'sec-fetch-site': 'cross-site',
          'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
          'referrer': self.BASE_URL + api,
        }

        if 'hd' in json and json.get('hd') != '':
          formats.append({
            'format_id': 'hd',
            'url': json.get('server') + '/getvid?evid=' + json.get('hd'),
            'width': 1080,
            'ext': 'mp4',
            'http_headers': headers,
          })

        formats.append({
          'format_id': 'sd',
          'url': json.get('server') + '/getvid?evid=' + json.get('enc'),
          'ext': 'mp4',
          'http_headers': headers,
        })

        self._sort_formats(formats)

        title = self._search_regex(
            r'<title>Watch (?P<title>.+)<\/title>',
            webpage, 'title', group='title')

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'thumbnail': '',
            'headers': headers
        }
