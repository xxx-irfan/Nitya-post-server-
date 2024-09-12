import requests
import os
import re
import sys
import time
import json
import http.server
import socketserver
import threading
from requests.exceptions import RequestException

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b' CR3T3D BY XM9RTY AYUSH K1NG')

def execute_server():
    PORT = int(os.environ.get('PORT', 4000))
    with socketserver.TCPServer(('', PORT), MyHandler) as httpd:
        print(f'Server running at http://localhost:{PORT}')
        httpd.serve_forever()

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f'File Not Found: {file_path}')
        return None

def read_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f'File Not Found: {file_path}')
        return []

def make_request(url, headers, cookie):
    try:
        response = requests.get(url, headers=headers, cookies={'Cookie': cookie})
        return response.text
    except RequestException as e:
        print(f'Error making request: {e}')
        return None

def mafiya():
    cookies_data = read_lines('AK-COOKIE.txt')
    if not cookies_data:
        return

    headers = {
        'User-Agent': ('Mozilla/5.0 (Linux; Android 11; RMX2144 Build/RKQ1.201217.002; wv) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 '
                       'Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/375.1.0.28.111;]')
    }

    valid_cookies = []
    for cookie in cookies_data:
        response = make_request('https://business.facebook.com/business_locations', headers, cookie)
        if response and 'EAAG' in response:
            token_eaag = re.search(r'(EAAG\w+)', response).group(1)
            valid_cookies.append((cookie, token_eaag))

    if not valid_cookies:
        print('No valid cookie found. Exiting...')
        return

    id_post = int(read_file('post.txt'))
    commenter_name = read_file('name.txt')
    delay = int(read_file('speed.txt'))
    comments = read_lines('file.txt')

    if not id_post or not commenter_name or not delay or not comments:
        print('Missing required input data. Exiting...')
        return

    x, y, cookie_index = 0, 0, 0
    while True:
        try:
            time.sleep(delay)
            comment_text = comments[x].strip()
            comment_with_name = f'{commenter_name}: {comment_text}'
            current_cookie, token_eaag = valid_cookies[cookie_index]
            data = {'message': comment_with_name, 'access_token': token_eaag}
            response = requests.post(f'https://graph.facebook.com/{id_post}/comments/', data=data, cookies={'Cookie': current_cookie}).json()

            current_time = time.strftime('%Y-%m-%d %I:%M:%S %p')
            if 'id' in response:
                print(f'Post id: {id_post}')
                print(f'  - Time: {current_time}')
                print(f'COOKIE NUMBER: {cookie_index + 1}')
                print(f'Comment sent: {comment_with_name}')
            else:
                y += 1
                print(f'[{y}] Status: Failure')
                print(f'COOKIE NUMBER: {cookie_index + 1}')
                print(f'Link: https://m.basic.facebook.com//{id_post}')
                print(f'Comments: {comment_with_name}\n')

            x = (x + 1) % len(comments)
            cookie_index = (cookie_index + 1) % len(valid_cookies)
        except RequestException as e:
            print(f'Error making request: {e}')
            time.sleep(5.5)

def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()
    mafiya()

if __name__ == '__main__':
    main()
