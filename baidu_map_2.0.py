import os
import time
import execjs
import _thread
import requests
import configparser
from time import sleep
from random import randint


def exce_node_js_obj_data(top, right, level):
    os.environ["NODE_PATH"] = os.getcwd()+"/node_modules"
    nodejs = execjs.compile("""
        function getMapData(top, right, level) {
            var leftTop = top.split(',')
            var RightBottom = right.split(',')
            var TileLnglatTransformBaidu = require('tile-lnglat-transform').TileLnglatTransformBaidu;
            let mapData = {}
            t = TileLnglatTransformBaidu.lnglatToTile(
                leftTop[0], leftTop[1], level)
            r = TileLnglatTransformBaidu.lnglatToTile(
                RightBottom[0], RightBottom[1], level)
            mapData.x = [t.tileX, r.tileX]
            mapData.y = [r.tileY, t.tileY]
            return mapData;
        }
    """)
    sleep(1)
    print('获取点位成功')
    get_tiles(nodejs.call("getMapData", top, right, level))


def get_tiles(obj):
    xidx = obj['x']
    yidx = obj['y']
    print('开始爬虫！！！')
    try:
        _thread.start_new_thread(ing, ())
    except:
        print('error')
    for y in range(yidx[0], yidx[1]+1):
        for x in range(xidx[0], xidx[1]+1):
            url = "http://maponline{i}.bdimg.com/tile/?qt=vtile&x={x}&y={y}&z={z}&styles=pl" \
                "&scaler=1&udt={t}&from=jsapi2_0".format(
                    i=randint(0, 3), x=x, y=y, z=zoom_level, t=time.strftime("%Y%m%d", time.localtime()))
            save_pictures_via_url(url)
    sleep(1)
    global ing_b
    ing_b = 0
    sleep(1)
    openFile()


def ing():
    index = ["/", "─", "\\", ]
    while bool(int(ing_b)):
        for i in range(len(index)):
            print("\r"+index[i], end="")
            sleep(0.2)


def openFile():  # 完成
    print()
    print("爬取完成！即将打开存储空间")
    sleep(3)
    start_directory = os.getcwd()+"\\map\\"+file_name
    os.startfile(start_directory)


def save(res, x, y, z):
    if not os.path.isdir(path):
        print()
        print("创建储存环境")
        os.makedirs(path)
    sname = path+"/map{z}_{x}_{y}.png".format(z=z, x=x, y=y)
    with open(sname, 'ab') as pngf:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                pngf.write(chunk)
                pngf.flush()


def save_pictures_via_url(url):
    arr = url.split("&")
    save(requests.get(url),
         arr[1].replace("x=", ""),
         arr[2].replace("y=", ""),
         arr[3].replace("z=", ""))


if __name__ == "__main__":
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, "config.ini")
    conf = configparser.ConfigParser()
    conf.read(cfgpath, encoding="utf-8")
    top = conf.get("lan666", "top")
    right = conf.get("lan666", "right")
    zoom_level = conf.get("lan666", "zoom_level")
    ing_b = conf.get("lan666", "ing_b")
    file_name = conf.get("lan666", "file_name")
    path = os.getcwd()+"\\map\\"+file_name+"\\"

    print('程序初始化正常')
    exce_node_js_obj_data(top, right, zoom_level)
