#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.web
import os
import re
import time


class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
        <html>
          <head><title>Upload File</title></head>
          <body>
            <form action='file' enctype="multipart/form-data" method='post'>
            <input type='file' name='file'/><br/>
            <input type='submit' value='submit'/>
            </form>
            <li><a href="download/3333"/>333</li> 
          </body>
        </html>
        ''')

    def post(self):
        # 文件的暂存路径
        upload_path=os.path.join(os.path.dirname(__file__),'files')  
        # 提取表单中‘name’为‘file’的文件元数据
        file_metas=self.request.files['file']    
        for meta in file_metas:
            filename = meta['filename']
            filepath = os.path.join(upload_path,filename)
            # 有些文件需要已二进制的形式存储，实际中可以更改
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
            self.write('finished!')


class DownloadFileHandler(tornado.web.RequestHandler):
    def get(self,filename):
        print('i download file handler : ',filename)
        # Content-Type这里我写的时候是固定的了，也可以根据实际情况传值进来
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename='+filename)
        # 读取的模式需要根据实际情况进行修改
        filepath = os.path.join(os.path.dirname(__file__),'static/UploadImage/1.bmp')
        with open(filepath, 'rb') as f:
            while True:
                data = f.read()
                if not data:
                    break
                self.write(data)
        # 记得有finish哦
        self.finish()


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class UploadImageHandler(tornado.web.RequestHandler):
    def post(self):
        # 文件的暂存路径
        upload_path=os.path.join(os.path.dirname(__file__),'static/UploadImage')  
        # 提取表单中‘name’为‘file’的文件元数据
        file_metas=self.request.files['upload']    
        for meta in file_metas:
            filename=meta['filename']
            callback=self.get_argument("CKEditorFuncNum")
            if re.compile(r"[\S]+\.(png|jpg|gif|bmp)").match(filename):
                filename = time.strftime("%Y%m%d%H%M%S")+re.findall(r"(\.png|\.jpg|\.gif|\.bmp)", filename)[0]
                filepath = os.path.join(upload_path, filename)
                # 有些文件需要已二进制的形式存储，实际中可以更改
                with open(filepath,'wb') as up:
                    up.write(meta['body'])
                    script = "<script type=\"text/javascript\">"
                    script2 = "window.parent.CKEDITOR.tools.callFunction(" + callback + ",'" + \
                              "/static/UploadImage/" + filename + "','')"
                    script3="</script>"
                self.write(script+script2+script3)
            else:
                script="<script type=\"text/javascript\">"
                script2 = u"window.parent.CKEDITOR.tools.callFunction(" + callback + u",''," \
                          + u"'文件格式不正确（必须为.jpg/.gif/.bmp/.png文件）');"
                script3 = u"</script>"

                self.write(script+script2+script3)


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "debug": True
}

app = tornado.web.Application([
    (r'/file',UploadFileHandler),
    (r'/download/([0-9]+)', DownloadFileHandler),
    (r'/', IndexHandler),
    (r'/UploadImages', UploadImageHandler),
    ], **settings)


if __name__ == '__main__':
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()