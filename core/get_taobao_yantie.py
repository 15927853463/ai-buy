import os
import asyncio
from pyppeteer import launch
import datetime
import time
import random
# from exe_js import js1, js2, js3, js4, js5
# from alifunc import mouse_slide, input_time_random
from core.User import User

width, height = 1600, 900
count = int (input("开启多少个窗口"))
# ==== 设定账号密码 （修改此处，指定账号密码）====
users = list()
i = 0
user = User('15927853463', 'whyyan.1020')
while i < count:
    i += 1
    u = User(str(input("请输入第"+str(i)+"个账号")),str(input("请输入第"+str(i)+"个密码")))
    users.append(u)

# USERNAME = '15377645098'
# PASSWORD = 'wcyxfkl1234'
# ==== 设定抢购 截止时间 （修改此处，指定抢购时间点）====
BUY_TIME = str(input("抢购时间，例如：早上八点半就是  0830"))
now_time = datetime.datetime.now()
BUY_TIME = str(now_time.date())+' '+BUY_TIME[0:2]+":"+BUY_TIME[2:]+':00'
print('抢购开始时间：'+BUY_TIME)
#BUY_TIME = '2020-11-15 17:15:55'
buy_time_object = datetime.datetime.strptime(BUY_TIME, '%Y-%m-%d %H:%M:%S')

#if now_time > buy_time_object:
#    print("当前已过抢购时间，请确认抢购时间是否填错...")
#    exit(0)

async def main():
    url = 'https://login.taobao.com/member/login.jhtml'
    #global browser
    global i

    #在浏览器上创建新页面
    #pages = await browser.pages()
    #page = pages[0]
    #await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
    #await page.setViewport({'width': width, 'height': height})
    await asyncio.gather(*[test() for _ in range(count)])  # 开启5个窗口并发
    await asyncio.sleep(100000)

