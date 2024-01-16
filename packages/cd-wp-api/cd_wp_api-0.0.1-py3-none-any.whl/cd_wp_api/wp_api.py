import wordpress_api
from dateutil import parser


class WordPressManager:
    """
    A manager class for interacting with a WordPress site using the wordpress-api library.
    Handles common tasks like creating, updating, deleting posts, and managing tags and categories.
    """

    def __init__(self, url, username, password):
        """
        Initialize the WordPressManager with site credentials.

        Args:
            url (str): The URL of the WordPress site.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        self.client = wordpress_api.Client(url, username, password)

    def create_post(self, title, description, content, tags=None, categories=None, scheduled_datetime=None):
        """
        Create a new post on the WordPress site.

        Args:
            title (str): The title of the post.
            description (str): A short description or excerpt of the post.
            content (str): The main content/body of the post.
            tags (list, optional): A list of tags for the post.
            categories (list, optional): A list of categories for the post.
            scheduled_datetime (str, optional): The datetime when the post should be published in string format.
                                                If set to a future date, the post will be scheduled.

        Returns:
            dict: The created post data.
        """
        data = {
            "title": title,
            "excerpt": description,
            "content": content,
            "status": "publish"
        }

        if tags:
            data["tags"] = self.get_or_create_tags(tags)

        if categories:
            data["categories"] = self.get_or_create_categories(categories)

        if scheduled_datetime:
            datetime_obj = self.parse_datetime(scheduled_datetime)
            data["date"] = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S')

        return self.client.posts().create(data)

    def update_post(self, post_id, title=None, description=None, content=None, tags=None, categories=None, scheduled_datetime=None):
        """
        Update an existing post on the WordPress site.

        Args:
            post_id (int): The ID of the post to update.
            title (str, optional): Updated title of the post.
            description (str, optional): Updated short description or excerpt of the post.
            content (str, optional): Updated content/body of the post.
            tags (list, optional): Updated list of tags for the post.
            categories (list, optional): Updated list of categories for the post.
            scheduled_datetime (str, optional): The datetime when the post should be published in string format.
                                                If set to a future date, the post will be rescheduled.

        Returns:
            dict: The updated post data.
        """
        data = {}
        if title:
            data["title"] = title
        if description:
            data["excerpt"] = description
        if content:
            data["content"] = content

        if tags:
            data["tags"] = self.get_or_create_tags(tags)

        if categories:
            data["categories"] = self.get_or_create_categories(categories)

        if scheduled_datetime:
            datetime_obj = self.parse_datetime(scheduled_datetime)
            data["date"] = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S')

        return self.client.posts().update(post_id, data)

    def delete_post(self, post_id, force=False):
        """
        Delete a post from the WordPress site.

        Args:
            post_id (int): The ID of the post to delete.
            force (bool, optional): If True, the post will be permanently deleted.
                                    Otherwise, it will be moved to the trash.

        Returns:
            dict: The deleted post data.
        """
        return self.client.posts().delete(post_id, force=force)

    def get_or_create_tags(self, tag_names):
        """
        Retrieve IDs of existing tags or create them if they don't exist.

        Args:
            tag_names (list): A list of tag names.

        Returns:
            list: A list of tag IDs.
        """
        tag_ids = []
        for tag_name in tag_names:
            tags = self.client.tags().list(search=tag_name)
            if tags:
                tag_ids.append(tags[0]["id"])
            else:
                new_tag = self.client.tags().create({"name": tag_name})
                tag_ids.append(new_tag["id"])
        return tag_ids

    def get_or_create_categories(self, category_names):
        """
        Retrieve IDs of existing categories or create them if they don't exist.

        Args:
            category_names (list): A list of category names.

        Returns:
            list: A list of category IDs.
        """
        category_ids = []
        for category_name in category_names:
            categories = self.client.categories().list(search=category_name)
            if categories:
                category_ids.append(categories[0]["id"])
            else:
                new_category = self.client.categories().create({"name": category_name})
                category_ids.append(new_category["id"])
        return category_ids

    def get_categories(self):
        """
        Retrieve all categories from the WordPress site.

        Returns:
            list: A list of categories, where each category is represented as a dictionary.
        """
        return self.client.categories().list()
