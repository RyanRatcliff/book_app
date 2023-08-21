from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection


BOOKS = [
    {
        "id": "847383e0-fa9f-4025-9d03-6325d84c25f7",
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "rating": 4,
    },
    {
        "id": "45d35eeb-a27b-4df8-a89d-4f5e98730b12",
        "title": "The Ultimate Hitchhiker's Guide",
        "author": "Douglas Adams",
        "rating": 4,
    },
    {
        "id": "44069053-23c3-4185-a95f-0534ca7465c5",
        "title": "A Short History of Nearly Everything",
        "author": "Bill Bryson",
        "rating": 4,
    },
    {
        "id": "4246970c-1c19-4ee9-a280-5717b6929661",
        "title": "Bill Bryson's African Diary",
        "author": "Bill Bryson",
        "rating": 3,
    },
    {
        "id": "a1ab70c2-27e9-4052-a2cb-c3a14e0f72bc",
        "title": "Bryson's Dictionary of Troublesome Words",
        "author": "Bill Bryson",
        "rating": 3,
    },
    {
        "id": "545cb2fb-1922-4d7e-953c-62d5cb974453",
        "title": "In a Sunburned Country",
        "author": "Bill Bryson",
        "rating": 4,
    },
    {
        "id": "baf13c76-62a9-4d2d-995b-89f588350554",
        "title": "I'm a Stranger Here Myself",
        "author": "Bill Bryson",
        "rating": 3,
    },
]


class AuthorIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        # You can override the index name by setting it below
        index_name = "AuthorsIndex"
        billing_mode = "PAY_PER_REQUEST"
        # All attributes are projected
        projection = AllProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    author = UnicodeAttribute(hash_key=True)


class DynamoBook(Model):
    class Meta:
        table_name = "Book"
        region = "us-east-2"
        billing_mode = "PAY_PER_REQUEST"

    id = UnicodeAttribute(hash_key=True)
    title = UnicodeAttribute()
    author = UnicodeAttribute()
    author_index = AuthorIndex()
    rating = NumberAttribute()


if not DynamoBook.exists():
    DynamoBook.create_table(wait=True)
    for book in BOOKS:
        # generate a Book from row
        book = DynamoBook(
            id=book["id"],
            title=book["title"],
            author=book["author"],
            rating=book["rating"],
        )
        book.save()
    print("Table Book created.")
