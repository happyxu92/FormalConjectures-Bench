---
name: lean-task-repair
description: 检查并修复用户指定的单个 Lean task，依次排查搜索路径、Lean 依赖、Unicode 定理头、checker 语义遮蔽、数学陈述有效性和公开完整 Lean4 证明；运行实际 checker 入口，并记录验证覆盖范围。
---

# 单个 Task 六项检查与修复

用户会指定一个 task，agent 在该 task 的当前目录中直接进行修复。以当前目录作为任务根目录，对这一题依次执行下面六项；每项先判断是否存在，再按证据修复或标记，并验证结果。不能只列建议就结束，也不能因为前几项正常就跳过后面的检查。

按下文 1–6 顺序开展检查：先在步骤 2 检查额外 import、补齐预编译依赖并配置构建验证，在步骤 3 修复 Unicode 与冻结头匹配，再在步骤 4 实施和验证语义隔离。步骤 5 仅检查并标记数学陈述或定义中导致目标无法成立的明显问题，允许合理变体，不修改数学陈述或定义；步骤 6 对照当前任务实际保留的命题核对公开证明。所有修改完成后，复核 Dockerfile 末尾保留步骤 2 的普通用户依赖验证。

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

**检查：** 查看 Target 是否先导入可编辑的 Submission/helper，checker 是否在加载候选后才解析预期命题。提交可以通过名称、记号或类型类实例改变命题及前缀定义的含义，即使定理头和冻结哈希未变。已有 Spec 时，也须核对它的生成输入、编译环境、存放位置和实际加载路径是否可信。

**修复方案：修复 task 时提前生成、预编译可信 Spec；verifier 直接加载固定产物，检查完整定理类型。** 预期命题在没有候选参与的环境中完成 elaboration，保存为 Lean 类型表达式。只保存定理头字符串，之后在候选环境中重新解析，仍会留下语义遮蔽问题。verifier 不生成、提取或重新编译 Spec，也不在产物缺失时自动回退到源码编译。

### 修复阶段：生成并交付可信产物

1. **确定可信输入。** 从本题原始 `golden_env` 取得完整前缀及目标声明，移除对 Submission/helper 的导入。在与本题锁定的 Lean、依赖修订和目标平台匹配的干净环境中生成、编译，不加载候选源码、Lake 配置或缓存。优先使用匹配的本地 Docker 环境完成预编译；不能将宿主机其他版本生成的 `.olean` 直接视为兼容。
2. **提取完整类型。** 用 Lean parser/elaborator 提取完整目标类型及 universe 参数，保留全部显式、隐式和实例参数。前缀定义保留原名；将完整类型表达式存为 `FCBTrustedSpec.ExpectedType` 的定义值。不能用字符串常量、新 axiom 或正则拼接类型替代。提取时如使用占位证明，临时目标声明不得导出到交付 Spec，其证明也不得进入 ExpectedType 或其传递依赖。交付模块应能独立于候选加载。
3. **预编译并审计。** 编译生成 Spec 的 `.olean` 及该工具链实际需要的配套产物；保留可复现的源码和生成代码或命令。独立导入该模块，核对 ExpectedType 的定义值、完整参数和 universe 参数，并审计它及其引用的前缀定义的传递依赖。只能依赖任务允许的标准 Lean 公理，不能依赖临时占位证明的 `sorryAx` 或新增公理。生成或审计失败时先修复，不能交付未验证的产物。
4. **同步两份可信包。** 将同一次生成的源码、编译产物和清单分别保存到 `tests/trusted_spec/` 与 `environment/data/checker/trusted_spec/`；如本题已有等价布局则沿用。清单记录 task ID、目标名、原始 golden 输入哈希、生成源码/代码及编译产物哈希、Lean 版本、平台、依赖修订和 universe 参数的名称与顺序。两份包内容须一致，清单及其哈希依据也属于可信文件。原始数学输入、工具链或依赖发生变化后，须在修复阶段重新生成、审计并同步，不由 verifier 自行刷新。

`golden_env`、公开 Target、冻结前缀哈希和定理头均保留原样，不改仓库中的 `GoldenCheck.lean`。新增 Spec 是由可信原题导出的评测产物，不是修改数学陈述或引入任务答案。

### verifier 阶段：加载固定 Spec 并检查候选

两份 `test_target.py` 只增加加载可信包、组装验证副本和完整类型检查所需的逻辑，保留原冻结检查、源码限制、公理审计和 sorry canary，不全面禁用正常的 `def`、`lemma`、`instance`。

