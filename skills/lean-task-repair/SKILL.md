---
name: lean-task-repair
description: 检查并修复用户指定的单个 Lean task，依次排查搜索路径、Lean 依赖、Unicode 定理头、checker 语义遮蔽、原题一致性和公开完整 Lean4 证明；运行实际 checker 入口，并记录验证覆盖范围。
---

# 单个 Task 六项检查与修复

用户会指定一个 task，agent 在该 task 的当前目录中直接进行修复。以当前目录作为任务根目录，对这一题依次执行下面六项；每项先判断是否存在，再按证据修复或标记，并验证结果。不能只列建议就结束，也不能因为前几项正常就跳过后面的检查。

按下文 1–6 顺序开展检查：先在步骤 2 检查额外 import、补齐预编译依赖并配置构建验证，在步骤 3 修复 Unicode 与冻结头匹配，再在步骤 4 实施和验证语义隔离。步骤 5 仅检查并标记原题一致性，不修改数学陈述或定义；步骤 6 对照当前任务实际保留的命题核对公开证明。所有修改完成后，复核 Dockerfile 末尾保留步骤 2 的普通用户依赖验证。

每题结果统一写入 `<task根目录>/repair-report.json`，按文末的简单 JSON 格式逐项说明是否存在问题、是否已修复。受阻或部分完成也要保存结果。

## 1. instruction 的搜索路径是否遗漏 packages

**检查：** 定位本题 instruction.md 的源码搜索命令，确认其显式包含下面三个路径。父目录 /opt/formal-conjectures 不等于已显式覆盖隐藏的 .lake/packages。

**存在则修复为：**

```bash
rg --glob '*.lean' 'search term' \
  /app \
  /opt/formal-conjectures \
  /opt/formal-conjectures/.lake/packages
```

保留 instruction 其他规则。后续步骤 2 或 4 若改变布局，返回同步说明可编辑文件和测试入口。

**验证：** 确认命令语法正确，能搜到选定的 package 内已知 Lean 定义。rg 退出码 1 可能只是没有匹配，不能当路径错误或通过的依据；权限/路径错误单独记录。

## 2. Lean 依赖是否可在真实运行用户下加载

**检查：** 读取本题 `Target.lean`（以任务中的实际路径及大小写为准），检查是否有以下两个模块之外的 import：

```lean
import FormalConjectures.Util.ProblemImports
import FormalConjecturesBench.Submission
```

**补充预编译：** 如有额外的上游 import，将其去重后追加到本题 Dockerfile 的 `lake build FormalConjectures.Util.ProblemImports` 命令后。例如额外导入 `FormalConjectures.Wikipedia.Schinzel` 时，改为：

```dockerfile
    lake build FormalConjectures.Util.ProblemImports FormalConjectures.Wikipedia.Schinzel && \
```

按本题实际 imports 补齐，保留原命令链；预编译在源码清理及切换用户之前完成。本地 `FormalConjecturesBench` 模块由 `/app` 工程构建，不加入上游预编译命令。

**最后用 ubuntu 构建 Target 验证：** 无论是否有额外 import，都在本题 Dockerfile 完成源码复制、清理和权限设置后，以如下片段结尾；已有相同验证时不重复添加。

```dockerfile
WORKDIR /app
ENV HOME=/home/ubuntu
USER ubuntu

# Exercise the same build as the checker without granting write access to the
# trusted dependency. Missing precompiled imports must fail the image build.
RUN lake build +FormalConjecturesBench.Target
```

缺少依赖时应让镜像构建失败，不忽略退出码，也不放宽依赖权限。

**验证：** 静态核对额外 imports 与预编译命令、Dockerfile 末尾验证的位置和运行用户。

## 3. 定理头是否因 Unicode 编码被误判

**根因：** 生成器将默认 `json.dumps(header)` 的输出直接当作 Python 字面量写入 checker。非 BMP 字符如 `𝓝`（U+1D4DD）会被转义成 `\ud835\udcdd`，Python 将其解析为两个代理码点，与 UTF-8 Target 中的单个字符不相等，导致未修改的定理头也被误判。生成 Python 常量应使用 `repr(header)`；真正的 JSON 则通过 `json.loads` 解析。

