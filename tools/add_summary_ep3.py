# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-10-24\stanford_cs146s_3"
folder_name = "2026-10-24-stanford-cs146s-3"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **The MCP Standardization Paradigm**: Model Context Protocol (MCP) serves as the "LSP for AI Agents", replacing brittle $N \\times M$ custom wrappers with an open, bidirectional JSON-RPC 2.0 protocol across AI hosts and tools.
2. **Decoupling Brain from Hands**: The LLM context window remains strictly dedicated to high-level logical reasoning, delegating physical I/O and state mutations to sandboxed, isolated MCP servers.
3. **Dual Transport Architecture**: High-speed, local low-latency workflows execute via sub-millisecond Stdio pipes, while enterprise distributed agents scale via Streamable HTTP/SSE secured with OAuth 2.0.
4. **Human-in-the-Loop Security Guardrails**: Mission-critical agent deployments enforce the Principle of Least Privilege—blocking destructive disk and database state mutations until explicit developer confirmation is granted.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **MCP 표준화의 패러다임**: Model Context Protocol(MCP)은 AI 에이전트 계의 LSP(Language Server Protocol)로서, $N \\times M$ 스파게티 연동 문제를 해결하고 개방형 JSON-RPC 2.0 표준 통신을 확립했습니다.
2. **두뇌와 물리적 손의 완벽한 분리**: LLM은 복잡한 논리 추론에만 집중하고, 파일 I/O와 데이터베이스 쿼리 등 상태를 변경하는 물리적 작업은 샌드박스화된 MCP 서버가 전담합니다.
3. **이원화된 전송 계층 (Stdio vs HTTP/SSE)**: 로컬 개발 환경에서는 밀리초 미만의 초고속 Stdio 파이프라인을 사용하고, 원격 엔터프라이즈 환경에서는 OAuth 2.0 기반의 스트리밍 HTTP/SSE 전송을 채택합니다.
4. **인간 승인 기반의 보안 가드레일**: 강력한 에이전트 자율성 뒤에 '최소 권한의 원칙'과 파일 삭제·DB 수정 시 개발자의 명시적 승인을 요구하는 Human-in-the-Loop 방어선을 구축해야 안전합니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **MCPによる標準化パラダイム**: Model Context Protocol(MCP)は「AIエージェント界のLSP」として、$N \\times M$ の独自連携スパゲッティを解消し、オープンな双方向JSON-RPC 2.0規格を確立しました。
2. **頭脳と物理的な手の完全分離**: LLMはコンテキスト内での論理推論に専念し、ファイルI/OやDBクエリといった物理的実行はサンドボックス化されたMCPサーバへ安全に委任されます。
3. **2系統のトランスポート層 (Stdio vs HTTP/SSE)**: ローカル開発ではサブミリ秒の高速Stdioパイプを活用し、リモートのエンタープライズ連携ではOAuth 2.0認可を伴うストリーミングHTTP/SSEが機能します。
4. **人間の承認による安全ガードレール**: 強力な自律エージェント運用において最小権限の原則を徹底し、破壊的な状態変更には必ず人間の明示的な承認を挟む設計が不可欠です。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **El Paradigma de Estandarización de MCP**: Model Context Protocol (MCP) actúa como el "LSP para Agentes de IA", resolviendo el espagueti de integraciones $N \\times M$ mediante un protocolo abierto y bidireccional JSON-RPC 2.0.
2. **Desacoplamiento entre Cerebro y Manos**: El LLM se concentra exclusivamente en el razonamiento lógico, mientras que las mutaciones físicas de estado e I/O se delegan a servidores MCP aislados.
3. **Arquitectura de Doble Transporte (Stdio vs HTTP/SSE)**: Permite flujos locales de sub-milisegundo mediante pipes Stdio de alta velocidad, escalando a entornos remotos con streaming HTTP/SSE protegido por OAuth 2.0.
4. **Guardarraíles de Seguridad con Humano en el Bucle**: Aplica el principio de mínimo privilegio, bloqueando cualquier mutación destructiva de disco o base de datos hasta recibir confirmación explícita del desarrollador.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **MCP 工业级标准化范式**：模型上下文协议 (MCP) 被誉为“AI 智能体领域的 LSP”，彻底终结了 $N \\times M$ 的私有胶水代码乱象，建立了开放双向的 JSON-RPC 2.0 通信标准。
2. **大脑决策与物理执行解耦**：大模型专注于上下文逻辑推理与决策，文件读写与数据库变更等有状态物理操作全权交由沙箱化 MCP 服务端隔离执行。
3. **双重传输层架构 (Stdio vs HTTP/SSE)**：本地开发环境借助亚毫秒级 Stdio 高速管道交互，远程企业级集群则通过经由 OAuth 2.0 鉴权的流式 HTTP/SSE 实现弹性扩展。
4. **人在回路安全防线**：坚决贯彻最小权限原则，对文件删除与数据库覆盖等高危破坏性操作强制引入人类开发者确认卡点，杜绝智能体失控风险。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **MCP 工業級標準化範式**：模型上下文協定 (MCP) 被譽為「AI 智慧體領域的 LSP」，徹底終結了 $N \\times M$ 的私有膠水程式碼亂象，建立了開放雙向的 JSON-RPC 2.0 通訊標準。
2. **大腦決策與物理執行解耦**：大型語言模型專注於上下文邏輯推理與決策，檔案讀寫與資料庫變更等有狀態物理操作全權交由沙箱化 MCP 伺服端隔離執行。
3. **雙重傳輸層架構 (Stdio vs HTTP/SSE)**：本機開發環境藉由亞毫秒級 Stdio 高速管道互動，遠端企業級叢集則透過經由 OAuth 2.0 鑑權的串流 HTTP/SSE 實現彈性擴展。
4. **人在迴路安全防線**：堅決貫徹最小權限原則，對檔案刪除與資料庫覆寫等高危破壞性操作強制引入人類開發者確認卡點，杜絕智慧體失控風險。
"""

nb_summary = """
---

