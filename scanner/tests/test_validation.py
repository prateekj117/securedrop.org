from bs4 import BeautifulSoup
from unittest import mock

from django.test import TestCase

from scanner import scanner


class MultipleCacheControlDirectivesSuccess(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.page.headers = {
            'Cache-Control': 'private, max-age=0, no-store, no-cache, must-revalidate, no-transform'
        }

    def test_cache_control_must_revalidate_set(self):
        self.assertTrue(scanner.validate_cache_must_revalidate(self.page))

    def test_cache_control_nocache_set(self):
        self.assertTrue(scanner.validate_nocache(self.page))

    def test_cache_control_notransform_set(self):
        self.assertTrue(scanner.validate_notransform(self.page))

    def test_cache_control_nostore_set(self):
        self.assertTrue(scanner.validate_nostore(self.page))

    def test_cache_cache_control_private_set(self):
        self.assertTrue(scanner.validate_private(self.page))


class MultipleCacheControlDirectivesFailure(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.page.headers = {
            'Cache-Control': 'public, max-age=0, store, cache, must-not-revalidate, transform'
        }

    def test_cache_control_must_revalidate_set(self):
        self.assertFalse(scanner.validate_cache_must_revalidate(self.page))

    def test_cache_control_nocache_set(self):
        self.assertFalse(scanner.validate_nocache(self.page))

    def test_cache_control_notransform_set(self):
        self.assertFalse(scanner.validate_notransform(self.page))

    def test_cache_control_nostore_set(self):
        self.assertFalse(scanner.validate_nostore(self.page))

    def test_cache_cache_control_private_set(self):
        self.assertFalse(scanner.validate_private(self.page))


class VerificationUtilityTest(TestCase):
    def test_onion_link_is_in_href(self):
        test_html = "<a href='notavalidaddress.onion'>SecureDrop</a>"
        soup = BeautifulSoup(test_html, "lxml")
        self.assertFalse(scanner.validate_onion_address_not_in_href(soup))

    def test_onion_link_is_not_in_href(self):
        test_html = "Go to notavalidaddress.onion and leak dem docs"
        soup = BeautifulSoup(test_html, "lxml")
        self.assertTrue(scanner.validate_onion_address_not_in_href(soup))

    def test_url_does_not_have_subdomain(self):
        self.assertFalse(scanner.validate_subdomain('https://example.com/securedrop'))

    def test_url_does_have_subdomain(self):
        self.assertTrue(scanner.validate_subdomain('https://securedrop.example.com'))

    def test_guardian_url_does_have_subdomain(self):
        self.assertTrue(scanner.validate_subdomain('https://securedrop.theguardian.com'))

    def test_guardian_url_does_not_have_protocol(self):
        self.assertTrue(scanner.validate_subdomain('securedrop.theguardian.com'))

    def test_www_url_does_not_have_subdomain(self):
        self.assertFalse(scanner.validate_subdomain('https://www.example.com/securedrop'))

    def test_second_level_domain_in_country_code_does_not_have_subdomain(self):
        self.assertFalse(scanner.validate_subdomain('https://bbc.co.uk/securedrop'))

    def test_www_url_with_country_code_does_not_have_subdomain(self):
        self.assertFalse(scanner.validate_subdomain('https://www.example.co.uk'))

    def test_second_level_domain_in_country_code_does_have_subdomain(self):
        self.assertTrue(scanner.validate_subdomain('https://tips.bbc.co.uk'))

    def test_url_first_level_domain_in_country_code_does_not_have_subdomain(self):
        self.assertFalse(scanner.validate_subdomain('https://example.no'))

    def test_url_first_level_domain_in_country_code_does_have_subdomain(self):
        self.assertTrue(scanner.validate_subdomain('https://subdomain.example.no'))

    def test_url_with_file_extension_does_not_have_subdomain(self):
        self.assertFalse(scanner.validate_subdomain('https://example.org/tips.html'))

    def test_server_header_software_present_nginx(self):
        page = mock.Mock()
        page.headers = {'Server': 'nginx/1.6.3'}
        self.assertFalse(scanner.validate_server_software(page))

    def test_server_header_software_present_apache(self):
        page = mock.Mock()
        page.headers = {'Server': 'Apache/2.4.10 (Debian)'}
        self.assertFalse(scanner.validate_server_software(page))

    def test_server_header_software_not_present(self):
        page = mock.Mock()
        page.headers = {'Server': ''}
        self.assertTrue(scanner.validate_server_software(page))

    def test_server_header_version_not_present(self):
        page = mock.Mock()
        page.headers = {'Server': ''}
        self.assertTrue(scanner.validate_server_version(page))

    def test_server_header_version_is_present(self):
        page = mock.Mock()
        page.headers = {'Server': 'Apache/2.4.10 (Debian)'}
        self.assertFalse(scanner.validate_server_version(page))

    def test_cloudflare_headers_not_present(self):
        page = mock.Mock()
        page.headers = {'Server': ''}
        self.assertTrue(scanner.validate_not_using_cdn(page))

    def test_cloudflare_headers_present(self):
        page = mock.Mock()
        page.headers = {'CF-Cache-Status': 'weeee'}
        self.assertFalse(scanner.validate_not_using_cdn(page))

    def test_google_analytics_present(self):
        page = mock.Mock()
        page.content = '<script src="analytics.js"></script>'
        self.assertFalse(scanner.validate_not_using_analytics(page))

    def test_google_analytics_not_present(self):
        page = mock.Mock()
        page.content = '<h1>My Good SecureDrop Landing Page</h1>'
        self.assertTrue(scanner.validate_not_using_analytics(page))

    def test_csp_not_present(self):
        page = mock.Mock()
        page.headers = {'Content-Security-Policy': 'Random Crazy Value'}
        self.assertFalse(scanner.validate_csp(page))

    def test_csp_present_single_value(self):
        page = mock.Mock()
        page.headers = {'Content-Security-Policy': "default-src 'self'"}
        self.assertTrue(scanner.validate_csp(page))

    def test_csp_present_multiple_values(self):
        """CSP check should pass with multiple values as long as "default-src 'self'" is among them. """
        page = mock.Mock()
        page.headers = {'Content-Security-Policy': "default-src 'self' style-src 'self'"}
        self.assertTrue(scanner.validate_csp(page))

    def test_xss_protection_not_present(self):
        page = mock.Mock()
        page.headers = {'X-XSS-Protection': 'Crazy Value'}
        self.assertFalse(scanner.validate_xss_protection(page))

    def test_xss_protection_present(self):
        page = mock.Mock()
        page.headers = {'X-XSS-Protection': '1; mode=block'}
        self.assertTrue(scanner.validate_xss_protection(page))

    def test_nosniff_protection_not_present(self):
        page = mock.Mock()
        page.headers = {'X-Content-Type-Options': 'Crazy Value'}
        self.assertFalse(scanner.validate_no_sniff(page))

    def test_nosniff_protection_present(self):
        page = mock.Mock()
        page.headers = {'X-Content-Type-Options': 'nosniff'}
        self.assertTrue(scanner.validate_no_sniff(page))

    def test_no_download_option_not_present(self):
        page = mock.Mock()
        page.headers = {'X-Download-Options': 'open'}
        self.assertFalse(scanner.validate_download_options(page))

    def test_no_download_option_present(self):
        page = mock.Mock()
        page.headers = {'X-Download-Options': 'noopen'}
        self.assertTrue(scanner.validate_download_options(page))

    def test_clickjacking_protection_not_present(self):
        page = mock.Mock()
        page.headers = {'X-Frame-Options': 'ALLOW'}
        self.assertFalse(scanner.validate_clickjacking_protection(page))

    def test_clickjacking_protection_present(self):
        page = mock.Mock()
        page.headers = {'X-Frame-Options': 'DENY'}
        self.assertTrue(scanner.validate_clickjacking_protection(page))

    def test_cross_domain_policy_not_set_properly(self):
        page = mock.Mock()
        page.headers = {'X-Permitted-Cross-Domain-Policies': 'Crazy'}
        self.assertFalse(scanner.validate_cross_domain_policy(page))

    def test_cross_domain_policy_set_properly(self):
        page = mock.Mock()
        page.headers = {'X-Permitted-Cross-Domain-Policies': 'master-only'}
        self.assertTrue(scanner.validate_cross_domain_policy(page))

    def test_pragma_header_not_disabling_caching(self):
        page = mock.Mock()
        page.headers = {'Pragma': 'so-much-cache'}
        self.assertFalse(scanner.validate_pragma(page))

    def test_pragma_header_disabling_caching(self):
        page = mock.Mock()
        page.headers = {'Pragma': 'no-cache'}
        self.assertTrue(scanner.validate_pragma(page))

    def test_expires_header_not_disabling_caching(self):
        page = mock.Mock()
        page.headers = {'Expires': '10033213'}
        self.assertFalse(scanner.validate_expires(page))

    def test_expires_header_disabling_caching(self):
        page = mock.Mock()
        page.headers = {'Expires': '-1'}
        self.assertTrue(scanner.validate_expires(page))

    def test_cache_control_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': ''}
        self.assertTrue(scanner.validate_cache_control_set(page))

    def test_cache_control_not_set(self):
        page = mock.Mock()
        page.headers = {'Expires': '-1'}
        self.assertFalse(scanner.validate_cache_control_set(page))

    def test_cache_control_must_revalidate_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': 'must-revalidate'}
        self.assertTrue(scanner.validate_cache_must_revalidate(page))

    def test_cache_control_must_not_revalidate_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': 'must-not-revalidate'}
        self.assertFalse(scanner.validate_cache_must_revalidate(page))

    def test_cache_control_validate_nocache_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': 'no-cache'}
        self.assertTrue(scanner.validate_nocache(page))

    def test_cache_control_validate_nocache_not_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': 'cache'}
        self.assertFalse(scanner.validate_nocache(page))

    def test_cache_control_validate_notransform_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': 'no-transform'}
        self.assertTrue(scanner.validate_notransform(page))

    def test_cache_control_validate_notransform_not_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': 'transform'}
        self.assertFalse(scanner.validate_notransform(page))

    def test_cache_control_validate_nostore_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': 'no-store'}
        self.assertTrue(scanner.validate_nostore(page))

    def test_cache_control_validate_nostore_not_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': 'store'}
        self.assertFalse(scanner.validate_nostore(page))

    def test_cache_control_validate_private_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': 'private'}
        self.assertTrue(scanner.validate_private(page))

    def test_cache_control_validate_private_not_set(self):
        page = mock.Mock()
        page.headers = {'Cache-Control': 'public'}
        self.assertFalse(scanner.validate_private(page))

    def test_referrer_policy_no_referrer_set(self):
        page = mock.Mock()
        page.headers = {'Referrer-Policy': 'no-referrer'}
        self.assertTrue(scanner.validate_no_referrer_policy(page))

    def test_referrer_policy_no_referrer_not_set(self):
        page = mock.Mock()
        page.headers = {'Referrer-Policy': 'origin'}
        self.assertFalse(scanner.validate_no_referrer_policy(page))

    def test_validate_utf_8_encoding(self):
        page = mock.Mock()
        page.encoding = 'utf-8'
        self.assertTrue(scanner.validate_encoding(page))

    def test_validate_iso_8859_1_encoding(self):
        page = mock.Mock()
        page.encoding = 'iso-8859-1'
        self.assertTrue(scanner.validate_encoding(page))

    def test_do_not_validate_no_encoding(self):
        page = mock.Mock()
        page.encoding = None
        self.assertFalse(scanner.validate_encoding(page))

    def test_urls_on_same_domain(self):
        self.assertTrue(
            scanner.same_domain(
                'http://www.example.com',
                'http://example.com',
            )
        )
        self.assertFalse(scanner.same_domain('www.a1.com', 'www.a2.com'))
