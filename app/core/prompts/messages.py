from app.schemas.messages import MessageRequest
from app.core.config import settings


class MessageBotPrompt:
    @classmethod
    def make_prompt(cls, params: MessageRequest) -> str:
        base_prompts = settings.BASE_MESSAGE_PROMPT
        system_prompt = cls._get_system()
        user_prompt = cls._get_user(base_prompts, params)
        assistant_prompt = cls._get_assistant(base_prompts)
        return [system_prompt, user_prompt, assistant_prompt]

    @classmethod
    def _get_system(cls):
        return {"role": "system", "content": "You are a message creator."}

    @classmethod
    def _get_user(cls, base_prompts: list, params: MessageRequest) -> dict:
        user_prompt_dict = {
            "0": base_prompts[0],
            "1": f"{base_prompts[1]} {params.relation}. {params.name} {settings.NAME_PROMPT} Remember {params.name} is the recipient of the message.!"  # noqa: E501
            if params.name
            else f"{base_prompts[1]} {params.relation} Remember {params.relation} is the recipient of the message.!",
            "2": f"{base_prompts[2]} {params.reason}",
            "3": f"{base_prompts[3]} {params.manner}",
            "4": f"{base_prompts[4]} {params.max_length}",
            "5": f"{base_prompts[5]}",
            "6": f"{base_prompts[6]}",
        }
        results = ""
        for value in user_prompt_dict.values():
            results += f"{value} "
        return {"role": "user", "content": results}

    @classmethod
    def _get_assistant(cls, base_prompts: list):
        return {"role": "assistant", "content": base_prompts[7]}
