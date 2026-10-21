import os

base = r"D:\ai\antigravity\global_blog\i18n"

zh_hans_dir = os.path.join(base, "zh-Hans", "docusaurus-plugin-content-pages")
zh_hant_dir = os.path.join(base, "zh-Hant", "docusaurus-plugin-content-pages")

os.makedirs(zh_hans_dir, exist_ok=True)
os.makedirs(zh_hant_dir, exist_ok=True)

# zh-Hans contact.md
contact_hans = """---
title: 联系我们
description: Global Dev Blog 作者与维护者 Jihwan Park (朴智焕) 的联络方式。
keywords: [联系我们, Jihwan Park, 邮箱, GitHub, 技术合作]
---

# 联系我们

感谢您访问 **Global Dev Blog**。无论您是对文中的技术实现有疑问、有合作意向，还是对文章有任何反馈建议，我都非常期待收到您的来信。

---

## 📬 直接联络

- **邮箱**: [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com)  
  *欢迎随时就研究讨论、工程技术咨询或错误排查进行交流。*

---

## 💻 开源与代码仓库

- **GitHub 主页**: [@jbjihwan](https://github.com/jbjihwan)
- **博客源码仓库**: [github.com/jbjihwan/global_blog](https://github.com/jbjihwan/global_blog)
- **问题反馈**: 如果您在文章中发现任何拼写错误、代码 Bug 或失效链接，欢迎在 GitHub 提交 Issue：  
  👉 [在 GitHub 上提交 Issue](https://github.com/jbjihwan/global_blog/issues)

---

## ⏱️ 回复时间

我通常会在 **24 至 48 小时内** 查阅并回复技术来信。涉及关键安全或隐私问题，请在邮件主题中标注 `[Security]` 或 `[Privacy]`。
"""

# zh-Hant contact.md
contact_hant = """---
title: 聯絡我們
description: Global Dev Blog 作者與維護者 Jihwan Park (朴智煥) 的聯絡方式。
keywords: [聯絡我們, Jihwan Park, 電子郵件, GitHub, 技術合作]
---

# 聯絡我們

感謝您造訪 **Global Dev Blog**。無論您是對文中的技術實作有疑問、有合作意向，還是對文章有任何回饋建議，我都非常期待收到您的來信。

---

## 📬 直接聯絡

- **電子郵件**: [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com)  
  *歡迎隨時就研究討論、工程技術諮詢或問題回報進行交流。*

---

## 💻 開源與代碼儲存庫

- **GitHub 主頁**: [@jbjihwan](https://github.com/jbjihwan)
- **部落格原始碼儲存庫**: [github.com/jbjihwan/global_blog](https://github.com/jbjihwan/global_blog)
- **問題回報**: 如果您在文章中發現任何錯字、代碼 Bug 或失效連結，歡迎在 GitHub 提交 Issue：  
  👉 [在 GitHub 上提交 Issue](https://github.com/jbjihwan/global_blog/issues)

---

## ⏱️ 回覆時間

我通常會在 **24 至 48 小時內** 查閱並回覆技術來信。涉及關鍵安全或隱私問題，請在信件主旨中標註 `[Security]` 或 `[Privacy]`。
"""

