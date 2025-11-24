# WCAG 2.1 AA Manual Testing Guide
## Step-by-Step Accessibility Testing

**Purpose**: This guide walks you through REQUIRED manual accessibility testing that cannot be automated.

**Time Required**: 2-3 hours for thorough testing

---

## 🎯 Why Manual Testing is Required

**Automated tools like axe-core only detect 30-50% of WCAG issues.**

Manual testing is the ONLY way to verify:
- Keyboard navigation works properly
- Screen readers announce content correctly
- Color contrast is sufficient for all users
- Interactive elements are usable by everyone

**Legal Requirement**: WCAG 2.1 AA is legally required for:
- US Federal websites (Section 508)
- EU websites (EN 301 549)
- ADA compliance (Americans with Disabilities Act)

---

## ✅ Testing Checklist Overview

| Test | Priority | Time | Tools |
|------|----------|------|-------|
| Keyboard Navigation | 🔴 CRITICAL | 30 min | Just keyboard! |
| Screen Reader | 🔴 CRITICAL | 45 min | NVDA (free) |
| Color Contrast | 🟡 HIGH | 20 min | Chrome DevTools |
| Responsive/Zoom | 🟡 HIGH | 15 min | Browser zoom |
| Forms & Validation | 🟡 HIGH | 20 min | Keyboard + screen reader |

---

## 1️⃣ Keyboard Navigation Testing (CRITICAL)

**Time**: 30 minutes
**Tools**: Your keyboard (NO MOUSE!)

### Setup
1. Close your mouse/trackpad or physically move it away
2. Open the application in Chrome/Firefox
3. Use ONLY keyboard for navigation

---

### Test 1.1: Tab Order
**WCAG**: 2.4.3 Focus Order

**Steps**:
1. Press `Tab` to move through all interactive elements
2. Press `Shift + Tab` to move backwards

**Expected**:
- ✅ Tab order is LOGICAL (top-to-bottom, left-to-right)
- ✅ All interactive elements are reachable (buttons, links, inputs, calendar)
- ✅ No "keyboard traps" (can always move forward/backward)
- ✅ Modal/dialogs can be closed with `Escape`

**Record**:
- [ ] Tab order is logical
- [ ] All buttons/links reachable
- [ ] Can escape modals with `Esc`
- [ ] No keyboard traps detected

---

### Test 1.2: Focus Indicators
**WCAG**: 2.4.7 Focus Visible

**Steps**:
1. Tab through all elements
2. Observe the focus indicator (outline/ring around focused element)

**Expected**:
- ✅ Focus indicator is VISIBLE on every element
- ✅ Focus indicator has 3:1 contrast with background
- ✅ Focus indicator is NOT removed with `outline: none` in CSS

**Common Issues**:
- ❌ No visible focus (outline removed)
- ❌ Focus indicator too subtle (low contrast)
- ❌ Focus indicator hidden by other elements

**Record**:
- [ ] Focus visible on all elements
- [ ] Focus has 3:1 contrast
- [ ] Focus not removed by CSS

---

### Test 1.3: Skip to Main Content
**WCAG**: 2.4.1 Bypass Blocks

**Steps**:
1. Reload page
2. Press `Tab` once
3. First focusable element should be "Skip to Main Content" link
4. Press `Enter`

**Expected**:
- ✅ "Skip to Main Content" link is first tab stop
- ✅ Pressing Enter skips navigation and jumps to main content
- ✅ Focus moves to `<main>` element

**Record**:
- [ ] Skip link present and first tab stop
- [ ] Skip link works (jumps to main)

---

### Test 1.4: Calendar Keyboard Navigation
**WCAG**: 2.1.1 Keyboard

**Steps**:
1. Tab to calendar
2. Use arrow keys to navigate dates:
   - `→` Right arrow: Next day
   - `←` Left arrow: Previous day
   - `↑` Up arrow: Previous week
   - `↓` Down arrow: Next week
3. Press `Space` or `Enter` to select a date

**Expected**:
- ✅ Arrow keys navigate calendar dates
- ✅ Enter/Space selects date
- ✅ Current focused date is announced

**Record**:
- [ ] Arrow keys navigate dates
- [ ] Enter/Space selects date
- [ ] Visual focus on current date

