#!/usr/bin/env python3
"""
小红书电影趋势自动更新脚本
按顺序执行三个模块：数据获取 → 趋势分析 → 内容生成
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


class AutoUpdater:
    """自动更新器"""
    
    def __init__(self, log_file: str = "auto_update.log"):
        """初始化更新器"""
        self.log_file = log_file
        self.project_dir = Path(__file__).parent
        
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def run_script(self, script_name: str) -> bool:
        """
        运行Python脚本
        
        Args:
            script_name: 脚本文件名
            
        Returns:
            是否执行成功
        """
        script_path = self.project_dir / script_name
        
        if not script_path.exists():
            self.log(f"❌ 错误：脚本 {script_name} 不存在")
            return False
        
        self.log(f"🚀 开始执行: {script_name}")
        
        try:
            # 执行脚本
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(self.project_dir),
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            # 打印输出
            if result.stdout:
                print(result.stdout)
            
            # 检查是否成功
            if result.returncode == 0:
                self.log(f"✅ 成功完成: {script_name}")
                return True
            else:
                self.log(f"❌ 执行失败: {script_name}")
                if result.stderr:
                    self.log(f"错误信息: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log(f"⏰ 超时: {script_name} 执行超过5分钟")
            return False
        except Exception as e:
            self.log(f"❌ 异常: {script_name} - {str(e)}")
            return False
    
    def run_full_update(self) -> bool:
        """
        执行完整的更新流程
        
        Returns:
            是否全部成功
        """
        self.log("="*60)
        self.log("🎬 开始小红书电影趋势自动更新")
        self.log("="*60)
        
        # 定义执行顺序
        scripts = [
            ("fetch_xiaohongshu_notes.py", "数据获取"),
            ("analyze_trends.py", "趋势分析"),
            ("generate_content.py", "内容生成")
        ]
        
        # 依次执行
        for script_name, description in scripts:
            self.log(f"\n📍 步骤: {description}")
            
            success = self.run_script(script_name)
            
            if not success:
                self.log(f"\n❌ 更新流程中断于: {description}")
                self.log("="*60)
                return False
            
            self.log(f"✓ {description} 完成")
        
        # 全部成功
        self.log("\n" + "="*60)
        self.log("🎉 自动更新流程全部完成！")
        self.log("="*60)
        self.log("✓ 数据已更新")
        self.log("✓ 趋势已分析")
        self.log("✓ 内容已生成")
        self.log(f"✓ 日志文件: {self.log_file}")
        self.log("="*60)
        
        return True


def main():
    """主函数"""
    updater = AutoUpdater()
    success = updater.run_full_update()
    
    # 返回退出码（0表示成功，1表示失败）
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