# zh-Hans about.md
about_hans = """---
title: 关于我与博客
description: 关于作者 Jihwan Park (朴智焕) 与 Global Dev Blog - 人工智能、机器人、计算机视觉与强化学习深度工程实践。
keywords: [关于我, Jihwan Park, AI 工程师, 机器人, 计算机视觉, 强化学习, 心理守护者]
---

# 关于我与博客

欢迎来到 **Global Dev Blog**，这是由 **Jihwan Park (jbjihwan)** 维护的技术实验笔记与工程专栏。

本博客旨在忠实记录在 **人工智能 (AI)、机器人控制 (Robotics)、计算机视觉 (Computer Vision) 与强化学习 (Reinforcement Learning)** 领域的实战研发历程、生产部署瓶颈、系统架构权衡与客观基准测试。

---

## 👨‍💻 作者简介

我是一名专注于将前沿理论算法转化为高可靠、实时边缘端与云端系统的人工智能与机器人软件工程师。核心专长涵盖：

- **自主移动系统与强化学习**: 马尔可夫决策过程 (MDP) 构建、连续-离散状态动作映射、稠密奖励函数整形 (Reward Shaping) 及 Sim-to-Real 真实硬件迁移。
- **深度计算机视觉**: 实时多阶段推理流水线、目标检测 (YOLO 系列)、多目标跟踪 (CSRT, DeepSORT)、超分辨率图像重建 (EDSR) 及基于时序投票机制的 OCR 引擎。
- **自然语言处理与 AI 安全对齐**: Llama 架构的高效微调 (PEFT/LoRA)、极端类别不平衡下的序数回归 (Ordinal Regression) 与确定性安全拦截网 (Safety Wrapper)。
- **全栈机器学习工程**: 高吞吐 FastAPI 微服务、容器化部署、Docusaurus 多语言技术文档及 React Native 跨平台应用研发。

---

## 📚 博客核心连载专栏

### 1. 🧠 心灵守护者 (Maeumjigi) 毕业设计全纪实 (共 23 篇)
基于多智能体与大模型构建的自杀危机识别与心理干预系统开发实录。

### 2. 🤖 Webots Q-Learning 自主移动机器人 (共 5 篇)
从零知识随机探索到物理双差速小车避障导航的 Sim-to-Real 全闭环实战。

### 3. 🚗 行车记录仪车辆检测与车道入侵视觉 AI (共 5 篇)
应对高速公路真实恶劣光照与抖动的 30 FPS 实时嵌入式边缘视觉系统。
"""

# zh-Hant about.md
about_hant = """---
title: 關於我與部落格
description: 關於作者 Jihwan Park (朴智煥) 與 Global Dev Blog - 人工智慧、機器人、電腦視覺與強化學習深度工程實踐。
keywords: [關於我, Jihwan Park, AI 工程師, 機器人, 電腦視覺, 強化學習, 心靈守護者]
---

# 關於我與部落格

歡迎來到 **Global Dev Blog**，這是由 **Jihwan Park (jbjihwan)** 維護的技術實驗筆記與工程專欄。

本部落格旨在忠實記錄在 **人工智慧 (AI)、機器人控制 (Robotics)、電腦視覺 (Computer Vision) 與強化學習 (Reinforcement Learning)** 領域的實戰研發歷程、生產部署瓶頸、系統架構權衡與客觀基準測試。

---

## 👨‍💻 作者簡介

我是一名專注於將前沿理論演算法轉化為高可靠、即時邊緣端與雲端系統的人工智慧與機器人軟體工程師。核心專長涵蓋：

- **自主移動系統與強化學習**: 馬可夫決策過程 (MDP) 構建、連續-離散狀態動作映射、稠密獎勵函數整形 (Reward Shaping) 及 Sim-to-Real 真實硬體遷移。
- **深度電腦視覺**: 即時多階段推論管線、目標檢測 (YOLO 系列)、多目標追蹤 (CSRT, DeepSORT)、超解析度影像重建 (EDSR) 及基於時序投票機制的 OCR 引擎。
- **自然語言處理與 AI 安全對齊**: Llama 架構的高效微調 (PEFT/LoRA)、極端類別不平衡下的序數回歸 (Ordinal Regression) 與確定性安全攔截網 (Safety Wrapper)。
- **全端機器學習工程**: 高吞吐 FastAPI 微服務、容器化部署、Docusaurus 多語言技術文件及 React Native 跨平台應用研發。

---

## 📚 部落格核心連載專欄

### 1. 🧠 心靈守護者 (Maeumjigi) 畢業設計全紀實 (共 23 篇)
基於多智慧代理與大模型構建的自殺危機辨識與心理干預系統開發實錄。

### 2. 🤖 Webots Q-Learning 自主移動機器人 (共 5 篇)
從零知識隨機探索到物理雙差速自走車避障導航的 Sim-to-Real 全閉環實戰。

### 3. 🚗 行車記錄器車輛辨識與車道入侵視覺 AI (共 5 篇)
應對高速公路真實惡劣光照與抖動的 30 FPS 即時嵌入式邊緣視覺系統。
"""

