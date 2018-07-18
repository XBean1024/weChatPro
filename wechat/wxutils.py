# -*- coding:utf-8 -*-
import time
from io import StringIO
import itchat
import os
import math
import matplotlib.pyplot as plt
import random
import Image
from PIL import ImageFont
from wordcloud import WordCloud
import jieba
import re
import pygame
import os


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("--文件夹已创建---")
    else:
        print("---文件夹已存在!---")


# 获取头像
def headImg():
    print("正在获取头像……………………")
    friends = itchat.get_friends(update=True)
    # itchat.get_head_img() 获取到头像二进制，并写入文件，保存每张头像
    print("您的好友总数为：" + str(len(friends)))
    mkdir("img")  # 调用函数
    for count, f in enumerate(friends):
        # 根据userName获取头像
        print("正在创建第" + str(count) + "头像")
        img = itchat.get_head_img(userName=f["UserName"])
        imgFile = open("img/" + str(count) + ".png", "wb")
        imgFile.write(img)
        imgFile.close()


# 头像拼接图
def createImg():
    x = 0
    y = 0
    imgs = os.listdir("img")
    random.shuffle(imgs)
    # 创建640*640的图片用于填充各小图片
    newImg = Image.new('RGBA', (640, 640))
    # 以640*640来拼接图片，math.sqrt()开平方根计算每张小图片的宽高，
    width = int(math.sqrt(640 * 640 / len(imgs)))
    # 每行图片数
    numLine = 640 / width
    for count, i in enumerate(imgs):
        path = "img/" + i
        try:
            if os.path.getsize(path) == 0:  # 获取文件大小
                os.remove(path)
                continue
            img = Image.open(path)
            # 缩小图片
            img = img.resize((width, width), Image.ANTIALIAS)
            # 拼接图片，一行排满，换行拼接
            newImg.paste(img, (x * width, y * width))
            print(path + "  " + str(count))
            x += 1
            if x >= numLine:
                x = 0
                y += 1
        except IOError as e:
            print(repr(e))
            # continue
    newImg.save("all.png")


# 性别统计
def getSex():
    friends = itchat.get_friends(update=True)
    sex = dict()
    for f in friends:
        if f["Sex"] == 1:  # 男
            sex["man"] = sex.get("man", 0) + 1
        elif f["Sex"] == 2:  # 女
            sex["women"] = sex.get("women", 0) + 1
        else:  # 未知
            sex["unknown"] = sex.get("unknown", 0) + 1
    # 柱状图展示
    for i, key in enumerate(sex):
        plt.bar(key, sex[key])
    plt.savefig("getsex.png")  # 保存图片
    plt.ion()
    plt.pause(5)
    plt.close()  # 图片显示5s，之后关闭
    # plt.show() #不建议用show，show是堵塞式


