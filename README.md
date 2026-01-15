# 🎬 小红书电影趋势分析器

> 自动抓取小红书电影笔记，分析热门趋势，生成优质内容

[![自动更新](https://github.com/你的用户名/你的仓库名/actions/workflows/update-data.yml/badge.svg)](https://github.com/你的用户名/你的仓库名/actions/workflows/update-data.yml)
[![在线访问](https://img.shields.io/badge/在线访问-GitHub%20Pages-blue)](https://你的用户名.github.io/你的仓库名/)

## ✨ 功能特点

- 🔄 **自动数据抓取** - 每天自动从小红书获取最新电影笔记
- 📊 **趋势分析** - 智能分析热门主题和用户关注点
- ✍️ **内容生成** - 基于AI生成小红书风格的电影笔记
- 🌐 **在线访问** - 部署在GitHub Pages，随时随地查看
- 🤖 **全自动运行** - GitHub Actions定时任务，无需人工干预

## 🚀 在线访问

👉 **[点击这里访问在线版本](https://你的用户名.github.io/你的仓库名/)**

数据每天自动更新，展示最新的电影趋势和生成内容。

## 📸 截图预览

*（这里可以添加网站截图）*

## 🛠️ 技术栈

- **前端**: HTML5 + CSS3 + JavaScript
- **后端**: Python 3.9+
- **数据采集**: requests + BeautifulSoup4
- **AI生成**: OpenAI API
- **自动化**: GitHub Actions
- **部署**: GitHub Pages

## 📦 本地运行

### 前置要求

- Python 3.9+
- pip

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名
```

2. **安装依赖**
```bash
pip install requests beautifulsoup4 openai python-dotenv
```

3. **配置环境变量**

创建 `.env` 文件（可选，如果需要使用AI生成功能）：
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
```

4. **运行数据更新**
```bash
python auto_update.py
```

5. **启动本地服务器**
```bash
python3 -m http.server 8000
```

6. **访问网页**

打开浏览器访问: http://localhost:8000

## 🔄 自动更新机制

本项目使用GitHub Actions实现自动化：

- ⏰ **定时任务**: 每天UTC时间2点（北京时间上午10点）自动运行
- 🔍 **数据抓取**: 自动获取小红书最新电影笔记（前20条）
- 📈 **趋势分析**: 统计热词、主题分布、情感分析
- ✨ **内容生成**: 基于热门主题生成5篇新笔记
- 💾 **自动提交**: 更新后的数据自动提交到仓库
- 🌐 **自动部署**: GitHub Pages自动更新网站

### 查看运行日志

1. 进入GitHub仓库
2. 点击 "Actions" 标签
3. 查看最新的工作流运行记录

## ⚙️ 配置说明

### 必需配置（用于自动更新）

在GitHub仓库设置中添加以下Secrets：

| Secret名称 | 说明 | 是否必需 |
|-----------|------|---------|
| `OPENAI_API_KEY` | OpenAI API密钥 | ✅ 必需 |
| `OPENAI_API_BASE` | OpenAI API地址 | ⚠️ 可选（默认官方地址） |

**添加步骤**：
1. 进入仓库设置: `Settings` → `Secrets and variables` → `Actions`
2. 点击 `New repository secret`
3. 添加上述配置

### 可选配置

编辑 `.github/workflows/update-data.yml` 可以修改：
- 运行时间（cron表达式）
- Python版本
- 其他自定义参数

## 📁 项目结构

```
.
├── .github/
│   └── workflows/
│       └── update-data.yml          # GitHub Actions自动化配置
├── index.html                        # 主页面
├── auto_update.py                    # 主控脚本
├── fetch_xiaohongshu_notes.py       # 数据抓取
├── analyze_trends.py                # 趋势分析
├── generate_content.py              # 内容生成
├── xiaohongshu_notes_latest.json    # 抓取数据
├── trend_analysis_latest.json       # 分析结果
├── generated_notes_latest.json      # 生成内容
├── .gitignore                       # Git忽略配置
└── README.md                        # 项目文档
```

## 🎯 使用场景

- 📱 **小红书运营** - 了解电影领域热门话题
- ✍️ **内容创作** - 获取创作灵感和参考
- 📊 **市场分析** - 研究用户关注趋势
- 🤖 **AI应用** - 学习自动化内容生成

## 🔧 常见问题

<details>
<summary><b>Q: GitHub Actions运行失败怎么办？</b></summary>

1. 检查Secrets配置是否正确
2. 查看Actions日志查看具体错误
3. 确认API密钥有效且有足够额度
</details>

<details>
<summary><b>Q: 如何修改更新频率？</b></summary>

编辑 `.github/workflows/update-data.yml`，修改cron表达式：
```yaml
schedule:
  - cron: '0 */6 * * *'  # 改为每6小时运行一次
```
</details>

<details>
<summary><b>Q: 数据没有更新？</b></summary>

1. 检查Actions是否成功运行
2. 查看最新commit是否有数据更新
3. 清除浏览器缓存后重新访问
</details>

<details>
<summary><b>Q: 如何手动触发更新？</b></summary>

1. 进入仓库的 "Actions" 标签
2. 选择 "自动更新小红书数据" 工作流
3. 点击 "Run workflow" 按钮
</details>

## 📝 更新日志

### 2026-01-15
- ✨ 初始版本发布
- 🚀 支持GitHub Pages部署
- 🤖 集成GitHub Actions自动更新

## 📄 开源协议

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题或建议，欢迎通过以下方式联系：

- GitHub Issues: [提交Issue](https://github.com/你的用户名/你的仓库名/issues)
- Email: your-email@example.com

---

⭐ 如果这个项目对你有帮助，欢迎Star支持！
