from AI_ASSISTANTS_AUTOGEN_SETUP import config_list
from autogen import AssistantAgent, ConversableAgent
from autogen import GroupChat, GroupChatManager
from autogen.coding import LocalCommandLineCodeExecutor


executor = LocalCommandLineCodeExecutor(
    timeout=60,
    work_dir="coding"
)

code_executor_agent = ConversableAgent(
    name = "code_executor_agent",
    llm_config=False,
    code_execution_config={"executor": executor},
    human_input_mode="NEVER",
    default_auto_reply=
    "Please continue. If everything is done, reply 'TERMINATE'.",
)

code_writer_agent = AssistantAgent(
    name="code_writer_agent",
    llm_config={"config_list": config_list},
    code_execution_config=False,
    human_input_mode="NEVER",
)


code_writer_agent_system_message = code_writer_agent.system_message


code_rewiew_agent = ConversableAgent(
    name="code_rewiew_agent",
    llm_config={"config_list": config_list},
    system_message="You are a code rewiew agent, your job is to rewiew written code and make shure thet it uses correct libraries and cslls their functions correctly.",
    code_execution_config=False,
    human_input_mode="NEVER",
)


groupchat = GroupChat(
    agents=[code_writer_agent, code_executor_agent, code_rewiew_agent],
    messages=[],
)

manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})


message = """Напиши мне json код для n8n диаграммы которая решает описанный мной бизнес-процесс, посмотри на BPMN диаграмму и используй
ёё как основу для твоего кода"""
chat_result = code_writer_agent.initiate_chat(
    manager,
    message=message,
)