# zh-Hans privacy-policy.md
privacy_hans = """---
title: 隐私政策
description: Global Dev Blog 关于 Google Analytics 4、Google AdSense Cookie 与访客数据保护的隐私政策。
keywords: [隐私政策, Google AdSense, Google Analytics, GDPR, CCPA, Cookies]
---

# 隐私政策

**生效日期：** 2026年10月18日  
**最近更新：** 2026年10月21日

在 **Global Dev Blog**（访问网址：[https://globaldevlog.com/](https://globaldevlog.com/)），访客的个人隐私对我们至关重要。本隐私政策文件详细说明了 Global Dev Blog 接收和收集的个人信息类型及其使用方式。

如有任何疑问，请随时联系我们：[jbgihwan@gmail.com](mailto:jbgihwan@gmail.com)。

---

## 1. 日志文件 (Log Files)

Global Dev Blog 遵循使用日志文件的标准流程。收集的信息包括 IP 地址、浏览器类型、网络服务提供商 (ISP)、日期时间戳、引用/退出页面等，用于分析趋势与优化站点性能，不与任何个人身份挂钩。

## 2. Cookie 与网络信标 (Cookies)

本网站使用 Cookie 来存储访客的主题偏好（深色/浅色模式）以及多语言设置（英语、韩语、日语、西班牙语、简体中文、繁体中文）。

## 3. Google Analytics 4 (GA4)

本站采用 Google Analytics 4（测量 ID：`G-VM2CVW28SL`）进行匿名访问量统计，已开启 IP 匿名化机制。

## 4. Google AdSense 广告投放

Google 作为第三方广告供应商，使用 Cookie 根据访客访问本网站及其他站点的历史记录投放广告。访客可前往 Google 广告设置页面选择停用个性化广告。
"""

# zh-Hant privacy-policy.md
privacy_hant = """---
title: 隱私權政策
description: Global Dev Blog 關於 Google Analytics 4、Google AdSense Cookie 與訪客數據保護的隱私權政策。
keywords: [隱私權政策, Google AdSense, Google Analytics, GDPR, CCPA, Cookies]
---

# 隱私權政策

**生效日期：** 2026年10月18日  
**最近更新：** 2026年10月21日

在 **Global Dev Blog**（造訪網址：[https://globaldevlog.com/](https://globaldevlog.com/)），訪客的個人隱私對我們至關重要。本隱私權政策文件詳細說明了 Global Dev Blog 接收和收集的個人資訊類型及其使用方式。

如有任何疑問，請隨時聯絡我們：[jbgihwan@gmail.com](mailto:jbgihwan@gmail.com)。

---

## 1. 記錄檔 (Log Files)

Global Dev Blog 遵循使用記錄檔的標準流程。收集的資訊包括 IP 位址、瀏覽器類型、網路服務供應商 (ISP)、日期時間戳記、參照/結束頁面等，用於分析趨勢與優化網站效能，不與任何個人身分掛鉤。

## 2. Cookie 與網路信標 (Cookies)

本網站使用 Cookie 來儲存訪客的主題偏好（深色/淺色模式）以及多語言設定（英語、韓語、日語、西班牙語、簡體中文、繁體中文）。

## 3. Google Analytics 4 (GA4)

本站採用 Google Analytics 4（評估 ID：`G-VM2CVW28SL`）進行匿名流量統計，已開啟 IP 匿名化機制。

## 4. Google AdSense 廣告投放

Google 作為第三方廣告供應商，使用 Cookie 根據訪客造訪本網站及其他網站的歷史記錄投放廣告。訪客可前往 Google 廣告設定頁面選擇停用個人化廣告。
"""

with open(os.path.join(zh_hans_dir, "contact.md"), "w", encoding="utf-8") as f:
    f.write(contact_hans)
with open(os.path.join(zh_hant_dir, "contact.md"), "w", encoding="utf-8") as f:
    f.write(contact_hant)

with open(os.path.join(zh_hans_dir, "about.md"), "w", encoding="utf-8") as f:
    f.write(about_hans)
with open(os.path.join(zh_hant_dir, "about.md"), "w", encoding="utf-8") as f:
    f.write(about_hant)

with open(os.path.join(zh_hans_dir, "privacy-policy.md"), "w", encoding="utf-8") as f:
    f.write(privacy_hans)
with open(os.path.join(zh_hant_dir, "privacy-policy.md"), "w", encoding="utf-8") as f:
    f.write(privacy_hant)

print("Successfully wrote Chinese pages for zh-Hans and zh-Hant!")
