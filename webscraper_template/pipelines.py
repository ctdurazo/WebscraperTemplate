import pymongo
from itemadapter import ItemAdapter


class WebscraperTemplatePipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    """Define an Item Pipeline to write data to MongoDB.
    An Item pipeline is just a regular Python class with some
    predefined methods that will be used by Scrapy.
    """

    def __init__(self, mongo_uri, mongo_db):
        """Init the Item pipeline with settings for MongoDB."""
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """Create a pipeline instance from a Crawler.
        A Crawler object provides access to all Scrapy core components
        like settings.
        This method must return a new instance of the pipeline.
        """
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "bowlingdb"),
        )

    def open_spider(self, spider):
        """Connect to MongoDB when the spider is opened."""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[spider.name]
        # Start with a clean database
        self.collection.delete_many({})


    def close_spider(self, spider):
        """Close the connection to MongoDB when the spider is closed."""
        self.client.close()

    def process_item(self, item, spider):
        """Process the items one by one.
        Here you can filter some data, normalize the data, or save it
        to an external database as we are doing here.
        Specially, in modern Scrapy projects, ItemAdapter provides a
        common interface that can be used to deal with all kinds Item
        types such as dictionaries, Item objects, dataclass objects,
        and attrs objects.
        Reference:
          - https://docs.scrapy.org/en/latest/topics/items.html#item-types
        """
        item_dict = ItemAdapter(item).asdict()
        self.collection.insert_one(item_dict)
        return item