# 自动化配置说明

## GitHub Actions 每日价格更新

本项目使用 GitHub Actions 实现比特币价格的每日自动更新功能。

### 配置文件

#### 1. 工作流文件 (`.github/workflows/update-btc-price.yml`)

```yaml
name: 每日更新比特币价格

on:
  schedule:
    # 每天北京时间 12:00 运行 (UTC 04:00)
    - cron: '0 4 * * *'
  workflow_dispatch: # 允许手动触发

jobs:
  update-price:
    runs-on: ubuntu-latest
    
    steps:
      - name: 检出代码
      - name: 设置 Python 环境
      - name: 安装依赖
      - name: 运行价格更新脚本
      - name: 配置 Git
      - name: 提交并推送更改
```

#### 2. 更新脚本 (`update_btc_price.py`)

脚本主要功能：
- 从 CoinGecko API 获取当前比特币价格
- 计算北京时间日期（UTC+8）
- 检查日期是否已存在，避免重复添加
- 将新价格插入到 CSV 文件的第二行（表头之后）
- 保持日期倒序排列

### 触发方式

#### 自动触发
- **时间**：每天北京时间 12:00（UTC 04:00）
- **频率**：每天一次
- **操作**：自动运行，无需人工干预

#### 手动触发
1. 访问 GitHub 仓库页面
2. 点击 "Actions" 标签
3. 选择 "每日更新比特币价格" 工作流
4. 点击 "Run workflow" 按钮
5. 选择分支（通常是 main 或 master）
6. 点击 "Run workflow" 确认

### 权限配置

工作流使用 `GITHUB_TOKEN` 进行身份验证，无需额外配置。该令牌由 GitHub 自动提供，具有以下权限：
- 读取仓库内容
- 提交代码更改
- 推送到仓库

### API 使用

#### CoinGecko API
- **端点**：`https://api.coingecko.com/api/v3/simple/price`
- **参数**：
  - `ids=bitcoin`
  - `vs_currencies=usd`
- **限制**：免费使用，无需 API Key
- **频率限制**：50 次/分钟（足够使用）

### 数据格式

#### CSV 文件结构
```csv
date,btc price
2025-11-20,90302
2025-11-19,92819
2025-11-18,92036
...
```

- **日期格式**：`YYYY-MM-DD`
- **价格格式**：整数（美元）
- **排序方式**：倒序（最新日期在前）

### 故障排查

#### 工作流失败
1. 检查 Actions 日志
2. 查看具体失败步骤
3. 常见问题：
   - API 请求失败：网络问题或 API 限制
   - Git 推送失败：权限问题
   - Python 依赖安装失败：版本不兼容

#### 价格未更新
1. 确认工作流是否成功运行
2. 检查日期是否已存在（不会重复添加）
3. 查看 API 响应是否正常

#### 手动恢复
如果自动化失败，可以手动运行更新脚本：

```bash
# 克隆仓库
git clone https://github.com/lovexw/dca.git
cd dca

# 安装依赖
pip install requests

# 运行更新脚本
python3 update_btc_price.py

# 提交更改
git add btc-price\ all.csv
git commit -m "手动更新比特币价格"
git push
```

### 监控和维护

#### 监控建议
- 定期检查 Actions 运行状态
- 设置 GitHub Actions 邮件通知
- 每周查看数据连续性

#### 维护建议
- 每月检查 API 是否正常
- 验证价格数据的准确性
- 备份 CSV 文件

### 扩展功能

#### 添加备用 API
可以在脚本中添加备用 API，当主 API 失败时自动切换：
- CoinDesk API
- Binance API
- Kraken API

#### 添加数据验证
- 价格合理性检查（与前一天对比）
- 数据完整性验证
- 异常值告警

#### 添加通知功能
- 更新成功时发送通知
- 失败时发送告警邮件
- 集成到 Slack/Discord

### 相关文档

- [GitHub Actions 官方文档](https://docs.github.com/actions)
- [CoinGecko API 文档](https://www.coingecko.com/en/api/documentation)
- [Python requests 文档](https://requests.readthedocs.io/)

### 更新历史

- **2025-11-20**：初始配置，实现每日自动更新功能