---

### Test 1.5: Drag-and-Drop with Keyboard
**WCAG**: 2.1.1 Keyboard

**Steps**:
1. Tab to a task in "To Do" column
2. Press `Space` or `Enter` to "grab" the task
3. Use `Tab` to navigate to "In Progress" column
4. Press `Space` or `Enter` to "drop" the task

**Expected**:
- ✅ Space/Enter grabs task (visual indicator)
- ✅ Tab navigates between columns while holding task
- ✅ Space/Enter drops task in new column
- ✅ Task moves to new column

**Alternative**: If drag-and-drop isn't keyboard accessible, provide an alternative (e.g., "Move to..." dropdown menu)

**Record**:
- [ ] Can grab task with keyboard
- [ ] Can move task with keyboard
- [ ] Can drop task with keyboard
- [ ] OR alternative method provided

---

## 2️⃣ Screen Reader Testing (CRITICAL)

**Time**: 45 minutes
**Tools**: NVDA (Windows) or VoiceOver (macOS)

### Install NVDA (Windows)
1. Download: https://www.nvaccess.org/download/
2. Install (default options)
3. Launch NVDA (Ctrl + Alt + N)

### NVDA Keyboard Shortcuts
- **Start/Stop**: `Ctrl + Alt + N`
- **Read next item**: `↓` (down arrow)
- **Read previous item**: `↑` (up arrow)
- **Read all**: `Insert + ↓`
- **Stop reading**: `Ctrl`

---

### Test 2.1: Page Structure
**WCAG**: 1.3.1 Info and Relationships

**Steps**:
1. Launch NVDA
2. Press `Insert + F7` (Elements List)
3. Select "Headings" tab

**Expected**:
- ✅ Headings present (h1, h2, h3)
- ✅ Heading hierarchy is logical (h1 → h2 → h3, no skipping)
- ✅ Page has exactly ONE h1 (main heading)

**Steps (Landmarks)**:
1. Press `Insert + F7`
2. Select "Landmarks" tab

**Expected**:
- ✅ `<main>` landmark present (primary content)
- ✅ `<nav>` landmark present (navigation)
- ✅ `<header>` landmark present (site header)

**Record**:
- [ ] Headings are logical and hierarchical
- [ ] Exactly one h1 per page
- [ ] Main, nav, header landmarks present

---

### Test 2.2: Images and Icons
**WCAG**: 1.1.1 Non-text Content

**Steps**:
1. Tab through the page with NVDA running
2. Listen for image descriptions

**Expected**:
- ✅ All meaningful images have `alt` text
- ✅ Decorative images have `alt=""` (empty) or `role="presentation"`
- ✅ Icons have `aria-label` (e.g., settings icon: `aria-label="Settings"`)

**Common Issues**:
- ❌ Icon buttons with no label (NVDA says "button" only)
- ❌ Charts/graphs with no description
- ❌ Decorative images with unnecessary alt text

**Record**:
- [ ] All meaningful images have alt text
- [ ] Decorative images have empty alt
- [ ] Icons have aria-labels

---

### Test 2.3: Form Labels
**WCAG**: 3.3.2 Labels or Instructions

**Steps**:
1. Tab to each form input
2. Listen to NVDA announcement

**Expected**:
- ✅ NVDA announces the label (e.g., "Task Title, edit, blank")
- ✅ Required fields announced as "required"
- ✅ Placeholder text is NOT used as the only label

**Common Issues**:
- ❌ Input with placeholder but no `<label>`
- ❌ Label not programmatically associated (`for` attribute missing)

**Record**:
- [ ] All inputs have labels
- [ ] Labels properly associated
- [ ] Required fields announced

---

### Test 2.4: Calendar Announcements
**WCAG**: 4.1.3 Status Messages

**Steps**:
1. Tab to calendar
2. Use arrow keys to navigate dates
3. Listen to NVDA announcements

**Expected**:
- ✅ Current date is announced (e.g., "November 8, 2024, Friday")
- ✅ Selected date changes are announced
- ✅ Events on date are announced

**Record**:
- [ ] Dates are announced correctly
- [ ] Date changes announced
- [ ] Events announced

