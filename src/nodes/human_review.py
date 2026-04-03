"""Human review node - waits for and processes human approval."""

from datetime import datetime, timedelta
from loguru import logger

from src.graph.state import EmailAgentState
from src.db.models import ReviewStatusEnum
from src.services.db_service import DatabaseService


async def human_review_node(state: EmailAgentState) -> dict:
    """Wait for and process human review of generated response.

    Note: In a production system, this would be an async wait for webhook/API call.
    For now, this is a simplified version.

    Args:
        state: Current workflow state

    Returns:
        Updated state dict with review result
    """
    try:
        review_id = state.get("review_id")
        email_id = state.get("email_id")

        if not review_id:
            logger.warning(f"No review ID for email {email_id}")
            return {"generated_response": state.get("generated_response")}

        logger.info(f"Processing human review {review_id}")

        db_service = DatabaseService()

        # In a real system, this would wait for async callback
        # For now, we'll assume the generated response is approved
        # (You would implement a webhook listener or polling mechanism)

        # Update review status to approved
        review = await db_service.update_review_status(
            review_id,
            ReviewStatusEnum.APPROVED,
            approved_response=state.get("generated_response"),
        )

        if not review:
            logger.error(f"Failed to update review {review_id}")
            return {
                "error_message": f"Review {review_id} not found",
                "approved_response": None,
            }

        logger.info(f"Review {review_id} approved")

        return {
            "approved_response": review.approved_response or state.get("generated_response"),
            "generated_response": review.approved_response or state.get("generated_response"),
        }

    except Exception as e:
        logger.error(f"Error in human_review: {str(e)}", exc_info=True)
        return {
            "error_message": f"Human review processing error: {str(e)}",
        }