**执行：** 使用随技能提供的 [scripts/check_unicode_header.py](scripts/check_unicode_header.py)，一次完成检测、按需修复和复验。以下命令在本技能目录执行，传入当前 task 根目录的绝对路径：

```bash
python3 scripts/check_unicode_header.py "<task根目录绝对路径>"
```

脚本只处理本题 `tests/test_target.py` 和 `environment/data/checker/test_target.py`：通过 AST 读取常量，检测 Unicode 代理码点，并与原始 Target 和两份可信 golden Target 核对头、冻结前缀及 `:=` 边界。确认只是合法代理对编码问题后，用 `repr(header)` 同步修复两份 `EXPECTED_HEADER`，再验证原始头通过、修改头与移除 `:=` 被拒绝、两份 checker 一致。无问题则不修改。

**结果：** 根据脚本的 `case` 填写结果：`no_issue` 为“无问题、无需修复”，`unicode_repaired` 为“有问题、已修复”；其他值按 `error` 排查，记为未修复。无法判定是否存在问题时填“未知”，孤立代理项属于有问题。不要求在报告粘贴完整 JSON 或日志。

退出码 `0` 表示无问题或修复成功，`2` 表示未解决。JSON 中 `has_problem` / `has_unicode_issue` 表示是否发现问题，`repair_attempted` / `repair_success` 表示是否尝试及完成修复，`modified` 表示最终是否有改动；`checkers` 提供每份文件的详情，`rollback` 说明失败后是否恢复原内容。无法判定或未尝试的字段可能为 null，不能当作 false。

**边界：** 输入必须是同一修订版本的可信原始任务。孤立代理项、基线不符或 checker 的其他差异均拒绝自动覆盖；写入或复验失败时尝试恢复原内容。仅替换两份头部字面量，不修改 Target、冻结基线或共享生成器，不放宽检查。脚本不执行 checker 顶层代码，不运行 Lean；本项通过不代表原题证明通过。

## 4. checker 是否只冻结文字，仍允许语义偷换

**检查：** 查看 Target 是否先导入可编辑的 Submission/helper，golden 是否在导入 Target 后才解析预期命题。提交可能通过名称、记号或类型类实例改变命题及前缀定义的含义，定理头和哈希不变仍可通过。已有 Spec 时，也须检查其生成过程和依赖是否受候选影响。

**存在则修复：先编译可信 Spec，再加载候选，检查完整定理类型。**

1. **生成 Spec。** verifier 从本题原始 `golden_env` 取前缀定义和目标声明，移除对 Submission/helper 的导入，在全新临时工程中用锁定的 Lean 和可信依赖编译，不复用候选缓存或配置。用 Lean parser/elaborator 提取完整目标类型及 universe 参数，保留全部显式、隐式和实例参数。前缀定义保留原名；完整命题存为 `FCBTrustedSpec.ExpectedType` 的定义值，不用字符串、新 axiom 或正则拼接类型，提取时的占位证明不得进入其依赖。
2. **组装验证副本。** 加载任何候选文件前完成 Spec 编译，保护其源码、产物和传递依赖，固定搜索路径以防同名模块或缓存遮蔽。仅复制允许的候选源码，先导入 Spec，再加载 Submission/helper 和目标证明；前缀定义统一来自 Spec。只转换临时 Target，不改公开 Target 或刷新冻结基线。
3. **检查目标定理。** 由 `test_target.py` 生成临时 Lean 检查文件，用根限定名检查整条定理类型，替换原先复制并执行 `GoldenCheck.lean` 的类型检查路径。例如无 universe 参数的目标：

   ```lean
   example : _root_.FCBTrustedSpec.ExpectedType :=
     @_root_.Arxiv.«0912.2382».curling_number_conjecture
   ```

   多态目标按可信 universe 参数实例化。元程序辅助比较时，应比较 ExpectedType 的 **value** 与目标的 **type**，并引用同一份可信定义；不能在候选环境重新解析预期命题，或跨环境仅按常量名判等。