## 📌 3~5줄 최종 요약
1. **MCP 표준화의 힘**: AI 에이전트 계의 LSP로서 복잡한 개별 연동 코드를 없애고 오픈 JSON-RPC 2.0 표준을 구축했습니다.
2. **두뇌와 손의 분리**: LLM은 논리 추론에만 집중하고, 실제 파일 및 DB 작업은 독립된 샌드박스 MCP 서버가 수행합니다.
3. **초고속 Stdio & 확장형 HTTP/SSE**: 로컬에서는 지연 없는 Stdio 파이프로, 원격에서는 보안 OAuth 2.0 기반 HTTP 스트리밍으로 연동합니다.
4. **인간 승인 가드레일**: 파일 삭제나 DB 수정 등 위험한 작업은 반드시 개발자의 승인[Y/n]을 거쳐야 실행되는 안전장치를 갖췄습니다.
"""

def append_summary(file_path, summary_text, ref_marker):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "Executive Summary" in content or "최종 요약" in content or "Resumen Ejecutivo" in content or "核心总结" in content or "核心總結" in content:
        print(f"Summary already present in {file_path}")
        return
    
    if ref_marker in content:
        parts = content.split(ref_marker, 1)
        new_content = parts[0].rstrip() + "\n" + summary_text.strip() + "\n\n" + ref_marker + parts[1]
    else:
        new_content = content.rstrip() + "\n" + summary_text.strip() + "\n"
        
    # Clean double hr
    new_content = re.sub(r'---\s*\r?\n\s*---', '---', new_content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Appended summary to: {file_path}")

# Apply to all 6 locales
append_summary(f"{gb_root}/blog/{folder_name}/index.md", en_summary, "### References & Course Materials")
append_summary(f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md", ko_summary, "### References & Course Materials")
append_summary(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", ja_summary, "### 参考文献 & 公式教材")
append_summary(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", es_summary, "### Referencias y Materiales del Curso")
append_summary(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hans_summary, "### 课程参考资料")
append_summary(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hant_summary, "### 課程參考資料")

# Apply to Naver Blog
append_summary(f"{nb_root}/post.md", nb_summary, "## 5. 글로벌 기술 블로그에서 상세 아키텍처 다이어그램 확인하기")

print("Episode 3 summary injection finished successfully!")
