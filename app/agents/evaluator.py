"""FinSight AI - Evaluator Agent (LLM-as-a-Judge)"""

from langchain_core.messages import HumanMessage
from app.models.schemas import AgentState
from app.prompts.templates import EVALUATOR_PROMPT
from app.config import get_llm


def evaluator_agent(state: AgentState) -> AgentState:
    """Evaluate the quality of the generated report."""
    report = state.get("report", "")
    logs = state.get("agent_logs", [])
    errors = state.get("errors", [])

    if not report or report.startswith("Error"):
        logs.append("[Evaluator] No valid report to evaluate")
        return {
            **state,
            "evaluation": {"overall": "N/A", "feedback": "No report was generated."},
            "agent_logs": logs, "errors": errors,
        }

    logs.append("[Evaluator] Evaluating report quality (LLM-as-Judge)...")

    try:
        llm = get_llm()
        prompt = EVALUATOR_PROMPT.format(report=report)
        response = llm.invoke([HumanMessage(content=prompt)])
        text = response.content.strip()

        evaluation = {"raw_evaluation": text}

        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("ACCURACY:"):
                evaluation["accuracy"] = line.split(":", 1)[1].strip()
            elif line.startswith("COMPLETENESS:"):
                evaluation["completeness"] = line.split(":", 1)[1].strip()
            elif line.startswith("CLARITY:"):
                evaluation["clarity"] = line.split(":", 1)[1].strip()
            elif line.startswith("USEFULNESS:"):
                evaluation["usefulness"] = line.split(":", 1)[1].strip()
            elif line.startswith("OVERALL:"):
                evaluation["overall"] = line.split(":", 1)[1].strip()
            elif line.startswith("FEEDBACK:"):
                evaluation["feedback"] = line.split(":", 1)[1].strip()

        logs.append(f"[Evaluator] Overall Score: {evaluation.get('overall', 'N/A')}")
        logs.append(f"[Evaluator] Feedback: {evaluation.get('feedback', 'N/A')}")

        return {**state, "evaluation": evaluation, "agent_logs": logs, "errors": errors}

    except Exception as e:
        errors.append(f"[Evaluator] Error: {str(e)}")
        logs.append(f"[Evaluator] Failed: {str(e)}")
        return {
            **state,
            "evaluation": {"overall": "N/A", "feedback": f"Error: {str(e)}"},
            "agent_logs": logs, "errors": errors,
        }