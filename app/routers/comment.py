from fastapi import HTTPException, status, APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .. import schemas, oauth2, database, models
from typing import List, Optional

router = APIRouter(
    tags=['Comments']
)


@router.post("/posts/{id_post}/comments", status_code=status.HTTP_201_CREATED, 
             response_model=schemas.CommentResponse)
def create_comment(id_post: int, Comment_details: schemas.CommentCreate, db: Session=Depends(database.get_db),
                   current_user: dict = Depends(oauth2.get_current_user)):
    
    parent_post = db.query(models.Post).filter(models.Post.id == id_post).first()

    if not parent_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the id: {id_post} not found')
    
    new_comment = models.Comment(
        content = Comment_details.content,
        post_id = id_post,
        owner_id = current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment




@router.get("/posts/{id_post}/comments", response_model=List[schemas.CommentResponse])
def get_all_comments(id_post: int, db: Session=Depends(database.get_db),
                     current_user: dict = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, 
                     search: Optional[str] = ""):
    """
    Get all the comments to a single post
    """
    
    parent_post = db.query(models.Post).filter(models.Post.id == id_post).first()

    if not parent_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the id: {id_post} not found')
    else:
        comments_query = db.query(models.Comment).filter(
                models.Comment.post_id == id_post,
            )

        if not comments_query.all():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                details=f"Comments for the post with id: {id_post} not found")

        if search:
            comments = comments_query.filter(
                models.Comment.content.ilike(f"%{search}%")
            ).limit(limit).offset(skip).all()
            return comments
        else:
            return comments_query.all()
    



@router.get("/posts/{id_post}/comments/{id_comment}", response_model=schemas.UserResponse)
def get_a_comment(id_post: int, id_comment: int, db: Session=Depends(database.get_db),
                  current_user: dict = Depends(oauth2.get_current_user)):
    """
    Get the a single comment to a post. first we check the existence of the post and then the comment
    """
    parent_post = db.query(models.Post).filter(models.Post.id == id_post).first()

    if not parent_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the id: {id_post} not found')
    else:
        comment = db.query(models.Comment).filter(
            models.Comment.post_id == id_post, 
            models.Comment.id == id_comment
        ).first()

        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                details=f"Comment with the id: {id_comment} for the post with id: {id_post} not found")
        else:
            return comment

    



@router.delete("/posts/{id_post}/comments/{id_comment}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id_post: int, id_comment: int, db: Session=Depends(database.get_db),
                  current_user: dict = Depends(oauth2.get_current_user)):
    
    parent_post = db.query(models.Post).filter(models.Post.id == id_post).first()

    if not parent_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the id: {id_post} not found')
    
    comment_query = db.query(models.Comment).filter(
        models.Comment.post_id == id_post, 
        models.Comment.id == id_comment
    )
    comment = comment_query.first() 

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with the id: {id_comment} for the post with id: {id_post} not found")

    # Authorization Check
    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform requested action")
    
    comment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/posts/{id_post}/comments/{id_comment}", response_model=schemas.CommentResponse)
def update_comment(id_post: int, id_comment: int, updated_comment: schemas.CommentCreate, 
                   db: Session = Depends(database.get_db), 
                   current_user: models.User = Depends(oauth2.get_current_user)):

    comment_query = db.query(models.Comment).filter(
        models.Comment.post_id == id_post, 
        models.Comment.id == id_comment
    )
    comment = comment_query.first()

    if not comment :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id: {id_comment} not found on post {id_post}.")

    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform requested action.")
    
    
    comment_query.update(updated_comment.model_dump(), synchronize_session=False)
    db.commit()
    
    return comment_query.first()