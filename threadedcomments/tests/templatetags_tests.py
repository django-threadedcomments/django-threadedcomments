import datetime

from xml.dom.minidom import parseString

from django.core import mail
from django.urls import reverse
from django.template import Context, Template
from django.test import TestCase
from json import loads

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from threadedcomments.models import FreeThreadedComment, ThreadedComment
from threadedcomments.tests.models import Person
from threadedcomments.models import MARKDOWN, TEXTILE, REST, PLAINTEXT
from threadedcomments.templatetags import threadedcommentstags as tags


__all__ = ("TemplateTagTestCase",)


class TemplateTagTestCase(TestCase):
    urls = "threadedcomments.tests.threadedcomments_urls"
    extra_apps = ['threadedcomments.tests']

    def test_get_comment_url(self):
        User = get_user_model()

        user = User.objects.create_user('user', 'floguy@gmail.com', password='password')

        topic = Person.objects.create(name="Test2")
        content_type = ContentType.objects.get_for_model(topic)

        comment = ThreadedComment.objects.create_for_object(topic,
            user = user,
            ip_address = '127.0.0.1',
            comment = "My test comment!",
        )

        c = Context({
            'topic': topic,
            'parent': comment
        })
        sc = {
            "ct": content_type.pk,
            "id": topic.pk,
            "pid": comment.pk,
        }

        self.assertEquals(Template('{% load threadedcommentstags %}{% get_comment_url topic %}').render(c), u'/comment/%(ct)s/%(id)s/' % sc)
        self.assertEquals(Template('{% load threadedcommentstags %}{% get_comment_url topic parent %}').render(c), u'/comment/%(ct)s/%(id)s/%(pid)s/' % sc)
        self.assertEquals(Template('{% load threadedcommentstags %}{% get_comment_url_json topic %}').render(c), u'/comment/%(ct)s/%(id)s/json/' % sc)
        self.assertEquals(Template('{% load threadedcommentstags %}{% get_comment_url_xml topic %}').render(c), u'/comment/%(ct)s/%(id)s/xml/' % sc)
        self.assertEquals(Template('{% load threadedcommentstags %}{% get_comment_url_json topic parent %}').render(c), u'/comment/%(ct)s/%(id)s/%(pid)s/json/' % sc)
        self.assertEquals(Template('{% load threadedcommentstags %}{% get_comment_url_xml topic parent %}').render(c), u'/comment/%(ct)s/%(id)s/%(pid)s/xml/' % sc)

    def test_get_free_comment_url(self):

        topic = Person.objects.create(name="Test2")
        content_type = ContentType.objects.get_for_model(topic)

        comment = FreeThreadedComment.objects.create_for_object(topic,
            ip_address = '127.0.0.1',
            comment = "My test free comment!",
        )

        c = Context({
            'topic': topic,
            'parent': comment,
        })
        sc = {
            "ct": content_type.pk,
            "id": topic.pk,
            "pid": comment.pk,
        }

        self.assertEquals(Template('{% load threadedcommentstags %}{% get_free_comment_url topic %}').render(c), u'/freecomment/%(ct)s/%(id)s/' % sc)
        self.assertEquals(Template('{% load threadedcommentstags %}{% get_free_comment_url topic parent %}').render(c), u'/freecomment/%(ct)s/%(id)s/%(pid)s/' % sc)
        self.assertEquals(Template('{% load threadedcommentstags %}{% get_free_comment_url_json topic %}').render(c), u'/freecomment/%(ct)s/%(id)s/json/' % sc)
        self.assertEquals(Template('{% load threadedcommentstags %}{% get_free_comment_url_xml topic %}').render(c), u'/freecomment/%(ct)s/%(id)s/xml/' % sc)
        self.assertEquals(Template('{% load threadedcommentstags %}{% get_free_comment_url_json topic parent %}').render(c), u'/freecomment/%(ct)s/%(id)s/%(pid)s/json/' % sc)
        self.assertEquals(Template('{% load threadedcommentstags %}{% get_free_comment_url_xml topic parent %}').render(c), u'/freecomment/%(ct)s/%(id)s/%(pid)s/xml/' % sc)

    def test_get_comment_count(self):

        User = get_user_model()
        user = User.objects.create_user('user', 'floguy@gmail.com', password='password')

        topic = Person.objects.create(name="Test2")

        comment = ThreadedComment.objects.create_for_object(topic,
            user = user,
            ip_address = '127.0.0.1',
            comment = "My test comment!",
        )

        c = Context({
            'topic': topic,
        })

        self.assertEquals(
            Template('{% load threadedcommentstags %}{% get_comment_count for topic as count %}{{ count }}').render(c),
            u'1'
        )

    def test_get_free_comment_count(self):

        topic = Person.objects.create(name="Test2")

        comment = FreeThreadedComment.objects.create_for_object(topic,
            ip_address = '127.0.0.1',
            comment = "My test free comment!",
        )

        c = Context({
            'topic': topic,
        })

        self.assertEquals(
            Template('{% load threadedcommentstags %}{% get_free_comment_count for topic as count %}{{ count }}').render(c),
            u'1'
        )

    def test_get_threaded_comment_form(self):
        actual = Template('{% load threadedcommentstags %}{% get_threaded_comment_form as form %}{{ form }}').render(Context({}))

        # Verify textarea field
        self.assertIn('textarea', actual)
        self.assertIn('id="id_comment"', actual)
        self.assertIn('name="comment"', actual)
        self.assertIn('maxlength="1000"', actual)
        self.assertIn('required', actual)

        # Verify markup fields
        self.assertIn('value="5" selected', actual)
        self.assertIn('plaintext', actual.lower())

    def test_get_latest_comments(self):

        User = get_user_model()
        user = User.objects.create_user('user', 'floguy@gmail.com', password='password')

        topic = Person.objects.create(name="Test2")
        old_topic = topic
        content_type = ContentType.objects.get_for_model(topic)

        ThreadedComment.objects.create_for_object(topic,
            user = user,
            ip_address = '127.0.0.1',
            comment = "Test 1",
        )
        ThreadedComment.objects.create_for_object(topic,
            user = user,
            ip_address = '127.0.0.1',
            comment = "Test 2",
        )
        ThreadedComment.objects.create_for_object(topic,
            user = user,
            ip_address = '127.0.0.1',
            comment = "Test 3",
        )

        self.assertEquals(
            Template('{% load threadedcommentstags %}{% get_latest_comments 2 as comments %}{{ comments }}').render(Context({})),
            u'[&lt;ThreadedComment: Test 3&gt;, &lt;ThreadedComment: Test 2&gt;]'
        )

    def test_get_latest_free_comments(self):

        topic = Person.objects.create(name="Test2")

        FreeThreadedComment.objects.create_for_object(topic,
            ip_address = '127.0.0.1',
            comment = "Test 1",
        )
        FreeThreadedComment.objects.create_for_object(topic,
            ip_address = '127.0.0.1',
            comment = "Test 2",
        )
        FreeThreadedComment.objects.create_for_object(topic,
            ip_address = '127.0.0.1',
            comment = "Test 3",
        )

        self.assertEquals(
            Template('{% load threadedcommentstags %}{% get_latest_free_comments 2 as comments %}{{ comments }}').render(Context({})),
            u'[&lt;FreeThreadedComment: Test 3&gt;, &lt;FreeThreadedComment: Test 2&gt;]'
        )

    def test_get_threaded_comment_tree(self):

        User = get_user_model()
        user = User.objects.create_user('user', 'floguy@gmail.com', password='password')

        topic = Person.objects.create(name="Test2")

        parent1 = ThreadedComment.objects.create_for_object(topic,
            user = user,
            ip_address = '127.0.0.1',
            comment = "test1",
        )
        ThreadedComment.objects.create_for_object(topic,
            user = user,
            ip_address = '127.0.0.1',
            comment = "test2",
            parent = parent1,
        )
        parent2 = ThreadedComment.objects.create_for_object(topic,
            user = user,
            ip_address = '127.0.0.1',
            comment = "test3",
        )
        ThreadedComment.objects.create_for_object(topic,
            user = user,
            ip_address = '127.0.0.1',
            comment = "test4",
            parent = parent2,
        )

        c = Context({
            'topic': topic,
        })

        self.assertEquals(
            Template('{% load threadedcommentstags %}{% get_threaded_comment_tree for topic as tree %}[{% for item in tree %}({{ item.depth }}){{ item.comment }},{% endfor %}]').render(c),
            u'[(0)test1,(1)test2,(0)test3,(1)test4,]'
        )
        self.assertEquals(
            Template('{% load threadedcommentstags %}{% get_threaded_comment_tree for topic 3 as tree %}[{% for item in tree %}({{ item.depth }}){{ item.comment }},{% endfor %}]').render(c),
            u'[(0)test3,(1)test4,]'
        )

    def test_get_free_threaded_comment_tree(self):

        topic = Person.objects.create(name="Test2")

        parent1 = FreeThreadedComment.objects.create_for_object(topic,
            ip_address = '127.0.0.1',
            comment = "test1",
        )
        FreeThreadedComment.objects.create_for_object(topic,
            ip_address = '127.0.0.1',
            comment = "test2",
            parent = parent1,
        )
        parent2 = FreeThreadedComment.objects.create_for_object(topic,
            ip_address = '127.0.0.1',
            comment = "test3",
        )
        FreeThreadedComment.objects.create_for_object(topic,
            ip_address = '127.0.0.1',
            comment = "test4",
            parent = parent2,
        )

        c = Context({
            'topic': topic,
        })

        self.assertEquals(
            Template('{% load threadedcommentstags %}{% get_free_threaded_comment_tree for topic as tree %}[{% for item in tree %}({{ item.depth }}){{ item.comment }},{% endfor %}]').render(c),
            u'[(0)test1,(1)test2,(0)test3,(1)test4,]'
        )
        self.assertEquals(
            Template('{% load threadedcommentstags %}{% get_free_threaded_comment_tree for topic 3 as tree %}[{% for item in tree %}({{ item.depth }}){{ item.comment }},{% endfor %}]').render(c),
            u'[(0)test3,(1)test4,]'
        )

    def test_user_comment_tags(self):

        User = get_user_model()
        user1 = User.objects.create_user('eric', 'floguy@gmail.com', password='password')
        user2 = User.objects.create_user('brian', 'brosner@gmail.com', password='password')

        topic = Person.objects.create(name="Test2")

        ThreadedComment.objects.create_for_object(topic,
            user = user1,
            ip_address = '127.0.0.1',
            comment = "Eric comment",
        )
        ThreadedComment.objects.create_for_object(topic,
            user = user2,
            ip_address = '127.0.0.1',
            comment = "Brian comment",
        )

        c = Context({
            'user': user1,
        })

        self.assertEquals(
            Template('{% load threadedcommentstags %}{% get_user_comments for user as comments %}{{ comments }}').render(c),
            u'[&lt;ThreadedComment: Eric comment&gt;]'
        )
        self.assertEquals(
            Template('{% load threadedcommentstags %}{% get_user_comment_count for user as comment_count %}{{ comment_count }}').render(c),
            u'1',
        )

    def test_markdown_comment(self):
        User = get_user_model()
        user = User.objects.create_user('user', 'floguy@gmail.com', password='password')
        topic = Person.objects.create(name="Test2")

        comment_markdown = ThreadedComment.objects.create_for_object(
            topic, user=user, ip_address='127.0.0.1', markup=MARKDOWN,
            comment="This is a simple comment",
        )

        c = Context({
            'comment': comment_markdown,
        })
        s = Template("{% load threadedcommentstags %}{% auto_transform_markup comment %}").render(c)
        self.assertEquals(s, "This is a simple comment")

    def test_rest_comment(self):
        User = get_user_model()
        user = User.objects.create_user('user', 'floguy@gmail.com', password='password')
        topic = Person.objects.create(name="Test2")

        test_txt = "This is a simple comment.\nIt has a newline."

        comment_rest = ThreadedComment.objects.create_for_object(
            topic,
            user=user,
            ip_address='127.0.0.1',
            markup=REST,
            comment=test_txt,
        )

        c = Context({
            'comment': comment_rest
        })

        # Test rendering
        rendered = Template("{% load threadedcommentstags %}{% auto_transform_markup comment %}").render(c)

        # Verify comment text appears in output
        self.assertTrue("This is a simple comment" in rendered)

        # Verify newline exists
        self.assertTrue("has a newline" in rendered)

    def test_plaintext_comment(self):

        User = get_user_model()
        user = User.objects.create_user('user', 'floguy@gmail.com', password='password')
        topic = Person.objects.create(name="Test2")

        comment_plaintext = ThreadedComment.objects.create_for_object(
            topic, user = user, ip_address = '127.0.0.1', markup = PLAINTEXT,
            comment = '<b>This is Funny</b>',
        )
        c = Context({
            'comment': comment_plaintext
        })
        self.assertEquals(
            Template("{% load threadedcommentstags %}{% auto_transform_markup comment %}").render(c),
            u'&lt;b&gt;This is Funny&lt;/b&gt;'
        )

        comment_plaintext = ThreadedComment.objects.create_for_object(
            topic, user = user, ip_address = '127.0.0.1', markup = PLAINTEXT,
            comment = '<b>This is Funny</b>',
        )
        c = Context({
            'comment': comment_plaintext
        })
        self.assertEquals(
            Template("{% load threadedcommentstags %}{% auto_transform_markup comment as abc %}{{ abc }}").render(c),
            u'&lt;b&gt;This is Funny&lt;/b&gt;'
        )

    def test_gravatar_tags(self):
        c = Context({
            'email': "floguy@gmail.com",
            'rating': "G",
            'size': 30,
            'default': 'overridectx',
        })
        self.assertEquals(
            Template('{% load gravatar %}{% get_gravatar_url for email %}').render(c),
            u'http://www.gravatar.com/avatar.php?gravatar_id=04d6b8e8d3c68899ac88eb8623392150&rating=R&size=80&default=img%3Ablank'
        )
        self.assertEquals(
            Template('{% load gravatar %}{% get_gravatar_url for email as var %}Var: {{ var }}').render(c),
            u'Var: http://www.gravatar.com/avatar.php?gravatar_id=04d6b8e8d3c68899ac88eb8623392150&rating=R&size=80&default=img%3Ablank'
        )
        self.assertEquals(
            Template('{% load gravatar %}{% get_gravatar_url for email size 30 rating "G" default override as var %}Var: {{ var }}').render(c),
            u'Var: http://www.gravatar.com/avatar.php?gravatar_id=04d6b8e8d3c68899ac88eb8623392150&rating=G&size=30&default=override'
        )
        self.assertEquals(
            Template('{% load gravatar %}{% get_gravatar_url for email size size rating rating default default as var %}Var: {{ var }}').render(c),
            u'Var: http://www.gravatar.com/avatar.php?gravatar_id=04d6b8e8d3c68899ac88eb8623392150&rating=G&size=30&default=overridectx'
        )
        self.assertEquals(
            Template('{% load gravatar %}{{ email|gravatar }}').render(c),
            u'http://www.gravatar.com/avatar.php?gravatar_id=04d6b8e8d3c68899ac88eb8623392150&rating=R&size=80&default=img%3Ablank'
        )
