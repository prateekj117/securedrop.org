import random

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import transaction

from blog.models import BlogIndexPage, CategoryPage
from blog.tests.factories import BlogPageFactory, BlogIndexPageFactory, CategoryPageFactory
from github.factories import ReleaseFactory
from home.models import HomePage


class Command(BaseCommand):
    help = 'Creates blog data appropriate for development'

    def add_arguments(self, parser):
        parser.add_argument('number_of_posts', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        number_of_posts = options['number_of_posts']

        home_page = HomePage.objects.get(slug='home')

        if BlogIndexPage.objects.all():
            blog_index_page = BlogIndexPage.objects.all().first()
        else:
            blog_index_page = BlogIndexPageFactory(parent=home_page, title="News")

        CATEGORY_NAMES = [
            'Release Announcement',
            'Pre-Release Announcement',
            'Interest Article',
            'Security Advisory',
        ]

        categories = []
        for name in CATEGORY_NAMES:
            try:
                category_page = CategoryPage.objects.get(title=name)
            except ObjectDoesNotExist:
                category_page = CategoryPageFactory(title=name, parent=blog_index_page)

            categories.append(category_page)

        for x in range(number_of_posts):
            category = random.choice(categories)

            blog_page = BlogPageFactory(
                parent=blog_index_page,
                category=category,
            )
            if category.title == 'Release Announcement':
                release = ReleaseFactory()
                blog_page.release = release

            blog_page.save()