- **加载前校验。** 根据固定的可信位置读取清单和预编译产物，核对输入、版本、产物哈希及本题目标是否匹配；缺失、损坏或不兼容时明确失败。运行时不从候选目录寻找替代 Spec，不调用生成器，也不从候选环境重新解析 ExpectedType 的定义。
- **统一加载位置。** 正式 verifier 执行前，Harbor 将宿主任务的 `tests/` 上传到容器 `/tests/`，包括预编译 Spec。checker 使用 `SPEC_DIR = TESTS_DIR / "trusted_spec"`：正式入口取 `/tests/trusted_spec/`；本地 `check.sh` 通过已有 `FCB_TESTS_DIR` 取 `/opt/formal-conjectures-bench-checker/trusted_spec/`，沿用 Dockerfile 的复制及权限设置。正式入口不改读 agent 阶段预装的副本，也不要求两处在运行时互相比对。
- **固定搜索路径。** 使用锁定工具链和可信依赖路径，保证 `FCBTrustedSpec` 只解析到已验证的预编译模块；候选同名模块、`.lake` 缓存或环境变量不能覆盖它。不使用候选 Lake 配置重建可信模块或依赖。
- **组装临时候选。** 仅复制允许的候选 Lean 源码，不复用候选编译缓存。先导入可信 Spec，再加载 Submission/helper 和目标证明；临时 Target 中的前缀定义统一来自 Spec，避免重复定义同名常量。保留目标所需的 namespace、scoped 设置及上下文。只转换临时副本，不修改公开 Target 或刷新冻结基线；候选编译仍以真实用户 `ubuntu` 执行。
- **检查完整类型。** 替换原先复制并执行 `GoldenCheck.lean` 的类型检查路径。checker 可以生成一个临时 Lean 检查文件，但其中只引用已编译的 ExpectedType，不重复书写或解析原命题。例如无 universe 参数时：

  ```lean
  import FCBTrustedSpec
  import FormalConjecturesBench.Target

  example : _root_.FCBTrustedSpec.ExpectedType :=
    @_root_.Arxiv.«0912.2382».curling_number_conjecture
  ```

  用本题实际的根限定目标名替换示例。多态目标按可信清单记录的 universe 参数完整实例化。若用元程序辅助比较，应在同一环境中比较可信 ExpectedType 的 **value** 与目标的 **type**，不能只比较 ExpectedType 自身的类型，也不能跨环境仅按常量名判等。导入预编译 Spec 后，名称和实例选择已经固定；候选新实例若改变目标类型，完整类型检查应拒绝。

**修改范围：** 只增加两份 checker 的 Spec 加载、临时副本和类型比较逻辑，新增两份一致的 Spec 包；复用原有检查、构建流程及入口，必要时仅调整编译搜索路径。不要求文件一律归 root 所有，不新增全依赖权限扫描或 Dockerfile 的 `chown/chmod` 加固。实际打包或加载故障按证据做最小修复，不新增 `sudo` 或 root supervisor。步骤 2 的 Dockerfile 末尾普通用户依赖验证仍须保留。

### 验证与验收

**静态核对：** 用 Python AST 检查两份 checker 语法，核对入口逻辑和可信包内容一致；检查 Spec 的可信输入、预编译/审计记录及完整参数，确认运行时仅加载固定产物，候选缓存不能遮蔽它。确认临时 Target 引用同一份前缀定义，以及冻结检查、源码限制、公理审计和 sorry canary 的调用路径保留。AST 通过不代表生成的 Lean 检查代码正确，也不代表预编译产物能在 task 中加载。

**实际入口：使用当前本地 task 构建 Harbor Docker 子容器。** 使用本题修改后的 checker、可信 Spec 包、`environment/Dockerfile` 和 `task.toml`，不能拉取 registry 的旧 task 替代。构建、启动及保留容器的参数以本机 Harbor CLI 帮助为准；不挂载 Docker socket 或额外宿主机依赖，不放宽权限。预编译使用过的环境不能代替最终交付包的本地 Harbor 构建验收。

核对容器内两份 checker、Spec 包和 golden 与本地的哈希一致，确认 `/tests` 由 Harbor 在 verifier 阶段提供，正式与本地入口分别加载 `/tests` 和 `/opt` 下的包。由 Harbor 提供 `/logs/verifier` 后运行正式入口，例如：

```bash
docker exec "<Harbor task 子容器名>" bash /tests/test.sh
```

核对 `/tests/test.sh` 实际以 `FCB_TASK_DIR=/app`、`FCB_TESTS_DIR=/tests` 调用修复后的 checker，检查退出码、日志和 `/logs/verifier/reward.txt`。在同一子容器中以 ubuntu 运行 `/app/check.sh`，确认本地入口也直接使用相同的预编译 Spec；不要把 checker 或 Spec 源码目录混入提交目录。

**补测提前退出后未覆盖的路径。** 不要求提供或构造原题完整证明，也不要求 checker 返回 0 或 reward 为 1；原始 Target 的 `sorry`、证明未完成或公理审计因此拒绝，属于可记录的预期结果。若正式入口提前退出，须在同一 Harbor 子容器内用独立临时验证程序调用该 checker 的实际函数，补测预编译 Spec 的加载和可信类型审计、ubuntu 候选编译、完整类型检查、目标公理审计及 sorry canary。可在隔离 fixture 中保留占位证明来覆盖后续路径，并确认公理审计检测、拒绝其 `sorryAx`；不得修改正式 checker、公开 Target 或 golden，也不得关闭、放宽或伪造正式检查。

