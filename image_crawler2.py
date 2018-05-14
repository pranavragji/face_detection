# -*- coding:utf-8 -*-
import requests
import os
import io
import imghdr
import uuid
import json

query = input('検索名: ')
dir_name = input('保存ディレクトリ名: ')
all_img = input('ダウンロード枚数: ')

endpoint = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'
headers = { 'Ocp-Apim-Subscription-Key': '0234f84c9d464fc4960e31f76e338829' }
params = {
    'q':query,
    'mkt':'en-US',
    'count':50,
}
ImageUrls = []

#ダウンロードする画像URLのリストを作成(ImageUrls)
def GetImageUrls(endpoint, headers, params):
    global ImageUrls
    for i in range(int(all_img) // params['count']):
        offset = i * params['count']
        params['offset'] = offset

        response_json = requests.get(endpoint, headers=headers, params=params)
        response = json.loads(response_json.text)

        for i in range(params['count']):
            ImageUrls.append(response['value'][i]['contentUrl'])
    return ImageUrls

#imagesディレクトリの下に個別ディレクトリを作成
def mkdir(dir_name):
    if os.path.isdir('images'+'/'+dir_name) == False:
        os.mkdir('images'+'/'+dir_name)
    else:
        pass

#ImageUrlsリスト内の画像をダウンロード
def DownloadImages(ImageUrls, dir_name):
    TIMEOUT = 5
    num_err = 0
    num_suc = 0

    for ImageUrl in ImageUrls:
        try:
            response_image = requests.get(ImageUrl, timeout=TIMEOUT)
            image_binary = response_image.content
        except requests.exceptions.RequestException:
            num_err += 1
            continue

        #画像ファイルを解析し、jpg、png、それ以外を判別、jpg、pngのみダウンロード
        with io.BytesIO(image_binary) as fh:
            image_type = imghdr.what(fh)

            if image_type == 'jpeg':
                extension = '.jpg'
            elif image_type == 'png':
                extension = '.png'
            else:
                continue

            file_name = str(uuid.uuid4()) + extension
        with open('images'+'/'+dir_name+'/'+file_name, 'wb') as f:
            f.write(image_binary)
            f.close()
        num_suc += 1
    print('エラー数: '+ str(num_err))
    print('ダウンロード数: '+ str(num_suc))

GetImageUrls(endpoint, headers, params)
mkdir(dir_name)
DownloadImages(ImageUrls, dir_name)