4. **同步本题入口。** 默认只修改 `tests/test_target.py` 和 `environment/data/checker/test_target.py`。Spec、辅助 Lean 文件和验证副本均由 Python 在运行时生成到临时目录；`golden_env` 作为只读基线，不改仓库中的 `GoldenCheck.lean` 或 Dockerfile。若现有环境无法满足依赖或隔离要求，再按具体缺口最小修改并说明原因。记录输入哈希及 Lean/依赖版本，保留原冻结检查、源码限制、公理审计和 sorry canary；可信类型及依赖也须审计，不全面禁用正常的 `def`、`lemma`、`instance`。

**静态检查：** 用 Python AST 解析检查两份 `test_target.py` 的语法；核对两个入口逻辑一致、Spec 输入可信且先于候选加载、产物及依赖受保护、完整类型及 universe 参数进入检查，并确认原冻结检查、公理审计和 sorry canary 的调用路径保留。Python AST 通过只能说明 Python 语法合法，不能验证字符串中生成的 Lean 代码。

**实际入口验证：** 在任务锁定的工具链、依赖及隔离环境中，实际运行修复后的 `tests/test_target.py`，验证 Python 编排路径。用隔离工作目录准备固定配置及原始目标源码，不把 checker 自身的源码目录混入提交目录。例如：

```bash
FCB_TASK_DIR="<隔离的 task 工作目录>" \
FCB_TESTS_DIR="<task根目录>/tests" \
python3 "<task根目录>/tests/test_target.py"
```

记录实际命令、退出码、日志和最后到达阶段，区分输入被预期规则拒绝与 checker 自身故障。工具链定位、依赖权限、临时目录、编译顺序、结果解析、公理审计及 canary 均可能出现运行时问题，单独编译 Lean 或导入 Python 模块不能代替这一项。两份 checker 内容一致时可运行正式入口并核对本地入口一致性；有差异时须分别验证。

修复任务不要求提供或构造原题完整证明，也不以 checker 返回 0 为验收条件。原始 Target 含 `sorry`，通常会在源码限制检查处提前退出；这只覆盖已执行的检查，不能据此判定后续流程正确。对尚未到达的关键路径，在独立临时验证程序中调用同一份 checker 的实际函数，补测可信 Spec 和审计代码的生成与编译、候选编译、完整类型检查、公理审计及 canary。需要编译候选时可在隔离 fixture 中保留占位证明，并确认其 `sorryAx` 可见且会被拒绝；不得为此放宽正式 checker、修改公开 Target 或刷新 golden 基线。

**结果与受阻处理：** 实现完整、静态检查通过、实际入口已运行且后续关键路径已按上述方式验证，确认 checker 自身故障已排除后，才可填 `repaired`。note 分别说明入口的预期退出原因、组件验证结果及未覆盖阶段；组件验证通过不等于完整入口所有分支均已验证，更不等于原题证明通过。缺少锁定工具链、依赖或隔离能力，或关键路径尚未验证时，可完成静态修改，但填 `not_repaired` 并注明“已修改，待运行验证”及具体缺口；不因缺少运行环境强制构建镜像，也不能退回受候选影响的检查并判通过。

## 5. Lean 陈述及定义是否与原题一致

**本项仅检查和标记，不修改问题。** 即使差异明确且知道如何修正，也保留本题的数学陈述、定理头、假设和定义；不通过改 Spec、golden 或冻结哈希变相纠正数学问题。

**检查：** 从本题注释/manifest 找原题，实际读取原始论文、作者网页或题目来源。对照完整前缀定义和定理，而非只读 theorem 头：量词、域、假设、区间、常数、严格性、取整、渐近范围、非空/非负/可积性、GRH 的具体版本和方向都需核对。

优先复核已知案例：Constant1a 的卷积区间和可积性/sSup；Green38 best_lower 的 ε 范围；Green32 dirichlet_regime 的 ω 与 floor 边界。不能因此把同一题号的其他变体也判错。还要检查“无限多个”误成“充分大均成立”、≥误成>、Euler–Mascheroni 与 Catalan 混淆等差异。

**存在或存疑则标记：** 在本题 task.toml 的 metadata 和报告中分别标 statement_status=mismatch 或 suspect，附原文位置、Lean 位置、具体差异/反例；核对一致时标 consistent，证据不足时标 unknown。

