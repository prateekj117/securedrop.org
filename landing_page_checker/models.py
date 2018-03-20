from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models import Func, F, Value
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from django.core.validators import RegexValidator

from wagtail.wagtailcore.models import Page, PageManager, PageQuerySet
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from autocomplete.edit_handlers import AutocompleteFieldPanel
from common.models.mixins import MetadataPageMixin
from search.utils import get_search_content_by_fields
from common.models.edit_handlers import ReadOnlyPanel


class SecuredropOwner(models.Model):
    page = ParentalKey(
        'landing_page_checker.SecuredropPage',
        related_name='owners'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='instances'
    )

    def __str__(self):
        return self.owner.email


class SecuredropPageQuerySet(PageQuerySet):
    def with_domain_annotation(self):
        """
        Return the queryset with a `domain` field annotated on containing the
        domain as extracted from the `landing_page_domain` field
        """

        # Assuming all landing_page_domains include http:// or https:// as a
        # protocol (as enforced by URLField logic) we can count on the domain
        # being the third token when splitting on '/'
        return self.annotate(
            domain=Func(
                F('landing_page_domain'),
                Value('/'),
                Value(3),
                function='SPLIT_PART'
            )
        )


class SecuredropPageManager(PageManager):
    """
    This thin manager class is necessary for Wagtail 1.12.
    (See: https://github.com/wagtail/wagtail/pull/3557) After upgrading past
    Wagtail 1.13, this can be replaced with the following line of code:

        SecuredropPageManager = PageManager.from_queryset(SecuredropPageQuerySet)
    """

    def get_queryset(self):
        return SecuredropPageQuerySet(self.model)


SecuredropPageManager = SecuredropPageManager.from_queryset(SecuredropPageQuerySet)


class SecuredropPage(MetadataPageMixin, Page):
    objects = SecuredropPageManager()

    landing_page_domain = models.URLField(
        'Landing page domain name',
        max_length=255,
        unique=True
    )

    onion_address = models.CharField(
        'SecureDrop onion address',
        max_length=255,
        unique=True,
        validators=[RegexValidator(regex=r'\.onion$', message="Enter a valid .onion address.")]
    )

    added = models.DateTimeField(auto_now_add=True)

    organization_logo = models.ForeignKey(
        'common.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    organization_logo_homepage = models.ForeignKey(
        'common.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Optional second logo optimized to show up on dark backgrounds. For instances that are featured on the homepage.'
    )

    organization_description = models.CharField(max_length=95, blank=True, null=True, help_text="A micro description of your organization that will be displayed in the directory.")

    languages = ParentalManyToManyField(
        'directory.Language',
        blank=True,
        verbose_name='Languages accepted',
        related_name='languages'
    )

    countries = ParentalManyToManyField(
        'directory.Country',
        blank=True,
        verbose_name='Countries',
        related_name='countries'
    )

    topics = ParentalManyToManyField(
        'directory.Topic',
        blank=True,
        verbose_name='Preferred topics',
        related_name='topics'
    )

    content_panels = Page.content_panels + [
        ReadOnlyPanel('added', label='Date Added'),
        FieldPanel('landing_page_domain'),
        FieldPanel('onion_address'),
        FieldPanel('organization_description'),
        ImageChooserPanel('organization_logo'),
        ImageChooserPanel('organization_logo_homepage'),
        AutocompleteFieldPanel('languages', 'directory.Language'),
        AutocompleteFieldPanel('countries', 'directory.Country'),
        AutocompleteFieldPanel('topics', 'directory.Topic'),
        InlinePanel('owners', label='Owners'),
        InlinePanel('results', label='Results'),
    ]

    search_fields_pgsql = ['title', 'landing_page_domain', 'onion_address', 'organization_description']

    def serve(self, request):
        owners = [sd_owner.owner for sd_owner in self.owners.all()]
        if request.user in owners:
            self.editable = True
        else:
            self.editable = False

        return super(SecuredropPage, self).serve(request)

    def get_live_result(self):
        # Used in template to get the latest live result.
        return self.results.filter(live=True).latest()

    def get_search_content(self):
        search_content = get_search_content_by_fields(self, self.search_fields_pgsql)

        for field in ['languages', 'countries', 'topics']:
            titles = [item.title for item in getattr(self, field).all()]
            search_content += " ".join(titles) + ' '

        return search_content

    def save(self, *args, **kwargs):
        super(SecuredropPage, self).save(*args, **kwargs)
        self.results = Result.objects.filter(landing_page_domain=self.landing_page_domain)


