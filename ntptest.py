import ntplib
from datetime import datetime

def test_ntp_server(server, num_tests):
    failures = 0
    total_delay = 0
    
    for i in range(num_tests):
        try:
            client = ntplib.NTPClient()
            response = client.request(server, version=3, timeout=1)
            delay = round(response.delay * 1000, 2)  # 将延迟转换为毫秒并保留两位小数
            total_delay += delay
            str_time = datetime.fromtimestamp(response.tx_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"NTP服务器 {server} 的第{i+1}次延迟为：{delay} 毫秒，获取到的时间为：{str_time}")
        except Exception as e:
            failures += 1
            print(f"无法连接到NTP服务器 {server}，错误信息：{str(e)}")
    
    if num_tests > 0:
        avg_delay = round(total_delay / num_tests, 2)
        print(f"NTP服务器 {server} 的延迟平均值为：{avg_delay} 毫秒\n")
    
    return failures, avg_delay

def main():
    file_path = 'ntp_servers.txt'  # txt 文件路径
    with open(file_path, 'r') as f:
        servers = f.readlines()
    
    num_tests = 4  # 测试次数
    
    results = []
    
    for server in servers:
        server = server.strip()  # 去除换行符和空格
        if server:
            print(f"正在测试服务器：{server}")
            failures, avg_delay = test_ntp_server(server, num_tests)
            results.append((avg_delay, failures, server))
    
    # 根据失败次数和平均延迟进行排序
    results.sort(key=lambda x: (x[1], x[0]))
    
    print("\n===== 排序结果 =====")
    print(f"延时(毫秒){'':4}失败次数{'':4}服务器地址")
    for avg_delay, failures, server in results:
        print(f"{avg_delay: <12}  {failures: <10}  {server}")

if __name__ == '__main__':
    main()
