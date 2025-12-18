"""
通过agent的状态图来理解checkpointer，表现形式就是一个存储
checkpointer：检查点管理器
checkpoint：检查点，状态图的在某一步骤的状态总体快照
thread_id：管理状态点
作用：记忆管理、时间旅行（time travel）、暂停（pause，human-in-the-loop）、容错
"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver  # checkpointer

from langchain_core.runnables import RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from operator import add


# 状态图：整个状态图的状态
class State(TypedDict):
    foo: str
    # 追加的列表
    bar: Annotated[list[str], add]


# 定义节点a
def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}


# 定义节点b
def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}


# 构建状态图，并且指定状态图使用什么数据结构描述状态信息
workflow = StateGraph(State)
# 添加节点
workflow.add_node(node_a)
workflow.add_node(node_b)
# 添加边，边是有方向的，起始，终止
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

# 检查点管理器
checkpointer = InMemorySaver()

# 将定义编译成可运行的图，编译时关联到检查点管理器
graph = workflow.compile(checkpointer=checkpointer)

# 配置
config: RunnableConfig = {
    "configurable": {"thread_id": "1"},
}

# 运行
results = graph.invoke({"foo": ""}, config=config)
print(results)
# {'foo': 'b', 'bar': ['a', 'b']}

# 状态查看
print(graph.get_state(config))
# StateSnapshot(values={'foo': 'b', 'bar': ['a', 'b']},
# next=(),
# config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0dc132-5a90-64e3-8002-c7ef608d1cf9'}},
# metadata={'source': 'loop', 'step': 2, 'parents': {}},
# created_at='2025-12-18T13:12:04.280854+00:00',
# parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0dc132-5a8c-69b9-8001-5d2b4dacd312'}}, tasks=(), interrupts=())

# 查看检查点
for checkpoint_tuple in checkpointer.list(config):
    print("*" * 28)
    print(checkpoint_tuple)
#     CheckpointTuple(config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0dc138-b2f1-6c9a-8002-3bd6e7adabba'}},
#     checkpoint={'v': 4, 'ts': '2025-12-18T13:14:54.609525+00:00', 'id': '1f0dc138-b2f1-6c9a-8002-3bd6e7adabba',
#     'channel_versions':
#       {'__start__': '00000000000000000000000000000002.0.7968696097629369', 'foo': '00000000000000000000000000000004.0.5227045507265191', 'branch:to:node_a': '00000000000000000000000000000003.0.4432628222723163', 'bar': '00000000000000000000000000000004.0.5227045507265191', 'branch:to:node_b': '00000000000000000000000000000004.0.5227045507265191'},
#       'versions_seen':
#           {'__input__': {},
#           '__start__': {'__start__': '00000000000000000000000000000001.0.4297477828884003'},
#           'node_a': {'branch:to:node_a': '00000000000000000000000000000002.0.7968696097629369'},
#           'node_b': {'branch:to:node_b': '00000000000000000000000000000003.0.4432628222723163'}},
#           'updated_channels': ['bar', 'foo'],
#           'channel_values': {'foo': 'b', 'bar': ['a', 'b']}},
#          metadata={'source': 'loop', 'step': 2, 'parents': {}},
#          parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0dc138-b2ef-658d-8001-e39370f6592a'}},
#          pending_writes=[])
