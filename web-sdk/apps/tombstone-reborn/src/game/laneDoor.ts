/**
 * Frame contract for the last-reel lane door (tools/make_lane_door_atlas.py).
 * Closed face is frame 0; the last frame is the door edge-on after the swing.
 * One transform for every frame: the shared canvas fills the last-reel slot.
 */
export const LANE_DOOR_ASSET = 'laneDoor';
export const LANE_DOOR_FRAME_COUNT = 16;
export const LANE_DOOR_FPS = 16;
export const LANE_DOOR_OPEN_MS = (LANE_DOOR_FRAME_COUNT / LANE_DOOR_FPS) * 1000;
/**
 * Close slam: not the full reverse. These poses swing it back in,
 * last one is the impact. Hold frame 0 after.
 */
export const LANE_DOOR_CLOSE_SLAM = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] as const;
export const LANE_DOOR_CLOSE_MS = 320;
export const LANE_DOOR_COVER_SCALE_X = 1.28;
export const LANE_DOOR_COVER_SCALE_Y = 1.16;
