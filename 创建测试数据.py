import pymysql
from datetime import datetime

# 数据库配置信息
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',  # 替换为你的 MySQL 密码
    'charset': 'utf8mb4',
    'database': 'movie'  # 我们将创建的数据库名
}

def create_database_and_tables():
    """创建数据库和表结构"""
    try:
        # 首先连接 MySQL（不指定数据库）
        conn = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset=DB_CONFIG['charset']
        )
        cursor = conn.cursor()
        
        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"数据库 {DB_CONFIG['database']} 创建成功")
        
        # 切换到新数据库
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # 创建 user 表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            pwd VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            info TEXT,
            face VARCHAR(255),
            uuid VARCHAR(255) NOT NULL,
            addtime DATETIME NOT NULL
        )
        """)
        
        # 创建 comment 表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_id INT NOT NULL,
            user_id INT NOT NULL,
            content TEXT NOT NULL,
            addtime DATETIME NOT NULL
        )
        """)
        
        # 创建 moviecol 表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS moviecol (
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_id INT NOT NULL,
            user_id INT NOT NULL,
            addtime DATETIME NOT NULL
        )
        """)
        
        # 创建 userlog 表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS userlog (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            ip VARCHAR(100) NOT NULL,
            addtime DATETIME NOT NULL
        )
        """)
        
        print("所有表创建成功")
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"创建数据库或表时出错: {e}")
        return False

def execute_insert_statements():
    """执行所有插入语句"""
    try:
        # 连接到 movie 数据库
        conn = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            charset=DB_CONFIG['charset']
        )
        cursor = conn.cursor()
        
        # 插入用户数据
        users = [
            ('鼠', '1231', '1231@123.com', '13888888881', '鼠', '1f401.png', 'd32a72bdac524478b7e4f6dfc8394fc0'),
            ('牛', '1232', '1232@123.com', '13888888882', '牛', '1f402.png', 'd32a72bdac524478b7e4f6dfc8394fc1'),
            ('虎', '1233', '1233@123.com', '13888888883', '虎', '1f405.png', 'd32a72bdac524478b7e4f6dfc8394fc2'),
            ('兔', '1234', '1234@123.com', '13888888884', '兔', '1f407.png', 'd32a72bdac524478b7e4f6dfc8394fc3'),
            ('龙', '1235', '1235@123.com', '13888888885', '龙', '1f409.png', 'd32a72bdac524478b7e4f6dfc8394fc4'),
            ('蛇', '1236', '1236@123.com', '13888888886', '蛇', '1f40d.png', 'd32a72bdac524478b7e4f6dfc8394fc5'),
            ('马', '1237', '1237@123.com', '13888888887', '马', '1f434.png', 'd32a72bdac524478b7e4f6dfc8394fc6'),
            ('羊', '1238', '1238@123.com', '13888888888', '羊', '1f411.png', 'd32a72bdac524478b7e4f6dfc8394fc7'),
            ('猴', '1239', '1239@123.com', '13888888889', '猴', '1f412.png', 'd32a72bdac524478b7e4f6dfc8394fc8'),
            ('鸡', '1240', '1240@123.com', '13888888891', '鸡', '1f413.png', 'd32a72bdac524478b7e4f6dfc8394fc9'),
            ('狗', '1241', '1241@123.com', '13888888892', '狗', '1f415.png', 'd32a72bdac524478b7e4f6dfc8394fd0'),
            ('猪', '1242', '1242@123.com', '13888888893', '猪', '1f416.png', 'd32a72bdac524478b7e4f6dfc8394fd1')
        ]
        
        for user in users:
            cursor.execute(
                "INSERT INTO user (name, pwd, email, phone, info, face, uuid, addtime) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())",
                user
            )
        print("用户数据插入完成")
        
        # 插入评论数据
        comments = [
            (7, 1, "好看"),
            (7, 2, "不错"),
            (7, 3, "经典"),
            (7, 4, "给力"),
            (8, 5, "难看"),
            (8, 6, "无聊"),
            (8, 7, "乏味"),
            (8, 8, "无感")
        ]
        
        for comment in comments:
            cursor.execute(
                "INSERT INTO comment (movie_id, user_id, content, addtime) "
                "VALUES (%s, %s, %s, NOW())",
                comment
            )
        print("评论数据插入完成")
        
        # 插入收藏数据
        moviecols = [
            (7, 1), (7, 2), (7, 3), (7, 4),
            (8, 5), (8, 6), (8, 7), (8, 8)
        ]
        
        for moviecol in moviecols:
            cursor.execute(
                "INSERT INTO moviecol (movie_id, user_id, addtime) "
                "VALUES (%s, %s, NOW())",
                moviecol
            )
        print("收藏数据插入完成")
        
        # 插入用户日志数据
        userlogs = [
            (1, "192.168.4.1"), (2, "192.168.4.2"), (3, "192.168.4.3"),
            (4, "192.168.4.4"), (5, "192.168.4.5"), (6, "192.168.4.6"),
            (7, "192.168.4.7"), (8, "192.168.4.8"), (9, "192.168.4.9")
        ]
        
        for userlog in userlogs:
            cursor.execute(
                "INSERT INTO userlog (user_id, ip, addtime) "
                "VALUES (%s, %s, NOW())",
                userlog
            )
        print("用户日志数据插入完成")
        
        # 设置自增ID从1开始
        tables = ['user', 'comment', 'moviecol']
        for table in tables:
            cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
            print(f"{table} 表自增ID重置为1")
        
        conn.commit()
        print("所有数据插入完成并已提交")
        
        # 验证数据插入
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        print(f"成功插入 {user_count} 条用户数据")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"插入数据时出错: {e}")
        return False

def main():
    # 检查并创建数据库和表
    if not create_database_and_tables():
        print("数据库和表创建失败，程序终止")
        return
    
    # 执行插入操作
    if not execute_insert_statements():
        print("数据插入失败")
        return
    
    print("数据库初始化和数据插入全部完成！")

if __name__ == "__main__":
    main()
