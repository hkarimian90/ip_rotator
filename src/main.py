import logging
import asyncio
import time
from datetime import datetime
from typing import Callable
logger = logging.getLogger(__name__)

def method_logger(fn: Callable) -> Callable:
    """
    A decorator to log the start and end of a function, including its execution time.
    Supports both synchronous and asynchronous functions.
    """
    async def async_wrapper(*args, **kwargs) -> None:
        name = fn.__name__
        start_time = datetime.now()
        logger.debug(f'function: {name} Started')
        try:
            result = await fn(*args, **kwargs)  # Await the coroutine if the function is async
            logger.debug(f'function: {name} End finished in ({(datetime.now() - start_time).total_seconds()})s')
            return result
        except Exception as e:
            logger.error(f'function: {name} failed with error: {e}')
            raise

    def sync_wrapper(*args, **kwargs) -> None:
        name = fn.__name__
        start_time = datetime.now()
        logger.debug(f'function: {name} Started')
        try:
            result = fn(*args, **kwargs)  # Call the synchronous function
            logger.debug(f'function: {name} End finished in ({(datetime.now() - start_time).total_seconds()})s')
            return result
        except Exception as e:
            logger.error(f'function: {name} failed with error: {e}')
            raise

    # Return the appropriate wrapper based on whether the function is async
    if asyncio.iscoroutinefunction(fn):
        return async_wrapper
    else:
        return sync_wrapper

class IpRotator:
    def __init__(
        self,
        target_url: str,
        proxy:tuple[str, str|int, str]|None=None,
        header:dict|None=None,
        get_proxy_retry:int=3,
        get_proxy_timeout:int=3,
        log_level="INFO" #CRITICAL,ERROR,WARNING,INFO,DEBUG,
        )->None:
        """
        Initializes the IpRotator class.

        This class is designed to get a list of proxies from:
            hasdata.com
            freeproxy.world
            proxybros.com
            advanced.name
            iproyal.com
            hidemy.life
        test their validity by making requests
        to the target URL, remove failed proxies, and provide a random proxy from the cleaned list
        when the `pull_proxy()` method is called.

        Args:
            target_url (str): The URL of the target site to which the proxies will be tested.
            proxy (tuple[str, str | int, str] | None):try to get proxy list using this proxy A tuple containing proxy details in the format
                (ip|domain, port, protocol). For example, ("127.0.0.1", 8080, "http"). If None, no initial
                proxy is set. Defaults to None.
            header (dict | None): A dictionary of HTTP headers to be used in requests. If None, no
                custom headers are set. Defaults to None.
            get_proxy_retry (int): The number of retries for fetching a working proxy. Defaults to 3.
            get_proxy_timeout (int): The timeout (in seconds) for proxy testing requests. Defaults to 3.
            log_level (str): The logging level for the class. Possible values are:
                - "CRITICAL"
                - "ERROR"
                - "WARNING"
                - "INFO"
                - "DEBUG"
                Defaults to "INFO".

        Example:
            >>> rotator = IpRotator(
            ...     target_url="https://example.com",
            ...     proxy=("127.0.0.1", 8080,"http"),
            ...     header={"User-Agent": "Mozilla/5.0"},
            ...     get_proxy_retry=5,
            ...     get_proxy_timeout=5,
            ...     log_level="DEBUG"
            ... )
            >>> rotator.pull_proxy()
            "http://127.0.0.1:8080"

        Notes:
            - The class automatically tests proxies by making requests to the `target_url`.
            - Failed proxies are removed from the list, ensuring only working proxies are used.
            - The `pull_proxy()` method returns a random proxy from the cleaned list.
        """
        

        self._logger_setter(log_level)
        logger.debug(f'logger set to:{logger}')

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
        
    def _logger_setter(self,log_level:str)->None:
        
        match log_level.upper():
            case "CRITICAL":
                log_level = logging.CRITICAL
            case "ERROR":
                log_level = logging.ERROR
            case "WARNING":
                log_level = logging.WARNING
            case "INFO":
                log_level = logging.INFO
            case "DEBUG":
                log_level = logging.DEBUG
            case _:
                raise ValueError(f"Invalid log level: {log_level}")


        logging.basicConfig(
            # filename='myapp.log',
            handlers=[logging.StreamHandler(),logging.FileHandler('ip_rotator.log')],
            level=log_level,
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    
    @method_logger
    async def show_get_status(self,interval: int = 3)->None:
        
        """
        Periodically print the status of the proxy gatherers until all are done,failed or disable.
        Args:
            interval (int) : update interval in seconds
        """
        colors = {
            "reset": "\033[0m",
            "disable": "\033[30m",      # مشکی (Black)
            "not_started": "\033[97m",  # سفید (White)
            "started": "\033[34m",      # آبی (Blue)
            "getting_data": "\033[33m",  # زرد تیره/نارنجی (Dark Yellow/Orange)
            "done": "\033[92m",         # سبز (Green)
            "failed": "\033[91m",        # قرمز (Red)
        }
        self._status=[
            {"src":"hasdata.com","status":"not_started","page":None,"start_time":None,"end_time":None} ,#status: not_statted,started, geting_data,done,faild
            {"src":"freeproxy.world","status":"not_started","page":None,"start_time":None,"end_time":None} ,
            {"src":"proxybros.com","status":"not_started","page":None,"start_time":None,"end_time":None} ,
            {"src":"advanced.name","status":"not_started","page":None,"start_time":None,"end_time":None} ,
            {"src":"iproyal.com","status":"not_started","page":None,"start_time":None,"end_time":None} ,
            {"src":"hidemy.life","status":"not_started","page":None,"start_time":None,"end_time":None} ,
        ]
        
        while True:
            # Print the current status
            print("\nCurrent Status:")
            print("=" * 50)
            print("Proxy Gatherers:")
            for gatherer in self._status:
                print(
                    f"Source: {gatherer['src']}, "
                    f"Status:{colors[gatherer['status']]} {gatherer['status']} {colors['reset']}, "
                    f"Page: {gatherer['page']}, "
                    f"Start Time: {gatherer['start_time']}, "
                    f"End Time: {gatherer['end_time']}"
                ,sep='  ')

            time.sleep(interval)



            # Check if all gatherers are done, failed, or disabled
            all_done = all(
                gatherer["status"] in ["done", "failed", "disabled"]
                for gatherer in self._status
            )
            if all_done:
                print("All proxy gatherers are done, failed, or disabled. Exiting status updates.")
                break




async def main():
    a=IpRotator('yahoo',log_level='debug')
    await a.show_get_status(interval=4)
    a._status
if __name__ =='__main__':
    asyncio.run(main())
    # a=IpRotator('yahoo',log_level='info')
    # asyncio.run() 
