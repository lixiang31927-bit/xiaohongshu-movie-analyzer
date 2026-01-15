#!/usr/bin/env python3
"""
小红书笔记内容生成脚本
基于热门主题生成符合小红书风格的电影笔记内容
"""

import json
import glob
import os
import random
from datetime import datetime
from typing import List, Dict


class ContentGenerator:
    """内容生成器"""
    
    # 表情符号库
    EMOJIS = {
        'movie': ['🎬', '📽️', '🎞️', '🎥'],
        'star': ['⭐️', '✨', '🌟', '💫'],
        'heart': ['❤️', '💕', '💖', '💗', '😍'],
        'fire': ['🔥', '💥', '👍', '💯'],
        'think': ['💭', '💡', '🤔', '📝'],
        'cry': ['😭', '😢', '🥺', '💔'],
        'happy': ['😊', '🥰', '😌', '🤗'],
        'exclaim': ['❗️', '‼️', '❓', '⁉️']
    }
    
    # 电影库（按主题分类）
    MOVIES_BY_TOPIC = {
        "恐怖电影推荐": [
            "《寂静之地》", "《遗传厄运》", "《小丑回魂》", "《招魂》",
            "《闪灵》", "《咒怨》", "《午夜凶铃》", "《惊声尖叫》"
        ],
        "奥斯卡获奖电影": [
            "《寄生虫》", "《月光男孩》", "《水形物语》", "《鸟人》",
            "《国王的演讲》", "《艺术家》", "《12年为奴》", "《聚焦》"
        ],
        "爱情电影推荐": [
            "《怦然心动》", "《爱在三部曲》", "《泰坦尼克号》", "《恋恋笔记本》",
            "《时空恋旅人》", "《初恋50次》", "《真爱至上》", "《遇见你之前》"
        ],
        "最新上映电影": [
            "《奥本海默》", "《芭比》", "《沙丘2》", "《银河护卫队3》",
            "《碟中谍7》", "《蜘蛛侠：纵横宇宙》", "《疾速追杀4》", "《变形金刚：超能勇士崛起》"
        ],
        "小众文艺片": [
            "《海街日记》", "《小森林》", "《百元之恋》", "《被嫌弃的松子的一生》",
            "《四月物语》", "《花束般的恋爱》", "《蓝色大门》", "《不能说的秘密》"
        ]
    }
    
    def __init__(self, analysis_file: str = None):
        """
        初始化内容生成器
        
        Args:
            analysis_file: 趋势分析结果文件，如果为None则自动查找最新文件
        """
        if analysis_file is None:
            analysis_file = self._find_latest_analysis_file()
        
        self.analysis_file = analysis_file
        self.analysis_data = self._load_analysis()
        print(f"📂 加载分析文件: {analysis_file}")
        print(f"🎯 识别到 {len(self.analysis_data['top_topics'])} 个热门主题\n")
    
    def _find_latest_analysis_file(self) -> str:
        """查找最新的分析文件"""
        # 优先使用latest版本
        latest_file = "trend_analysis_latest.json"
        if os.path.exists(latest_file):
            return latest_file
        
        # 如果latest不存在，查找带时间戳的文件
        files = glob.glob("trend_analysis_*.json")
        if not files:
            raise FileNotFoundError("未找到趋势分析文件，请先运行分析脚本")
        
        files.sort(reverse=True)
        return files[0]
    
    def _load_analysis(self) -> Dict:
        """加载分析文件"""
        with open(self.analysis_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_all_notes(self, notes_per_topic: int = 1) -> Dict:
        """
        为所有热门主题生成笔记
        
        Args:
            notes_per_topic: 每个主题生成几篇笔记
        
        Returns:
            生成结果字典
        """
        print(f"✍️ 开始生成内容（每个主题 {notes_per_topic} 篇）...\n")
        
        result = {
            "generation_time": datetime.now().isoformat(),
            "based_on_analysis": self.analysis_file,
            "notes_per_topic": notes_per_topic,
            "generated_notes": []
        }
        
        for topic_info in self.analysis_data['top_topics']:
            topic = topic_info['topic']
            rank = topic_info['rank']
            
            print(f"📝 正在为主题 #{rank} 「{topic}」生成内容...")
            
            for i in range(notes_per_topic):
                note = self._generate_note_for_topic(topic, topic_info)
                result['generated_notes'].append(note)
                print(f"   ✓ 生成第 {i+1} 篇")
            
            print()
        
        print(f"✅ 共生成 {len(result['generated_notes'])} 篇笔记内容")
        return result
    
    def _generate_note_for_topic(self, topic: str, topic_info: Dict) -> Dict:
        """为单个主题生成笔记"""
        # 选择电影
        movie = self._select_movie(topic)
        
        # 生成标题
        title = self._generate_title(topic, movie)
        
        # 生成正文
        content = self._generate_content(topic, movie, topic_info)
        
        # 生成标签
        tags = self._generate_tags(topic)
        
        # 生成话题
        hashtags = self._generate_hashtags(topic, movie)
        
        return {
            "topic": topic,
            "topic_rank": topic_info['rank'],
            "topic_heat_score": topic_info['heat_score'],
            "movie": movie,
            "title": title,
            "content": content,
            "tags": tags,
            "hashtags": hashtags,
            "estimated_reading_time": "2-3分钟",
            "target_audience": self._get_target_audience(topic),
            "best_posting_time": self._get_best_posting_time(topic)
        }
    
    def _select_movie(self, topic: str) -> str:
        """根据主题选择电影"""
        movies = self.MOVIES_BY_TOPIC.get(topic, [
            "《肖申克的救赎》", "《盗梦空间》", "《星际穿越》"
        ])
        return random.choice(movies)
    
    def _generate_title(self, topic: str, movie: str) -> str:
        """生成标题"""
        emoji1 = random.choice(self.EMOJIS['movie'])
        emoji2 = random.choice(self.EMOJIS['star'])
        
        templates = [
            f"{emoji1}必看！{movie} 真的太绝了｜{topic.replace('推荐', '')}",
            f"{emoji2}{movie}｜不看后悔系列{emoji1}",
            f"{emoji1}强推！{movie} 让我久久不能平静",
            f"{emoji2}宝藏电影！{movie} 值得刷三遍{emoji1}",
            f"{emoji1}{movie}｜{topic.replace('推荐', '')}天花板{emoji2}",
            f"{emoji2}含泪推荐！{movie} 每一帧都是艺术{emoji1}",
        ]
        
        # 根据主题选择合适的模板
        if "恐怖" in topic:
            return f"{emoji1}胆小勿入！{movie} 吓到我睡不着{random.choice(self.EMOJIS['exclaim'])}"
        elif "爱情" in topic:
            heart = random.choice(self.EMOJIS['heart'])
            return f"{heart}{movie}｜爱情片天花板！看哭了{random.choice(self.EMOJIS['cry'])}"
        elif "奥斯卡" in topic:
            return f"{emoji2}奥斯卡获奖！{movie} 实至名归的神作{emoji1}"
        else:
            return random.choice(templates)
    
    def _generate_content(self, topic: str, movie: str, topic_info: Dict) -> str:
        """生成正文内容"""
        # 开场
        opening = self._generate_opening(topic, movie)
        
        # 电影信息
        info_section = self._generate_info_section(movie)
        
        # 亮点分析
        highlights = self._generate_highlights(topic, movie)
        
        # 个人感受
        feelings = self._generate_feelings(topic, movie)
        
        # 互动引导
        cta = self._generate_cta(topic)
        
        # 组合内容
        content = f"{opening}\n\n"
        content += f"{info_section}\n\n"
        content += f"{highlights}\n\n"
        content += f"{feelings}\n\n"
        content += f"{cta}"
        
        return content
    
    def _generate_opening(self, topic: str, movie: str) -> str:
        """生成开场"""
        openings = [
            f"姐妹们！今天必须给大家安利 {movie}！",
            f"终于看了传说中的 {movie}，现在就来分享！",
            f"朋友们！{movie} 真的太好看了，不吐不快！",
            f"刷了三遍 {movie}，每次都有新的感动！",
            f"强烈推荐！{movie} 是我今年看过最好的电影！",
        ]
        
        if "恐怖" in topic:
            return f"胆小勿入！昨晚看完 {movie}，一个人不敢睡觉了😱"
        elif "爱情" in topic:
            cry = random.choice(self.EMOJIS['cry'])
            return f"姐妹们！{movie} 让我哭到停不下来{cry} 真的太虐了！"
        else:
            return random.choice(openings)
    
    def _generate_info_section(self, movie: str) -> str:
        """生成电影信息部分"""
        movie_emoji = random.choice(self.EMOJIS['movie'])
        star = random.choice(self.EMOJIS['star'])
        
        return f"{movie_emoji} 电影：{movie}\n{star} 类型：根据主题推荐\n⏱️ 时长：适中，不拖沓"
    
    def _generate_highlights(self, topic: str, movie: str) -> str:
        """生成亮点部分"""
        star = random.choice(self.EMOJIS['star'])
        fire = random.choice(self.EMOJIS['fire'])
        
        highlights_pool = [
            f"{star} 剧情：完全不拖沓，每一分钟都是精华",
            f"{star} 演技：演员们的表演真的太绝了！",
            f"{star} 配乐：BGM 简直是神来之笔，听得起鸡皮疙瘩",
            f"{star} 画面：每一帧都可以截图当壁纸",
            f"{star} 台词：金句频出，建议记笔记",
            f"{star} 节奏：张弛有度，完全抓住观众的心",
        ]
        
        # 根据主题添加特定亮点
        if "恐怖" in topic:
            highlights_pool.extend([
                f"{star} 氛围：营造得太到位了，全程紧张",
                f"{star} 惊吓点：设计得很巧妙，不是那种低级吓人",
            ])
        elif "爱情" in topic:
            highlights_pool.extend([
                f"{star} 感情线：细腻真实，让人共鸣满满",
                f"{star} 甜度：甜而不腻，恰到好处",
            ])
        
        selected = random.sample(highlights_pool, k=3)
        return "\n".join(selected) + f"\n{fire} 总之就是神作！"
    
    def _generate_feelings(self, topic: str, movie: str) -> str:
        """生成个人感受部分"""
        think = random.choice(self.EMOJIS['think'])
        heart = random.choice(self.EMOJIS['heart'])
        
        feelings = [
            f"{think} 看完后久久不能平静，脑子里全是电影画面",
            f"{heart} 这部片子会一直珍藏在我的心里",
            f"{think} 每个细节都值得回味，建议二刷三刷",
            f"{heart} 真的强烈推荐给所有人！",
        ]
        
        if "恐怖" in topic:
            return f"{think} 看完整个人都不好了，但又觉得很爽！这种又怕又想看的感觉，懂的都懂~"
        elif "爱情" in topic:
            cry = random.choice(self.EMOJIS['cry'])
            return f"{cry} 看完整个人都被治愈了，相信爱情的力量！单身狗表示受到了一万点暴击哈哈~"
        else:
            return random.choice(feelings)
    
    def _generate_cta(self, topic: str) -> str:
        """生成互动引导"""
        ctas = [
            "💬 你们看过这部电影吗？来评论区聊聊！",
            "👍 觉得有用的话给个赞吧，你的点赞是我持续分享的动力~",
            "⭐️ 收藏起来，周末就去看！",
            "📝 评论区说说你最喜欢的电影吧！",
            "🔥 记得关注我，持续分享好片推荐！",
        ]
        return random.choice(ctas)
    
    def _generate_tags(self, topic: str) -> List[str]:
        """生成标签"""
        base_tags = ["电影推荐", "影评", "观影笔记"]
        
        topic_tags = {
            "恐怖电影推荐": ["恐怖片", "惊悚片", "悬疑"],
            "奥斯卡获奖电影": ["奥斯卡", "获奖电影", "经典电影"],
            "爱情电影推荐": ["爱情片", "浪漫电影", "情侣观影"],
            "最新上映电影": ["新片推荐", "院线电影", "最新电影"],
            "小众文艺片": ["文艺片", "小众电影", "独立电影"],
        }
        
        specific_tags = topic_tags.get(topic, ["好片推荐"])
        
        additional_tags = ["高分电影", "必看电影", "周末观影", "电影分享"]
        
        all_tags = base_tags + specific_tags + random.sample(additional_tags, k=2)
        return all_tags[:8]  # 限制在8个以内
    
    def _generate_hashtags(self, topic: str, movie: str) -> List[str]:
        """生成话题标签"""
        hashtags = [
            f"#{topic}",
            f"#{movie}",
            "#电影推荐",
            "#影单分享"
        ]
        return hashtags
    
    def _get_target_audience(self, topic: str) -> str:
        """获取目标受众"""
        audiences = {
            "恐怖电影推荐": "喜欢惊悚刺激的年轻观众",
            "奥斯卡获奖电影": "追求高质量电影的影迷",
            "爱情电影推荐": "喜欢浪漫爱情故事的观众",
            "最新上映电影": "关注院线新片的观众",
            "小众文艺片": "文艺青年、独立电影爱好者",
        }
        return audiences.get(topic, "电影爱好者")
    
    def _get_best_posting_time(self, topic: str) -> str:
        """获取最佳发布时间"""
        return "晚上 8-10 点（用户活跃高峰期）"
    
    def save_notes(self, result: Dict, filename: str = None) -> str:
        """保存生成的笔记（同时保存带时间戳和latest版本）"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"generated_notes_{timestamp}.json"
        
        # 保存带时间戳的版本（历史记录）
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n💾 笔记内容已保存到: {filename}")
        
        # 保存latest版本（供网页读取）
        latest_filename = "generated_notes_latest.json"
        with open(latest_filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 最新笔记已更新: {latest_filename}")
        
        return filename
    
    def display_notes(self, result: Dict):
        """展示生成的笔记"""
        print("\n" + "="*70)
        print("📝 生成的小红书笔记内容预览")
        print("="*70)
        
        for i, note in enumerate(result['generated_notes'], 1):
            print(f"\n【笔记 {i}】")
            print(f"主题：{note['topic']} (排名#{note['topic_rank']})")
            print(f"电影：{note['movie']}")
            print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"标题：{note['title']}")
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"\n{note['content']}")
            print(f"\n🏷️  标签：{' '.join(['#' + tag for tag in note['tags']])}")
            print(f"\n📊 目标受众：{note['target_audience']}")
            print(f"⏰ 建议发布时间：{note['best_posting_time']}")
            print("\n" + "="*70)


def main():
    """主函数"""
    # 创建生成器
    generator = ContentGenerator()
    
    # 生成笔记（每个热门主题生成1篇）
    result = generator.generate_all_notes(notes_per_topic=1)
    
    # 保存结果
    filename = generator.save_notes(result)
    
    # 展示预览
    generator.display_notes(result)
    
    print("\n✅ 第三步完成！所有笔记内容已生成。")
    print("\n" + "="*70)
    print("🎉 完整流程已完成！")
    print("="*70)
    print("✓ 步骤1: 已获取 100 条小红书笔记数据")
    print("✓ 步骤2: 已识别 Top 5 热门主题")
    print("✓ 步骤3: 已生成 5 篇小红书风格笔记")
    print("\n💡 提示：生成的内容仅供参考，建议根据实际情况调整后发布。")
    print("="*70)


if __name__ == "__main__":
    main()
