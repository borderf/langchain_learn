"""
没有记忆管理的情况，大模型不会记住之前的问题
"""
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

agent = create_agent(
    model="openai:Qwen/Qwen3-8B"
)
"""
================================ Human Message =================================

给我来一首宋词
================================== Ai Message ==================================

当然可以！以下是一首经典的宋词，出自宋代著名词人——**辛弃疾**的《青玉案·元夕》：

---

**青玉案·元夕**  
辛弃疾

东风夜放花千树，  
更吹落，星如雨。  
宝马雕车香满路。  
凤箫声动，玉壶光转，  
一夜鱼龙舞。

蛾儿雪柳黄金缕，  
笑迎春入，香尘无觅处。  
欲将心事付瑶琴，  
知音少，弦断有谁听？

---

这首词描写了元宵节的热闹景象，也隐含了词人对人生境遇的感慨。上阕写灯会的繁华，下阕转为抒情，表达了词人怀才不遇、孤独寂寞的情感。

如果你想要一首更婉约、写景或写情的宋词，也可以告诉我，我可以为你挑选或创作一首！
"""
results = agent.invoke({"messages": [{"role": "user", "content": "给我来一首宋词"}]})
messages = results["messages"]
for message in messages:
    message.pretty_print()

"""
================================ Human Message =================================

再来一首
================================== Ai Message ==================================

当然可以！你喜欢哪种类型的歌曲？比如流行、古风、民谣、摇滚、R&B 或其他风格？告诉我你的偏好，我来为你创作一首新的歌曲～
"""
# 这时候大模型不会记住上下文的
results = agent.invoke({"messages": [{"role": "user", "content": "再来一首"}]})
messages = results["messages"]
for message in messages:
    message.pretty_print()
