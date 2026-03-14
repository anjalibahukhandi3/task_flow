from sqlalchemy.orm import Session
import models, database, auth

def manual_register():
    db = next(database.get_db())
    email = "test@example.com"
    user_exists = db.query(models.User).filter(models.User.email == email).first()
    if user_exists:
        print(f"User {email} already exists")
        return
    
    hashed_password = auth.get_password_hash("password123")
    db_user = models.User(
        name="Test User",
        email=email,
        hashed_password=hashed_password,
        role=models.RoleEnum.user
    )
    db.add(db_user)
    db.commit()
    print(f"Successfully registered {email}")

if __name__ == "__main__":
    try:
        manual_register()
    except Exception as e:
        print(f"Error: {str(e)}")
