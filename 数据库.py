import sqlite3
from datetime import datetime
from langchain_community.utilities import SQLDatabase
class ChatHistoryDB:
    def __init__(self, db_path='历史对话_Sqlite.db'):
        self.db_path = db_path
        
        # 初始化数据库连接并创建表
        self._initialize_db()

        # LangChain 的 SQLDatabase 对象
        self.sql_db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")

    def _initialize_db(self):
        """连接数据库并创建表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    user_question TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        # print("✅ 表 chat_records 已初始化完成")

    def save_record(self, user_id: str, user_question: str, ai_response: str):
        """保存一条对话记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO chat_records (user_id, user_question, ai_response)
                VALUES (?, ?, ?)
            ''', (user_id, user_question, ai_response))
            conn.commit()
        print(f"📌 用户 {user_id} 的对话已保存")

    def get_records_by_user(self, user_id: str):
        """根据 user_id 查询记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM chat_records WHERE user_id = ?', (user_id,))
            return cursor.fetchall()