# 获取个性签名
def getSignature():
    friends = itchat.get_friends(update=True)
    print(friends)
    file = open('name_sign.txt', 'a', encoding='utf-8')
    text = ""
    for count, f in enumerate(friends):
        rec = re.compile("1f\d+\w*|[<>/=]")

        signature = f["Signature"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        signature = rec.sub("", signature)

        # remarks = f["RemarkName"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        # remarks = rec.sub("", remarks)

        nickname = f["NickName"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        nickname = rec.sub("", nickname)

        print("昵称：" + nickname)
        # print("备注：" + remarks)
        print("签名：" + signature)
        print("---------------------")
        strs = str(count) + " \n昵称：" + nickname + "\n" + "签名：" + signature + "\n"
        if not signature.strip():
            text = text + "签名：" + signature + "\n"
        file.write(strs + "\n")
    saveTxtToPNG(text)


# 生成词云图
def create_word_cloud(filename):
    # 读取文件内容
    text = open("{}.txt".format(filename), encoding='utf-8').read()

    # 注释部分采用结巴分词
    # wordlist = jieba.cut(text, cut_all=True)
    # wl = " ".join(wordlist)

    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置最大显示的词云数
        max_words=2000,
        # 这种字体都在电脑字体中，window在C:\Windows\Fonts\下，mac下可选/System/Library/Fonts/PingFang.ttc 字体
        font_path='C:\\Windows\\Fonts\\simfang.ttf',
        height=500,
        width=500,
        # 设置字体最大值
        max_font_size=60,
        # 设置有多少种随机生成状态，即有多少种配色方案
        random_state=30,
    )

    myword = wc.generate(text)  # 生成词云 如果用结巴分词的话，使用wl 取代 text， 生成词云图
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file('signature.png')  # 把词云保存下


def removeIpg():
    jpg = os.listdir("img")
    jpg.sort()
    for img in jpg:
        if img.endswith('.jpg'):
            print(img)
            os.remove("img/" + img)  # 要加完整路径


def saveTxtToPNG(text):
    print("将文本保存为图片")
    pygame.init()

    im = Image.new("RGB", (2000, 45000), (255, 255, 255))
    from PIL import ImageDraw
    dr = ImageDraw.Draw(im)
    font_size = 30
    font = ImageFont.truetype(os.path.join("fonts", "minishaoer.ttc"), font_size)

    dr.text((50, 5), text, font=font, fill="#000000")

    im.show()
    im.save("t.png")
    print("保存为图片--Done")


def getFriendsList():
    print("获取成员列……")
    fds = itchat.get_friends(update=True)
    print(fds)
    fs = []
    for count, f in enumerate(fds):
        nickname = f["NickName"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        print(nickname)
        fs.append(nickname)
    return fs


def createChatRoom():
    chatroomUserName = '@1234567'
    friend = getFriendsList()
    # friend = itchat.get_friends(update=True)
    print(friend)
    r = itchat.add_member_into_chatroom(chatroomUserName, friend)
    print(r)
    # if r['BaseResponse']['ErrMsg'] == '':
    #     status = r['MemberList'][0]['MemberStatus']
    #     # itchat.delete_member_from_chatroom(chatroom['UserName'], [friend])
    #     return {3: u'该好友已经将你加入黑名单。',
    #             4: u'该好友已经将你删除。', }.get(status,u'该好友仍旧与你是好友关系。')


def sendGroupAssistant():
    SINCERE_WISH = u'许彬彬\n\t祝 %s[%s]新年快乐！么么哒'

    friendList = itchat.get_friends(update=True)[0:]  # 排除登录者本人的微信
    print("开始群发消息")
    print("您总共有 " + str(len(friendList)) + " 个好友")
    for count, friend in enumerate(friendList):
        if count > 0:
            return
            # 如果是演示目的，把下面的方法改为print即可
        itchat.send("么么哒😘ლ(′◉❥◉｀ლ)", toUserName=friend['UserName'])
        print(str(count))
        itchat.send(
            SINCERE_WISH % (friend['DisplayName'] or friend['NickName'], friend['RemarkName'] or friend['PYQuanPin']),
            friend['UserName'])
        print(str(count) + " " + SINCERE_WISH % (
            friend['DisplayName'] or friend['NickName'], friend['RemarkName'] or friend['PYQuanPin']))
        time.sleep(.5)
    print("群发完成")


if __name__ == "__main__":
    print("扫码登陆……")
    itchat.auto_login(hotReload=True)
    print("登陆成功……")
    # print(itchat.search_friends())  # 获取自己的用户信息，返回自己的属性字典
    # print(itchat.search_friends(wechatAccount='qq18667155877'))  # 获取特定UserName的用户信息
    
    """
    itchat.auto_login(hotReload=True)
    @itchat.msg_register(itchat.content.TEXT) # msg.text 就是回复的文本信息内容
    def text_reply(msg):
        return '自动回复测试 ：' + msg.text
    itchat.run()
    """

    # itchat.send('Hello, filehelper', toUserName='filehelper')# 发送信息给文件助手
    # friends = itchat.get_friends(update=True)
    # print(friends)
    # headImg()
    # createImg()
    # removeIpg()
    # getSignature()
    # getFriendsList()
    # createChatRoom()
    sendGroupAssistant()  # 群发微信消息