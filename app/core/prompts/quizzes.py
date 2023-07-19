from app.core.config import settings


class QuizPrompt:
    @classmethod
    def make_prompt(cls, artist: str) -> str:
        base_prompts = settings.BASE_QUIZ_PROMPT
        system_prompt = cls._get_system()
        user_prompt = cls._get_user(base_prompts, artist)
        assistant_prompt = cls._get_assistant(base_prompts, artist)
        return [system_prompt, user_prompt, assistant_prompt]

    @classmethod
    def _get_system(cls) -> dict:
        return {"role": "system", "content": "you are a kpop quiz creator"}

    @classmethod
    def _get_user(cls, base_prompts: list, artist: str) -> dict:
        return {"role": "user", "content": base_prompts[0].replace("blank_1", artist)}

    @classmethod
    def _get_assistant(cls, base_prompts: list, artist: str) -> dict:
        return {
            "role": "assistant",
            "content": base_prompts[1].replace("blank_1", artist),
        }
