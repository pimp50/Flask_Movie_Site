import pymysql
from datetime import datetime

# 数据库配置信息
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',  # 替换为您的 MySQL 密码
    'charset': 'utf8mb4',
    'database': 'movie'  # 数据库名称
}

def create_database_and_tables():
    """创建数据库和所有表结构"""
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
        
        # 创建前台表
        
        # 1. 会员表 (user)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            pwd VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            phone VARCHAR(20) NOT NULL UNIQUE,
            info TEXT,
            face VARCHAR(255) UNIQUE,
            uuid VARCHAR(255) NOT NULL UNIQUE,
            addtime DATETIME NOT NULL
        )
        """)
        
        # 2. 会员登录日志表 (userlog)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS userlog (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            ip VARCHAR(100) NOT NULL,
            addtime DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
        )
        """)
        
        # 3. 标签表 (tag)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tag (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            addtime DATETIME NOT NULL
        )
        """)
        
        # 4. 电影表 (movie)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL UNIQUE,
            url VARCHAR(255) NOT NULL UNIQUE,
            info TEXT,
            logo VARCHAR(255) UNIQUE,
            star TINYINT UNSIGNED,
            playnum BIGINT UNSIGNED DEFAULT 0,
            commentnum BIGINT UNSIGNED DEFAULT 0,
            tag_id INT NOT NULL,
            area VARCHAR(100),
            release_time DATE,
            length VARCHAR(20),
            addtime DATETIME NOT NULL,
            FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
        )
        """)
        
        # 5. 上映预告表 (preview)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS preview (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL UNIQUE,
            logo VARCHAR(255) UNIQUE,
            addtime DATETIME NOT NULL
        )
        """)
        
        # 6. 评论表 (comment)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content TEXT NOT NULL,
            movie_id INT NOT NULL,
            user_id INT NOT NULL,
            addtime DATETIME NOT NULL,
            FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
        )
        """)
        
        # 7. 电影收藏表 (moviecol)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS moviecol (
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_id INT NOT NULL,
            user_id INT NOT NULL,
            addtime DATETIME NOT NULL,
            FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
        )
        """)
        
        # 创建后台表
        
        # 8. 权限表 (auth)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            url VARCHAR(255) NOT NULL UNIQUE,
            addtime DATETIME NOT NULL
        )
        """)
        
        # 9. 角色表 (role)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS role (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            auths VARCHAR(255),
            addtime DATETIME NOT NULL
        )
        """)
        
        # 10. 管理员表 (admin)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            pwd VARCHAR(100) NOT NULL,
            is_super TINYINT UNSIGNED DEFAULT 0,
            role_id INT,
            addtime DATETIME NOT NULL,
            FOREIGN KEY (role_id) REFERENCES role(id) ON DELETE SET NULL
        )
        """)
        
        # 11. 管理员登录日志表 (adminlog)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS adminlog (
            id INT AUTO_INCREMENT PRIMARY KEY,
            admin_id INT NOT NULL,
            ip VARCHAR(100) NOT NULL,
            addtime DATETIME NOT NULL,
            FOREIGN KEY (admin_id) REFERENCES admin(id) ON DELETE CASCADE
        )
        """)
        
        # 12. 操作日志表 (oplog)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS oplog (
            id INT AUTO_INCREMENT PRIMARY KEY,
            admin_id INT NOT NULL,
            ip VARCHAR(100) NOT NULL,
            reason VARCHAR(255),
            addtime DATETIME NOT NULL,
            FOREIGN KEY (admin_id) REFERENCES admin(id) ON DELETE CASCADE
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
    """执行所有插入语句，添加测试数据"""
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
        
        # 1. 插入标签数据
        tags = [
            "动作", "喜剧", "科幻", "恐怖", "爱情", 
            "剧情", "动画", "悬疑", "犯罪", "冒险"
        ]
        
        for tag_name in tags:
            cursor.execute(
                "INSERT INTO tag (name, addtime) VALUES (%s, NOW())",
                (tag_name,)
            )
        print(f"成功插入 {len(tags)} 条标签数据")
        
        # 2. 插入用户数据
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
        
        # 3. 插入电影数据 (假设标签ID从1开始)
        movies = [
            ('肖申克的救赎', r"C:\Users\联想\Desktop\调试信息.mp4", '两个被囚禁的男人在多年间建立了友谊...', 'shawshank.jpg', 5, 1, '美国', '1994-09-23', '142分钟'),
            ('阿甘正传', 'movie2.mp4', '一个智商只有75的男人取得惊人成就的故事...', 'forrestgump.jpg', 5, 2, '美国', '1994-07-06', '142分钟'),
            ('盗梦空间', 'movie3.mp4', '一群梦境窃贼的故事...', 'inception.jpg', 5, 3, '美国', '2010-07-16', '148分钟'),
            ('泰坦尼克号', 'movie4.mp4', '豪华邮轮上的爱情悲剧...', 'titanic.jpg', 5, 4, '美国', '1997-12-19', '195分钟'),
            ('星际穿越', 'movie5.mp4', '一群探险家穿越虫洞的故事...', 'interstellar.jpg', 5, 3, '美国', '2014-11-07', '169分钟'),
            ('楚门的世界', 'movie6.mp4', '一个男人发现自己生活是电视节目的故事...', 'truman.jpg', 5, 2, '美国', '1998-06-05', '103分钟'),
            ('这个杀手不太冷', 'movie7.mp4', '职业杀手和一个小女孩的故事...', 'leon.jpg', 5, 1, '法国', '1994-09-14', '133分钟'),
            ('海上钢琴师', 'movie8.mp4', '一个在船上度过一生的钢琴师的故事...', 'pianist.jpg', 5, 5, '意大利', '1998-10-28', '165分钟')
        ]
        
        for movie in movies:
            cursor.execute(
                "INSERT INTO movie (title, url, info, logo, star, tag_id, area, release_time, length, addtime) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())",
                movie
            )
        print("电影数据插入完成")
        
        # 4. 插入上映预告数据
        previews = [
            ('复仇者联盟5', 'avengers5.jpg'),
            ('阿凡达3', 'avatar3.jpg'),
            ('蜘蛛侠：英雄归来', 'spiderman.jpg'),
            ('星球大战10', 'starwars10.jpg')
        ]
        
        for preview in previews:
            cursor.execute(
                "INSERT INTO preview (title, logo, addtime) VALUES (%s, %s, NOW())",
                preview
            )
        print("上映预告数据插入完成")
        
        # 5. 插入评论数据
        comments = [
            (1, 1, "这部电影让我热泪盈眶"),
            (1, 2, "史上最佳电影之一"),
            (2, 3, "阿甘的精神令人感动"),
            (3, 4, "诺兰的又一神作"),
            (4, 5, "永恒的经典"),
            (5, 6, "科幻电影的巅峰"),
            (6, 7, "发人深省的电影"),
            (7, 8, "让·雷诺的经典之作"),
            (8, 9, "音乐和画面都太美了")
        ]
        
        for comment in comments:
            cursor.execute(
                "INSERT INTO comment (movie_id, user_id, content, addtime) "
                "VALUES (%s, %s, %s, NOW())",
                comment
            )
        print("评论数据插入完成")
        
        # 6. 插入电影收藏数据
        moviecols = [
            (1, 1), (1, 2), (1, 3), (2, 4),
            (3, 5), (4, 6), (5, 7), (6, 8),
            (7, 9), (8, 10), (1, 5), (3, 7)
        ]
        
        for moviecol in moviecols:
            cursor.execute(
                "INSERT INTO moviecol (movie_id, user_id, addtime) "
                "VALUES (%s, %s, NOW())",
                moviecol
            )
        print("收藏数据插入完成")
        
        # 7. 插入会员登录日志数据
        userlogs = [
            (1, "192.168.4.1"), (2, "192.168.4.2"), (3, "192.168.4.3"),
            (4, "192.168.4.4"), (5, "192.168.4.5"), (6, "192.168.4.6"),
            (7, "192.168.4.7"), (8, "192.168.4.8"), (9, "192.168.4.9"),
            (10, "192.168.4.10"), (11, "192.168.4.11"), (12, "192.168.4.12")
        ]
        
        for userlog in userlogs:
            cursor.execute(
                "INSERT INTO userlog (user_id, ip, addtime) "
                "VALUES (%s, %s, NOW())",
                userlog
            )
        print("用户日志数据插入完成")
        
        # 8. 插入权限数据
        auths = [
            ("添加标签", "/admin/tag/add"),
            ("编辑标签", "/admin/tag/edit"),
            ("标签列表", "/admin/tag/list"),
            ("添加电影", "/admin/movie/add"),
            ("电影列表", "/admin/movie/list"),
            ("添加预告", "/admin/preview/add"),
            ("预告列表", "/admin/preview/list"),
            ("会员列表", "/admin/user/list"),
            ("评论列表", "/admin/comment/list"),
            ("收藏列表", "/admin/moviecol/list"),
            ("操作日志", "/admin/oplog/list"),
            ("管理员登录日志", "/admin/adminloginlog/list"),
            ("权限添加", "/admin/auth/add"),
            ("权限列表", "/admin/auth/list"),
            ("角色添加", "/admin/role/add"),
            ("角色列表", "/admin/role/list"),
            ("管理员添加", "/admin/admin/add"),
            ("管理员列表", "/admin/admin/list")
        ]
        
        for auth in auths:
            cursor.execute(
                "INSERT INTO auth (name, url, addtime) VALUES (%s, %s, NOW())",
                auth
            )
        print("权限数据插入完成")
        
        # 9. 插入角色数据
        roles = [
            ("超级管理员", "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"),
            ("内容管理员", "1,2,3,4,5,6,7,8,9,10"),
            ("用户管理员", "8,9,10"),
            ("日志管理员", "11,12")
        ]
        
        for role in roles:
            cursor.execute(
                "INSERT INTO role (name, auths, addtime) VALUES (%s, %s, NOW())",
                role
            )
        print("角色数据插入完成")
        
        # 10. 插入管理员数据
        admins = [
            ("admin", "admin123", 1, None),
            ("content_admin", "content123", 0, 2),
            ("user_admin", "user123", 0, 3),
            ("log_admin", "log123", 0, 4)
        ]
        
        for admin in admins:
            cursor.execute(
                "INSERT INTO admin (name, pwd, is_super, role_id, addtime) "
                "VALUES (%s, %s, %s, %s, NOW())",
                admin
            )
        print("管理员数据插入完成")
        
        # 11. 插入管理员登录日志数据
        adminlogs = [
            (1, "192.168.1.1"), (1, "192.168.1.2"), (2, "192.168.1.3"),
            (3, "192.168.1.4"), (4, "192.168.1.5")
        ]
        
        for adminlog in adminlogs:
            cursor.execute(
                "INSERT INTO adminlog (admin_id, ip, addtime) "
                "VALUES (%s, %s, NOW())",
                adminlog
            )
        print("管理员登录日志数据插入完成")
        
        # 12. 插入操作日志数据
        oplogs = [
            (1, "192.168.1.1", "添加了新电影"),
            (2, "192.168.1.2", "修改了标签"),
            (3, "192.168.1.3", "禁用了用户"),
            (4, "192.168.1.4", "查看了日志")
        ]
        
        for oplog in oplogs:
            cursor.execute(
                "INSERT INTO oplog (admin_id, ip, reason, addtime) "
                "VALUES (%s, %s, %s, NOW())",
                oplog
            )
        print("操作日志数据插入完成")
        
        # 设置自增ID从1开始
        tables = [
            'user', 'userlog', 'tag', 'movie', 'preview',
            'comment', 'moviecol', 'auth', 'role', 'admin',
            'adminlog', 'oplog'
        ]
        
        for table in tables:
            cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
            print(f"{table} 表自增ID重置为1")
        
        conn.commit()
        print("所有数据插入完成并已提交")
        
        # 验证数据插入
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        print(f"成功插入 {user_count} 条用户数据")
        
        cursor.execute("SELECT COUNT(*) FROM movie")
        movie_count = cursor.fetchone()[0]
        print(f"成功插入 {movie_count} 条电影数据")
        
        cursor.execute("SELECT COUNT(*) FROM admin")
        admin_count = cursor.fetchone()[0]
        print(f"成功插入 {admin_count} 条管理员数据")
        
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
    
    print("\n数据库初始化和数据插入全部完成！")
    print("前台系统包含：会员、电影、标签、评论等模块")
    print("后台系统包含：管理员、权限、角色、日志等模块")
    print("您可以使用以下账号登录后台：")
    print("超级管理员: admin / admin123")
    print("内容管理员: content_admin / content123")
    print("用户管理员: user_admin / user123")
    print("日志管理员: log_admin / log123")

if __name__ == "__main__":
    main()
