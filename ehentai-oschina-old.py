#!/usr/bin/env python
#-*- coding:utf-8 -*-
import httplib,urllib,urllib2,cookielib
import os,re,sys,time,socket

def ProxyDown(addr,path,proxy='xionghaizi.3owl.com/gg'):
	'''
	ʹ����ҳ����ץȡ��ҳ
	������ģʽ��/browse.php?u=[encoded url]&b=4[&f=norefer]
	���ߴ���վ��
	http://la.huoliquankai.info/
	'''
	def GetSize(str):
		'''
		����"xxx KB"/"xxx MB"���ַ��������ش�Լ���ֽ���
		'''
		mem=str.split(' ')
		size=float(mem[0])*1024
		if mem[1][0]=='M':size*=1024
		return size
	#���򣺻�ȡͼƬ����
	num=re.compile('Showing\s1\s-\s[0-9]+\sof\s([0-9]+)\simages')
	#���򣺻�ȡĿ¼��ҳ��
	idx=re.compile('<a\shref="([^<>"]*)"><img[^<>]*><br[^<>]*>[0-9]+</a>')
	#���򣺻�ȡ��һҳ����ҳ��
	nxt=re.compile('<a\shref="([^<>]*)"><img\ssrc="[^<>]*"\sstyle="[^<>]*"\s/></a>')
	#���򣺴�����ҳ���ȡͼƬ��ַ
	adr=re.compile('<a\shref="[^<>]*"><img\ssrc="([^<>]*)"\sstyle="[^<>]*"\s/></a>')
	#���򣺴�����ҳ���ȡͼƬ��С
	dsz=re.compile('<div>.*\s::\s[0-9]+\sx\s[0-9]+\s::\s(.*)</div>')
	#�����������ԭʼ��ͼ����ȡ���ַ
	pic=re.compile('<a\shref="([^<>"]*)">Download\soriginal')
	#�����������ԭʼ��ͼ����ȡ���С
	psz=re.compile('Download\soriginal\s[0-9]+\sx\s[0-9]+\s(.*)\ssource')
	#����cookie
	cookie_support=urllib2.HTTPCookieProcessor(cookielib.CookieJar())
	#����opener
	opener=urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
	#����header
	header={
	'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727)',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Accept-Charset':'utf-8;q=0.7,*;q=0.7',
	'Host':proxy,
	'connection':'keep-alive'}
	#��ҳ������ԭ��վ��GET��ʽ�ύ
	query={
	'u':'http://e-hentai.org/bounce_login.php?b=d&bt=1-1',
	'b':'4',
	'f':'norefer'}
	#EHentai�˺������룬û�еĻ�ɾ�����������ĵ�¼���֣������ǲ��ܴ�exhentai��
	login={
	'ipb_login_password':'1993x429',#�����������
	'ipb_login_submit':'Login!',
	'ipb_login_username':'fffonion'}#��������˻�
	#����������ҳ��
	try:
		Url='http://%s/index.php'%(proxy)
		req=urllib2.Request(Url,headers=header)
		opener.open(req).read()
		print unicode('�ɹ��򿪴�����վ��','utf-8')
	except urllib2.HTTPError,e:
		print unicode('�޷��򿪴�����վ : %s'%(e),'utf-8')
		sys.exit(1)
	#��¼E-Hentai��վ
	try:
		header['Referer']=Url
		Url='http://%s/browse.php?%s'%(proxy,urllib.urlencode(query))
		req=urllib2.Request(Url,data=urllib.urlencode(login),headers=header)
		opener.open(req).read()
		print unicode('�ɹ���¼��ʿ(��)��','utf-8')
		del query['f']
		header['Referer']=Url
		query['u']='http://exhentai.org/'
		Url='http://%s/browse.php?%s'%(proxy,urllib.urlencode(query))
		req=urllib2.Request(Url,headers=header)
		opener.open(req).read()
		print unicode('�ɹ���¼��ʿ(��)��','utf-8')
	except urllib2.HTTPError,e:
		print unicode('��¼ʧ�� : %s'%(e),'utf-8')
		sys.exit(1)
	#�������Ŀ¼
	path='\\'.join(path.split('\\'))
	if not os.path.isdir(path):os.mkdir(path)
	path+='\\'
	#��������ѭ��
	try:
		#��Ŀ¼ҳ��
		header['Referer']=Url
		query['u']=addr
		Url='http://%s/browse.php?%s'%(proxy,urllib.urlencode(query))
		req=urllib2.Request(Url,headers=header)
		content=opener.open(req).read()
		NUM=num.findall(content)
		PGE=idx.findall(content)
		if NUM and PGE:
			NUM=int(NUM[0])
			print unicode('������ %03d ��ͼƬ��'%(NUM),'utf-8')
			t=0
			for i in xrange(NUM):
				while 1:
					try:
						if t>10:
							print unicode('�ۼ�10�δ����˳���','utf-8')
							sys.exit(1)
						header['Referer']=Url
						req=urllib2.Request(PGE[0],headers=header)
						content=opener.open(req).read()
						print unicode('�� %03d ��ҳ���Ѵ�'%(i+1),'utf-8'),
						name='%s%03d.jpg'%(path,i+1)
						if os.path.isfile(name):
							print unicode('ͼƬ�Ѿ�����','utf-8')
						else:
							PIC=pic.findall(content)
							if PIC:
								PSZ=psz.findall(content)
								print unicode('--> [�����] -->','utf-8'),
								header['Referer']=Url
								query['u']=PIC[0]
								req=urllib2.Request(PIC[0],headers=header)
								photo=opener.open(req).read()
								if float(len(photo))*1.02<GetSize(PSZ[0]):
									print unicode('Download Error','utf-8')
									time.sleep(5)
									t+=1
									continue
								else:
									print unicode('�������','utf-8')
									file=open(name,'wb')
									file.write(photo)
									file.close()
							else:
								ADR=adr.findall(content)
								if ADR:
									DSZ=dsz.findall(content)
									print unicode('--> [��ͨ��] -->','utf-8'),
									req=urllib2.Request(ADR[0],headers=header)
									photo=opener.open(req).read()
									if float(len(photo))*1.02<GetSize(DSZ[0]):
										print unicode('Download Error','utf-8')
										time.sleep(5)
										t+=1
										continue
									else:
										print unicode('�������','utf-8')
										file=open(name,'wb')
										file.write(photo)
										file.close()
								else:
									print unicode('��ҳ��δ�ҵ�ͼƬ��','utf-8')
						Url=PGE[0]
						PGE=nxt.findall(content)
						if PGE:
							t=0
							break
						else:
							print unicode('δ�ҵ���һҳͼƬ��','utf-8')
							time.sleep(5)
							t+=1
					except socket.error,e:
						print unicode('Socket Error %s'%(e),'utf-8')
						time.sleep(5)
						t+=1
					except urllib2.URLError,e:
						print unicode('URL Error %s'%(e),'utf-8')
						time.sleep(5)
						t+=1
					except httplib.BadStatusLine,e:
						print unicode('Status Error','utf-8')
						time.sleep(5)
						t+=1
		else:
			print unicode('δ����ͼƬ��','utf-8')
	except urllib2.HTTPError,e:
		print unicode('ͼƬ����ʧ�� : %s'%(e),'utf-8')
		sys.exit(1)
	
if __name__=='__main__':
	addr=raw_input('Input URL : ')
	path=raw_input('Input DIR : ')
	addr=unicode(addr,'utf-8')
	path=unicode(path,'utf-8')
	ProxyDown(addr,path)