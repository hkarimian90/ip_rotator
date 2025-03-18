class IpRotator:
    def __init__(self,
                target_url: str,
                proxy:tuple[str, str|int, str]|None=None,
                header:dict|None=None,
                get_proxy_retry:int=3,
                get_proxy_timeout:int=3,
                )->None:
        self.target_url=target_url
        self._proxy=proxy
        if header != None:
            self._header=header
        else:
            self._header={
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
            }
        self._get_proxy_retry=get_proxy_retry
        self._get_proxy_timeout=get_proxy_timeout
        self.proxies=[]
