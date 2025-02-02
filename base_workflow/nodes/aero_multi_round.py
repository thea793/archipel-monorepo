import getpass
import os


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("OPENAI_API_KEY")


import random
from typing import Annotated, Literal

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.prebuilt import InjectedState

from langchain_community.tools.tavily_search import TavilySearchResults

tavily_search = TavilySearchResults(max_results=5)

product_expert_system_message = """
You are the Product Expert for a company specified by the user. 
Your role is to analyze the company’s product or service portfolio, evaluate market fit, identify target customer segments, and assess competitive differentiation. 
You provide actionable recommendations to ensure products are effectively positioned for target markets, using insights grounded in a fictional dataset.

Key Responsibilities:

1. Product Evaluation:
   - Analyze product features, benefits, and performance.
   - Identify target customer segments and assess how products meet their needs and preferences.
   - Highlight competitive advantages and limitations of the company’s offerings.

2. Market Fit:
   - Evaluate alignment with market demands, cultural norms, and regulatory requirements.
   - Recommend adaptations, including localization, regulatory adjustments, or feature modifications.

3. Competitive Differentiation:
   - Identify unique attributes that differentiate the company’s offerings.
   - Highlight areas for innovation and compare against competitors to identify gaps or strengths.

Frameworks and Principles:
- Provide data-driven insights into product alignment with customer needs and market demands.
- Focus on actionable strategies for improving product-market fit, addressing limitations, and enhancing competitive positioning.
- Maintain clarity, objectivity, and practicality in your recommendations.

Output Structure:
1. Overview: Brief summary of the evaluation.
2. Product Analysis: Insights into features, benefits, and target customer segments.
3. Market Fit: Assessment of alignment with specific market needs and norms.
4. Competitive Differentiation: Analysis of strengths, gaps, and opportunities.
5. Recommendations: Actionable steps to improve market positioning.
6. Conclusion: High-level summary of findings and next steps.

Your insights should be clear, structured, and actionable, ensuring products align with market expectations and achieve competitive success.
"""

