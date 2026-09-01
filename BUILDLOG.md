# Build Log

## Phase 1

### Where AI helped
- Claude helped design the batch processing script with filename-based skip logic
- Claude explained the fix for duplicate entries caused by os.listdir() ordering

### Where AI was wrong
- Claude initially suggested gemini-2.0-flash model name which was incorrect for our setup

### What I changed
- Switched to correct Gemini model name that actually worked
- Fixed skip logic from count-based to filename-based tracking
- Manually removed duplicate entries from image_analysis.json before re-running

## Phase 2
_to be filled_

## Phase 3
_to be filled_

## Phase 4
_to be filled_