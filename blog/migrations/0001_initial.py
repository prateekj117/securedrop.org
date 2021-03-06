# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-23 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.routable_page.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtailmetadata.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('body', wagtail.core.fields.StreamField((('rich_text', wagtail.core.blocks.RichTextBlock(icon='doc-full', label='Rich Text')), ('image', wagtail.images.blocks.ImageChooserBlock()), ('raw_html', wagtail.core.blocks.RawHTMLBlock())), blank=True)),
                ('link_to_page_text', models.CharField(default='Read More', help_text='Text to display at the bottom of blog teasers that links to the blog page.', max_length=100)),
                ('release_title', models.CharField(default='Current Release', help_text='Text to display as a title for the current release in the sidebar.', max_length=100)),
                ('feed_limit', models.PositiveIntegerField(default=20, help_text='Maximum number of posts to be included in the syndication feed. 0 for unlimited.')),
                ('per_page', models.PositiveIntegerField(default=8, help_text='Number of posts to display per page.')),
                ('orphans', models.PositiveIntegerField(default=5, help_text='Minimum number of stories on the last page (if the last page is smaller, they will get added to the preceding page).')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('publication_datetime', models.DateTimeField(help_text='Past or future date of publication')),
                ('body', wagtail.core.fields.StreamField((('text', wagtail.core.blocks.RichTextBlock()), ('code', wagtail.core.blocks.StructBlock((('language', wagtail.core.blocks.ChoiceBlock(choices=[('python', 'Python'), ('bash', 'Bash/Shell'), ('html', 'HTML'), ('css', 'CSS'), ('scss', 'SCSS'), ('json', 'JSON')])), ('code', wagtail.core.blocks.TextBlock())), label='Code Block')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')]))))), ('raw_html', wagtail.core.blocks.RawHTMLBlock()), ('blockquote', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.RichTextBlock()), ('source_text', wagtail.core.blocks.RichTextBlock(required=False)), ('source_url', wagtail.core.blocks.URLBlock(help_text='Source text will link to this url.', required=False))))), ('list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(label='List Item'), template='common/blocks/list_block_columns.html')), ('video', wagtail.core.blocks.StructBlock((('video', wagtail.embeds.blocks.EmbedBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')]))))), ('heading_1', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),))), ('heading_2', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),))), ('heading_3', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),)))))),
                ('teaser_text', wagtail.core.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='CategoryPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', wagtail.core.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
    ]