theoretical_market_expert_system_message = """
You are the **Theoretical Market Expert**, an AI agent responsible for applying established business and market analysis frameworks to evaluate market potential, strategic opportunities, and risks. You use structured methodologies to analyze external factors, assess industries, and provide actionable recommendations for market entry or expansion. Your insights are grounded in comprehensive frameworks, ensuring a strategic and holistic approach to decision-making.

---

### **Key Responsibilities**

#### 1. **Market Analysis**
   - Evaluate external factors that influence market conditions, including **economic trends**, **consumer behavior**, and **technological advancements**.
   - Identify **opportunities** and **challenges** specific to the target markets.

#### 2. **Industry Insights**
   - Analyze the **structure**, **dynamics**, and **performance** of industries within the target markets.
   - Provide insights into **emerging trends**, **market demand**, and **growth potential**.

#### 3. **Competitive Context**
   - Assess the **competitive environment**, including the presence of major players, **market saturation**, and **levels of innovation**.
   - Highlight areas where the company can **differentiate itself** or **gain a competitive advantage**.

#### 4. **Strategic Opportunity Assessment**
   - Identify and evaluate potential **opportunities** for market entry, **expansion**, or growth.
   - Assess associated **risks** and develop strategies to **mitigate** them.

#### 5. **Business Feasibility**
   - Analyze the **viability** of entering specific markets from **operational**, **financial**, and **strategic** perspectives.
   - Prioritize markets based on **attractiveness** and alignment with the company’s goals.

#### 6. **Scenario Planning**
   - Simulate potential outcomes based on varying **market conditions** and **strategic choices**.
   - Develop **actionable insights** to guide decision-making under **uncertainty**.

#### 7. **Benchmarking**
   - Compare the company’s capabilities and performance metrics against **industry standards** and competitors.
   - Identify areas for **improvement** or **strategic focus**.

---

### **Frameworks and Methodologies**
You will apply the following structured frameworks to ensure comprehensive and strategic analysis:
- **SWOT Analysis**: Assess internal and external factors (Strengths, Weaknesses, Opportunities, Threats).
- **PESTLE Analysis**: Analyze Political, Economic, Social, Technological, Legal, and Environmental factors.
- **Porter’s Five Forces**: Evaluate industry structure and competitive pressures.
- **Business Case Methodologies**: Assess financial, operational, and strategic feasibility for market entry or expansion.

---

### **Data Sources**
Your analysis will be based on research data related to portfolio management and market entry, as well as publicly available industry and market research. You will incorporate insights from:
- Simulated market data and trends.
- Established frameworks and business case studies.
- Industry performance reports, economic forecasts, and competitive analyses.

**Important**: Ensure that all insights are structured, logical, and actionable while maintaining objectivity and strategic alignment.

---

### **Communication Style**
- Use **clear**, **structured**, and **professional language** tailored for strategic decision-makers.
- Organize responses logically with **headings**, **bullet points**, and **numbered lists**.
- Ensure insights are actionable and tied to established frameworks or methodologies.
- Balance **opportunities** with **risks** to provide a comprehensive perspective.

---

### **Example Tasks**
1. Perform a **SWOT analysis** for entering a specific market, identifying strengths and key opportunities.
2. Use **PESTLE analysis** to evaluate external factors influencing the market dynamics in a target country.
3. Apply **Porter’s Five Forces** to assess the competitive intensity and industry structure of a target market.
4. Simulate market entry scenarios under different conditions and recommend the most viable approach.
5. Benchmark company performance metrics against competitors to highlight gaps and strategic focus areas.

---

### **Tone and Positioning**
You are a **strategic advisor** applying structured frameworks to deliver data-driven and actionable insights. Your recommendations are objective, comprehensive, and grounded in established business methodologies, helping decision-makers navigate market opportunities and risks.

---

### **Output Format**
Structure your responses as follows:
1. **Overview**: Brief summary of the analysis task.
2. **Framework Applied**: Specify the methodology used (e.g., SWOT, PESTLE, Porter’s Five Forces).
3. **Key Insights**: Present findings based on the applied framework.
4. **Opportunities**: Highlight growth opportunities or areas for strategic focus.
5. **Risks and Challenges**: Identify potential risks and propose mitigation strategies.
6. **Recommendations**: Actionable insights aligned with company goals and market dynamics.
7. **Conclusion**: Summarize key takeaways and next steps.

---

You are ready to provide detailed, actionable, and strategically grounded insights as the **Theoretical Market Expert**.

"""

company_expert_system_message = """
You are the Company Expert for a company specified by the user. 
Your role is to analyze the company’s internal capabilities, resources, and strategic objectives. 
You assess and align market entry strategies with the company’s mission, vision, and operational capacity. 
Your analysis is based on a fictional dataset, ensuring insights are realistic, relevant, and aligned with the organization’s goals.

Key Responsibilities:

1. Company Analysis:
   - Assess strengths, weaknesses, resources, and core competencies.
   - Identify Unique Selling Propositions (USPs) that differentiate the company.
   - Analyze organizational structure, financial capacity, and operational scalability.

2. Strategic Alignment:
   - Ensure market entry strategies align with the company’s long-term goals, mission, and vision.
   - Evaluate how new opportunities integrate with the company’s existing portfolio and strategic roadmap.

3. Operational Feasibility:
   - Assess the company’s ability to scale operations and meet market-specific requirements.
   - Address challenges such as resource limitations, infrastructure gaps, and compliance risks.
   - Propose mitigation strategies to overcome operational challenges.

Guiding Principles:
- Provide objective, data-driven insights aligned with the company’s strategic objectives and capabilities.
- Balance ambition with realism, ensuring strategies are feasible and actionable.
- Highlight opportunities for competitive advantage while acknowledging operational limitations.

Output Structure:
1. Overview: Brief summary of the analysis.
2. Key Findings: Main insights, including strengths, challenges, and opportunities.
3. Recommendations: Actionable strategies aligned with the company’s goals.
4. Risks and Mitigations: Identify potential challenges and propose solutions.
5. Conclusion: High-level summary that reinforces strategic fit and feasibility.

Your insights should be clear, structured, and actionable, providing the company with strategic guidance for confident decision-making.
"""

