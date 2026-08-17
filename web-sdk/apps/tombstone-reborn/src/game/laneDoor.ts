/**
 * Frame contract for the last-reel lane door (tools/make_lane_door_atlas.py).
 * Closed face is frame 0; the last frame is the door edge-on after the swing.
 * One transform for every frame: the shared canvas fills the last-reel slot.
 * Same box as the saloon door — full pitch, not the card, or the timber
 * shows as a grey strip beside the lid.
 */
export const LANE_DOOR_ASSET = 'laneDoor';
export const LANE_DOOR_FRAME_COUNT = 9;
export const LANE_DOOR_FPS = 16;
export const LANE_DOOR_OPEN_MS = (LANE_DOOR_FRAME_COUNT / LANE_DOOR_FPS) * 1000;
/**
 * Close slam: not the full reverse. These poses swing it back in,
 * last one is the impact. Hold frame 0 after.
 */
export const LANE_DOOR_CLOSE_SLAM = [5, 4, 3, 2, 1, 0] as const;
export const LANE_DOOR_CLOSE_MS = 320;
export const LANE_DOOR_COVER_SCALE_X = 1.28;
/** Same box as the working lid — translate only, never squash the art. */
export const LANE_DOOR_SHIFT_Y = -3;
/** Lane layer above the board. The sliding gold card is under the lid. */
export const LANE_DOOR_Z = 12;
export const LANE_CARD_Z = 11;
/**
 * Recraft door is hot orange (sat ~0.65). Board timber is dusty brown
 * (sat ~0.39). Pull toward that wood grade, not full greyscale.
 */
export const LANE_DOOR_GRADE_SATURATE = -0.58;
export const LANE_DOOR_GRADE_BRIGHTNESS = 0.88;
