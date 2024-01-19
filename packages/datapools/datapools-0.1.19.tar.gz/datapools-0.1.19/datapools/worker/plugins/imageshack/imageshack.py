import asyncio
import traceback
from typing import Union

# import httpx
from bs4 import BeautifulSoup

from ....common.logger import logger
from ....common.storage import BaseStorage
from ....common.types import (
    CrawlerBackTask,
    CrawlerContent,
    DatapoolContentType,
)
from ..base_plugin import BasePlugin, BaseTag

# from typing import List

DOMAIN="imageshack.com"

class ImageshackPlugin(BasePlugin):
    def __init__(self, storage):
        super().__init__(storage)

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        # logger.info( f'imageshack {u=}')
        return u.netloc == DOMAIN

    async def process(self, url):
        logger.info(f"imageshack::process({url})")

        logger.info(f"loading url {url}")
        r = await self.download(url)
        # logger.info( f'text: {r}')
        logger.info(f"got url content length={len(r)}")

        soup = BeautifulSoup(r, "html.parser")
        
        platform_tag = await self.get_platform_tag( DOMAIN, soup, 3600 )
        platform_tag = BaseTag("a35")  # FIXME: remove this when imageshack.com adds real tag!!!
        if platform_tag and platform_tag.is_crawling_allowed() is False:
            logger.info("Crawling disabled by tag")
            return
            

        # 1.search for photo LINKS and return them as new tasks
        links = soup.body.find_all("a", attrs={"class": "photo"})

        for l in links:
            yield CrawlerBackTask(url=f'https://{DOMAIN}/{l["href"]}')

        # 2. search for photo IMAGES
        img = soup.body.find("img", attrs={"id": "lp-image"})
        if img:
            logger.info(f'found image {img["src"]}')
            
            copyright_owner_tag = None
            
            #check for user license on his public profile page
            profile_link = soup.body.find('a', attrs={"class":"profile-link"})
            if profile_link:
                #profile_link['href'] = '/user/sergpsu' test
                copyright_owner_tag = await self.parse_user_profile(profile_link['href'])
                if copyright_owner_tag is not None:
                    logger.info( f'found {copyright_owner_tag=}')
                    if copyright_owner_tag.is_crawling_allowed() is False:
                        logger.info( 'User disabled crawling')
                        return


            url = f'https://{DOMAIN}/{img["src"]}'
            #url = img['src']    #url like "//imagizer.imageshack.com/v2/465x700q70/901/KyWfgS.jpg"
            content = await self.download(url)
            if content:
                image_tag = BasePlugin.parse_image_tag(content)
                if image_tag is not None and image_tag.is_crawling_allowed() is False:
                    logger.info( f'crawling is disabled by {str(image_tag)}' )
                    return
                
                if image_tag is None and copyright_owner_tag is None and platform_tag is None:
                    logger.info( 'no tag available')
                    return
                
                storage_id = BaseStorage.gen_id(url)

                try:
                    await self.storage.put(storage_id, content)

                    yield CrawlerContent(
                        tag_id=str(image_tag) if image_tag is not None else None,
                        copyright_tag_id=str(copyright_owner_tag) if copyright_owner_tag is not None else None,
                        platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                        type=DatapoolContentType.Image,
                        storage_id=storage_id,
                        url=url,
                    )
                except Exception as e:
                    logger.error(f"failed put to storage {e}")
                    logger.error(traceback.format_exc())

                await asyncio.sleep(2)

            else:
                logger.error("failed download image")

    async def parse_user_profile(self, href) -> Union[BaseTag,None]:
        username = href.split('/')[-1]
        if not self.copyright_tags_cache.contains( username, 3600 ): 
            url = f'https://{DOMAIN}/{href}'
            
            logger.info(f"parsing user profile {url=}")

            r = await self.download(url)
            # logger.info( f'text: {r}')
            logger.info(f"got url content length={len(r)}")

            soup = BeautifulSoup(r, "html.parser")
            about = soup.body.find('div', attrs={"class":"bio tall"} )
            if about:
                self.copyright_tags_cache.set( username, BasePlugin.parse_tag_in_str( about.contents[0] ) )
            else:
                self.copyright_tags_cache.set( username, None )
        return self.copyright_tags_cache.get(username)
