#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author  : Hu Ji
@file    : _download.py 
@time    : 2022/05/28
@site    :  
@software: PyCharm 

              ,----------------,              ,---------,
         ,-----------------------,          ,"        ,"|
       ,"                      ,"|        ,"        ,"  |
      +-----------------------+  |      ,"        ,"    |
      |  .-----------------.  |  |     +---------+      |
      |  |                 |  |  |     | -==----'|      |
      |  | $ sudo rm -rf / |  |  |     |         |      |
      |  |                 |  |  |/----|`---=    |      |
      |  |                 |  |  |   ,/|==== ooo |      ;
      |  |                 |  |  |  // |(((( [33]|    ,"
      |  `-----------------'  |," .;'| |((((     |  ,"
      +-----------------------+  ;;  | |         |,"
         /_)______________(_/  //'   | +---------+
    ___________________________/___  `,
   /  oooooooooooooooo  .o.  oooo /,   \,"-----------
  / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
 /_==__==========__==_ooo__ooo=_/'   /___________,"
"""

import contextlib
import json
import os
import shelve
import shutil
from typing import Dict, Union, List, Tuple
from urllib import parse

from ._utils import Timeout, get_md5, ignore_error, parse_version, timeoutable
from .._environ import environ
from .._rich import create_progress
from ..decorator import cached_property, singleton
from ..references.fake_useragent import UserAgent

_logger = environ.get_logger("utils.url")

DataType = Union[str, int, float]
QueryType = Union[DataType, List[DataType], Tuple[DataType]]


@singleton
class _UserAgent(UserAgent):

    def __init__(self):
        super().__init__(
            path=environ.get_asset_path(f"fake_useragent.json"),
            fallback=environ.get_config("DEFAULT_USER_AGENT", type=str),
        )


def user_agent(style=None) -> str:

    ua = _UserAgent()

    try:
        if style:
            return ua[style]

        return ua.random

    except Exception as e:
        _logger.debug(f"fetch user agent error: {e}")

    return ua.fallback


def make_url(url: str, *paths: str, **kwargs: QueryType) -> str:
    result = url

    for path in paths:
        result = result.rstrip("/") + "/" + path.lstrip("/")

    if len(kwargs) > 0:
        queries = []
        for key, value in kwargs.items():
            if isinstance(value, (list, tuple)):
                queries.extend((key, v) for v in value)
            else:
                queries.append((key, value))

        result = result + "?" + parse.urlencode(queries)

    return result


def guess_file_name(url: str) -> str:
    if not url:
        return ""
    try:
        return os.path.split(parse.urlparse(url).path)[1]
    except:
        return ""


def _parseparam(s):
    while s[:1] == ';':
        s = s[1:]
        end = s.find(';')
        while end > 0 and (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
            end = s.find(';', end + 1)
        if end < 0:
            end = len(s)
        f = s[:end]
        yield f.strip()
        s = s[end:]


def parse_header(line):
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    """
    parts = _parseparam(';' + line)
    key = parts.__next__()
    pdict = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1:].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict


def parser_cookie(cookie: str) -> Dict[str, str]:
    cookies = {}
    for item in cookie.split(";"):
        key_value = item.split("=", 1)
        cookies[key_value[0].strip()] = key_value[1].strip() if len(key_value) > 1 else ''
    return cookies


class DownloadError(Exception):
    pass


class DownloadHttpError(DownloadError):

    def __init__(self, code, e):
        super().__init__(e)
        self.code = code


class DownloadContextVar(property):

    def __init__(self, key, default=None):
        def fget(o: "DownloadContext"):
            return o._db.get(key, default)

        def fset(o: "DownloadContext", v):
            o._db[key] = v

        super().__init__(fget=fget, fset=fset)


class DownloadContext:
    url: str = DownloadContextVar("Url")
    user_agent: str = DownloadContextVar("UserAgent")
    headers: dict = DownloadContextVar("Headers")
    file_path: str = DownloadContextVar("FilePath")
    file_size: int = DownloadContextVar("FileSize")
    file_name: str = DownloadContextVar("FileName")
    completed: bool = DownloadContextVar("IsCompleted", False)
    max_times: int = DownloadContextVar("MaxTimes")

    def __init__(self, path: str):
        self._db = shelve.open(path)

    def __enter__(self):
        self._db.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        self._db.__exit__(*args, **kwargs)

    def download(self, timeout: Timeout):
        _logger.debug(f"Download file to temp path {self.file_path}")

        initial = 0
        # 如果文件存在，则继续上一次下载
        if os.path.exists(self.file_path):
            size = os.path.getsize(self.file_path)
            _logger.debug(f"{size} bytes downloaded, continue")
            initial = size

        self.headers = {
            "User-Agent": self.user_agent,
            "Range": f"bytes={initial}-",
        }

        try:
            import requests
            fn = self._download_with_requests
        except ModuleNotFoundError:
            fn = self._download_with_urllib

        with create_progress() as progress:
            task_id = progress.add_task(self.file_name, total=0)
            progress.advance(task_id, initial)

            with open(self.file_path, 'ab') as fp:
                offset = 0
                for data in fn(timeout.remain):
                    advance = len(data)
                    offset += advance
                    fp.write(data)
                    progress.update(
                        task_id,
                        advance=advance,
                        description=self.file_name
                    )
                    if self.file_size is not None:
                        progress.update(
                            task_id,
                            total=initial + self.file_size
                        )

            if self.file_size is not None and self.file_size > offset:
                raise DownloadError(
                    f"download size {initial + self.file_size} bytes was expected,"
                    f" got {initial + offset} bytes"
                )

            if os.path.getsize(self.file_path) == 0:
                raise DownloadError(f"download {self.url} error")

    def _download_with_requests(self, timeout: float):
        import requests
        from requests import HTTPError

        bs = 1024 * 8

        with requests.get(self.url, headers=self.headers, stream=True, timeout=timeout) as resp:

            try:
                resp.raise_for_status()
            except HTTPError as e:
                raise DownloadHttpError(resp.status_code, e)

            if "Content-Length" in resp.headers:
                self.file_size = int(resp.headers.get("Content-Length"))
            if "Content-Disposition" in resp.headers:
                _, params = parse_header(resp.headers["Content-Disposition"])
                if "filename" in params:
                    self.file_name = params["filename"]

            for chunk in resp.iter_content(bs):
                if chunk:
                    yield chunk

    def _download_with_urllib(self, timeout: float):
        from urllib.request import urlopen, Request
        from urllib.error import HTTPError

        bs = 1024 * 8

        url = Request(self.url, headers=self.headers)

        try:
            resp = urlopen(url=url, timeout=timeout)
        except HTTPError as e:
            raise DownloadHttpError(e.code, e)

        with contextlib.closing(resp) as fp:

            headers = fp.info()
            if "Content-Length" in headers:
                self.file_size = int(headers["Content-Length"])
            if "Content-Disposition" in headers:
                _, params = parse_header(headers["Content-Disposition"])
                if "filename" in params:
                    self.file_name = params["filename"]

            while True:
                chunk = fp.read(bs)
                if not chunk:
                    break
                yield chunk


class UrlFile:

    def __init__(self, url: str):
        self._url = url
        self._ident = f"{get_md5(url)}_{guess_file_name(url)[-100:]}"
        self._root_path = environ.get_temp_path("download", self._ident)
        self._file_path = os.path.join(self._root_path, "file")
        self._context_path = os.path.join(self._root_path, "context")

    @cached_property
    def _lock(self):
        from filelock import FileLock
        return FileLock(
            environ.get_temp_path("download", "lock", self._ident, create_parent=True)
        )

    @timeoutable
    def save(self, save_dir: str = None, save_name: str = None, timeout: Timeout = None, retry: int = 2, **kwargs) -> str:
        """
        从指定url下载文件
        :param save_dir: 文件路径，如果为空，则保存到temp目录
        :param save_name: 文件名，如果为空，则默认为下载的文件名
        :param timeout: 超时时间
        :param retry: 重试次数
        :return: 文件路径
        """

        lock = self._lock
        target_path = self._file_path

        try:
            lock.acquire(timeout=timeout.remain, poll_interval=1)

            if not os.path.exists(self._root_path):
                os.makedirs(self._root_path)

            with DownloadContext(self._context_path) as context:

                if os.path.exists(self._file_path) and context.completed:
                    # 下载完成了，那就不用再下载了
                    _logger.debug(f"{self._file_path} downloaded, skip")

                else:
                    # 初始化环境信息
                    context.url = self._url
                    context.file_path = self._file_path
                    context.file_size = None

                    if not context.file_name:
                        context.file_name = save_name or guess_file_name(self._url)
                    if not context.user_agent:
                        context.user_agent = kwargs.pop("user_agent", None) or user_agent("chrome")

                    # 开始下载
                    last_error = None
                    context.completed = False
                    context.max_times = 1 + max(retry or 0, 0)
                    for i in range(context.max_times, 0, -1):
                        try:
                            if last_error is not None:
                                _logger.warning(
                                    f"Download retry {context.max_times - i}, "
                                    f"{last_error.__class__.__name__}: {last_error}")
                            context.download(timeout)
                            context.completed = True
                            break
                        except Exception as e:
                            last_error = e

                    if not context.completed:
                        raise last_error

                if save_dir:
                    # 如果指定了路径，先创建路径
                    if not os.path.exists(save_dir):
                        _logger.debug(f"{save_dir} does not exist, create")
                        os.makedirs(save_dir)

                    # 然后把文件保存到指定路径下
                    target_path = os.path.join(save_dir, save_name or context.file_name)
                    _logger.debug(f"Rename {self._file_path} to {target_path}")
                    os.rename(self._file_path, target_path)

                    # 把文件移动到指定目录之后，就可以清理缓存文件了
                    self.clear(timeout=timeout.remain)

        except DownloadError:
            raise

        except Exception as e:
            raise DownloadError(e)

        finally:
            ignore_error(lock.release)

        return target_path

    def clear(self, timeout: int = None):
        """
        清空缓存文件
        """
        lock = self._lock
        with lock.acquire(timeout):
            if not os.path.exists(self._root_path):
                _logger.debug(f"{self._root_path} does not exist, skip")
                return
            _logger.debug(f"Clear {self._root_path}")
            if os.path.exists(self._file_path):
                os.remove(self._file_path)
            if os.path.exists(self._context_path):
                os.remove(self._context_path)
            if not os.listdir(self._root_path):
                shutil.rmtree(self._root_path, ignore_errors=True)

    def __enter__(self):
        self._lock.acquire()
        return self

    def __exit__(self, *args, **kwargs):
        self._lock.release()


class NotFoundError(Exception):
    pass


def get_chrome_driver(version: str):
    chrome_driver = environ.get_tool("chromedriver")
    base_url = chrome_driver.config.get("base_url")

    versions = parse_version(version)
    if versions[0] >= 70:
        file = UrlFile(f"{base_url}/LATEST_RELEASE_{versions[0]}")
        with open(file.save(), "rt") as fd:
            return chrome_driver.copy(version=fd.read(), cmdline=None)

    path = environ.get_asset_path("chrome-driver.json")
    with open(path, "rt") as fd:
        version_map = json.load(fd)

    for key, value in version_map.items():
        if versions[0] == parse_version(value)[0]:
            return chrome_driver.copy(version=key, cmdline=None)

    raise NotFoundError(version)
