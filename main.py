"""
- 模拟查询tidb 集群 tidb 集群中已经创建了test database 以及user表
- 该脚本只能在tidb同一个k8s 集群中跑，否则网络则不通

"""

import time
import pymysql
import datetime
import os


def main():
    start = time.time()
    print("Starting connect to tidb....")
    db = pymysql.connect(host='basic-tidb.tidb-cluster.svc.cluster.local',
                         port=4000,
                         user='root',
                         database='test')
    print("Connected to tidb....")
    cursor = db.cursor()
    now = datetime.datetime.now()
    minute = now.minute
    # 读取出先前分钟数的第一位 如 18:30分钟  则 t1 = 3
    t1 = int(str(minute)[0])
    # 计算当前分钟数第二位 然后默认 * 1000  如 18：35分 则 5 * 1000
    times = (minute % 10) * os.getenv("TIMES", 1000)
    if (t1 % 2) == 0:
        # 为了让请求呈正弦分布，这里让times对称
        times = (10 - (minute % 10)) * os.getenv("TIMES", 1000)
    print("time: " + now.strftime("%Y-%m-%d %H:%M:%S") + "  times: ", str(times))
    while times > 0:
        cursor.execute("SELECT * from `app_user` limit 1")
        data = cursor.fetchall()
        times -= 1
    end = time.time()
    print("fetch data success,use time seconds=" + str(end - start))
    db.close()


if __name__ == "__main__":
    main()
