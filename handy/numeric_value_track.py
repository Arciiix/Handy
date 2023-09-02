from datetime import datetime, timedelta
import cv2


from action import Action
from action_context import ActionContext
from config import CONFIG
from frame import handle_frame
from logger import logger
from video_feed import Streamer


async def numeric_value_track(
    action: Action, cap: Streamer, ctx: ActionContext, holistic, model
):
    """
    Some of the actions, like changing volume, have to know the numeric value of change.
    This function tracks user positions as long as they're in the ROI.
    If user raises their right arm, the value increases by 1
    If user raises their left arm, the value decreases by 1
    If user raises both their right and left arm or leaves the viewport, the value is submitted
    """
    last_processing_time = datetime.now()

    last_time_arm_was_raised = datetime.now()

    # Get initial volume value
    if action.init_value_getter is not None:
        ctx.numeric_value, domain = await action.init_value_getter(ctx)
        if ctx.numeric_value is None:
            logger.error("Numeric value is None at start")
            return None
        if domain is not None:
            ctx.domain = domain
    else:
        # If there's no getter, set this to the minimum
        ctx.numeric_value = action.numeric_value_range[0]

    logger.info(f"Set initial numeric value to {ctx.numeric_value}")
    while True:
        frame = cap.get_processed_frame()

        # Limit the processing to the FPS
        if datetime.now() - last_processing_time < timedelta(
            milliseconds=1000 / CONFIG.fps
        ):
            continue
        last_processing_time = datetime.now()

        # In case of empty frame
        if frame is None:
            logger.warning("Frame empty")
            continue

        angles, _, _ = handle_frame(frame, holistic, model, dont_predict_pose=True)

        """
        (from train/angles.png)
        Right arm = angle 3 is higher
        Left arm = angle 2 is higher
        """

        # The minimum angle to consider the arm to be raised
        min_angle = CONFIG.min_arm_angle_for_numeric_value_change

        if CONFIG.is_dev:
            if angles is not None:
                logger.debug(f"Angles: {','.join([str(a) for a in angles])}")
            else:
                logger.debug("Angles are none")

        if (
            angles is None
            or (angles[3] > min_angle and angles[2] > min_angle)
            or (datetime.now() - last_time_arm_was_raised)
            > CONFIG.numeric_value_max_waiting_time
        ):
            # It means user is not in ROI anymore, raised both their arms, or didn't raise neither of them
            logger.info("Quitting numeric value")

            if CONFIG.is_dev:
                logger.debug("Conditions:")
                logger.debug(f"Angles is none: {str(angles is None)}")
                if angles is not None:
                    logger.debug(
                        f"Both hands: {str(angles[3] > min_angle and angles[2] > min_angle)}"
                    )
                logger.debug(
                    f"Time limit reached: {str((datetime.now() - last_time_arm_was_raised) > CONFIG.numeric_value_max_waiting_time)}"
                )
            break
        else:
            # Limit the value update to the value set by user
            if (
                datetime.now() - last_time_arm_was_raised
                >= CONFIG.get_numeric_value_interval
            ):
                if angles[2] > min_angle:
                    last_time_arm_was_raised = datetime.now()

                    # Add the numeric value but also remember about the maximum value (from range)
                    ctx.numeric_value = min(
                        ctx.numeric_value + action.numeric_value_multiplier,
                        action.numeric_value_range[1],
                    )
                    logger.debug(f"Right arm - value add = {ctx.numeric_value}")

                    await action.handler(ctx)

                elif angles[3] > min_angle:
                    last_time_arm_was_raised = datetime.now()

                    # Subtract the numeric value but also remember about the minimum value (from range)
                    ctx.numeric_value = max(
                        ctx.numeric_value - action.numeric_value_multiplier,
                        action.numeric_value_range[0],
                    )
                    logger.debug(f"Left arm - value subtract = {ctx.numeric_value}")

                    await action.handler(ctx)

        if CONFIG.is_dev and cv2.waitKey(1) & 0xFF == ord("q"):
            break

    logger.info(f"Final numeric value {ctx.numeric_value}")
    return ctx.numeric_value