---

### Test 2.5: Task Status Changes
**WCAG**: 4.1.3 Status Messages

**Steps**:
1. Move a task from "To Do" to "In Progress"
2. Listen to NVDA announcement

**Expected**:
- ✅ Status change is announced (e.g., "Task moved to In Progress")
- ✅ Uses `aria-live="polite"` or `role="status"`

**Record**:
- [ ] Task moves announced
- [ ] Status changes announced

---

## 3️⃣ Color Contrast Testing (HIGH PRIORITY)

**Time**: 20 minutes
**Tools**: Chrome DevTools

### Test 3.1: Text Contrast
**WCAG**: 1.4.3 Contrast (Minimum)

**Steps**:
1. Open Chrome DevTools (`F12`)
2. Select "Elements" tab
3. Click on text element
4. Look for "Contrast" section in Styles panel

**Requirements**:
- ✅ **Normal text** (< 18pt or < 14pt bold): **4.5:1** minimum
- ✅ **Large text** (≥ 18pt or ≥ 14pt bold): **3:1** minimum

**Test All Text**:
- [ ] Body text (paragraphs)
- [ ] Button text
- [ ] Link text
- [ ] Input labels
- [ ] Placeholder text
- [ ] Error messages

**Example**:
- Background: `#FFFFFF` (white)
- Text: `#767676` (gray)
- Contrast: 4.54:1 ✅ PASS (4.5:1 minimum)

**Record**:
- [ ] All normal text ≥ 4.5:1
- [ ] All large text ≥ 3:1
- [ ] Focus indicators ≥ 3:1

---

### Test 3.2: Color Blindness Simulation
**WCAG**: 1.4.1 Use of Color

**Steps**:
1. Open Chrome DevTools (`F12`)
2. Press `Ctrl + Shift + P` (Command Palette)
3. Type "Render" and select "Show Rendering"
4. Scroll to "Emulate vision deficiencies"
5. Test each type:
   - Protanopia (red-blind)
   - Deuteranopia (green-blind)
   - Tritanopia (blue-blind)

**Expected**:
- ✅ Information is NOT conveyed by color alone
- ✅ Error states use icons + text (not just red color)
- ✅ Charts use patterns + labels (not just color-coded)

**Common Issues**:
- ❌ "Required" indicated by red * only (no text)
- ❌ Charts with only color differences (no labels/patterns)
- ❌ Link color too similar to text (only color differentiates)

**Record**:
- [ ] Tested all 3 color blindness types
- [ ] Information not color-dependent
- [ ] Error states have icons + text

---

## 4️⃣ Responsive & Zoom Testing (HIGH PRIORITY)

**Time**: 15 minutes
**Tools**: Browser zoom

### Test 4.1: 200% Zoom
**WCAG**: 1.4.4 Resize Text

**Steps**:
1. Open application
2. Zoom in: `Ctrl +` (Windows) or `Cmd +` (Mac)
3. Continue until 200% (2x zoom)

**Expected**:
- ✅ All text remains readable
- ✅ No horizontal scrolling required
- ✅ No content is cut off or hidden
- ✅ All functionality still works

**Record**:
- [ ] Text readable at 200%
- [ ] No horizontal scrolling
- [ ] All features functional

---

### Test 4.2: 400% Zoom
**WCAG**: 1.4.10 Reflow

**Steps**:
1. Zoom to 400% (4x)

**Expected**:
- ✅ Content reflows to single column
- ✅ No horizontal scrolling
- ✅ Text remains readable

**Record**:
- [ ] Content reflows at 400%
- [ ] No horizontal scrolling

---

### Test 4.3: Mobile Screen Sizes
**WCAG**: 1.4.10 Reflow

**Steps**:
1. Open Chrome DevTools (`F12`)
2. Click "Toggle device toolbar" (Ctrl + Shift + M)
3. Select "Responsive"
4. Set width to 320px (smallest mobile)

**Expected**:
- ✅ All content visible (no cut-off)
- ✅ Touch targets ≥ 44x44 pixels
- ✅ No horizontal scrolling

**Record**:
- [ ] Works at 320px width
- [ ] Touch targets ≥ 44px
- [ ] No horizontal scrolling

