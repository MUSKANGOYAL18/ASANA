import logging
import random

logger = logging.getLogger(__name__)

try:
    import openai
except ImportError:
    openai = None


class LLMGenerator:
    """
    Optional LLM-based generator.
    Falls back to deterministic template-based generation if OpenAI is unavailable.
    """

    def __init__(self, model=None, temperature=0.7):
        self.model = model
        self.temperature = temperature
        self.rng = random.Random(42)

        if openai is None:
            logger.warning("OpenAI not available. Using fallback text generation.")

    # -------- TASK NAME --------
    def generate_task_name(self, project_type, workflow_type, context=None) -> str:
        """
        Generate a realistic task name.
        Fallback version (no OpenAI).
        """
        verbs = [
            "Implement", "Fix", "Review", "Design", "Update",
            "Analyze", "Prepare", "Launch", "Refactor", "Document"
        ]

        objects = [
            "API", "dashboard", "workflow", "campaign",
            "feature", "pipeline", "report", "integration"
        ]

        return f"{self.rng.choice(verbs)} {self.rng.choice(objects)}"

    # -------- TASK DESCRIPTION --------
    def generate_task_description(self, project_type, workflow_type, context=None) -> str:
        """
        Generate a task description.
        """
        return (
            "This task was generated using a fallback template.\n\n"
            "- Review requirements\n"
            "- Implement changes\n"
            "- Validate results\n"
        )

    # -------- COMMENT TEXT --------
    def generate_comment(self, context=None) -> str:
        """
        Generate a realistic comment.
        """
        comments = [
            "Working on this now.",
            "This is blocked pending review.",
            "Changes are ready for QA.",
            "Can someone please confirm the requirements?",
            "This should be completed by EOD."
        ]
        return self.rng.choice(comments)
