/**
 * Last-reel lane door. Closed stills cover the slot; the open still is the
 * swung leaf used when SUPER scatter / DIG UP unlocks the grave lane.
 */
export const LANE_DOOR_CLOSED_ASSET = 'laneDoorClosed';
export const LANE_DOOR_CLOSED_SMALL_ASSET = 'laneDoorClosedSmall';
export const LANE_DOOR_OPEN_ASSET = 'laneDoorOpenSuper';
export const LANE_DOOR_OPEN_MS = 562;
export const LANE_DOOR_CLOSE_MS = 320;
export const LANE_DOOR_COVER_SCALE_X = 1.28;
/** Same box as the working lid — translate only, never squash the art. */
export const LANE_DOOR_SHIFT_Y = -3;
/** Lane layer above the board. The sliding gold card is under the lid. */
export const LANE_DOOR_Z = 12;
export const LANE_CARD_Z = 11;

/**
 * board_frame (MAIN_FRAME) is dusty charcoal: sat ~0.18, luma ~41.
 * The Recraft leaf is hot orange (sat ~0.54). Same ColorMatrix family as
 * locked symbols, not a full greyscale.
 */
export const LANE_DOOR_GRADE = { saturate: -0.58, brightness: 0.84 } as const;
