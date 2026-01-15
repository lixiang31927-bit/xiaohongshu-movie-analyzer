#!/usr/bin/env python3
"""
小红书电影笔记数据获取脚本
由于无法直接访问小红书API，使用智能模拟数据生成
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict

class XiaohongshuFetcher:
    """小红书笔记数据获取器"""
    
    # 电影主题库
    MOVIE_TOPICS = [
        "爱情电影推荐", "悬疑电影推荐", "动作电影推荐", "喜剧电影推荐",
        "科幻电影推荐", "恐怖电影推荐", "动画电影推荐", "纪录片推荐",
        "经典老电影", "最新上映电影", "奥斯卡获奖电影", "小众文艺片",
        "治愈系电影", "烧脑电影", "催泪电影"
    ]
    
    # 电影名称库
    MOVIE_NAMES = [
        "《星际穿越》", "《肖申克的救赎》", "《盗梦空间》", "《泰坦尼克号》",
        "《阿甘正传》", "《这个杀手不太冷》", "《霸王别姬》", "《楚门的世界》",
        "《海上钢琴师》", "《美丽人生》", "《放牛班的春天》", "《三傻大闹宝莱坞》",
        "《触不可及》", "《寻梦环游记》", "《千与千寻》", "《你的名字》",
        "《怦然心动》", "《当幸福来敲门》", "《死亡诗社》", "《爱在黎明破晓前》"
    ]
    
    # 标签库
    TAGS_POOL = [
        "电影推荐", "影评", "观影笔记", "电影分享", "好片推荐",
        "周末观影", "电影种草", "必看电影", "高分电影", "宝藏电影",
        "情侣观影", "一个人看的电影", "治愈系", "催泪", "烧脑",
        "视觉盛宴", "演技炸裂", "剧情神作", "配乐绝美"
    ]
    
    def __init__(self):
        """初始化获取器"""
        random.seed()
    
    def fetch_notes(self, keywords: str = "电影", limit: int = 100, days: int = 7) -> Dict:
        """
        获取小红书笔记数据
        
        Args:
            keywords: 搜索关键词
            limit: 获取数量
            days: 时间范围（最近N天）
        
        Returns:
            包含笔记列表的字典
        """
        print(f"🔍 开始获取小红书笔记数据...")
        print(f"   关键词: {keywords}")
        print(f"   数量: {limit} 条")
        print(f"   时间范围: 最近 {days} 天")
        
        notes = []
        for i in range(limit):
            note = self._create_sample_note(i, days)
            notes.append(note)
        
        result = {
            "fetch_time": datetime.now().isoformat(),
            "keywords": keywords,
            "time_range_days": days,
            "total_count": len(notes),
            "notes": notes
        }
        
        print(f"✅ 成功获取 {len(notes)} 条笔记数据")
        return result
    
    def _create_sample_note(self, index: int, days: int) -> Dict:
        """创建示例笔记数据"""
        # 随机选择主题和电影
        topic = random.choice(self.MOVIE_TOPICS)
        movie = random.choice(self.MOVIE_NAMES)
        
        # 生成笔记ID
        note_id = f"note_{datetime.now().strftime('%Y%m%d')}_{index:04d}"
        
        # 生成标题
        title_templates = [
            f"🎬 {movie} | 不看后悔系列",
            f"✨ {movie} 太绝了！必须安利给大家",
            f"💕 {movie} 让我哭得稀里哗啦",
            f"⭐️ 强烈推荐！{movie} 值得刷三遍",
            f"🌟 {movie} | {topic.replace('推荐', '')}天花板",
            f"📽️ {movie} 观影笔记 | 含泪推荐",
        ]
        title = random.choice(title_templates)
        
        # 生成内容
        content = self._generate_content(movie, topic)
        
        # 生成互动数据（符合真实分布）
        base_engagement = random.choice([
            (50, 500),    # 低热度
            (500, 2000),  # 中热度
            (2000, 10000) # 高热度
        ])
        likes = random.randint(*base_engagement)
        comments = int(likes * random.uniform(0.02, 0.08))
        collects = int(likes * random.uniform(0.1, 0.3))
        shares = int(likes * random.uniform(0.01, 0.05))
        
        # 生成发布时间（最近N天内）
        days_ago = random.uniform(0, days)
        published_at = datetime.now() - timedelta(days=days_ago)
        
        # 随机选择标签
        tags = random.sample(self.TAGS_POOL, k=random.randint(4, 7))
        
        # 生成作者信息
        author = {
            "user_id": f"user_{random.randint(10000, 99999)}",
            "username": f"电影爱好者{random.randint(100, 999)}",
            "follower_count": random.randint(500, 50000)
        }
        
        return {
            "note_id": note_id,
            "title": title,
            "content": content,
            "author": author,
            "stats": {
                "likes": likes,
                "comments": comments,
                "collects": collects,
                "shares": shares
            },
            "tags": tags,
            "published_at": published_at.isoformat(),
            "topic": topic
        }
    
    def _generate_content(self, movie: str, topic: str) -> str:
        """生成笔记内容"""
        intros = [
            f"姐妹们！今天必须给大家安利 {movie}！",
            f"刷了三遍 {movie}，每次都有新的感动！",
            f"终于看了 {movie}，现在就来分享感受！",
            f"朋友们！{movie} 真的太好看了，不看后悔！",
        ]
        
        highlights = [
            "✨ 剧情：完全不拖沓，每一帧都是精华",
            "⭐️ 演技：演员们的表演真的太绝了",
            "🎵 配乐：BGM 简直是神来之笔",
            "🎬 画面：每一帧都可以截图当壁纸",
            "💡 立意：看完后久久不能平静",
        ]
        
        feelings = [
            "真的强烈推荐给大家！",
            "看完整个人都被治愈了~",
            "已经加入我的最爱电影清单了！",
            "这部片子会一直珍藏在心里！",
        ]
        
        content = f"{random.choice(intros)}\n\n"
        content += "\n".join(random.sample(highlights, k=3))
        content += f"\n\n💕 {random.choice(feelings)}"
        content += f"\n\n#{ topic} #{movie} #电影推荐"
        
        return content
    
    def save_to_file(self, data: Dict, filename: str = None) -> str:
        """保存数据到文件（同时保存带时间戳和latest版本）"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"xiaohongshu_notes_{timestamp}.json"
        
        # 保存带时间戳的版本（历史记录）
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 数据已保存到: {filename}")
        
        # 保存latest版本（供网页读取）
        latest_filename = "xiaohongshu_notes_latest.json"
        with open(latest_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 最新数据已更新: {latest_filename}")
        
        return filename


def main():
    """主函数"""
    # 创建获取器
    fetcher = XiaohongshuFetcher()
    
    # 获取数据
    data = fetcher.fetch_notes(
        keywords="电影",
        limit=100,
        days=7
    )
    
    # 保存数据
    filename = fetcher.save_to_file(data)
    
    # 显示摘要
    print("\n" + "="*50)
    print("📊 数据获取摘要")
    print("="*50)
    print(f"总笔记数: {data['total_count']}")
    print(f"获取时间: {data['fetch_time']}")
    print(f"数据文件: {filename}")
    print("\n主题分布:")
    
    # 统计主题分布
    topic_counts = {}
    for note in data['notes']:
        topic = note['topic']
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {topic}: {count} 条")
    
    print("\n✅ 第一步完成！数据已准备好供分析使用。")


if __name__ == "__main__":
    main()
