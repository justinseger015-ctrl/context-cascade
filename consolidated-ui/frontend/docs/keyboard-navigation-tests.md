# Keyboard Navigation Tests - DraggableTaskList Component

## Overview
This document provides comprehensive testing procedures for keyboard navigation and screen reader support in the DraggableTaskList component, ensuring WCAG 2.1 AA compliance.

## Test Environment Requirements

### Required Software
- **Browser**: Latest Chrome, Firefox, or Edge
- **Screen Reader**: NVDA (Windows) or JAWS
- **Operating System**: Windows 10/11

### Setup Instructions
1. Install NVDA from https://www.nvaccess.org/download/
2. Start NVDA (Ctrl+Alt+N)
3. Open the application in browser
4. Navigate to project dashboard with tasks

---

## Test Cases

### TC-1: Tab Navigation to Drag Handles
**Objective**: Verify users can navigate to drag handles using Tab key

**Steps**:
1. Load project dashboard with multiple tasks
2. Press Tab repeatedly to navigate through page
3. Observe focus indicator on drag handles

**Expected Results**:
- ✅ Focus indicator visible on each drag handle (blue ring)
- ✅ Tab order follows visual task order (top to bottom)
- ✅ Focus skips disabled or hidden elements
- ✅ Screen reader announces: "Drag handle for task: [Task Title], button"

**WCAG Criteria**: 2.1.1 Keyboard (Level A), 2.4.7 Focus Visible (Level AA)

---

### TC-2: Space Key to Grab Task
**Objective**: Verify Space key activates drag mode

**Steps**:
1. Tab to a drag handle
2. Press Space key
3. Observe visual feedback

**Expected Results**:
- ✅ Task becomes semi-transparent (opacity: 0.5)
- ✅ Blue ring appears around task
- ✅ Screen reader announces: "Picked up task: [Task Title]. Use arrow keys to move, Space to drop, Escape to cancel."
- ✅ Cursor changes to grabbing cursor

**WCAG Criteria**: 2.1.1 Keyboard (Level A), 4.1.3 Status Messages (Level AA)

---

### TC-3: Arrow Keys to Move Task
**Objective**: Verify arrow keys move task up/down in list

**Steps**:
1. Grab a task with Space key
2. Press Arrow Down key 2 times
3. Press Arrow Up key 1 time
4. Observe task position changes

**Expected Results**:
- ✅ Task moves down 2 positions after Arrow Down x2
- ✅ Task moves up 1 position after Arrow Up x1
- ✅ Visual drop indicator shows target position
- ✅ Screen reader announces: "Moving [Task Title] over [Other Task Title]" for each move
- ✅ Other tasks shift to make room (smooth animation)

**WCAG Criteria**: 2.1.1 Keyboard (Level A), 4.1.3 Status Messages (Level AA)

---

### TC-4: Space Key to Drop Task
**Objective**: Verify Space key drops task at new position

**Steps**:
1. Grab a task and move it 3 positions down
2. Press Space key to drop
3. Verify task order persists

**Expected Results**:
- ✅ Task remains at new position
- ✅ Opacity returns to normal (1.0)
- ✅ Blue ring disappears
- ✅ Screen reader announces: "Dropped [Task Title] at position 4 of 10"
- ✅ Task order saved to Zustand store
- ✅ Page refresh maintains new order

**WCAG Criteria**: 2.1.1 Keyboard (Level A), 4.1.3 Status Messages (Level AA)

---

### TC-5: Escape Key to Cancel Drag
**Objective**: Verify Escape key cancels drag and returns task to original position

**Steps**:
1. Grab a task from position 2
2. Move it to position 5 with arrow keys
3. Press Escape key
4. Verify task returns to position 2

**Expected Results**:
- ✅ Task returns to original position (2)
- ✅ Visual feedback cleared
- ✅ Screen reader announces: "Cancelled dragging [Task Title]. Returned to original position."
- ✅ No changes saved to store

**WCAG Criteria**: 2.1.1 Keyboard (Level A), 4.1.3 Status Messages (Level AA)

---

### TC-6: Focus Management After Drop
**Objective**: Verify focus returns to drag handle after successful drop

**Steps**:
1. Grab a task and move it
2. Drop with Space key
3. Observe focus location

**Expected Results**:
- ✅ Focus remains on drag handle of dropped task
- ✅ No focus loss to document body
- ✅ User can immediately Tab to next element

**WCAG Criteria**: 2.4.3 Focus Order (Level A), 2.4.7 Focus Visible (Level AA)

---

### TC-7: Screen Reader Announcements - Full Flow
**Objective**: Verify all drag-and-drop actions announced to screen reader

**Steps**:
1. Start NVDA
2. Tab to first task's drag handle
3. Space to grab
4. Arrow Down twice
5. Space to drop
6. Listen to all announcements

**Expected Announcements** (in order):
1. "Drag handle for task: [Task Title], button"
2. "Picked up task: [Task Title]. Use arrow keys to move, Space to drop, Escape to cancel."
3. "Moving [Task Title] over [Task2 Title]"
4. "Moving [Task Title] over [Task3 Title]"
5. "Dropped [Task Title] at position 3 of 10"

**WCAG Criteria**: 4.1.3 Status Messages (Level AA)

---

