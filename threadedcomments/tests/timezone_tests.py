__all__ = (
    "ThreadedCommentTimezoneTestCase",
    "FreeThreadedCommentTimezoneTestCase",
)


from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings
from django.utils import timezone

from threadedcomments.models import FreeThreadedComment, ThreadedComment
from threadedcomments.tests.models import Person


class ThreadedCommentTimezoneTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser', password='password',
        )
        self.topic = Person.objects.create(name='Test')
        self.content_type = ContentType.objects.get_for_model(self.topic)

    def _create_comment(self, approved=False):
        return ThreadedComment(
            user=self.user,
            content_type=self.content_type,
            object_id=self.topic.pk,
            comment='test comment',
            is_approved=approved,
        )

    @override_settings(USE_TZ=True)
    def test_date_submitted_is_aware_when_use_tz_true(self):
        comment = self._create_comment()
        comment.save()
        self.assertTrue(timezone.is_aware(comment.date_submitted))

    @override_settings(USE_TZ=False)
    def test_date_submitted_is_naive_when_use_tz_false(self):
        comment = self._create_comment()
        comment.save()
        self.assertTrue(timezone.is_naive(comment.date_submitted))

    @override_settings(USE_TZ=True)
    def test_date_modified_is_aware_when_use_tz_true(self):
        comment = self._create_comment()
        comment.save()
        self.assertTrue(timezone.is_aware(comment.date_modified))

    @override_settings(USE_TZ=False)
    def test_date_modified_is_naive_when_use_tz_false(self):
        comment = self._create_comment()
        comment.save()
        self.assertTrue(timezone.is_naive(comment.date_modified))

    @override_settings(USE_TZ=True)
    def test_date_approved_is_aware_when_use_tz_true(self):
        comment = self._create_comment(approved=True)
        comment.save()
        self.assertIsNotNone(comment.date_approved)
        self.assertTrue(timezone.is_aware(comment.date_approved))

    @override_settings(USE_TZ=False)
    def test_date_approved_is_naive_when_use_tz_false(self):
        comment = self._create_comment(approved=True)
        comment.save()
        self.assertIsNotNone(comment.date_approved)
        self.assertTrue(timezone.is_naive(comment.date_approved))


class FreeThreadedCommentTimezoneTestCase(TestCase):
    def setUp(self):
        self.topic = Person.objects.create(name='Test')
        self.content_type = ContentType.objects.get_for_model(self.topic)

    def _create_comment(self, approved=False):
        return FreeThreadedComment(
            name='Test User',
            content_type=self.content_type,
            object_id=self.topic.pk,
            comment='test comment',
            is_approved=approved,
        )

    @override_settings(USE_TZ=True)
    def test_date_submitted_is_aware_when_use_tz_true(self):
        comment = self._create_comment()
        comment.save()
        self.assertTrue(timezone.is_aware(comment.date_submitted))

    @override_settings(USE_TZ=False)
    def test_date_submitted_is_naive_when_use_tz_false(self):
        comment = self._create_comment()
        comment.save()
        self.assertTrue(timezone.is_naive(comment.date_submitted))

    @override_settings(USE_TZ=True)
    def test_date_modified_is_aware_when_use_tz_true(self):
        comment = self._create_comment()
        comment.save()
        self.assertTrue(timezone.is_aware(comment.date_modified))

    @override_settings(USE_TZ=False)
    def test_date_modified_is_naive_when_use_tz_false(self):
        comment = self._create_comment()
        comment.save()
        self.assertTrue(timezone.is_naive(comment.date_modified))

    @override_settings(USE_TZ=True)
    def test_date_approved_is_aware_when_use_tz_true(self):
        comment = self._create_comment(approved=True)
        comment.save()
        self.assertIsNotNone(comment.date_approved)
        self.assertTrue(timezone.is_aware(comment.date_approved))

    @override_settings(USE_TZ=False)
    def test_date_approved_is_naive_when_use_tz_false(self):
        comment = self._create_comment(approved=True)
        comment.save()
        self.assertIsNotNone(comment.date_approved)
        self.assertTrue(timezone.is_naive(comment.date_approved))
