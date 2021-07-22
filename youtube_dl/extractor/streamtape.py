# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from .openload import PhantomJSwrapper


class STREAMTAPEIE(InfoExtractor):
    IE_DESC = 'Streamtape'
    _VALID_URL = r'https?://streamtape\.com/e/(?P<id>[a-zA-Z0-9]+)'
    _TEST = {
        'url': 'https://streamtape.com/e/VdzV3xrpYkfzD9',
        'info_dict': {
            'id': 'VdzV3xrpYkfzD9',
            'title': 'md5:d06fc82eb5cafd1c972c8250d41180e7',
            'ext': 'mp4',
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(
            'https://streamtape.com/e/%s' % video_id, video_id)

        videolink = self._search_regex(
            r'<script>.+ = (?P<videolink>.+);<\/script>',
            webpage, 'videolink')

        videolink_clear = re.sub(r"[ +'\"]", "", videolink)

        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'thumbnail': self._og_search_thumbnail(webpage),
            'formats': [{
                'url': videolink_clear + '&stream=1',
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
                    'referrer': 'https://streamtape.com/'
                }
            }]
        }
