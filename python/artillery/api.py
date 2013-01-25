from ext.decorators import repeatable

def weak_token(data):
    return encode_user_id(data.id)

def token(data):
    return encode_user_id(data.id)
    if getattr(data, 'is_owner', False):
        return encode_user_id(data.id, OwnerPermission)
    return encode_user_id(data.id)

class DictFields:
    UserFields = ('username', 'first_name', 'last_name')
    SubscriptionFields = ('token',)
    ChapterFields = ('title', 'story', 'order', 'content', )
    
@repeatable
def dictify(things, fields):
    thing_dicts = []
    for thing in things:
        thing_dict = {}
        for field in fields:
            attr = getattr(thing, field)
            if callable(attr):
                thing_dict[field] = attr()
            else:
                thing_dict[field] = attr
        thing_dicts.append(thing_dict)
    return thing_dicts

def get_list(model, ids):
    lookup = model.objects.in_bulk(ids)
    return [lookup[int(obj_id)] for obj_id in ids]

# Users
@repeatable
def dictify_users(users, is_owner=False):
    user_dicts = dictify(users, DictFields.UserFields)
    for user_dict, user in zip(user_dicts,users):
        user_dict['weak_token'] = encode_user_id(user.id)
        if is_owner:
            user_dict['token'] = encode_user_id(user.id, OwnerPermission)
        user_dict['token'] = encode_user_id(user.id)
    return user_dicts

def get_users(uids):
    users = get_list(User, uids)
    return dictify_users(users)

# Chapter
@repeatable
def dictify_chapter(chapters):
    return dictify(chapters, DictFields.ChapterFields)

# Subscription
def create_subscription(canon_id, user_id):
    sub = models.Subscription.get_or_create(
        user_id=user_id, canon_id=canon_id)
    return sub

def subbed_stories_for_user(uid):
    subs = Subscription.objects.filter(user_id=uid)
    sub_ids = [sub.id for sub in subs]
    stories = Story.objects.filter(cannon__subscription__id__in = sub_ids)
    return stories

# Story
@repeatable
def dictify_stories(stories, viewers=None):
    story_dicts = dictify_stories(stories)
    for sub, sub_dict, story_dict in zip(subs, sub_dicts, story_dicts):
        chapter = sub.canon.story.chapter.order_by('-created_on')[0]
        sub_dict['latest_chapter'] = dictify_chapter(chapter)
    return sub_dicts
