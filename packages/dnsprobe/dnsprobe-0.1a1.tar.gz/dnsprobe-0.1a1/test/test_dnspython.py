from dns.resolver import NXDOMAIN, LifetimeTimeout, Resolver

# 定义要查询的域名
domain = "example123456xsafgnerib.com"


try:
    # 创建 DNS 解析器对象
    resolver = Resolver()
    # 设置 DNS 服务器（可选）
    resolver.nameservers = ['8.8.8.8']
    # 发起 A 记录查询
    answers = resolver.resolve(domain, lifetime=1.0)

    for answer in answers:
        print("IP Address:", answer.address)
except NXDOMAIN:
    print("NXDOMAIN")
except LifetimeTimeout:
    print("timeout")