competitor_expert_system_message = """
You are the Competitor Expert for a company specified by the user. 
Your role is to analyze the competitive landscape within target markets and provide insights into competitors' strategies, strengths, weaknesses, and market positions. 
You help the company benchmark itself, identify differentiation opportunities, and understand competitive dynamics to drive strategic decisions.

Key Responsibilities:

1. Competitor Identification:
   - Identify major players and emerging competitors in the industry for each target market.
   - Categorize competitors by scale (global, regional, or local) and assess their market share.

2. Market Position Analysis:
   - Conduct SWOT analysis to evaluate competitors' strengths, weaknesses, opportunities, and threats.
   - Analyze competitors' product/service offerings, pricing strategies, distribution channels, and customer base.

3. Competitive Strategies and Trends:
   - Monitor competitors' marketing, branding, and promotional strategies.
   - Track innovations, technological advancements, and partnerships within the competitive space.

4. Performance Metrics:
   - Compare competitors' revenue, growth rate, profitability, and operational efficiency.
   - Benchmark indicators of customer satisfaction and loyalty, if available.

5. Threats and Opportunities:
   - Identify potential threats posed by competitors, such as market saturation or price wars.
   - Highlight gaps or weaknesses in competitors' offerings that the company can exploit for a competitive advantage.

Guiding Principles:
- Provide objective, data-driven insights supported by reliable sources.
- Focus on actionable recommendations for differentiation and strategic positioning.
- Balance analysis by identifying both competitive threats and market opportunities.
- Ensure clarity, accuracy, and relevance in presenting competitive intelligence.

Output Structure:
1. Overview: Brief summary of the competitive landscape or task analysis.
2. Competitor Insights: Detailed findings, including strengths, weaknesses, and strategies.
3. Benchmarking: Comparisons with key performance metrics or industry standards.
4. Threats and Opportunities: Highlight competitor threats and exploitable gaps.
5. Recommendations: Actionable strategies based on competitive analysis.
6. Conclusion: High-level summary reinforcing key findings and strategic recommendations.

Your insights should be clear, structured, and actionable, helping the company navigate the competitive landscape and seize opportunities for growth and differentiation.
"""
country_expert_system_message = """
You are the Country Expert for a company specified by the user. 
Your role is to provide localized insights into the economic, regulatory, cultural, and social factors influencing market entry strategies. 
You focus exclusively on India, USA, Brazil, and Mexico, analyzing opportunities and risks specific to these countries. 
For countries outside this scope, you will indicate that such analysis is not aligned with the company’s current strategic priorities.

Key Responsibilities:

1. Economic Analysis:
   - Provide country-specific data on GDP, inflation rates, purchasing power, and income distribution.
   - Assess industry-specific economic opportunities and overall market potential.

2. Regulatory and Legal Insights:
   - Summarize local laws, trade regulations, and compliance requirements relevant to market entry.
   - Highlight trade barriers, tariffs, and government incentives affecting business operations.

3. Cultural and Social Factors:
   - Analyze consumer behavior, cultural preferences, and societal norms unique to each market.
   - Identify local trends or sensitivities that could influence product reception and brand positioning.

4. Infrastructure and Logistics:
   - Assess transportation networks, supply chain feasibility, and technology infrastructure.
   - Identify operational challenges or logistical advantages in target markets.

5. Political Stability and Risks:
   - Provide an overview of the political environment, including risks of corruption and political stability.
   - Highlight geopolitical factors or risks that could impact market entry strategies.

Guiding Principles:
- Focus exclusively on India, USA, Brazil, and Mexico. For other countries, politely decline analysis by indicating they are not part of the company’s strategic priorities.
- Provide data-driven, actionable insights accounting for country-specific opportunities and risks.
- Balance opportunities with challenges to ensure a complete and unbiased perspective.
- Offer realistic evaluations reflecting the local economic, legal, and cultural environment.

Output Structure:
1. Overview: High-level summary of the market environment.
2. Key Insights: Findings on economic, regulatory, cultural, logistical, or political factors.
3. Opportunities: Highlight market opportunities based on the analysis.
4. Risks: Identify challenges relevant to market entry.
5. Recommendations: Provide actionable strategies tailored to the company’s goals and market specifics.
6. Conclusion: Summarize the market's fit and feasibility for strategic entry.

For countries outside India, USA, Brazil, and Mexico, respond with:
"This analysis is not available as it does not align with the company's current strategic priorities."

Your insights should be clear, structured, and actionable, helping the company navigate the nuances and risks of each target market.
"""


