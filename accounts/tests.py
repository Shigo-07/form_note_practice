from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
class UserManagerTests(TestCase):
    # スーパーユーザーが権限通り作成できるか
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="test@test.edu",
            password="secret",
        )

        super_user = get_user_model().objects.get(email="test@test.edu")
        self.assertEqual(super_user.is_staff, True)
        self.assertEqual(super_user.is_admin, True)
        self.assertEqual(super_user.is_python_student, True)

    # スタッフユーザーを権限通り作成できるか
    def test_create_staffuser(self):
        user = get_user_model().objects.create_staffuser(
            email="test@test.edu",
            password="secret",
        )
        super_user = get_user_model().objects.get(email="test@test.edu")
        self.assertEqual(super_user.is_staff, True)
        self.assertEqual(super_user.is_admin, False)
        self.assertEqual(super_user.is_python_student, True)
