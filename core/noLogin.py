# 思路，先打包一个不会关闭的chromium  登录
# 测试idea 方法,则不登录测试购买
import os
import asyncio
from pyppeteer import launch
import datetime
import time

width, height = 1600, 900
USERNAME = '15927853463'
PASSWORD = 'whyyan.1020'
BUY_TIME = '2020-11-15 20:39:55'
buy_time_object = datetime.datetime.strptime(BUY_TIME, '%Y-%m-%d %H:%M:%S')
async def main():
    url = 'https://login.taobao.com/member/login.jhtml'
    browser = await launch(
        #设置pyppeteer为有头模式
        headless=False,
        #设置网页大小，无监控头
        args=[f'--window-size={width},{height}', '--disable-infobars']
    )
    #在浏览器上创建新页面
    # page = await browser.pages()[0]
    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
    await page.setViewport({'width': width, 'height': height})
    # await page.goto(url)
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
    # await page.type('input#fm-login-id', USERNAME)
    #password =
    # await page.type('input#fm-login-password', PASSWORD)
    time.sleep(2)

    # await page.click('.fm-btn')
    await asyncio.sleep(2)
    #await asyncio.sleep(2)
    #await buy(page)
    await test(page)

async def test(page):#测试从页面进入到提交订单
    print('test()')
    # url = 'https://item.taobao.com/item.htm?spm=a1z0d.6639537.1997196601.4.520a7484BZhDBa&id=5210509988'
    # url = 'https://chaoshi.detail.tmall.com/item.htm?id=20739895092&spm=a1z0k.6846577.0.0.15c326c1w9EH9B&_u=t2dmg8j26111'
    url = 'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.arkpub201114.2904984870.1.241aRVHxRVHxjF&id=620017913203'
    await page.goto(url)
    await asyncio.sleep(1)#await是关键字，理解为同步的意思
    # if await page.J('#J_isku>div>dl>dd>ul>li>a'):
    #     isku = await page.J('#J_isku>div>dl>dd>ul>li>a')
    #     await isku.click() #默认选中第一个
    if await page.J('.J_TSaleProp>li>a'):
        isku = await page.J('.J_TSaleProp>li>a')
        await isku.click() #默认选中第一个
    #await page.evaluate('document.querySelector("#J_Amount>span>input").value=""')
    await page.evaluate('document.querySelector("#J_Amount>span>input").value=""')#运行读取js代码，清空了商品数量
    #await page.type('#J_Amount>span>input','2')
    await page.type('#J_Amount>span>input','1')#这里是修改商品数量，暂时写死了，后面可以通过解析限购数量来获取
    await asyncio.sleep(10)
    # await page.click("#J_LinkBuy")
    while True:
        now = datetime.datetime.now()
        if now >= buy_time_object:
            try:
                if await page.J("#J_LinkBuy"):
                    await page.click('#J_LinkBuy')
                    print("进入提交订单页面")
                    print(datetime.datetime.now())
                    #await page.click('#submitOrderPC_1>div>a')
                else:
                    await page.click('#J_juValid>div>.J_LinkBuy')
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


asyncio.get_event_loop().run_until_complete(main())