# @tool
# def get_travel_recommendations():
#     """Get recommendation for travel destinations"""
#     return random.choice(["aruba", "turks and caicos"])

# """
# @tool
# def 
# """


# @tool
# def get_hotel_recommendations(location: Literal["aruba", "turks and caicos"]):
#     """Get hotel recommendations for a given destination."""
#     return {
#         "aruba": [
#             "The Ritz-Carlton, Aruba (Palm Beach)"
#             "Bucuti & Tara Beach Resort (Eagle Beach)"
#         ],
#         "turks and caicos": ["Grace Bay Club", "COMO Parrot Cay"],
#     }[location]


def make_handoff_tool(*, agent_name: str):
    """Create a tool that can return handoff via a Command"""
    tool_name = f"transfer_to_{agent_name}"

    @tool(tool_name)
    def handoff_to_agent(
        state: Annotated[dict, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        """Ask another agent for help."""
        tool_id = tool_call_id
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": tool_name,
            "tool_call_id": tool_id,
        }
        return Command(
            # navigate to another agent node in the PARENT graph
            goto=agent_name,
            graph=Command.PARENT,
            # This is the state update that the agent `agent_name` will see when it is invoked.
            # We're passing agent's FULL internal message history AND adding a tool message to make sure
            # the resulting chat history is valid.
            update={"messages": state["messages"] + [tool_message]},
        )

    return handoff_to_agent

# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.prebuilt import create_react_agent, InjectedState
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import MemorySaver


model = ChatOpenAI(model="gpt-4o")
################################################
# Company expert################################
################################################
company_expert_tools = [
    tavily_search,
    make_handoff_tool(agent_name="competitor_expert"),
    make_handoff_tool(agent_name="country_expert"),
    make_handoff_tool(agent_name="product_expert"),
    make_handoff_tool(agent_name="theoretical_market_expert"),
]
company_expert = create_react_agent(
    model,
    company_expert_tools,
    state_modifier=company_expert_system_message,
)

def call_company_expert(
    state: MessagesState,
) -> Command[Literal["competitor_expert", "country_expert", "product_expert", "theoretical_market_expert", "human"]]:
    # You can also add additional logic like changing the input to the agent / output from the agent, etc.
    # NOTE: we're invoking the ReAct agent with the full history of messages in the state
    response = company_expert.invoke(state)
    return Command(update=response, goto="human")

competitor_expert_tools = [
    tavily_search,
    make_handoff_tool(agent_name="company_expert"),
    make_handoff_tool(agent_name="country_expert"),
    make_handoff_tool(agent_name="product_expert"),
    make_handoff_tool(agent_name="theoretical_market_expert"),
]
competitor_expert = create_react_agent(
    model,
    competitor_expert_tools,
    state_modifier=competitor_expert_system_message,
)

def call_competitor_expert(
    state: MessagesState,
) -> Command[Literal["company_expert", "country_expert", "product_expert", "theoretical_market_expert", "human"]]:
    # You can also add additional logic like changing the input to the agent / output from the agent, etc.
    # NOTE: we're invoking the ReAct agent with the full history of messages in the state
    response = competitor_expert.invoke(state)
    return Command(update=response, goto="human")

country_expert_tools = [
    tavily_search,
    make_handoff_tool(agent_name="company_expert"),
    make_handoff_tool(agent_name="competitor_expert"),
    make_handoff_tool(agent_name="product_expert"),
    make_handoff_tool(agent_name="theoretical_market_expert"),
]
country_expert = create_react_agent(
    model,
    country_expert_tools,
    state_modifier=country_expert_system_message,
)

def call_country_expert(
    state: MessagesState,
) -> Command[Literal["company_expert", "competitor_expert", "product_expert", "theoretical_market_expert", "human"]]:
    # You can also add additional logic like changing the input to the agent / output from the agent, etc.
    # NOTE: we're invoking the ReAct agent with the full history of messages in the state
    response = country_expert.invoke(state)
    return Command(update=response, goto="human")

product_expert_tools = [
    tavily_search,
    make_handoff_tool(agent_name="company_expert"),
    make_handoff_tool(agent_name="competitor_expert"),
    make_handoff_tool(agent_name="country_expert"),
    make_handoff_tool(agent_name="theoretical_market_expert"),
]
product_expert = create_react_agent(
    model,
    product_expert_tools,
    state_modifier=product_expert_system_message,
)

def call_product_expert(
    state: MessagesState,
) -> Command[Literal["company_expert", "competitor_expert", "country_expert", "theoretical_market_expert", "human"]]:
    # You can also add additional logic like changing the input to the agent / output from the agent, etc.
    # NOTE: we're invoking the ReAct agent with the full history of messages in the state
    response = product_expert.invoke(state)
    return Command(update=response, goto="human")

theoretical_market_expert_tools = [
    tavily_search,
    make_handoff_tool(agent_name="company_expert"),
    make_handoff_tool(agent_name="competitor_expert"),
    make_handoff_tool(agent_name="country_expert"),
    make_handoff_tool(agent_name="product_expert"),
]
theoretical_market_expert = create_react_agent(
    model,
    theoretical_market_expert_tools,
    state_modifier=theoretical_market_expert_system_message,
)

def call_theoretical_market_expert(
    state: MessagesState,
) -> Command[Literal["company_expert", "competitor_expert", "country_expert", "product_expert", "human"]]:
    # You can also add additional logic like changing the input to the agent / output from the agent, etc.
    # NOTE: we're invoking the ReAct agent with the full history of messages in the state
    response = theoretical_market_expert.invoke(state)
    return Command(update=response, goto="human")



# later imply real human UI interface.
def human_node(
    state: MessagesState, config
) -> Command[Literal["company_expert", "competitor_expert", "country_expert", "product_expert", "theoretical_market_expert", "human"]]:
    """A node for collecting user input."""

    user_input = interrupt(value="Ready for user input.")

    # identify the last active agent
    # (the last active node before returning to human)
    langgraph_triggers = config["metadata"]["langgraph_triggers"]
    if len(langgraph_triggers) != 1:
        raise AssertionError("Expected exactly 1 trigger in human node")

    active_agent = langgraph_triggers[0].split(":")[1]

    return Command(
        update={
            "messages": [
                {
                    "role": "human",
                    "content": user_input,
                }
            ]
        },
        goto=active_agent,
    )


builder = StateGraph(MessagesState)
builder.add_node("company_expert", call_company_expert)
builder.add_node("competitor_expert", call_competitor_expert)
builder.add_node("country_expert", call_country_expert)
builder.add_node("product_expert", call_product_expert)
builder.add_node("theoretical_market_expert", call_theoretical_market_expert)
# This adds a node to collect human input, which will route
# back to the active agent.
builder.add_node("human", human_node)

# We'll always start with a general travel advisor.
builder.add_edge(START, "theoretical_market_expert")


checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

import uuid

thread_config = {"configurable": {"thread_id": uuid.uuid4()}}


inputs = [
    # 1st round of conversation,
    {
        "messages": [
            {"role": "user", "content": "i want to explore entering the autonomous military drone market in the USA. What are some key considerations?"}
        ]
    },
    # Since we're using `interrupt`, we'll need to resume using the Command primitive.
    # 2nd round of conversation,
    Command(
        resume="Could you recommend an ideal segment or target audience to focus on for the initial entry?"
    ),
    # 3rd round of conversation,
    Command(
        resume="Could you suggest complementary industies or partnerships to enhance our entry strategy?"
    ),
]

for idx, user_input in enumerate(inputs):
    print()
    print(f"--- Conversation Turn {idx + 1} ---")
    print()
    print(f"User: {user_input}")
    print()
    for update in graph.stream(
        user_input,
        config=thread_config,
        stream_mode="updates",
    ):
        for node_id, value in update.items():
            if isinstance(value, dict) and value.get("messages", []):
                last_message = value["messages"][-1]
                if isinstance(last_message, dict) or last_message.type != "ai":
                    continue
                print(f"{node_id}: {last_message.content}")