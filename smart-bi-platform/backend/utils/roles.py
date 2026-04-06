@router.post("/register")
def register(
    user: UserCreate,
    organization_name: str,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create organization
    org = Organization(name=organization_name)

    db.add(org)
    db.commit()
    db.refresh(org)

    # First user = Admin
    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        organization_id=org.id,
        role="admin"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered",
        "organization_id": org.id,
        "role": "admin"
    }