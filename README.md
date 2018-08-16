# weChatPro

## 该工程最初为了学习itchat而建，现在是一个python工具类


## 开发日志：
### 2018/8/16 
    renamefile.py
    
    新增一个工具类，用来批量重命名mac 系统下的一个文件夹下的所有文件
    原文件：/Users/binny/study/PS/CS6/094
    重命名：/Users/binny/study/PS/CS6/094曲线调整
    
    说明：
       原文件夹有两个文件
       1、曲线调整.exe
       2、教程使用说明.html
       原文件名表意不明，故修改为序号名+其子文件名

### 开发环境
##### python3.6
##### [mac-osx 版本安装](https://www.python.org/downloads/mac-osx/)
##### itchat 安装
    pip install itchat

 
##### 群发消息
    def sendGroupAssistant():
        SINCERE_WISH = u'你的名字\n\t祝 %s[%s]新年快乐！么么哒'
    
        friendList = itchat.get_friends(update=True)[0:]  # 排除登录者本人的微信
        print("开始群发消息")
        print("您总共有 " + str(len(friendList)) + " 个好友")
        for count, friend in enumerate(friendList):
            itchat.send("么么哒😘ლ(′◉❥◉｀ლ)", toUserName=friend['UserName'])
            print(str(count))
            itchat.send(
                SINCERE_WISH % (friend['DisplayName'] or friend['NickName'], friend['RemarkName'] or friend['PYQuanPin']),
                friend['UserName'])
            print(str(count) + " " + SINCERE_WISH % (
                friend['DisplayName'] or friend['NickName'], friend['RemarkName'] or friend['PYQuanPin']))
            time.sleep(.5)
        print("群发完成")
        
##### 获取朋友信息

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
##### 将文本保存为图片（获取个性签名中 有用到）

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
        
##### 获取个性签名
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
##### 获取头像，并保存
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


##### 头像拼接图
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
        print("保存完成")
##### 视图
![](https://github.com/Xbean1024/weChatPro/blob/master/wechat/all.png)
##### 全局变量
    告诉编译器这是全局变量a
    global a
    
    def set_value(value):
        # 告诉编译器我在这个方法中使用的a是刚才定义的全局变量a,而不是方法内部的局部变量.
        global a
        a = value
    
    def get_value():
        # 同样告诉编译器我在这个方法中使用的a是刚才定义的全局变量a,并返回全局变量a,而不是方法内部的局部变量.
        global a
        return a