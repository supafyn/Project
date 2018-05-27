import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['bobmovies.pro']
        self.base_link = 'http://bobmovies.pro'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url  % (search_id.replace(':', ' ').replace(' ', '+'))

            search_results = client.request(url)
            match = re.compile('<div id="post.+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(search_results)
            for row_url, row_title in match:
                if cleantitle.get(title) in cleantitle.get(row_title):
                    #if year in str(row_title):       # I commented this out so it would work on movies without a Year in their title ???
                        return row_url
            return
        except:
            failure = traceback.format_exc()
            log_utils.log('BobMoviesPro - movie - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources
            html = client.request(url)
            links = re.compile('<iframe width=".+?src="(.+?)"',re.DOTALL).findall(html)

            for link in links:
                quality,info = source_utils.get_release_quality(link, url)
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('BobMoviesPro - sources - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url