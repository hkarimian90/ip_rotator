import unittest
from src.main import IpRotator

class TestIpRotator(unittest.TestCase):
    def setUp(self):
        # Common setup for all tests
        self.target_url = "https://example.com"
        self.proxy = ("proxy.example.com", 8080, "http")
        self.header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.6',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }

    def test_initialization_with_default_values(self):
        # Test initialization with only target_url
        iprotator = IpRotator(self.target_url)

        # Check default values
        self.assertEqual(iprotator.target_url, self.target_url)
        self.assertIsNone(iprotator._proxy)
        self.assertEqual(iprotator._header, {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.6',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        })
        self.assertEqual(iprotator._get_proxy_retry, 3)
        self.assertEqual(iprotator._get_proxy_timeout, 3)
        self.assertEqual(iprotator.proxies, [])

    def test_initialization_with_custom_proxy(self):
        # Test initialization with custom proxy
        iprotator = IpRotator(self.target_url, proxy=self.proxy)

        # Check proxy is set correctly
        self.assertEqual(iprotator._proxy, self.proxy)

    def test_initialization_with_custom_header(self):
        # Test initialization with custom header
        iprotator = IpRotator(self.target_url, header=self.header)

        # Check header is set correctly
        self.assertEqual(iprotator._header, self.header)

    def test_initialization_with_custom_retry_and_timeout(self):
        # Test initialization with custom retry and timeout values
        iprotator = IpRotator(self.target_url, get_proxy_retry=5, get_proxy_timeout=10)

        # Check retry and timeout values
        self.assertEqual(iprotator._get_proxy_retry, 5)
        self.assertEqual(iprotator._get_proxy_timeout, 10)

    def test_initialization_with_all_custom_values(self):
        # Test initialization with all custom values
        iprotator = IpRotator(
            target_url=self.target_url,
            proxy=self.proxy,
            header=self.header,
            get_proxy_retry=5,
            get_proxy_timeout=10
        )

        # Check all values are set correctly
        self.assertEqual(iprotator.target_url, self.target_url)
        self.assertEqual(iprotator._proxy, self.proxy)
        self.assertEqual(iprotator._header, self.header)
        self.assertEqual(iprotator._get_proxy_retry, 5)
        self.assertEqual(iprotator._get_proxy_timeout, 10)
        self.assertEqual(iprotator.proxies, [])

    def test_proxies_attribute_is_empty_list(self):
        # Test that the proxies attribute is initialized as an empty list
        iprotator = IpRotator(self.target_url)
        self.assertEqual(iprotator.proxies, [])




if __name__ == '__main__':
    unittest.main()
