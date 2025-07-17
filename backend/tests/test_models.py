from db.db_models import User

def test_password_hashing():
    """
    Tests the password setting and checking functions in the User model.
    """
    u = User(username='testuser')
    u.set_password('my-secret-password')

    assert u.password_hash is not None
    assert u.password_hash != 'my-secret-password'
    assert u.check_password('my-secret-password')
    assert not u.check_password('wrong-password')
