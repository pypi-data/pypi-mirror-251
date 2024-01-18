# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
from collections import defaultdict

from sortedcontainers import SortedList

from common.base.executors.batch_work_executor import BatchWorkExecutor
from common.base.jobs.base_job import BaseJob
from telnet.check_telnet import  check_port, line_to_host_port
from telnet.helper import combine_list_number

logger = logging.getLogger(__name__)


class MultiThreadsTelnetJob(BaseJob):
    def __init__(
            self,
            work_iterable,
            max_workers=32,
            batch_size=1):
        self.work_iterable = work_iterable
        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self._dict_cache = []
        self.max_workers=max_workers
        self.list_open = defaultdict(SortedList)
        self.list_not_open = defaultdict(SortedList)

    def _start(self):
        # self.item_exporter.open()
        pass

    def _export(self):
        host_port_list = []
        # separate to host port pair
        for line in self.work_iterable:
            line =line.strip()
            if line.startswith("#"):
                continue
            host, ports, _range = line_to_host_port(line)
            for port in ports:
                host_port_list.append((host, port))

        self.batch_work_executor.execute(
            host_port_list,
            self._export_batch,
            total_items=len(host_port_list)
        )

    def _export_batch(self, work_data):
        for line in work_data:
            host, port = line
            ok = check_port(host,port)
            if ok:
                self.list_open[host].add(int(port))
            else:
                self.list_not_open[host].add(int(port))


    def _end(self):
        self.batch_work_executor.shutdown()
        # self.item_exporter.close()
        pass

    def get_cache(self):
        return self._dict_cache

    def clean_cache(self):
        self._dict_cache = []
    def get_result(self):
        for host in self.list_open:
            self.list_open[host] = combine_list_number(self.list_open[host])
        for host in self.list_not_open:
            self.list_not_open[host] = combine_list_number(self.list_not_open[host])

        return {
            "open": self.list_open,
            "close": self.list_not_open
        }
