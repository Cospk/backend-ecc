# backend-ecc Profiles 说明

## 一、Profiles 的作用

backend-ecc 通过 profile 控制安装范围。

profile 的目标不是让用户自由拼装所有模块，而是提供几组明确、稳定、可解释的能力组合。

当前 profile 设计原则：

- 少量预定义组合
- 语义清晰
- 与实际使用场景对应
- 不为未来假设需求过度抽象

---

## 二、当前可用 Profiles

### 1. `minimal`

`minimal` 是最小可用 profile，适合：

- 初次试装
- 轻量 Go 项目
- 想先验证 backend-ecc 是否符合自己的开发习惯

#### 当前包含

##### Commands
- 无

##### Agents
- 无

##### Skills
- `market-add-sports`

##### Rules
- 无

##### Hooks
- 无

#### 特点
- 面最小
- 安装结果最轻
- 适合验证 install / discoverability / 最小行为链

---

### 2. `backend-go`

`backend-go` 是默认 profile，适合：

- 日常 Go 后端开发
- 真实项目中的主工作流
- 需要完整 Go 后端闭环的人

#### 当前包含

##### Commands
- 无

##### Agents
- 无

##### Skills
- `market-add-sports`
- `market-game-conf`

##### Rules
- 无

##### Hooks
- 无

#### 特点
- 覆盖最完整的 Go 后端开发闭环
- 当前推荐默认 profile
- 也是 backend-ecc 当前最值得验证和使用的 profile
- 相比 `minimal`，额外包含 `market-game-conf` 这类 `market-server` 专项整理 skill

---

### 3. `author`

`author` 是维护者 profile，适合：

- backend-ecc 自身开发者
- 维护安装器、文档、adapter、profile 的人

#### 当前包含
- 继承 `backend-go`
- 额外包括：
  - `docs`
  - `install`
  - `adapters`
  - `profiles`
  - `hooks/templates`

#### 特点
- 不面向普通使用者
- 面向生态维护工作
- 更适合开发和调试 backend-ecc 本身

---

## 三、如何选择

### 如果你是第一次使用
推荐从：
- `minimal`
开始

### 如果你已经确定要在 Go 后端项目里实际使用
推荐直接使用：
- `backend-go`

### 如果你要维护 backend-ecc 本身
使用：
- `author`

---

## 四、当前不建议做的事

当前不建议：

- 增加过多 profile
- 做高度自由组合式 profile
- 为未来假设场景提前设计 profile

原因：
- profile 太多会让仓库重新走向复杂化
- 当前 backend-ecc 仍处于 v0.1，清晰比灵活更重要

---

## 五、后续可能的演进方向

未来如果 backend-ecc 在真实使用中稳定成立，可能会考虑新增：

- 更轻的 review-only profile
- 更偏验证链的 profile
- 面向不同团队开发习惯的 profile

但这些都应基于真实使用反馈，而不是预先设计。
