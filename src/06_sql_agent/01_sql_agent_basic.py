"""
SQL agent
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent

load_dotenv()

# 定义使用的模型
model = init_chat_model(
    model="openai:Qwen/Qwen3-8B",
    temperature=0.1,
)

# 连接数据库
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
print(f"Dialect: {db.dialect}")
print(f"Available tables: {db.get_usable_table_names()}")
print(f'Sample output: {db.run("SELECT * FROM Artist LIMIT 5;")}')

# 使用SQLDatabase工具箱来和数据库交互
toolkit = SQLDatabaseToolkit(db=db, llm=model)
# 获取工具箱中可以使用的工具
tools = toolkit.get_tools()
for tool in tools:
    print(f"可用的工具：{tool.name}: {tool.description}")

# 开始定义agent
# 提示词
system_prompt = """
您是一个用于与SQL数据库交互的智能体。
给定一个输入问题，首先创建一个语法正确的{dialect}查询语句，然后查看查询结果并返回答案。除非用户明确指定他们希望获取的具体示例数量，否则始终将查询结果限制在最多{top_k}条。
您可以通过相关列对结果进行排序，以返回数据库中最有意义的示例。永远不要查询特定表的所有列，只询问与问题相关的列。
在执行查询之前，您必须仔细检查查询语句。如果在执行查询时出现错误，请重新编写查询并重试。
不要对数据库执行任何DML语句（INSERT、UPDATE、DELETE、DROP等）。
开始时，您应该始终先查看数据库中的表，以了解可以查询什么。不要跳过此步骤。
然后您应该查询最相关表的模式结构。
""".format(
    dialect=db.dialect,
    top_k=5,
)

agent = create_agent(
    model=model,
    system_prompt=system_prompt,
    tools=tools,
)

question = "哪个流派的曲目平均长度最长？"

for step in agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
):
    step["messages"][-1].pretty_print()