class Result(models.Model):
    # This is different from STN's Scan object in that each scan here will not
    # produce a new Result row. If multiple consecutive scans have the same
    # result, then we only insert that result once and set the result_last_seen
    # to the date of the last scan.
    securedrop = ParentalKey(
        'landing_page_checker.SecuredropPage',
        related_name='results',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    landing_page_domain = models.URLField(
        'Landing page domain name',
        max_length=255,
        db_index=True,
    )
    live = models.BooleanField()

    # In order to save a scan result when it is different from the last scan
    # we store result_last_scan
    result_last_seen = models.DateTimeField(auto_now_add=True)

    # HTTPS fields populated with pshtt
    forces_https = models.NullBooleanField()
    hsts = models.NullBooleanField()
    hsts_max_age = models.NullBooleanField()
    hsts_entire_domain = models.NullBooleanField()
    hsts_preloaded = models.NullBooleanField()

    # Basic checks
    http_status_200_ok = models.NullBooleanField()
    http_no_redirect = models.NullBooleanField()
    expected_encoding = models.NullBooleanField()

    # Security headers
    no_server_info = models.NullBooleanField()
    no_server_version = models.NullBooleanField()
    csp_origin_only = models.NullBooleanField()
    mime_sniffing_blocked = models.NullBooleanField()
    noopen_download = models.NullBooleanField()
    xss_protection = models.NullBooleanField()
    clickjacking_protection = models.NullBooleanField()
    good_cross_domain_policy = models.NullBooleanField()
    http_1_0_caching_disabled = models.NullBooleanField()
    cache_control_set = models.NullBooleanField()
    cache_control_revalidate_set = models.NullBooleanField()
    cache_control_nocache_set = models.NullBooleanField()
    cache_control_notransform_set = models.NullBooleanField()
    cache_control_nostore_set = models.NullBooleanField()
    cache_control_private_set = models.NullBooleanField()
    expires_set = models.NullBooleanField()

    # Page content
    safe_onion_address = models.NullBooleanField()
    no_cdn = models.NullBooleanField()
    no_analytics = models.NullBooleanField()
    subdomain = models.NullBooleanField()
    no_cookies = models.NullBooleanField()

    grade = models.CharField(max_length=2, editable=False, default='?')

    panels = [
        ReadOnlyPanel('grade'),
        ReadOnlyPanel('live'),
        ReadOnlyPanel('result_last_seen'),
        ReadOnlyPanel("forces_https"),
        ReadOnlyPanel("hsts"),
        ReadOnlyPanel("hsts_max_age"),
        ReadOnlyPanel("hsts_entire_domain"),
        ReadOnlyPanel("hsts_preloaded"),
        ReadOnlyPanel("http_status_200_ok"),
        ReadOnlyPanel("http_no_redirect"),
        ReadOnlyPanel("expected_encoding"),
        ReadOnlyPanel("no_server_info"),
        ReadOnlyPanel("no_server_version"),
        ReadOnlyPanel("csp_origin_only"),
        ReadOnlyPanel("mime_sniffing_blocked"),
        ReadOnlyPanel("noopen_download"),
        ReadOnlyPanel("xss_protection"),
        ReadOnlyPanel("clickjacking_protection"),
        ReadOnlyPanel("good_cross_domain_policy"),
        ReadOnlyPanel("http_1_0_caching_disabled"),
        ReadOnlyPanel("cache_control_set"),
        ReadOnlyPanel("cache_control_revalidate_set"),
        ReadOnlyPanel("cache_control_nocache_set"),
        ReadOnlyPanel("cache_control_notransform_set"),
        ReadOnlyPanel("cache_control_nostore_set"),
        ReadOnlyPanel("cache_control_private_set"),
        ReadOnlyPanel("expires_set"),
        ReadOnlyPanel("safe_onion_address"),
        ReadOnlyPanel("no_cdn"),
        ReadOnlyPanel("no_analytics"),
        ReadOnlyPanel("subdomain"),
        ReadOnlyPanel("no_cookies"),
    ]

    class Meta:
        get_latest_by = 'result_last_seen'

    def is_equal_to(self, other):
        # We will use this equality method to compare the scan results only

        excluded_keys = ['_state', '_securedrop_cache', 'result_last_seen',
                         'id', 'grade']

        self_values_to_compare = [(k, v) for k, v in self.__dict__.items()
                                  if k not in excluded_keys]
        other_values_to_compare = [(k, v) for k, v in other.__dict__.items()
                                   if k not in excluded_keys]

        return self_values_to_compare == other_values_to_compare

    def __str__(self):
        return 'Scan result for {}'.format(self.landing_page_domain)

    def compute_grade(self):
        if self.live is False:
            self.grade = '?'
            return

        if (self.forces_https is False or
            self.no_cookies is False or
            self.http_no_redirect is False or
            self.http_status_200_ok is False or
            self.no_analytics is False):  # noqa: E129
            self.grade = 'F'
        elif (self.subdomain is True or
              self.no_cdn is False or
              self.no_server_info is False or
              self.no_server_version is False):
            self.grade = 'D'
        elif (self.hsts is False or
              self.expected_encoding is False or
              self.noopen_download is False or
              self.cache_control_set is False or
              self.csp_origin_only is False or
              self.mime_sniffing_blocked is False or
              self.xss_protection is False or
              self.clickjacking_protection is False or
              self.good_cross_domain_policy is False or
              self.http_1_0_caching_disabled is False or
              self.expires_set is False or
              self.hsts_max_age is False):
            self.grade = 'C'
        elif (self.cache_control_revalidate_set is False or
              self.cache_control_nocache_set is False or
              self.cache_control_notransform_set is False or
              self.cache_control_nostore_set is False or
              self.cache_control_private_set is False or
              self.hsts_preloaded is False or
              self.hsts_entire_domain is False):
            self.grade = 'B'
        else:
            self.grade = 'A'

    def save(self, *args, **kwargs):
        self.compute_grade()
        self.securedrop = SecuredropPage.objects.filter(landing_page_domain=self.landing_page_domain).first()
        super(Result, self).save(*args, **kwargs)
