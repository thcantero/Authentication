"""Seed file to sample database."""

from app import app
from models import db, User, Feedback
from sqlalchemy.exc import IntegrityError

with app.app_context():
    # Drop & recreate tables (optional)
    db.drop_all()
    db.create_all()

    # Clear out any existing rows
    User.query.delete()
    Feedback.query.delete()

    # ----- Create multiple users -----
    user1 = User.register(
        username="alice",
        pwd="password123",
        email="alice@example.com",
        first_name="Alice",
        last_name="Wonderland"
    )
    user2 = User.register(
        username="bob",
        pwd="secret456",
        email="bob@example.com",
        first_name="Bob",
        last_name="Builder"
    )
    user3 = User.register(
        username="carol",
        pwd="carol789",
        email="carol@example.com",
        first_name="Carol",
        last_name="Smith"
    )
    user4 = User.register(
        username="david",
        pwd="david101",
        email="david@example.com",
        first_name="David",
        last_name="Johnson"
    )

    db.session.add_all([user1, user2, user3, user4])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    # ----- Create multiple feedback items -----
    feedbacks = [
        Feedback(title="My first feedback", content="Loving this platform so far!", user_id=user1.id),
        Feedback(title="Feature request", content="Can we get a dark mode option?", user_id=user1.id),
        Feedback(title="Question", content="How do I reset my password?", user_id=user2.id),
        Feedback(title="Review", content="The UI is super intuitive. Keep it up!", user_id=user2.id),
        Feedback(title="Bug report", content="I ran into a small glitch on the profile page.", user_id=user3.id),
        Feedback(title="General Feedback", content="Everything works great, thanks!", user_id=user3.id),
        Feedback(title="Testing 1 2 3", content="Just testing the feedback feature...", user_id=user4.id),
        Feedback(title="Workflow tips", content="Loving the new workflow, but could use a tutorial.", user_id=user4.id),
    ]

    db.session.add_all(feedbacks)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    print("Seeding Complete!")