同时确认冻结修改、越界源码和语义偷换负例被拒绝；至少覆盖一个冻结文字不变而名称或实例改变目标含义的负例。检查同名候选模块或缓存不能遮蔽可信 Spec，预编译产物缺失或哈希不符时明确失败且不会触发运行时重新生成。记录各路径实际到达的阶段和预期结果，不能由提前退出推断后续逻辑正常。Python 异常、产物兼容性、Lean 生成代码、工具链/依赖权限、临时目录、结果解析或入口故障均须排查，不能归为“证明不通过”。

**结果与受阻处理：** 只有提前生成和审计已完成、两份可信包同步、静态核对通过、当前 task 的本地 Harbor Docker 构建及上述入口/关键路径实际验证完毕，且除预期证明失败外没有其他故障，才填 `repaired`。记录生成及构建/运行命令、镜像标识、可信输入和产物哈希、版本、退出码及日志位置；说明预期证明失败和未覆盖分支，不把本项通过写成原题证明通过。Docker/Harbor 不可用、预编译包缺失或不兼容、正式入口未加载本次上传的包、镜像构建失败或关键路径未验证时填 `not_repaired`，说明具体缺口并继续其他独立检查。不得退回候选环境解析预期命题或在 verifier 中临时生成 Spec 后宣称符合本方案。

## 5. Lean 陈述及定义是否存在导致目标无法成立的明显问题

**本项目的与边界：** 重点检查题目是否因陈述或定义错误而实际无解，不要求与原问题完全一致。任务可以是原问题的特例、受限范围、已知结果或其他合理变体；仅有范围、假设或目标差异，不构成问题。原问题仍开放、目标较难或未找到证明，也不能据此判定任务无解。

**本项仅检查和标记，不修改问题。** 即使错误明确且知道如何修正，也保留本题的数学陈述、定理头、假设和定义；不通过改 Spec、golden 或冻结哈希变相纠正数学问题。

**检查：** 先根据 task.toml 指定的上游源文件、目标定理和本题注释/manifest，确认本任务实际要求证明的命题及其变体定位，再读取相关原始论文、作者网页或题目来源。检查完整前缀定义和定理，而非只读 theorem 头：量词、域、假设、区间、常数、严格性、取整、渐近范围、非空/非负/可积性、GRH 的具体版本和方向都需核对。对差异判断其是否有意限定了任务，还是造成错误命题；判错应给出具体反例、矛盾推导或明确的定义错误依据，不能只以“与原题不同”为证据。

例如，`optimizationconstants-1a-c1a-lower-bound` 应重点检查 Constant1a 的卷积区间和可积性/sSup 是否使目标无法成立；Green38 best_lower 的 ε 范围、Green32 dirichlet_regime 的 ω 与 floor 边界也需结合实际定义核查。还要检查“无限多个”误成“充分大均成立”、≥误成>、Euler–Mascheroni 与 Catalan 混淆等可能导致命题错误的情况。不能因此把同一题号的其他变体也判错。

`erdosproblems-145-le-eleven-thirds` 是可接受的变体：原问题 `erdos_145` 询问对所有 α ≥ 0 极限是否存在，本任务只要求证明 0 ≤ α ≤ 11/3 时极限存在，注释将其列为已知结果，且与 task.toml 指定的上游目标一致。不能因它未覆盖完整开放问题而标错；应称为“证明 Erdős 145 的 le_eleven_thirds 变体”，不能称为“解决 Erdős 145 原问题”。

**标记与记录：** 保留现有 `statement_status` 和报告的 `statement_fidelity` 字段。在本题 task.toml 的 metadata 中，确认有上述数学错误时标 `statement_status=mismatch`，有具体错误线索但尚未证实时标 `suspect`，未发现明显问题（包括合理变体）时标 `consistent`，证据不足以判断时标 `unknown`。报告中附来源位置、Lean 位置及具体问题/反例；合理变体可在 note 中说明与原问题的关系，不因差异本身设置 `has_issue: true`。

可在报告中记录问题的数学原因和待审建议，但不应用修订，不因本项结果重建 Spec、刷新冻结基线或重写 golden。Constant1a 的区间、Green32 的边界条件等问题均只标记；若涉及配对任务，只记录受影响 ID，本次不修改其他任务。

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

第 5 项确认数学错误或发现具体错误疑点、第 6 项确认存在公开完整证明时，填 `has_issue: true`、`repair_status: "marked"`，不称为已修复。第 5 项的合理变体且未发现明显问题时填 `has_issue: false`、`repair_status: "not_needed"`；证据不足以判断时填 `has_issue: null` 并说明缺口。第 6 项的 `false` 仅表示按要求检索未找到，不表示证明绝对不存在。

前文检查要求的证据和验证仍须实际完成，但报告无需展开完整日志、脚本原始 JSON 或复查历史。受阻时继续其他不依赖它的检查，不把未确认当作无问题。保存后用 JSON 解析器确认文件合法。

最终回复提供报告的绝对路径链接，并简短说明未确认或未验收项；需要展示报告内容时使用 JSON 代码块。有未完成项时不能写“全部修复”。本次调用只处理用户指定的这一题。