可在报告中记录差异的数学原因和待审建议，但不应用修订，不因本项结果重建 Spec、刷新冻结基线或重写 golden。Constant1a 的区间、Green32 的边界条件等问题均只标记；若涉及配对任务，只记录受影响 ID，本次不修改其他任务。

## 6. 是否存在公开完整 Lean4 证明

**先查本地集合：** 按完整 task ID 精确匹配 [references/public-lean4-proofs.csv](references/public-lean4-proofs.csv) 的 `task` 列。集合包含 `task` 和 `proof_urls` 两列。命中即判定已有公开完整 Lean4 证明，设置 `public_lean4_proof=true`，记录来源，无需再次联网确认。

**未命中则充分搜索：** 尽力查找已知公开完整 Lean4 证明，不能仅凭一次搜索、一个来源或定理名无匹配就结束。结合题号、题目名称、数学陈述、完整 Lean 定理名及其别名、作者和相关论文，使用多组关键词检索原作者网页/仓库、上游 FormalConjectures、Mathlib、GitHub 等公开来源；追踪相关结果中的证明链接、PR、分支、fork 和引用，覆盖不同命名空间或等价表述下的证明。对有希望的线索实际读取 Lean4 源码，核对当前任务完整陈述、定义、方向和证明依赖。只有覆盖本目标且无 `sorry`、`admit` 或未经允许公理的完整证明才标 true；关键引理、骨架或反方向证明不算。步骤 5 的差异标记不改变检索目标。只有在主要来源已覆盖、相关线索已逐一核查且没有尚待跟进的有效线索后，才记录“经充分检索未找到已知公开完整 Lean4 证明”，并列明检索词、来源、候选排除原因及访问限制；存在无法访问的关键来源或未核实线索时记 `unknown` / `blocked`，不能称已确认找不到。公开检索不能绝对证明不存在证明。

**标记与记录：** 在本题 `task.toml` 的 metadata 和报告中标记结果，附 task ID、来源及实际验证情况；已有公开证明不等于已在本题环境编译。未找到或检索受阻时记录 `searched` / `unknown` / `blocked` 及原因，不能仅凭未命中断言不存在证明。只做标记，不替换目标、删除任务或将公开答案放入镜像。

## 单题报告与完成标准

报告写入 `<task根目录>/repair-report.json`，与 `task.toml` 同级，不复制进评测容器或作为测试输入。

固定使用以下结构，替换 task ID，并按实际检查结果更新六项初始值：

```json
{
  "task_id": "<完整 task ID>",
  "checks": {
    "instruction_search": {"has_issue": null, "repair_status": "not_repaired", "note": ""},
    "lean_dependency": {"has_issue": null, "repair_status": "not_repaired", "note": ""},
    "unicode_header": {"has_issue": null, "repair_status": "not_repaired", "note": ""},
    "semantic_checker": {"has_issue": null, "repair_status": "not_repaired", "note": ""},
    "statement_fidelity": {"has_issue": null, "repair_status": "not_repaired", "note": ""},
    "public_lean4_proof": {"has_issue": null, "repair_status": "not_repaired", "note": ""}
  }
}
```

- `has_issue`：`true` 表示存在问题，`false` 表示未发现，`null` 表示未知或尚未检查；保留修复前的发现，不把布尔值或 null 写成字符串。
- `repair_status`：仅用 `repaired`（已修复且完成要求的验证）、`not_repaired`（未修复或待验证）、`not_needed`（无问题，无需修复）、`marked`（仅标记）。
- `note`：简短说明实际修改、疑点或受阻原因，必要时附关键来源/位置；无需说明时填空字符串。

第 5 项发现命题差异或疑点、第 6 项确认存在公开完整证明时，填 `has_issue: true`、`repair_status: "marked"`，不称为已修复；第 6 项的 `false` 仅表示按要求检索未找到，不表示证明绝对不存在。

前文检查要求的证据和验证仍须实际完成，但报告无需展开完整日志、脚本原始 JSON 或复查历史。受阻时继续其他不依赖它的检查，不把未确认当作无问题。保存后用 JSON 解析器确认文件合法。

最终回复提供报告的绝对路径链接，并简短说明未确认或未验收项；需要展示报告内容时使用 JSON 代码块。有未完成项时不能写“全部修复”。本次调用只处理用户指定的这一题。
