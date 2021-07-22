# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from .openload import PhantomJSwrapper


class VUPLOADIE(InfoExtractor):
    _VALID_URL = r'https?://vupload\.com/(?P<id>[a-z0-9]+)'
    _TEST = {
        'url': 'https://vupload.com/b61tg89jyi72',
        'info_dict': {
            'id': 'b61tg89jyi72',
            'title': 'md5:74c82229b059846a82628e60dcc661b5',
            'ext': 'mp4',
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(
            'https://vupload.com/%s' % video_id, video_id, headers={'user-agent': 'curl/7.76.1'})

        obfu = self._search_regex(
            r'<script type=\'text\/javascript\'>eval\((?P<obfu>.+)\)',
            webpage, 'obfu')

        phantom = PhantomJSwrapper(self, required_version='2.0')
        data = phantom.eval('''
          const videojs = (_, sources) => (window.sources = sources)
          const result = String(%s)
          eval(result.split(';')[0])
          return {
            thumbnail: window.sources.poster,
            m3u8: window.sources.sources.filter(s => s.type === 'application/x-mpegURL')[0].src
          }
        ''' % obfu, video_id, parse_json=True, note='Deobfuscating')

        title = self._search_regex(
            r'<title>(?P<title>.+) - VUP<\/title>',
            webpage, 'title', group='title')

        formats = self._extract_m3u8_formats(data.get('m3u8'), video_id, ext='mp4')
        self._sort_formats(formats)

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'thumbnail': data.get('thumbnail'),
        }
