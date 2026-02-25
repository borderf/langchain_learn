from langchain.chat_models import init_chat_model
from app.config import settings
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools.arxiv.tool import ArxivQueryRun

class ResearchAgentService:
    """研究助手Agent服务"""
    def __init__(self):
        self.agent = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """初始化研究助手Agent"""
        # 初始化模型
        llm = init_chat_model(
            model=settings.model,
            temperature=settings.agent_temperature,
            max_tokens=settings.agent_max_tokens,
            timeout=None,
            max_retries=2,
            api_key=settings.api_key,
            base_url=settings.base_url,
        )

        # 2. 加载工具（保持原样）
        tools = [ArxivQueryRun()]
        
        # 3. 创建Agent
        system_prompt = """你是一个专业的研究助手，专门帮助用户查找、理解和总结学术论文。
        你可以使用以下工具：
        1. arxiv - 在arXiv上搜索和获取学术论文
        
        请按照以下步骤帮助用户：
        1. 理解用户的研究需求
        2. 使用合适的工具搜索相关论文
        3. 提供论文的关键信息：标题、作者、摘要、关键贡献
        4. 如果用户要求，可以提供论文的详细总结
        5. 保持回答专业、准确、有用
        
        **重要提示**：
        - 优先搜索最近2-3年的论文
        - 使用具体的搜索词，避免过于宽泛的查询
        - 最多搜索2-3次，避免过多API调用
        
        记住：始终用中文回答，除非用户特别要求使用其他语言。
        """
        
        self.agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=system_prompt
        )
        
        logger.info("Agent初始化成功")

    # async def process_message()
