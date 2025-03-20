import unittest
from src.main import IpRotator
import unittest
from unittest.mock import patch, call
import time

class TestShowGetStatus(unittest.TestCase):
    
    def setUp(self):
        
        self.proxy_gatherer = IpRotator('test.loc')  

    @patch('builtins.print')
    @patch('time.sleep')
    async def test_show_get_status_output(self, mock_sleep, mock_print):
        
        self.proxy_gatherer._status = [
            {"src": "hasdata.com", "status": "disable", "page": None, "start_time": None, "end_time": None},
            {"src": "freeproxy.world", "status": "not_started", "page": None, "start_time": None, "end_time": None},
            {"src": "proxybros.com", "status": "started", "page": None, "start_time": None, "end_time": None},
            {"src": "advanced.name", "status": "getting_data", "page": None, "start_time": None, "end_time": None},
            {"src": "iproyal.com", "status": "done", "page": None, "start_time": None, "end_time": None},
            {"src": "hidemy.life", "status": "failed", "page": None, "start_time": None, "end_time": None},
        ]

        
        await self.proxy_gatherer.show_get_status(interval=1)

        
        mock_sleep.assert_called_with(1)

        
        expected_calls = [
            call("\nCurrent Status:"),
            call("=" * 50),
            call("Proxy Gatherers:"),
            call("Source: hasdata.com, Status:\033[30m disable \033[0m, Page: None, Start Time: None, End Time: None"),
            call("Source: freeproxy.world, Status:\033[97m not_started \033[0m, Page: None, Start Time: None, End Time: None"),
            call("Source: proxybros.com, Status:\033[34m started \033[0m, Page: None, Start Time: None, End Time: None"),
            call("Source: advanced.name, Status:\033[33m getting_data \033[0m, Page: None, Start Time: None, End Time: None"),
            call("Source: iproyal.com, Status:\033[92m done \033[0m, Page: None, Start Time: None, End Time: None"),
            call("Source: hidemy.life, Status:\033[91m failed \033[0m, Page: None, Start Time: None, End Time: None"),
        ]

        
        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch('builtins.print')
    @patch('time.sleep')
    async def test_loop_breaks_when_all_done_failed_disabled(self, mock_sleep, mock_print):
        
        self.proxy_gatherer._status = [
            {"src": "hasdata.com", "status": "done", "page": None, "start_time": None, "end_time": None},
            {"src": "freeproxy.world", "status": "failed", "page": None, "start_time": None, "end_time": None},
            {"src": "proxybros.com", "status": "disable", "page": None, "start_time": None, "end_time": None},
            {"src": "advanced.name", "status": "done", "page": None, "start_time": None, "end_time": None},
            {"src": "iproyal.com", "status": "failed", "page": None, "start_time": None, "end_time": None},
            {"src": "hidemy.life", "status": "disable", "page": None, "start_time": None, "end_time": None},
        ]

        
        await self.proxy_gatherer.show_get_status(interval=1)

        
        mock_sleep.assert_called_once_with(1)

        
        expected_message = "All proxy gatherers are done, failed, or disabled. Exiting status updates."
        mock_print.assert_any_call(expected_message)

if __name__ == '__main__':
    unittest.main()