async def test():#测试从页面进入到提交订单
    global i
    #global browser
    i-=1
    index = i
    print('test('+str(index)+')')
    browser = await launch(
        #设置pyppeteer为有头模式
        headless=True,
        #设置网页大小，无监控头
        args=[f'--window-size={width},{height}'
            ,'--disable-infobars'
              #,'–disable-gpu'
              #,'–disable-dev-shm-usage'
              #,'–disable-setuid-sandbox'
              #,'–no-first-run'
              #,'–no-sandbox'
              #,'–no-zygote'
              #,'–single-process'
              ]
    )
    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
    await page.setViewport({'width': width, 'height': height})
    url = 'https://login.taobao.com/member/login.jhtml'
    await page.goto(url)
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }'''
    )
    #await page.evaluate(js)
    # await page.evaluate(js3)
    # await page.evaluate(js4)
    # await page.evaluate(js5)
    time.sleep(1)

    #await page.click('i#J_Quick2Static')
    #username =
    await page.type('input#fm-login-id', users[index].username)
    #password =
    await page.type('input#fm-login-password', users[index].password)
    await asyncio.sleep(2)
    #await page.evaluate('document.querySelector("button.password-login").click()')
    await page.click('.fm-btn')
    await asyncio.sleep(2)
    url = 'https://item.taobao.com/item.htm?spm=a1z0d.6639537.1997196601.4.520a7484BZhDBa&id=5210509988'
    #url = 'https://chaoshi.detail.tmall.com/item.htm?id=20739895092&spm=a1z0k.6846577.0.0.15c326c1w9EH9B&_u=t2dmg8j26111'
    #url = 'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.arkpub201114.2904984870.1.241aRVHxRVHxjF&id=620017913203'
    #url = 'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.20085333.9396952460.1.4cf054b4U8czGv&id=627324251849&locType=B2C&scm=1007.32172.190329.0.FF-hyhsfZD-627324251849_I-base_Q-2ca15bb7-2b01-4c33-8236-e6c8eeb452b2_T-ITEM_appId-22172_calibCTR-0_calibCVR-0_finalScore-0.6978095992_predCTR-0_predCVR-0.6978095992-FF&from_scene=B2C&skuId=4443916844327'
    await page.goto(url)
    await asyncio.sleep(4)#await是关键字，理解为同步的意思

    if await page.J('#J_isku>div>dl>dd>ul>li>a'):
        isku = await page.J('#J_isku>div>dl>dd>ul>li>a')
        await isku.click() #默认选中第一个
    #if await page.J('.J_TSaleProp>li>a'):
    #    isku = await page.J('.J_TSaleProp>li>a')
    #    await isku.click() #默认选中第一个
    await page.evaluate('document.querySelector("#J_IptAmount").value=""')
    #await page.evaluate('document.querySelector("#J_Amount>span>input").value=""')#运行读取js代码，清空了商品数量
    #await page.type('#J_Amount>span>input','1')
    await page.type('#J_IptAmount','1')#这里是修改商品数量，暂时写死了，后面可以通过解析限购数量来获取
    await asyncio.sleep(10)
    # await page.click("#J_LinkBuy")
    while True:
        now = datetime.datetime.now()
        if now >= buy_time_object:
            try:
                if await page.evaluate('document.querySelector("#J_LinkBuy")'):
                    await page.evaluate('document.querySelector("#J_LinkBuy").click()')
                    print("进入提交订单页面")
                    print(datetime.datetime.now())
                    #await page.click('#submitOrderPC_1>div>a')
                else:
                    await page.evaluate('document.querySelector("#J_juValid>div>.J_LinkBuy").click()')
                    print("进入提交订单页面")
                    print(datetime.datetime.now())
                while True:
                    try:#可能会出现页面未加载完的情况，死循环到点击了提交订单按钮
                        await page.evaluate('document.querySelector("#submitOrderPC_1>div>a.go-btn").click()')
                        print('提交订单')
                        print(datetime.datetime.now())
                        break
                    except Exception as e:
                        continue
            except Exception as e:
                continue


async def buy(page):
    #await page.goto('https://cart.taobao.com/cart.htm')
    # await page.goto('https://chaoshi.detail.tmall.com/item.htm?spm=a220l.1.0.0.2eb57f33q2MFLp&id=20739895092')
    await page.goto('https://chaoshi.detail.tmall.com/item.htm?id=20739895092&spm=a1z0k.6846577.0.0.15c326c1w9EH9B&_u=t2dmg8j26111')
    await asyncio.sleep(1)

    if await page.J("div#J_SelectAll1"):
        all = await page.J("div#J_SelectAll1")
        await all.click()
        print("已经选中购物车中全部商品 ...")

    await asyncio.sleep(1)

    submit_succ = False
    retry_submit_time = 1
    while True:
        now = datetime.datetime.now()
        if now >= buy_time_object:
            print('到达抢购时间，开始执行抢购...尝试次数' + str(retry_submit_time))
            if submit_succ:
                print('订单提交成功...')
                break
            if retry_submit_time > 50:
                print('超过次数，放弃尝试...')
                break

            retry_submit_time += 1

            try:
                if await page.J('a#J_Go'):
                    a = await page.J('a#J_Go')
                    await a.click()
                    print('点击结算按钮')
                    await asyncio.sleep(1)

                    click_submit_time = 1
                    while True:
                        try:
                            if click_submit_time < 10:
                                b = await page.J('a.go-btn')
                                await b.click()
                                print('已经点击提交订单按钮')
                                await asyncio.sleep(1)
                                submit_succ = True
                                break
                            else:
                                print('提交订单失败')


                                #await page.goto('https://cart.taobao.com/cart.htm')
                                #if await page.J("div#J_SelectAll1"):
                                #    all = await page.J("div#J_SelectAll1")
                                #    await all.click()
                                #    print("已经选中购物车中全部商品 ...")
                                #if await page.J('a#J_Go'):
                                #    a = await page.J('a#J_Go')
                                #    await a.click()
                                #    print('点击结算按钮')
                                #    await asyncio.sleep(1)
                        except Exception as ee:
                            print('未发现提交订单按钮，重试')

                            click_submit_time += 1
                            time.sleep(0.1)
                            await page.click('.info-img')
            except Exception as e:
                print(e)
                print('挂了，提交订单失败')
        await asyncio.sleep(0.1)

async def wait(page):
    print("当前距离抢购时间点还有较长时间，开始定时刷新防止登录超时...")
    while True:
            currenTime = datetime.datetime.now()
            if (buy_time_object - currenTime).seconds > 180:
                await page.goto('https://chaoshi.detail.tmall.com/item.htm?id=20739895092&spm=a1z0k.6846577.0.0.15c326c1w9EH9B&_u=t2dmg8j26111&skuId=4227830352490')
                print((buy_time_object - currenTime).seconds)
                print("刷新购物车界面，防止登录超时...")
                await asyncio.sleep(60)
            else:
                print((buy_time_object - currenTime).seconds)
                break

asyncio.get_event_loop().run_until_complete(main())


