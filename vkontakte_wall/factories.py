from vkontakte_users.factories import UserFactory
from vkontakte_groups.factories import GroupFactory
from vkontakte_api.factories import DjangoModelNoCommitFactory
from models import Post, Comment
from datetime import datetime
import factory


class MockDjangoMoelFactory(DjangoModelNoCommitFactory):

    @classmethod
    def get_mock_params_dict(cls, obj, **kwargs):
        result = {}
        for key, value in obj.__dict__.iteritems():
            if not key.startswith('_'):
                result[key] = value
        del result['id']
        del result['remote_id']
        del result['archived']
        result.update(kwargs)
        return result


class PostFactory(MockDjangoMoelFactory):
    FACTORY_FOR = Post

    date = datetime.now()

    wall_owner = factory.SubFactory(UserFactory)
    author = factory.SubFactory(UserFactory)
    remote_id = factory.LazyAttributeSequence(lambda o, n: '%s_%s' % (o.wall_owner.remote_id, n))


class GroupPostFactory(PostFactory):
    wall_owner = factory.SubFactory(GroupFactory)
    remote_id = factory.LazyAttributeSequence(lambda o, n: '-%s_%s' % (o.wall_owner.remote_id, n))


class CommentFactory(MockDjangoMoelFactory):
    FACTORY_FOR = Comment

    date = datetime.now()

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    remote_id = factory.LazyAttributeSequence(lambda o, n: '%s_%s' % (o.post.remote_id, n))
