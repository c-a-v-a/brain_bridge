"""Module providing CRUD operations for the 'comments' collection."""

from bson import ObjectId
from typing import List

from crud.mongodb_connector import MongoDBConnector
from models.comment import Comment, CommentFilter


client = MongoDBConnector()
db = client.get_db()
comments = db["comments"]


async def create_comment(user_id: str, comment: Comment) -> Comment:
    """Insert new comment to the database and return it.

    Args:
        user_id (str): Id of the comment's creator.
        comment (Comment): Comment that will be inserted.

    Returns:
        Comment: An inserted comment.
    """
    comment.user_id = user_id
    doc = comment.model_dump(by_alias=True, exclude_none=True)
    result = await comments.insert_one(doc)
    doc["_id"] = str(result.inserted_id)

    return Comment(**doc)


async def get_comments(filters: CommentFilter) -> List[Comment]:
    """Get comments that match the filter.
    
    Args:
        filter (CommentFilter): A filters used when searching for the comment.

    Returns
        List[Comment]: All comments that match the filter.
    """
    query = filters.model_dump(exclude_none=True, by_alias=True)

    if not query:
        return None

    cursor = comments.find(query)
    result = []

    async for doc in cursor:
        result.append(Comment.validate(doc))

    return result


async def delete_comment(comment_id: str, user_id: str) -> bool:
    """Remove the comment if it belongs to the user.
    
    Args:
        comment_id: Id of the comment that should be removed.
        user_id: Id of the user that tries to remove the comment.

    Returns:
        bool: True if the comment was removed, False otherwise.
    """
    result = await comments.collection.delete_one({
            "_id": ObjectId(comment_id),
            "user_id": user_id,
        })

    return result.deleted_count == 1
