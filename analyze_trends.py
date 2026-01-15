#!/usr/bin/env python3
"""
小红书笔记趋势分析脚本
统计各主题的热度并识别最热门的主题
"""

import json
import glob
import os
from datetime import datetime
from typing import List, Dict, Tuple
from collections import defaultdict


class TrendAnalyzer:
    """趋势分析器"""
    
    # 互动权重配置
    ENGAGEMENT_WEIGHTS = {
        'likes': 1.0,      # 点赞：基础互动
        'comments': 2.0,   # 评论：深度参与
        'collects': 1.5,   # 收藏：价值认可
        'shares': 3.0      # 分享：传播价值最高
    }
    
    def __init__(self, data_file: str = None):
        """
        初始化分析器
        
        Args:
            data_file: 数据文件路径，如果为None则自动查找最新文件
        """
        if data_file is None:
            data_file = self._find_latest_data_file()
        
        self.data_file = data_file
        self.data = self._load_data()
        print(f"📂 加载数据文件: {data_file}")
        print(f"📊 共加载 {len(self.data['notes'])} 条笔记数据\n")
    
    def _find_latest_data_file(self) -> str:
        """查找最新的数据文件"""
        # 优先使用latest版本
        latest_file = "xiaohongshu_notes_latest.json"
        if os.path.exists(latest_file):
            return latest_file
        
        # 如果latest不存在，查找带时间戳的文件
        files = glob.glob("xiaohongshu_notes_*.json")
        if not files:
            raise FileNotFoundError("未找到笔记数据文件，请先运行数据获取脚本")
        
        # 按文件名排序，返回最新的
        files.sort(reverse=True)
        return files[0]
    
    def _load_data(self) -> Dict:
        """加载数据文件"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_trends(self, top_n: int = 5) -> Dict:
        """
        分析趋势并提取热门主题
        
        Args:
            top_n: 提取前N个热门主题
        
        Returns:
            分析结果字典
        """
        print("🔍 开始分析趋势...")
        
        # 按主题分组统计
        topic_stats = self._calculate_topic_stats()
        
        # 计算热度评分
        topic_scores = self._calculate_heat_scores(topic_stats)
        
        # 排序并提取Top N
        sorted_topics = sorted(
            topic_scores.items(),
            key=lambda x: x[1]['heat_score'],
            reverse=True
        )[:top_n]
        
        # 构建分析结果
        result = {
            "analysis_time": datetime.now().isoformat(),
            "data_source": self.data_file,
            "total_notes": len(self.data['notes']),
            "total_topics": len(topic_stats),
            "top_n": top_n,
            "top_topics": []
        }
        
        print(f"\n🌟 识别出 Top {top_n} 热门主题：\n")
        
        for rank, (topic, stats) in enumerate(sorted_topics, 1):
            topic_result = {
                "rank": rank,
                "topic": topic,
                "note_count": stats['note_count'],
                "total_engagement": stats['total_engagement'],
                "heat_score": round(stats['heat_score'], 2),
                "avg_engagement_per_note": round(stats['avg_engagement'], 2),
                "sample_notes": stats['sample_notes'][:3]  # 取3个样本笔记ID
            }
            result['top_topics'].append(topic_result)
            
            # 打印结果
            print(f"  {rank}. {topic}")
            print(f"     📝 笔记数: {stats['note_count']}")
            print(f"     🔥 热度评分: {stats['heat_score']:.2f}")
            print(f"     💬 总互动量: {stats['weighted_engagement']:.0f}")
            print(f"     📈 平均互动: {stats['avg_engagement']:.2f}/篇")
            print()
        
        return result
    
    def _calculate_topic_stats(self) -> Dict[str, Dict]:
        """计算每个主题的统计数据"""
        topic_data = defaultdict(lambda: {
            'notes': [],
            'total_likes': 0,
            'total_comments': 0,
            'total_collects': 0,
            'total_shares': 0,
        })
        
        for note in self.data['notes']:
            topic = note['topic']
            stats = note['stats']
            
            topic_data[topic]['notes'].append(note)
            topic_data[topic]['total_likes'] += stats['likes']
            topic_data[topic]['total_comments'] += stats['comments']
            topic_data[topic]['total_collects'] += stats['collects']
            topic_data[topic]['total_shares'] += stats['shares']
        
        return topic_data
    
    def _calculate_heat_scores(self, topic_stats: Dict) -> Dict[str, Dict]:
        """
        计算热度评分
        
        公式：热度分数 = 主题笔记数 × 10 + 加权互动量 / 100
        """
        results = {}
        
        for topic, data in topic_stats.items():
            note_count = len(data['notes'])
            
            # 计算加权互动量
            weighted_engagement = (
                data['total_likes'] * self.ENGAGEMENT_WEIGHTS['likes'] +
                data['total_comments'] * self.ENGAGEMENT_WEIGHTS['comments'] +
                data['total_collects'] * self.ENGAGEMENT_WEIGHTS['collects'] +
                data['total_shares'] * self.ENGAGEMENT_WEIGHTS['shares']
            )
            
            # 计算热度评分
            heat_score = note_count * 10 + weighted_engagement / 100
            
            # 计算平均互动量
            total_engagement = (
                data['total_likes'] +
                data['total_comments'] +
                data['total_collects'] +
                data['total_shares']
            )
            avg_engagement = total_engagement / note_count if note_count > 0 else 0
            
            results[topic] = {
                'note_count': note_count,
                'total_engagement': {
                    'likes': data['total_likes'],
                    'comments': data['total_comments'],
                    'collects': data['total_collects'],
                    'shares': data['total_shares']
                },
                'weighted_engagement': weighted_engagement,
                'heat_score': heat_score,
                'avg_engagement': avg_engagement,
                'sample_notes': [note['note_id'] for note in data['notes']]
            }
        
        return results
    
    def save_analysis(self, result: Dict, filename: str = None) -> str:
        """保存分析结果（同时保存带时间戳和latest版本）"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"trend_analysis_{timestamp}.json"
        
        # 保存带时间戳的版本（历史记录）
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 分析结果已保存到: {filename}")
        
        # 保存latest版本（供网页读取）
        latest_filename = "trend_analysis_latest.json"
        with open(latest_filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 最新分析已更新: {latest_filename}")
        
        return filename
    
    def generate_report(self, result: Dict):
        """生成可读的分析报告"""
        print("\n" + "="*60)
        print("📊 趋势分析报告")
        print("="*60)
        print(f"分析时间: {result['analysis_time']}")
        print(f"数据来源: {result['data_source']}")
        print(f"总笔记数: {result['total_notes']}")
        print(f"主题总数: {result['total_topics']}")
        print(f"\n🏆 Top {result['top_n']} 热门主题详情:\n")
        
        for topic in result['top_topics']:
            print(f"排名 #{topic['rank']}: {topic['topic']}")
            print(f"  • 笔记数量: {topic['note_count']} 篇")
            print(f"  • 热度评分: {topic['heat_score']}")
            print(f"  • 平均互动: {topic['avg_engagement_per_note']:.2f} 次/篇")
            print()
        
        print("="*60)
        print("💡 内容创作建议:")
        print("="*60)
        print("基于以上热门主题，建议重点创作以下方向的内容：")
        for i, topic in enumerate(result['top_topics'][:3], 1):
            print(f"{i}. {topic['topic']} - 热度评分 {topic['heat_score']}")
        print()


def main():
    """主函数"""
    # 创建分析器
    analyzer = TrendAnalyzer()
    
    # 执行分析
    result = analyzer.analyze_trends(top_n=5)
    
    # 保存结果
    filename = analyzer.save_analysis(result)
    
    # 生成报告
    analyzer.generate_report(result)
    
    print("✅ 第二步完成！已识别热门主题，准备生成内容。\n")
    
    return filename


if __name__ == "__main__":
    main()
