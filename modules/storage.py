"""
Module lưu trữ dữ liệu
- Lưu tài khoản vào accounts.json
- Ghi lỗi vào bot_errors.log
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class StorageManager:
    """Quản lý lưu trữ dữ liệu (accounts.json, bot_errors.log)"""
    
    def __init__(self, data_dir="data", logs_dir="logs"):
        """
        Khởi tạo StorageManager
        
        Args:
            data_dir (str): Thư mục lưu dữ liệu
            logs_dir (str): Thư mục lưu logs
        """
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, data_dir)
        self.logs_dir = os.path.join(self.base_dir, logs_dir)
        
        # Tạo thư mục nếu không tồn tại
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        Path(self.logs_dir).mkdir(parents=True, exist_ok=True)
        
        self.accounts_file = os.path.join(self.data_dir, "accounts.json")
        self.errors_log_file = os.path.join(self.logs_dir, "bot_errors.log")
        
        # Khởi tạo file accounts.json nếu chưa tồn tại
        self._init_accounts_file()
        
        logger.info(f"✅ StorageManager initialized")
    
    def _init_accounts_file(self):
        """Tạo file accounts.json nếu chưa tồn tại"""
        if not os.path.exists(self.accounts_file):
            with open(self.accounts_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            logger.info(f"✅ Created {self.accounts_file}")
    
    def save_account(self, account_data):
        """
        Lưu tài khoản vào accounts.json
        
        Args:
            account_data (dict): Dữ liệu tài khoản
                {
                    "tab_id": "tab_1",
                    "website": "Website KJC",
                    "username": "longbm78",
                    "password": "nguyen1992",
                    "phone": "0987654321",
                    "name": "John Doe",
                    "id_code": "12345",
                    "branch": "Hà Nội",
                    "id_number": "123456789",
                    "passcode": "753911",
                    "status": "verified",
                    "created_at": "2024-06-24 10:30:45",
                    "verified_at": "2024-06-24 10:45:20"
                }
        
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            # Đọc dữ liệu hiện tại
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                accounts = json.load(f)
            
            # Thêm tài khoản mới
            accounts.append(account_data)
            
            # Ghi lại
            with open(self.accounts_file, "w", encoding="utf-8") as f:
                json.dump(accounts, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Saved account: {account_data.get('username')}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error saving account: {str(e)}")
            self.log_error(f"save_account", str(e))
            return False
    
    def get_all_accounts(self):
        """
        Lấy tất cả tài khoản
        
        Returns:
            list: Danh sách tài khoản
        """
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                accounts = json.load(f)
            return accounts
        except Exception as e:
            logger.error(f"❌ Error reading accounts: {str(e)}")
            return []
    
    def get_accounts_by_website(self, website):
        """
        Lấy tài khoản theo website
        
        Args:
            website (str): Tên website
        
        Returns:
            list: Danh sách tài khoản của website
        """
        accounts = self.get_all_accounts()
        return [acc for acc in accounts if acc.get("website") == website]
    
    def log_error(self, function_name, error_message, tab_id=None, extra_info=None):
        """
        Ghi lỗi vào bot_errors.log
        
        Args:
            function_name (str): Tên function gặp lỗi
            error_message (str): Nội dung lỗi
            tab_id (str, optional): ID tab
            extra_info (dict, optional): Thông tin thêm
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            log_entry = f"[{timestamp}] ERROR - {function_name}"
            if tab_id:
                log_entry += f" (Tab: {tab_id})"
            log_entry += f" - {error_message}"
            if extra_info:
                log_entry += f" - {extra_info}"
            
            with open(self.errors_log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
            
            logger.error(log_entry)
        
        except Exception as e:
            logger.error(f"❌ Error logging error: {str(e)}")
    
    def log_action(self, action, tab_id=None, details=None):
        """
        Ghi hành động vào log
        
        Args:
            action (str): Hành động
            tab_id (str, optional): ID tab
            details (str, optional): Chi tiết hành động
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            log_entry = f"[{timestamp}] ACTION - {action}"
            if tab_id:
                log_entry += f" (Tab: {tab_id})"
            if details:
                log_entry += f" - {details}"
            
            with open(self.errors_log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
            
            logger.info(log_entry)
        
        except Exception as e:
            logger.error(f"❌ Error logging action: {str(e)}")


# Sử dụng:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    storage = StorageManager()
    
    # Lưu tài khoản
    account = {
        "tab_id": "tab_1",
        "website": "Website KJC",
        "username": "longbm78",
        "password": "nguyen1992",
        "phone": "0987654321",
        "name": "John Doe",
        "id_code": "12345",
        "branch": "Hà Nội",
        "id_number": "123456789",
        "status": "verified",
        "created_at": "2024-06-24 10:30:45"
    }
    
    storage.save_account(account)
    
    # Lấy tất cả tài khoản
    accounts = storage.get_all_accounts()
    print(f"Total accounts: {len(accounts)}")
    
    # Ghi lỗi
    storage.log_error("test_function", "Test error message", "tab_1")
