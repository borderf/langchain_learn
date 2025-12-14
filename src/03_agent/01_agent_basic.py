"""
创建agent的基础
"""
from langchain.agents import create_agent
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

agent = create_agent(
    model="openai:Qwen/Qwen3-8B",  # 指定agent使用的LLM，注意使用 模型提供商:模型 的形式
)

# <langgraph.graph.state.CompiledStateGraph object at 0x000002126CE89DF0>
# agent就是编译过的状态图 nodes -> edges
print(agent)

# 目前这个图只有两个节点，一个start，一个model，类型都是 pregel
# pregel：google发布的技术，解决大型图问题的算法结构
# {'__start__': <langgraph.pregel._read.PregelNode object at 0x00000148EA534BC0>,
# 'model': <langgraph.pregel._read.PregelNode object at 0x00000148EA599EE0>}
print(agent.nodes)

# 调用的输入输出都是消息列表
results = agent.invoke({"messages": [{"role": "user", "content": "最近成都的天气怎么样"}]})
# {'messages': [HumanMessage(content='最近成都的天气怎么样', additional_kwargs={}, response_metadata={}, id='c3f45262-1a93-481b-afbc-a3f9e3c142dc'),
# AIMessage(content='截至2024年11月6日，成都的天气情况如下：\n\n- **天气状况**：近日成都总体以多云和阴天为主，偶有小雨，整体气温较为温和，昼夜温差稍大。\n- **气温范围**：白天平均气温在15℃左右，夜间平均气温约为9℃，建议根据天气变化适当增减衣物。\n- **湿度**：空气湿度较高，体感略有闷热，但白天的活动仍较为舒适。\n- **风力**：风力不大，多为微风或静风，空气流通较好。\n- **紫外线**：紫外线指数较低，外出无需特别防晒。\n\n最近几天的天气预报显示，未来几天很可能继续保持这种多云和阴雨交替的状态。如果你有具体的日期或行程安排，我可以帮你提供更详细的天气预报。若需出行建议，也可以告诉我哦！',
# additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 186, 'prompt_tokens': 17, 'total_tokens': 203, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'Qwen/Qwen3-8B', 'system_fingerprint': '', 'id': '019b1d71ee2d8b43328e55551cf06486', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--fea6ba56-7d7c-407b-bd44-f9cfe5ffd3c7-0', usage_metadata={'input_tokens': 17, 'output_tokens': 186, 'total_tokens': 203, 'input_token_details': {}, 'output_token_details': {'reasoning': 0}})]}
print(results)

"""
历史消息: 2 条
================================ Human Message =================================

最近成都的天气怎么样
================================== Ai Message ==================================

截至目前（2024年11月），成都市的天气情况会根据具体日期有所不同。以下是一些近期的天气特征和趋势供你参考：

### 1. **近期天气概况**
- **温度**：成都属于亚热带季风气候，冬季温和，但11月已进入初冬，平均气温通常在 **10°C~20°C** 之间，早晚温差较大，需注意保暖。
- **降水**：11月初成都市可能经历了小雨或阵雨，尤其在周末时段，降雨概率较高。整体降水较往年略少，但局部地区偶有阴雨。
- **湿度**：成都湿度通常较高，尤其在早晨和夜间，可能会感到潮湿。

### 2. **近期天气趋势（以2024年11月中旬为例）**
- **多云为主**：天气以多云为主，偶尔有小雨，整体较为阴凉。
- **寒冷预警**：随着冷空气活动增强，后期可能会有降温，需注意防寒保暖。
- **空气质量**：空气湿度适中，但降雨可能导致局部空气质量下降，需关注实时数据。

### 3. **具体天气预报（示例）**
- **11月25日**：多云，气温12°C~18°C，北风2级。
- **11月26日**：小雨，气温10°C~16°C，东北风3级。
- **11月27日**：多云转晴，气温9°C~17°C，西北风2级。

### 建议：
- 如计划出行，建议提前查看**中国天气网**或**成都气象局**的实时预报。
- 冬季衣物建议准备防风外套、保暖内衣等，以应对早晚温差。
- 雨天出行注意携带雨具，尤其是山区或郊区，可能有较大的雾或湿滑路面。

如果你需要更具体的某一天或某一周的数据，我可以帮你查询详细的天气预报。
"""
messages = results["messages"]
print(f"历史消息: {len(messages)} 条")
for message in messages:
    message.pretty_print()
