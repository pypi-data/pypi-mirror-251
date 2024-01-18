#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2024/1/4 22:37
@File  : MonitorBrowser.py
'''

import copy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep
from threading import Thread, Lock
'''
selenium > 4.14
'''

thread_lock = Lock()

# 定义一个简单的线程类
class MyThread(Thread):
    def __init__(self, name, target, args, **kwargs):
        super().__init__()
        self.name = kwargs.get('name')
        self.target = kwargs.get('target')
        self.args = kwargs.get('args')
        self.stop_flag = False

    def run(self):
        # print(f"线程 {self.name} 启动")
        while not self.stop_flag:
            self.target(self.args)
            # print(f"线程 {self.name} 正在运行")
            sleep(0.5)
        # print(f"线程 {self.name} 结束")

    def stop(self):
        # print(f"停止线程 {self.name}")
        self.stop_flag = True


def add_js_current_page_thread(browser: WebDriver):
    '''  为当前页面注入JS用于监听动作 '''
    thread_lock.acquire()  # 获取锁
    print('当前窗口:', browser.current_window_handle)
    # 等待所有元素加载完成
    WebDriverWait(browser, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*'))
    )
    ''' 添加js事件监听器 '''
    async_js_code = """
        function getXPathForElement(element) {
            if (element && element.id !== "" && element.id !== undefined) {
                return '//' + element.tagName.toLowerCase() + '[@id="' + element.id + '"]';
            }else if (element && element.name !== "" && element.name !== undefined) {
                return '//' + element.tagName.toLowerCase() + '[@name="' + element.name + '"]';
            }else if (element && element.name !== "" && element.name !== undefined) {
                return '//' + element.tagName.toLowerCase() + '[@href="' + element.href + '"]';
            }else if (element && element.src !== "" && element.src !== undefined) {
                return '//' + element.tagName.toLowerCase() + '[@src="' + element.src + '"]';
            }else if (element && element.value !== "" && element.value !== undefined) {
                return '//' + element.tagName.toLowerCase() + '[@value="' + element.value + '"]';
            }else if (element && element.tagName.toLowerCase() === 'html' && !element.parentNode) {
                return '/html';
            }else{
                var index = 0;
                var siblings = element.parentNode.childNodes;
        
                for (var i = 0; i < siblings.length; i++) {
                    var sibling = siblings[i];
        
                    if (sibling === element) {
                        return getXPathForElement(element.parentNode) + '/' + element.tagName + '[' + (index + 1) + ']';
                    }
        
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                        index++;
                    }
                }
            } 
        }
    
        var callback = arguments[arguments.length - 1];
        var clickedElement = null;
    
        //document.addEventListener('click', function (event) {
        //    clickedElement = event.target;
        //    callback(getXPathForElement(clickedElement));
        //});
        
        // 遍历当前网页HTML文档中的所有元素
        var elements = document.querySelectorAll('*');
        //console.log(elements);
        // 遍历所有 iframe 元素
        //document.querySelectorAll('iframe').forEach(function (iframe) {
            // 获取 iframe 内部的文档
        //    var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
        
            // 选择 iframe 内部的所有元素并将它们添加到 elements 列表中
        //    Array.prototype.push.apply(elements, iframeDocument.querySelectorAll('*'));
        //});
        //console.log(elements);
        for (var i = 0; i < elements.length; i++) {
            elements[i].addEventListener('click', function(event) {
                var clickedElement = event.target;
                // 获取最近的包含 iframe 的祖先元素
                var iframeAncestor = clickedElement.closest("iframe");
                
                // 点击元素的xpath表达式
                var xpath = getXPathForElement(clickedElement);
                
                // 部分元素type为submit需要存储到缓存中
                if (clickedElement && clickedElement.tagName.toLowerCase() === 'input' && clickedElement.type === 'submit') {
                    localStorage.setItem('XPATH', getXPathForElement(clickedElement));
                }
                
                var value = {
                    "url": window.location.href,
                    "title": document.title,
                    "iframeAncestor": iframeAncestor,
                    "clickedElement": clickedElement.tagName,
                    "localStorage": localStorage.getItem('XPATH'),
                    "xpath": xpath
                }
                
                console.log(value);
                callback(value);
            });
        }
    """

    # 执行异步JavaScript代码并获取返回值
    try:
        local_xpath = browser.execute_script("return localStorage.getItem('XPATH')")
        if local_xpath:
            print("您点击元素的Xpath表达式:", local_xpath)
            browser.execute_script("localStorage.removeItem('XPATH')")
        else:
            result = browser.execute_async_script(async_js_code)
            # 输出返回值
            print("您点击元素的Xpath表达式:", result)
    except Exception as e:
        pass
    thread_lock.release()  # 释放锁
def add_js_all_page_thread(browser: WebDriver):
    ''' 监控所有标签页，每生成一个标签页就调用线程用于单独监控当前活动页内的操作 '''
    old_window_list = browser.window_handles
    all_thread = []
    print('准备监控所有标签页')
    while len(old_window_list) >= 1:
        print(f'old_window_list:{old_window_list}')
        print(f'window_handles:{browser.window_handles}')
        new_diff = list(set(browser.window_handles) - set(old_window_list))
        print('新增窗口:', new_diff)
        for w in new_diff: #list(set(browser.window_handles) - set(old_window_list)):
            print('''  有新标签生成需要切换并执行注入JS ''')
            all_thread.append(MyThread(name=w, target=add_js_current_page_thread, args=(browser, w,)))
            for t in all_thread:
                t.setDaemon(True)
                t.start()

        old_diff = list(set(old_window_list) - set(browser.window_handles))
        print('消失窗口：', old_diff)
        for w in old_diff: #list(set(old_window_list) - set(browser.window_handles)):
            print('''  有标签页关闭需要从线程列表中找到并关闭线程 ''')
            all_thread[old_window_list.index(w)].stop()
        old_window_list = copy.deepcopy(browser.window_handles)
        sleep(1)


def add_js_page_all_iframe_thread(browser: WebDriver):
    '''  为页面中所有iframe内注入JS用于监听动作 '''


class MonitorBrowser(object):
    def __init__(self):
        ''' 初始化浏览器对象 '''
        Options = webdriver.ChromeOptions()
        Options.add_experimental_option('useAutomationExtension', False)      # 去除"Chrome正在受到自动化测试软件的控制"弹出框信息
        Options.add_experimental_option('excludeSwitches', ['--enable-automation'])  # 去除"Chrome正在受到自动化测试软件的控制"弹出框信息
        Options.add_experimental_option('detach', True)                       # 禁止自动关闭浏览器
        Options.add_argument('--ignore-ssl-errors')
        Options.add_argument('--disable-blink-features=AutomationControlled')   # 隐藏Webdriver特征
        self.browser = webdriver.Chrome(options=Options)
        self.browser.implicitly_wait(30)

    def addJSEventListener(self):
        # 切换回主frame（如果有iframe的话）
        self.browser.switch_to.default_content()
        # 等待所有元素加载完成
        WebDriverWait(self.browser, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*'))
        )
        ''' 添加js事件监听器 '''
        async_js_code = """
            function getXPathForElement(element) {
                if (element && element.id !== "" && element.id !== undefined) {
                    return '//' + element.tagName.toLowerCase() + '[@id="' + element.id + '"]';
                }else if (element && element.name !== "" && element.name !== undefined) {
                    return '//' + element.tagName.toLowerCase() + '[@name="' + element.name + '"]';
                }else if (element && element.name !== "" && element.name !== undefined) {
                    return '//' + element.tagName.toLowerCase() + '[@href="' + element.href + '"]';
                }else if (element && element.src !== "" && element.src !== undefined) {
                    return '//' + element.tagName.toLowerCase() + '[@src="' + element.src + '"]';
                }else if (element && element.value !== "" && element.value !== undefined) {
                    return '//' + element.tagName.toLowerCase() + '[@value="' + element.value + '"]';
                }else if (element && element.tagName.toLowerCase() === 'html' && !element.parentNode) {
                    return '/html';
                }else{
                    var index = 0;
                    var siblings = element.parentNode.childNodes;
            
                    for (var i = 0; i < siblings.length; i++) {
                        var sibling = siblings[i];
            
                        if (sibling === element) {
                            return getXPathForElement(element.parentNode) + '/' + element.tagName + '[' + (index + 1) + ']';
                        }
            
                        if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                            index++;
                        }
                    }
                } 
            }
        
            var callback = arguments[arguments.length - 1];
            var clickedElement = null;
        
            //document.addEventListener('click', function (event) {
            //    clickedElement = event.target;
            //    callback(getXPathForElement(clickedElement));
            //});
            
            // 遍历当前网页HTML文档中的所有元素
            var elements = document.querySelectorAll('*');
            //console.log(elements);
            // 遍历所有 iframe 元素
            //document.querySelectorAll('iframe').forEach(function (iframe) {
                // 获取 iframe 内部的文档
            //    var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
            
                // 选择 iframe 内部的所有元素并将它们添加到 elements 列表中
            //    Array.prototype.push.apply(elements, iframeDocument.querySelectorAll('*'));
            //});
            //console.log(elements);
            for (var i = 0; i < elements.length; i++) {
                elements[i].addEventListener('click', function(event) {
                    var clickedElement = event.target;
                    // 获取最近的包含 iframe 的祖先元素
                    var iframeAncestor = clickedElement.closest("iframe");
                    
                    // 点击元素的xpath表达式
                    var xpath = getXPathForElement(clickedElement);
                    
                    // 部分元素type为submit需要存储到缓存中
                    if (clickedElement && clickedElement.tagName.toLowerCase() === 'input' && clickedElement.type === 'submit') {
                        localStorage.setItem('XPATH', getXPathForElement(clickedElement));
                    }
                    
                    var value = {
                        "iframeAncestor": iframeAncestor,
                        "clickedElement": clickedElement.tagName,
                        "localStorage": localStorage.getItem('XPATH'),
                        "xpath": xpath
                    }
                    
                    console.log(value);
                    callback(value);
                });
            }
        """

        # 执行异步JavaScript代码并获取返回值
        try:
            local_xpath = self.browser.execute_script("return localStorage.getItem('XPATH')")
            if local_xpath:
                print("您点击元素的Xpath表达式:", local_xpath)
                self.browser.execute_script("localStorage.removeItem('XPATH')")
            else:
                result = self.browser.execute_async_script(async_js_code)
                # 输出返回值
                print("您点击元素的Xpath表达式:", result)
        except Exception as e:
            pass

    def browser_status(self):
        ''' 关闭浏览器 '''
        try:
            self.browser.title
            return True
        except Exception as e:
            return False

    def start(self):
        ''' 启动浏览器 '''
        # self.browser.get('https://mail.163.com/')  # iframe案例
        self.browser.get('https://www.baidu.com/')  # type=submit案例
        self.browser.set_script_timeout(10)
        while self.browser_status():
            all_window = self.browser.window_handles
            for w in all_window:
                self.browser.switch_to.window(w)
                add_js_current_page_thread(self.browser,)
            # self.addJSEventListener()
            sleep(0.1)
        self.browser.quit()


if __name__ == '__main__':
    MonitorBrowser().start()