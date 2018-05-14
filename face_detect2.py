# -*- coding:utf-8 -*-
import cv2, os, argparse, shutil

SAVE_PATH = "/users/TatsuruKikuchi/images/Donald_Trump/cutted_images/"
cascade_path = '/usr/local/Cellar/opencv/3.4.1_2/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'

# 基本的なモデルパラメータ
FLAGS = None

# 学習済モデルの種類
CASCADE = ["default","alt","alt2","tree","profile","nose"]

# 直接実行されている場合に通る(importされて実行時は通らない)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cascade",
        type=str,
        default="alt",
        choices=CASCADE,
        help="cascade file."
  )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.3,
        help="scaleFactor value of detectMultiScale."
  )
    parser.add_argument(
        "--neighbors",
        type=int,
        default=2,
        help="minNeighbors value of detectMultiScale."
  )
    parser.add_argument(
        "--min",
        type=int,
        default=80,
        help="minSize value of detectMultiScale."
  )
    parser.add_argument(
        "--input_dir",
        type=str,
        default="./images/Donald_Trump/",
        help="The path of input directory."
  )
    parser.add_argument(
        "--move_dir",
        type=str,
        default="./done/",
        help="The path of moving detected files."
  )

# パラメータ取得と実行
FLAGS, unparsed = parser.parse_known_args()

# 分類器ディレクトリ(以下から取得)
# https://github.com/opencv/opencv/blob/master/data/haarcascades/
# https://github.com/opencv/opencv_contrib/blob/master/modules/face/data/cascades/

# 学習済モデルファイル
# if   FLAGS.cascade == CASCADE[0]:#"default":
#     cascade_path = "./models/haarcascade_frontalface_default.xml"
# elif FLAGS.cascade == CASCADE[1]:#"alt":
#     cascade_path = "./models/haarcascade_frontalface_alt.xml"
# elif FLAGS.cascade == CASCADE[2]:#"alt2":
#     cascade_path = "./models/haarcascade_frontalface_alt2.xml"
# elif FLAGS.cascade == CASCADE[3]:#"tree":
#     cascade_path = "./models/haarcascade_frontalface_alt_tree.xml"
# elif FLAGS.cascade == CASCADE[4]:#"profile":
#     cascade_path = "./models/haarcascade_profileface.xml"
# elif FLAGS.cascade == CASCADE[5]:#"nose":
#     cascade_path = "./models/haarcascade_mcs_nose.xml"

#カスケード分類器の特徴量を取得する
faceCascade = cv2.CascadeClassifier(cascade_path)

# 顔検知に成功した数(デフォルトで0を指定)
face_detect_count = 0

# 顔検知に失敗した数(デフォルトで0を指定)
face_undetected_count = 0

# フォルダ内ファイルを変数に格納(ディレクトリも格納)
files =  os.listdir(FLAGS.input_dir)

# 成功ファイルを移動いない場合は、出力用のディレクトリが存在する場合、削除して再作成
if FLAGS.move_dir == "":
    if os.path.exists(SAVE_PATH):
        shutil.rmtree(SAVE_PATH)
    os.mkdir(SAVE_PATH)

print(FLAGS)

# 集めた画像データから顔が検知されたら、切り取り、保存する。
for file_name in files:

    # ファイルの場合(ディレクトリではない場合)
    if os.path.isfile(FLAGS.input_dir + file_name):

        # 画像ファイル読込
        img = cv2.imread(FLAGS.input_dir + file_name)

        # 大量に画像があると稀に失敗するファイルがあるのでログ出力してスキップ(原因不明)
        if img is None:
            print(file_name + ':Cannot read image file')
            continue

        # カラーからグレースケールへ変換(カラーで顔検出しないため)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 顔検出
        face = faceCascade.detectMultiScale(gray, scaleFactor=FLAGS.scale, minNeighbors=FLAGS.neighbors, minSize=(FLAGS.min, FLAGS.min))

        if len(face) > 0:
            for rect in face:
                # 切り取った画像出力
                cv2.imwrite(SAVE_PATH + str(face_detect_count) + file_name, img[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]])
                face_detect_count = face_detect_count + 1

            # 検出できたファイルは移動
            if FLAGS.move_dir != "":
                shutil.move(FLAGS.input_dir + file_name, FLAGS.input_dir + FLAGS.move_dir)
        else:
            print(file_name + ':No Face')
            face_undetected_count = face_undetected_count + 1

print('Undetected Image Files:%d' % face_undetected_count)