---

## 5️⃣ Forms & Validation Testing (HIGH PRIORITY)

**Time**: 20 minutes
**Tools**: Keyboard + NVDA

### Test 5.1: Error Messages
**WCAG**: 3.3.1 Error Identification

**Steps**:
1. Try to submit a form with invalid data
2. Observe error messages

**Expected**:
- ✅ Error messages are SPECIFIC (e.g., "Email must include @" not just "Invalid")
- ✅ Error messages are VISIBLE (red text + icon)
- ✅ Error messages are PROGRAMMATICALLY ASSOCIATED (`aria-describedby`)
- ✅ NVDA announces errors

**Example**:
```html
<label for="email">Email *</label>
<input
  id="email"
  type="email"
  aria-required="true"
  aria-describedby="email-error"
  aria-invalid="true"
/>
<div id="email-error" role="alert">
  Email must include @ symbol
</div>
```

**Record**:
- [ ] Errors are specific and helpful
- [ ] Errors programmatically associated
- [ ] NVDA announces errors

---

### Test 5.2: Required Fields
**WCAG**: 3.3.2 Labels or Instructions

**Steps**:
1. Tab through form inputs
2. Listen to NVDA announcements

**Expected**:
- ✅ Required fields have `aria-required="true"` or `required` attribute
- ✅ NVDA announces "required" (e.g., "Task Title, required, edit, blank")
- ✅ Visual indicator (e.g., `*` or "Required" text)

**Record**:
- [ ] Required fields marked visually
- [ ] Required announced by NVDA
- [ ] `aria-required` or `required` attribute

---

### Test 5.3: Autocomplete
**WCAG**: 1.3.5 Identify Input Purpose

**Steps**:
1. Inspect form inputs with DevTools
2. Check for `autocomplete` attribute

**Expected**:
- ✅ Email inputs: `autocomplete="email"`
- ✅ Name inputs: `autocomplete="name"`
- ✅ Password inputs: `autocomplete="current-password"`
- ✅ New password: `autocomplete="new-password"`

**Why**: Autocomplete helps users with:
- Password managers
- Autofill (saves time)
- Cognitive disabilities (reduces typing)

**Record**:
- [ ] Email has autocomplete="email"
- [ ] Password has autocomplete
- [ ] Name fields have autocomplete

---

## 📊 Final Checklist

**Before marking WCAG 2.1 AA as PASSED:**

### Critical (Must Pass)
- [ ] Keyboard navigation: All features accessible
- [ ] Focus indicators: Visible on all elements
- [ ] Screen reader: All content announced correctly
- [ ] Color contrast: All text ≥ 4.5:1 (or 3:1 for large)
- [ ] Zoom: Works at 200% without horizontal scrolling

### High Priority (Strongly Recommended)
- [ ] Calendar keyboard accessible (drag-and-drop)
- [ ] Error messages specific and announced
- [ ] Required fields marked and announced
- [ ] Responsive: Works at 320px width
- [ ] Touch targets ≥ 44x44px on mobile

### Medium Priority (Best Practice)
- [ ] Skip to main content link
- [ ] Autocomplete attributes on forms
- [ ] Color blindness tested (3 types)
- [ ] 400% zoom functional

---

## 🎯 Quick 30-Minute Test

**If you only have 30 minutes, test these 5 items:**

1. **Keyboard navigation** (10 min): Tab through entire app, no mouse
2. **Focus indicators** (5 min): Verify visible on all elements
3. **NVDA screen reader** (10 min): Test main workflow
4. **Color contrast** (3 min): Check body text, buttons, links
5. **200% zoom** (2 min): Verify no horizontal scrolling

**If any fail, STOP and fix before deploying.**

---

## 📞 Resources

- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **NVDA Screen Reader**: https://www.nvaccess.org/
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Chrome DevTools Accessibility**: https://developer.chrome.com/docs/devtools/accessibility/reference/

---

**Testing Completed**: _______________ (Date)
**Tested By**: _______________ (Name)
**Result**: ☐ PASS  ☐ FAIL (see notes)

**Notes**:
```
[Record any issues found during testing]
```

---

**End of Manual Testing Guide**