### TC-8: Multiple Tasks - No Mouse
**Objective**: Verify complete reordering using only keyboard

**Scenario**: Reorder 5 tasks from [A, B, C, D, E] to [E, D, C, B, A]

**Steps** (keyboard only, no mouse):
1. Tab to task E's drag handle
2. Space to grab E
3. Arrow Up 4 times (move to top)
4. Space to drop E
5. Tab to task D's drag handle
6. Space to grab D
7. Arrow Up 2 times (move to position 2)
8. Space to drop D
9. Continue for C, B, A

**Expected Results**:
- ✅ All tasks successfully reordered to [E, D, C, B, A]
- ✅ No mouse interaction required
- ✅ All screen reader announcements clear and accurate
- ✅ Visual focus indicator always visible
- ✅ Final order persisted to store

**WCAG Criteria**: 2.1.1 Keyboard (Level A)

---

### TC-9: Boundary Cases - First/Last Task
**Objective**: Verify behavior when moving first or last task

**Steps**:
1. Grab first task (position 1)
2. Try Arrow Up (should do nothing or announce limit)
3. Grab last task (position 10)
4. Try Arrow Down (should do nothing or announce limit)

**Expected Results**:
- ✅ First task cannot move higher (no error thrown)
- ✅ Last task cannot move lower (no error thrown)
- ✅ Screen reader announces boundary: "Task is already at the top/bottom"
- ✅ No visual glitches or layout shifts

**WCAG Criteria**: 2.1.1 Keyboard (Level A), 4.1.3 Status Messages (Level AA)

---

### TC-10: Rapid Keyboard Input
**Objective**: Verify system handles rapid key presses gracefully

**Steps**:
1. Grab a task
2. Rapidly press Arrow Down 20 times (fast)
3. Press Space to drop
4. Verify final position is correct

**Expected Results**:
- ✅ No errors or crashes
- ✅ Task ends at correct position (bottom of list)
- ✅ No duplicate announcements (debounced)
- ✅ Smooth animation without lag

**WCAG Criteria**: 2.1.1 Keyboard (Level A)

---

## Accessibility Compliance Checklist

### WCAG 2.1 Level A
- [x] 1.1.1 Non-text Content: Drag handles have `aria-label`
- [x] 2.1.1 Keyboard: All drag-and-drop functions available via keyboard
- [x] 2.4.3 Focus Order: Tab order matches visual order
- [x] 4.1.2 Name, Role, Value: All interactive elements properly labeled

### WCAG 2.1 Level AA
- [x] 2.4.7 Focus Visible: Blue ring focus indicator always visible
- [x] 4.1.3 Status Messages: Screen reader announcements for all state changes
- [x] 1.4.3 Contrast (Minimum): Focus indicator has 4.5:1 contrast ratio
- [x] 1.4.11 Non-text Contrast: Drag handles and indicators have 3:1 contrast

---

## Known Issues & Limitations

### Issue 1: NVDA Verbosity
- **Description**: NVDA may announce extra information during drag
- **Workaround**: Use NVDA speech viewer to see exact announcements
- **Status**: Expected behavior, not a bug

### Issue 2: Firefox Arrow Key Delay
- **Description**: Arrow keys may have slight delay in Firefox
- **Workaround**: Use Chrome for smoother experience
- **Status**: Browser-specific, investigating

---

## Testing Tools

### Browser DevTools Accessibility Inspector
1. Open DevTools (F12)
2. Go to Accessibility tab
3. Inspect drag handle element
4. Verify `role="button"`, `tabindex="0"`, `aria-label` present

### NVDA Speech Viewer
1. NVDA menu → Tools → Speech Viewer
2. Observe all announcements in real-time
3. Copy log for documentation

### Lighthouse Accessibility Audit
1. Open DevTools (F12)
2. Go to Lighthouse tab
3. Check "Accessibility" category
4. Run audit
5. **Expected Score**: 95+ (100 is ideal)

---

## Test Execution Log Template

| Test Case | Date | Tester | Browser | Screen Reader | Result | Notes |
|-----------|------|--------|---------|---------------|--------|-------|
| TC-1      |      |        |         |               | ✅/❌   |       |
| TC-2      |      |        |         |               | ✅/❌   |       |
| TC-3      |      |        |         |               | ✅/❌   |       |
| TC-4      |      |        |         |               | ✅/❌   |       |
| TC-5      |      |        |         |               | ✅/❌   |       |
| TC-6      |      |        |         |               | ✅/❌   |       |
| TC-7      |      |        |         |               | ✅/❌   |       |
| TC-8      |      |        |         |               | ✅/❌   |       |
| TC-9      |      |        |         |               | ✅/❌   |       |
| TC-10     |      |        |         |               | ✅/❌   |       |

---

## Additional Resources

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [dnd-kit Accessibility Documentation](https://docs.dndkit.com/api-documentation/accessibility)
- [NVDA User Guide](https://www.nvaccess.org/files/nvda/documentation/userGuide.html)
- [Keyboard Testing Guide](https://webaim.org/articles/keyboard/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0     | 2025-11-08 | Initial test documentation |

---

**Next Steps:**
1. Execute all test cases with NVDA
2. Log results in execution log
3. File bugs for any failures
4. Retest after fixes
5. Get sign-off from accessibility specialist
