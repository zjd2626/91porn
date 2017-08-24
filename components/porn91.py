#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os

import httputil
import logging
import htmlutil


class Porn91:
    def __init__(self, enter_point='http://91porn.com/index.php'):
        self._enter_point = enter_point
        #self._pending_videos = []
        logging.debug("Porn inited!")

    def fetch_home_page(self):
        """
        获取首页（入口地址）所有视频链接
        """
        return self.fetch(self._enter_point)

    def fetch(self, url):
        """
        获取指定网站所有视频链接
        """
        content = httputil.get_content(url)
        links = htmlutil.get_all_video_link(content)
        links = list(set(links))
        return links

    def download(self, video_link):
        content = httputil.get_content(video_link)
        url = self.parse_video_url(content)
        title = self.prase_title(content)
        logging.debug("video title %s download link %s" % (title, url))

        full_file_name = '%s.mp4' % title

        if os.path.exists(full_file_name):
            logging.debug("File Has Already Downloaded! Skip!")
            return url

        httputil.download_file('%s.mp4' % title, url)
        logging.debug("Video %s Downloaded!" % title)
        return url

    def parse_video_url(self, raw_html):
        return htmlutil.get_srouce_tag_src(raw_html)

    def prase_title(self, raw_html):
        return htmlutil.get_text_by_id(raw_html, 'viewvideo-title')