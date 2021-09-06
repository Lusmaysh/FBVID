# Last Update: 02-09-2021, Author: Lusmaysh
from bs4 import BeautifulSoup as bs
from datetime import datetime
from urllib.parse import unquote
import requests,re,os

Y = "\33[93m"
W = "\33[0m"
R = "\33[1;31m"
G = "\33[1;32m"

class Download:
	def __init__(self):
		pass
	def url(self, url):
		if re.search(r"www.facebook.com", url):
			url = url.replace("www", "mbasic")
		try:
			response = requests.get(url).text
			self.video_url = re.search(r'href\=\"\/video\_redirect\/\?src\=(.*?)\"', response)
			if self.video_url is not None:
				meta = bs(response,"html.parser").find('meta', {'property':'og:description'})
				try:
					self.caption = meta['content']
				except:
					self.caption = ''
				self.post_url = url
				self.video_url = unquote(self.video_url.group(1))
				print(f"{W}[!] {G}Video Found...")
				self.download()
			else:
				print(f"{W}(!) {R}Video Not Found...")
		except requests.exceptions.ConnectionError:
			print(f"{W}[!] {R}Connection Error, Please Check Your Internet")
		except requests.exceptions.MissingSchema:
			print(f"{W}[!] {R}Invalid Url")
	def info(self):
		print(f"{W}[•] {Y}Caption: {G}{self.caption}")
		if self.video_size > 1024:
			self.video_size = round(self.video_size/1024)
			m = "Mb"
		else:
			self.video_size = round(self.video_size)
			m = "Kb"
		print(f"{W}[•] {Y}Video Size: {G}{self.video_size} {m}")
	def download(self):
		content = requests.get(self.video_url)
		self.video_size = int(content.headers.get('Content-Length')) / 1024
		video_name = "fb_" + datetime.now().strftime('%m%d%Y%-H%M%S') + '.mp4'
		try:
			with open("/sdcard/videos/"+video_name, "wb") as filename:
				self.info()
				print(f"{W}[!] {G}Start Download...")
				filename.write(content.content)
			print(f"{W}[•] {Y}Videos Saved In {G}Sdcard/videos/{video_name}")
			print(f"\n{W}Github: {G}github.com/Lusmaysh\n")
		except FileNotFoundError:
			os.system("mkdir -p /sdcard/videos/")
			self.download()
if __name__=='__main__':
	os.system("clear")
	print(f'{G}[{W} FB Video Downloader {G}]{W}'.center(90))
	url = input(f"{W}[?] {Y}Url Video: {G}")
	Download().url(url)
