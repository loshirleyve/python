# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import os
import shutil

audio_path = ''
final_audio = ''


# 合并多个音频文件
def merge_file():
    path = os.path.join(os.getcwd(), 'audio')
    audios = os.listdir(path)  # 得到文件夹下的所有文件名称
    global final_audio
    final_audio = open('final_audio.mp3', 'wb')
    for audioIdx in range(len(audios)):
        name = str(audioIdx) + '.mp3'
        print(audioIdx)
        audiocode = open(os.path.join(path, name), 'rb')
        final_audio.write(audiocode.read())
        audiocode.close()
    final_audio.flush()
    final_audio.close()


# 声明为异步函数
async def job(session, url, idx):
    # 获得名字
    # name = url.split('/')[-1]
    suffix = url.split('.')[-1]
    name = str(idx) + '.' + suffix
    # 触发到await就切换，等待get到数据
    audio = await session.get(url)
    # 读取内容
    audiocode = await audio.read()

    # 写入至文件
    with open(audio_path + "/" + str(name), 'wb') as f:
        f.write(audiocode)
        return str(url)


async def main(loop, fileurl):
    # 建立会话 session
    async with aiohttp.ClientSession() as session:
        # 建立所有任务
        tasks = [loop.create_task(job(session, fileurl[_], _)) for _ in range(len(fileurl))]
        print(len(fileurl))
        # 触发await，等待任务完成
        finished, unfinished = await asyncio.wait(tasks)
        # 获取所有结果
        # all_results = [r.result() for r in finished]
        # print("ALL RESULT:"+str(all_results))


def done_callback(futu):
    print('Done')
    merge_file()


def init():
    path = os.getcwd()  # 文件夹目录
    global audio_path
    audio_path = os.path.join(path, 'audio')

    # 如果目录存在，直接删除
    if os.path.exists(audio_path):
        shutil.rmtree(audio_path)

    os.mkdir(audio_path)

    url = "https://delta-oss.ivykid.com/base/__k3om25xh__1.mp3", "https://delta-oss.ivykid.com/base/__k3om25yc__2.mp3", "https://delta-oss.ivykid.com/base/__k3om25yl__3.mp3", "https://delta-oss.ivykid.com/base/__k3om2fcq__0.mp3", "https://delta-oss.ivykid.com/base/__k3om2fd1__1.1.mp3", "https://delta-oss.ivykid.com/base/__k3om2fd9__2.1.mp3", "https://delta-oss.ivykid.com/base/__k3om2fsr__3.1.mp3", "https://delta-oss.ivykid.com/base/__k3om2ftj__4.1.mp3", "https://delta-oss.ivykid.com/base/__k3om2w8n__1.1.mp3", "https://delta-oss.ivykid.com/base/__k3om2w8v__1.2.mp3", "https://delta-oss.ivykid.com/base/__k3om2w90__1.3.mp3", "https://delta-oss.ivykid.com/base/__k3om2wk7__2.1.mp3", "https://delta-oss.ivykid.com/base/__k3pdtyu6__2.3.mp3", "https://delta-oss.ivykid.com/base/__k3om2wnb__2.4.mp3", "https://delta-oss.ivykid.com/base/__k3om3dml__0.mp3", "https://delta-oss.ivykid.com/base/__k3om3dn4__1.mp3", "https://delta-oss.ivykid.com/base/__k3om3dnb__2.mp3", "https://delta-oss.ivykid.com/base/__k3omykwf__0.mp3", "https://delta-oss.ivykid.com/base/__k3omykwu__1.mp3", "https://delta-oss.ivykid.com/base/__k3omykwz__2.mp3", "https://delta-oss.ivykid.com/base/__k3omyl9e__3.mp3", "https://delta-oss.ivykid.com/base/__k3omyl9f__4.mp3", "https://delta-oss.ivykid.com/base/__k3omyl9g__5.mp3", "https://delta-oss.ivykid.com/base/__k3on8avt__1.mp3", "https://delta-oss.ivykid.com/base/__k3on8aw3__2.mp3", "https://delta-oss.ivykid.com/base/__k3on8g1o__1.mp3", "https://delta-oss.ivykid.com/base/__k3on8g1z__2.mp3", "https://delta-oss.ivykid.com/base/__k3on8g26__3.mp3", "https://delta-oss.ivykid.com/base/__k3on8g6l__4.mp3"

    loop = asyncio.get_event_loop()
    futu = asyncio.ensure_future(main(loop, url))
    futu.add_done_callback(done_callback)
    # loop.run_until_complete(main(loop, url))
    loop.run_until_complete(futu)
    loop.close()


init()
