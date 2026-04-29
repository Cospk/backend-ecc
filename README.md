# ai-code

`ai-code` 是一个面向 AI 协作的系统认知与需求交付底座仓库。

它的目标不是单纯沉淀文档，而是为 AI 提供稳定、可复用的上下文，使 AI 能更低成本地接管需求理解、方案设计、代码实现、测试验收和问题定位。

## 仓库使命

这个仓库主要解决四类问题：

1. 让 AI 快速理解整个系统，而不是每次从零建模。
2. 让需求输入、方案输出和验收方式标准化。
3. 让某个服务组的职责、代码入口和关键链路可以快速定位。
4. 让真实需求和真实排障经验可以持续复用，而不是停留在对话里。

## 顶层结构

仓库按四层组织：

### 1. `00-system/`
系统级认知层。

回答：
- 整个系统是什么
- 我们负责哪些部分
- 有哪些服务组
- 核心链路怎么走

当前重点文件：
- `00-system/system-overview.md`
- `00-system/service-landscape.md`
- `00-system/core-flows.md`

### 2. `10-method/`
方法与模板层。

回答：
- 需求怎么提
- 方案怎么写
- 测试怎么验收
- 从需求到交付怎么走

当前重点文件：
- `10-method/overview/document-system-overview.md`
- `10-method/templates/requirement-template.md`
- `10-method/templates/design-template.md`
- `10-method/templates/test-acceptance-template.md`
- `10-method/sop/requirement-to-delivery-sop.md`

### 3. `20-services/`
服务组 / 仓库级认知层。

回答：
- 某个服务组在系统中的职责是什么
- 代码应该先看哪里
- 内部有哪些关键模块和链路
- 哪些位置是高频改动区或高频故障区

当前重点目录：
- `20-services/market-server/`

### 4. `30-cases/`
案例沉淀层。

回答：
- 以前类似需求怎么做
- 以前类似 bug 怎么查
- 哪些设计决策已经被验证过

## 推荐阅读顺序

### 当你要理解整个系统
先看：
1. `00-system/system-overview.md`
2. `00-system/service-landscape.md`
3. `00-system/core-flows.md`

### 当你要开始提需求
先看：
1. `10-method/templates/requirement-template.md`
2. 按模板整理需求
3. 再参考 `10-method/sop/requirement-to-delivery-sop.md`

### 当你要进入某个服务组
先看：
1. `20-services/<service>/service-group-overview.md`
2. `20-services/<service>/code-map.md`
3. 再进入该服务组的职责文档与流程文档

### 当你要复用历史经验
再看：
1. `30-cases/requirements/`
2. `30-cases/bugs/`
3. `30-cases/design-decisions/`

## 当前第一阶段范围

当前第一阶段只建设最小可用集，优先保证以下能力：

1. 系统边界清晰
2. 服务组定位清晰
3. 需求输入模板可用
4. 方案与验收模板可用
5. `market-server` 可以快速定位入口和链路

## 当前建设重点

当前系统认知已明确：

- 整个系统分为上游数据商、我们开发的业务系统、C 端 app（95e）三部分
- 当前团队主要关注中间这一层业务系统
- 当前文档建设重点是推送组
- `market-server` 只是整个系统中的一个服务组，不是整个系统本体

## 使用原则

1. 所有内容都要直接服务于 AI 的接管能力。
2. 优先写能帮助快速定位、快速设计、快速排障的文档。
3. 先系统，后服务，最后案例。
4. 如果某份文档不能明显降低后续协作成本，就不是优先项。

## 后续扩展方向

后续继续补充时，优先顺序建议为：

1. 完善系统服务地图
2. 完善系统级核心链路
3. 完善 `market-server` 服务组总览
4. 补充服务职责文档
5. 补充关键业务流程文档
6. 沉淀真实需求与排障案例
