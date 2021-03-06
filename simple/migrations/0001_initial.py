# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-23 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtailmetadata.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0002_auto_20180423_1812'),
        ('menus', '0001_initial'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('body', wagtail.core.fields.StreamField((('text', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')]))))), ('raw_html', wagtail.core.blocks.RawHTMLBlock()), ('blockquote', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.RichTextBlock()), ('source_text', wagtail.core.blocks.RichTextBlock(required=False)), ('source_url', wagtail.core.blocks.URLBlock(help_text='Source text will link to this url.', required=False))))), ('list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(label='List Item'), template='common/blocks/list_block_columns.html')), ('video', wagtail.core.blocks.StructBlock((('video', wagtail.embeds.blocks.EmbedBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')]))))), ('heading_1', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),))), ('heading_2', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),))), ('heading_3', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),)))), blank=True, null=True)),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='common.CustomImage')),
                ('sidebar_menu', models.ForeignKey(blank=True, help_text="If left empty, page will use parent's sidebar menu", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='menus.Menu')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='FaqQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('question', models.CharField(max_length=255)),
                ('answer', wagtail.core.fields.RichTextField()),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='simple.FAQPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SimplePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('body', wagtail.core.fields.StreamField((('text', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')]))))), ('raw_html', wagtail.core.blocks.RawHTMLBlock()), ('blockquote', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.RichTextBlock()), ('source_text', wagtail.core.blocks.RichTextBlock(required=False)), ('source_url', wagtail.core.blocks.URLBlock(help_text='Source text will link to this url.', required=False))))), ('list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(label='List Item'), template='common/blocks/list_block_columns.html')), ('video', wagtail.core.blocks.StructBlock((('video', wagtail.embeds.blocks.EmbedBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')]))))), ('heading_1', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),))), ('heading_2', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),))), ('heading_3', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),)))))),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='common.CustomImage')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='SimplePageWithMenuSidebar',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('body', wagtail.core.fields.StreamField((('text', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')]))))), ('raw_html', wagtail.core.blocks.RawHTMLBlock()), ('blockquote', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.RichTextBlock()), ('source_text', wagtail.core.blocks.RichTextBlock(required=False)), ('source_url', wagtail.core.blocks.URLBlock(help_text='Source text will link to this url.', required=False))))), ('list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(label='List Item'), template='common/blocks/list_block_columns.html')), ('video', wagtail.core.blocks.StructBlock((('video', wagtail.embeds.blocks.EmbedBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')]))))), ('heading_1', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),))), ('heading_2', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),))), ('heading_3', wagtail.core.blocks.StructBlock((('content', wagtail.core.blocks.CharBlock()),)))))),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='common.CustomImage')),
                ('sidebar_menu', models.ForeignKey(blank=True, help_text="If left empty, page will use parent's sidebar menu", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='menus.Menu')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
    ]
