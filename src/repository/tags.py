from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.database.models import Tag, User
from src.schemas import TagModel


async def get_tags(skip: int, limit: int, user: User, db: Session) -> List[Tag]:
    """
    The get_tags function returns a list of tags for the given user.

    :param skip: int: Skip the first n tags
    :param limit: int: Limit the number of tags returned
    :param user: User: Get the tags for a specific user
    :param db: Session: Pass the database session to the function
    :return: A list of tags
    :doc-author: Trelent
    """
    return db.query(Tag).filter(Tag.user_id == user.id).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, user: User, db: Session) -> Tag:
    """
    The get_tag function takes in a tag_id and user, and returns the Tag object with that id.
        If no such tag exists, it raises an HTTPException.

    :param tag_id: int: Specify the tag id that we want to get from the database
    :param user: User: Get the user's tags
    :param db: Session: Pass the database session to the function
    :return: The tag with the given id if it exists and is owned by the user
    :doc-author: Trelent
    """
    return db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()


async def create_tag(body: TagModel, user: User, db: Session) -> Tag:
    """
    The create_tag function creates a new tag in the database.

    :param body: TagModel: Pass the tag name to the function
    :param user: User: Get the user_id of the logged in user
    :param db: Session: Access the database
    :return: The newly created tag
    :doc-author: Trelent
    """
    tag = Tag(name=body.name, user_id=user.id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_tag(
    tag_id: int, body: TagModel, user: User, db: Session
) -> Tag | None:
    tag = db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()
    if tag:
        tag.name = body.name
        db.commit()
    return tag


async def remove_tag(tag_id: int, user: User, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag
