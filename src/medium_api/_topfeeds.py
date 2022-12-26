"""
topfeeds module containing `TopFeeds` class.
"""

class TopFeeds:
    """TopFeeds Class
    
    With `TopFeeds` object, you can use the following properties and methods:

        - topfeeds.ids
        - topfeeds.articles
        - topfeeds.fetch_articles()

    Note:
        `TopFeeds` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.topfeeds`.

    """
    def __init__(self, tag, mode, get_resp, fetch_articles, fetch_users):
        self.tag = str(tag)
        self.mode = str(mode)
        self.__get_resp = get_resp
        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users

        self.__ids = None
        self.__articles = None

    @property
    def ids(self):
        """To get a list of topfeeds `article_ids`
        
        Returns:
            list[str]: A list of `article_ids` (str) from the topfeeds for the given
            `tag` and `mode`.
        
        """
        if self.__ids is None:
            resp, _ = self.__get_resp(f'/topfeeds/{self.tag}/{self.mode}')
            self.__ids = list(resp['topfeeds'])

        return self.__ids

    @property
    def articles(self):
        """To get a list of topfeeds `Article` objects
        
        Returns:
            list[Article]: A list of `Article` objects from the topfeeds for the given
            `tag` and `mode`.
        
        """
        from medium_api._article import Article

        if self.__articles is None:
            self.__articles = [Article(article_id=article_id, 
                                       get_resp=self.__get_resp, 
                                       fetch_articles=self.__fetch_articles,
                                       fetch_users=self.__fetch_users,
                                       save_info=False) 
                                for article_id in self.ids]

        return self.__articles

    def fetch_articles(self, max_len=None, content=False, markdown=False):
        """To fetch all the topfeeds articles information (multithreading)

        Args:
            max_len (int, optional): Maximum number of articles to fetch

            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the article as well. Otherwise, default is `False`.

            markdown (bool, optional): Set it to `True` if you want to fetch the markdown of 
                the article as well. Otherwise, default is `False`

        Returns:
            None: All the fetched information will be access via topfeeds.articles.

            ``topfeeds.articles[0].title``
            ``topfeeds.articles[1].claps``
        """
        self.__fetch_articles(self.articles, max_len=max_len, content=content, markdown=markdown)