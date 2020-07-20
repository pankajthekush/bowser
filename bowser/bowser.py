from urllib.parse import urlparse
import requests
from bs4.element import Comment # pylint: disable=import-error
from bs4 import BeautifulSoup # pylint: disable=import-error
import pycurl # pylint: disable=import-error
from io import BytesIO
import json
import zlib
import brotli # pylint: disable=import-error
import gzip


class LinkCheck():
    def __init__(self,wbstring):
        self.headers = dict()
        self.wbstring = wbstring
        self.return_data = dict()
        self.get_info()


    def display_header(self,header_line):

        header_line = header_line.decode('iso-8859-1')

        # Ignore all lines without a colon
        if ':' not in header_line:
            return

        # Break the header line into header name and value
        h_name, h_value = header_line.split(':', 1)

        # Remove whitespace that may be present
        h_name = h_name.strip()
        h_value = h_value.strip()
        h_name = h_name.lower() # Convert header names to lowercase
        self.headers[h_name] = h_value # Header name and value.


    def get_info(self):
        storege = BytesIO()
        #b_obj = BytesIO()
        crl = pycurl.Curl() #curl object
        crl.setopt(crl.URL, self.wbstring) #setting url
        crl.setopt(crl.HEADERFUNCTION, self.display_header) # get headers
        crl.setopt(pycurl.TIMEOUT, 60)
        crl.setopt(pycurl.MAXREDIRS,5) 
        crl.setopt(pycurl.FOLLOWLOCATION, 1) 
        crl.setopt(pycurl.WRITEFUNCTION, storege.write) #write response to byte object
        crl.setopt(pycurl.SSL_VERIFYPEER,0) # ignore server certificate verification
        crl.setopt(pycurl.SSL_VERIFYHOST,0) #fix ssl certificate subject name error
        
        crl.setopt(pycurl.USERAGENT,'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')

        crl.setopt(pycurl.HTTPHEADER,["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                "Accept-Encoding: gzip, deflate, br",
                                "Connection: keep-alive"])        
        
        try:
            crl.perform()
        except Exception:
            self.return_data['input_url'] = self.wbstring
            self.return_data['output_url'] = 'error'
            self.return_data['body'] = 'error'
            self.return_data['status-code'] ='error'
            return

        st_code = crl.getinfo(pycurl.RESPONSE_CODE)
        locaiton = crl.getinfo(pycurl.EFFECTIVE_URL)
        crl.close()

        #get html by curl
        encoding = self.headers.get('content-encoding')
    
        html = None
        
        if encoding == 'gzip':
            try:
                #handle zlib.error: Error -3 while decompressing data: incorrect header check
                decompressed_data=zlib.decompress(storege.getvalue(), 16+zlib.MAX_WBITS)
                html  = decompressed_data
               
            except Exception as e:
                self.return_data['input_url'] = self.wbstring
                self.return_data['output_url'] = 'error'
                self.return_data['body'] = 'error'
                self.return_data['status-code'] ='error'
                self.return_data['error-comment'] = str(e)
                return
        elif encoding == 'br':
            try:
                decompressed_data = brotli.decompress(storege.getvalue())
                html  = decompressed_data
            except Exception as e:
                self.return_data['input_url'] = self.wbstring
                self.return_data['output_url'] = 'error'
                self.return_data['body'] = 'error'
                self.return_data['status-code'] ='error'
                self.return_data['error-comment'] = str(e)
                return
            
        elif encoding == 'deflate':
            try:
                html  = storege.getvalue()
            except Exception as e:
                self.return_data['input_url'] = self.wbstring
                self.return_data['output_url'] = 'error'
                self.return_data['body'] = 'error'
                self.return_data['status-code'] ='error'
                self.return_data['error-comment'] = str(e)
                return
        else:
            self.return_data['input_url'] = self.wbstring
            self.return_data['output_url'] = 'error'
            self.return_data['body'] = 'error'
            self.return_data['status-code'] ='error'
            self.return_data['error-comment'] = 'invalid content type'
            return

        visible_html = text_from_html(html)
        visible_html = visible_html.strip()
        self.return_data['input_url'] = self.wbstring
        self.return_data['output_url'] = locaiton
        self.return_data['body'] = visible_html
        self.return_data['status-code'] =st_code

        


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    print(texts)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)


def parse_url(url):

    result = urlparse(url)
    dict_result  = dict()

    dict_result['schema'] = result.scheme
    dict_result['netloc']  = result.netloc
    dict_result['path'] = result.path
    dict_result['params'] = result.params
    dict_result['quey'] = result.query
    dict_result['fragment'] = result.fragment
    return dict_result


class UrlChecker():
    def __init__(self,input_url,output_url=None,url_body=None,status_code=None):

        self.ucheck_result = dict()

        self.input_url = input_url
        self.output_url = output_url
        self.url_body = url_body
        self.status_code = status_code


        
        self.input_url_schema = None
        self.input_url_netloc = None
        self.input_url_path = None
        self.input_url_params = None
        self.input_url_query = None
        self.input_url_fragment = None


        self.output_url_schema = None
        self.output_url_netloc = None
        self.output_url_path = None
        self.output_url_params = None
        self.output_url_query = None
        self.output_url_fragment = None

        if self.output_url is None:
            lc = LinkCheck(self.input_url)
            dict_url_data = lc.return_data
            self.output_url = dict_url_data['output_url']
            self.url_body = dict_url_data['body']
            self.status_code = dict_url_data['status_code']

    def set_parsed_url_data(self):
        dict_input_url = parse_url(self.input_url)
        dict_output_url = parse_url(self.output_url)

         
        self.input_url_schema = dict_input_url['scheme']
        self.input_url_netloc = dict_input_url['netloc']
        self.input_url_path = dict_input_url['path']
        self.input_url_params = dict_input_url['params']
        self.input_url_query = dict_input_url['query']
        self.input_url_fragment = dict_input_url['fragment']



        self.output_url_schema = dict_output_url['scheme']
        self.output_url_netloc = dict_output_url['netloc']
        self.output_url_path = dict_output_url['path']
        self.output_url_params = dict_output_url['params']
        self.output_url_query = dict_output_url['query']
        self.output_url_fragment = dict_output_url['fragment']

    def compare_url(self):
        #if output url is not good 
        if self.output_url_schema is None or len(self.output_url_schema <=2):
            self.ucheck_result['input_url'] = self.input_url
            self.ucheck_result['output_url'] = self.output_url
            self.ucheck_result['status_code'] = self.status_code
            
            


        
            
        



    



if __name__ == "__main__":
    lc = LinkCheck('https://www.cloudsavvyit.com/1046/reduce-your-websites-size-with-gzip-and-deflate-compression/')
    print(lc.return_data)
