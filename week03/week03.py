from multiprocessing import Pool , cpu_count , Manager, Lock
from concurrent.futures import ThreadPoolExecutor 
import argparse, os, re, socket
import time
# print(cpu_count())

def command():
    '''返回parser.parse_args()'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', dest='number', type=int, default=4 , help='设置并发数量')
    parser.add_argument('-f', dest='ping_or_tcp',type=str, choices=['ping', 'tcp'], help='ping测试')
    parser.add_argument('-w', dest='wirte',type=str, default=None, help='结果保存')
    parser.add_argument('-m', dest='mood',type=str, choices=['proc', 'thread'], help='结果保存')
    parser.add_argument('-ip', dest='ip',type=str, help='结果保存')
    parser.add_argument('-v',dest='run_time', type=str, default=None, help= '查看运行时间')
    return parser.parse_args()
    # print(parser.parse_args().number)

def thread_run(run, args):
    '''以进程模型运行'''
    p = Pool(cpu_count())
    print('进程开始')
    # lock = Manager().RLock() # 定义一个进程锁
    # lock = Lock()
    lock = 1
    for i in args:
        p.apply_async(run,args=(i,lock,))
    p.close()
    p.join()
    print('进程结束')


def line_run(run, args):
    '''线程模型运行'''
    with ThreadPoolExecutor(3) as executor:
        executor.map(run, args)


def ping_test(ip, lock):
    '''测试ping'''
    # lock.acquire() # 锁住
    result = os.system(f'ping {ip}')
    if result == 0:
        print('ip连接正常')
    else:
        print('ip连接不正常')
    # lock.release() # 释放


def tcp_test(ipandport, lock, result_file_name=None ):
    '''测试端口时否开放'''
    # lock.acquire() # 锁住
    # time.sleep(4)
    ip = ipandport[0]
    port = ipandport[1]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip, port))
        result = '{0} port {1} is open'.format(ip, port)
        print(result)
        if result_file_name:
            logFile(result_file_name, result)
    except :
        result = '{0} port {1} is not open'.format(ip, port)
        print(result)
        if result_file_name :
            logFile(result_file_name, result)
    finally:
        server.close()
        # lock.release() # 释放

def logFile(filename, text):
    '''存储日志文件'''
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(str(localtime) + ': ' + text + '\r\n')


def run(command_word):
    # time.sleep(4)
    # print(i)
    ip_regex = re.compile('[^-]+')#分离ip地址
    ip_last_regex = re.compile('[^.]+')
    mo = ip_regex.findall(command_word.ip)
    ip_head = ip_last_regex.findall(mo[0])[-1]
    ip_list_lang = len( ip_head )
    ip_start = int( ip_head )#起始扫描地址段
    ip_end = int( ip_last_regex.findall(mo[-1])[-1] ) + 1#终止扫描地址段
    
    if command_word.mood =='thread':
        run_mood = line_run #以线程模式运行
    else:
        run_mood = thread_run #以进程模式运行
    if command_word.ping_or_tcp == 'ping':
        args = [mo[0][0:-ip_list_lang] + str(i) for i in range(ip_start, ip_end)]
        print('ping测试开始')
        run_mood(ping_test, args)
    else:
        args = [(mo[0] , i) for i in range(1,1024)]
        print('tcp测试开始')
        run_mood(tcp_test, args)

    



if __name__ == '__main__':
    start = time.time()
    # thread_run(run)

    l = 1
    # ping_test('127.0.0.1',l)
    thread_run(ping_test,['127.0.0.1','127.0.0.2'])
    # thread_run(ssss, ['+654+5+64+7+41+6416+','hfdkjdhsiuhfusfhdushkvkdsugvdyahoudvhuhsohnsdioa'])
    command_word = command()
    run(command_word)
    # print(command_word.ping_or_tcp)
    # print(command_word.ip)
    ip_regex = re.compile('[^-]+')#分离ip地址
    ip_last_regex = re.compile('[^.]+')
    mo = ip_regex.findall(command_word.ip)
    print(mo[0])
    print(mo[-1][0:-1])
    # print(mo[0])
    ip_start = int( ip_last_regex.findall(mo[0])[-1] )
    ip_end = int( ip_last_regex.findall(mo[-1])[-1] )
    ip_head = ip_last_regex.findall(mo[0])
    print(ip_head)
    print(ip_start)
    print(ip_end)
    # tcp_test('127.0.0.1','88')
    # x = [i for i in range(1,1)]
    # print(x)
    end = time.time()
    print(end-start)
