# crud/comments.py
from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from crud.mongodb_connector import MongoDBConnector
from models.comment import CommentCreate, CommentInDB

COMMENTS_COLLECTION = "comments"


class CommentCRUD:
    def __init__(self, db: MongoDBConnector):
        
        self.db = db.get_db()
        self.collection = self.db[COMMENTS_COLLECTION]

    async def create_comment(
        self,
        user_id: str,
        data: CommentCreate,
    ) -> CommentInDB:
        doc = {
            "idea_id": data.idea_id,
            "content": data.content,
            "user_id": user_id,
            "created_at": datetime.utcnow(),
        }

        result = await self.collection.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return CommentInDB(**doc)

    async def get_comments_for_idea(self, idea_id: str) -> List[CommentInDB]:
        cursor = self.collection.find({"idea_id": idea_id}).sort("created_at", 1)
        comments: List[CommentInDB] = []

        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            comments.append(CommentInDB(**doc))

        return comments

    async def get_comment(self, comment_id: str) -> Optional[CommentInDB]:
        doc = await self.collection.find_one({"_id": ObjectId(comment_id)})
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return CommentInDB(**doc)

    async def delete_comment(self, comment_id: str, user_id: str) -> bool:
        """Usuń komentarz tylko jeśli należy do usera."""
        result = await self.collection.delete_one(
            {
                "_id": ObjectId(comment_id),
                "user_id": user_id,
            }
        )
        return result.deleted_count == 1
