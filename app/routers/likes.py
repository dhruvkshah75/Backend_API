from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2, database

router = APIRouter(
    prefix="/likes",
    tags=['Likes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like_item(like: schemas.Like, db: Session = Depends(database.get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    """
    FLow of the func:
    Defining the LikeModel we want the Like_post or Like_comment 
    Now setting the Target model that is the model we want depending on liking a post or a comment
    setting the target_id_column which is the id of post or column depending on the target type

    """
    
    if like.target_type == 'post':
        LikeModel = models.Likes_posts  
        TargetModel = models.Post      
        target_id_column = LikeModel.post_id

    elif like.target_type == 'comment':
        LikeModel = models.Like_comments
        TargetModel = models.Comment
        target_id_column = LikeModel.comment_id

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid target_type. Must be 'post' or 'comment'."
        )

    target_item = db.query(TargetModel).filter(TargetModel.id == like.target_id).first()
    if not target_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{like.target_type.capitalize()} with ID: {like.target_id} not found."
        )

    like_query = db.query(LikeModel).filter(
        target_id_column == like.target_id,   # made like to post or comment 
        LikeModel.user_id == current_user.id  # has the current user made a like or not 
    )
    found_like = like_query.first()

    if like.direction == 1:  # to make a like
        if found_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"User {current_user.id} has already liked this {like.target_type} {like.target_id}"
            )

        new_like_data = {
            'user_id': current_user.id,
            target_id_column.key: like.target_id 
        }
        new_like = LikeModel(**new_like_data)

        db.add(new_like)
        db.commit()
        return {"message": f"Successfully liked {like.target_type}"}

    else:  # to remove the like
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User {current_user.id} has not liked this {like.target_type} {like.target_id}"
            )
        
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": f"Successfully unliked {like.target_type}"}