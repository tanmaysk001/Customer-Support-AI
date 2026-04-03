"""Review check node - determines if human review is needed."""

from loguru import logger

from src.graph.state import EmailAgentState


async def review_check_node(state: EmailAgentState) -> dict:
    """Determine if email needs human review.

    Args:
        state: Current workflow state

    Returns:
        Updated state dict with review decision
    """
    try:
        category = state.get("category", "other")
        priority = state.get("priority", "medium")
        confidence = state.get("confidence_score", 1.0)
        body = state.get("body", "").lower()

        email_id = state.get("email_id")
        logger.info(f"Checking if review needed for email {email_id}")

        needs_review = False
        review_reason = None

        # Rule 1: Low confidence classification
        if confidence < 0.6:
            needs_review = True
            review_reason = "Low classification confidence"
            logger.debug(f"Low confidence ({confidence}) - flagging for review")

        # Rule 2: Escalated complaints
        if category == "complaint" and priority in ["high", "urgent"]:
            needs_review = True
            review_reason = "Escalated complaint"
            logger.debug("Complaint with high/urgent priority - flagging for review")

        # Rule 3: Critical keywords
        critical_keywords = ["urgent", "fire", "down", "broken", "help", "emergency", "asap", "critical"]
        if any(keyword in body for keyword in critical_keywords):
            needs_review = True
            review_reason = "Critical keywords detected"
            logger.debug(f"Critical keywords found - flagging for review")

        # Rule 4: Uncertain categories
        if category == "other" and confidence < 0.8:
            needs_review = True
            review_reason = "Uncertain category"
            logger.debug("Uncertain category - flagging for review")

        logger.info(f"Review check complete: needs_review={needs_review}, reason={review_reason}")

        return {
            "needs_human_review": needs_review,
            "review_reason": review_reason,
        }

    except Exception as e:
        logger.error(f"Error in review_check: {str(e)}", exc_info=True)
        return {
            "needs_human_review": True,
            "review_reason": f"Review check error: {str(e)}",
        }
