# Phase 2, Week 3: AI Integration - Completion Guide

**Status**: 60% Complete - Ready for Final Implementation
**Remaining Time**: 2-3 hours
**Complexity**: Medium

---

## Quick Summary

**Completed**:
- ✅ Discovered Rose Tree AI stack (Anthropic + LaTeX/Markdown)
- ✅ Installed 4 AI packages (@anthropic-ai/sdk, katex, marked, marked-extended-latex)
- ✅ Copied utilities (marked.js) and components (FloatingTextInput, Button)

**Remaining**:
- ⏳ Create AI Assistant component (45-60 mins)
- ⏳ Create backend API endpoint (30-45 mins)
- ⏳ Create page and routing (15-30 mins)
- ⏳ Test and document (30-45 mins)

---

## Task 1: Create AI Assistant Component (45-60 mins)

### File: `consolidated-ui/frontend/src/components/AIAssistant/AIAssistant.tsx`

**Objective**: Adapt Rose Tree's SkillSidebar to general-purpose AI chat

**Reference**: `C:/Users/17175/skilltree/src/app/tree/skillSidebar/index.jsx`

**Key Changes**:
1. Remove skill tree specific logic
2. Replace with agent/task context
3. Keep LaTeX/Markdown rendering
4. Simplify to chat interface

**Implementation Template**:

```typescript
import React, { useState, useRef } from 'react';
import FloatingTextInput from '../FloatingTextInput';
import Button from '../Button';
import marked from '../../utils/marked';
import './AIAssistant.module.scss';

interface AIMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

export const AIAssistant: React.FC = () => {
  const [messages, setMessages] = useState<AIMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const inputRef = useRef<any>();

  const handleSendMessage = async () => {
    const userInput = inputRef.current?.getValue();
    if (!userInput) return;

    // Add user message
    const userMessage: AIMessage = {
      role: 'user',
      content: userInput,
      timestamp: Date.now(),
    };
    setMessages(prev => [...prev, userMessage]);

    // Clear input
    inputRef.current?.setValue('');

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/v1/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_input: userInput,
          context: {
            current_agent: 'general',
            conversation_history: messages.slice(-5), // Last 5 messages for context
          },
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();

      // Add AI message
      const aiMessage: AIMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: Date.now(),
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      console.error('[AIAssistant] Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-assistant">
      <div className="messages-container">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.role}`}>
            <div className="message-role">
              {msg.role === 'user' ? 'You' : 'AI Assistant'}
            </div>
            <div
              className="message-content"
              dangerouslySetInnerHTML={{
                __html: msg.role === 'assistant' ? marked(msg.content) : msg.content
              }}
            />
          </div>
        ))}

        {loading && (
          <div className="message message-assistant loading">
            <div className="message-role">AI Assistant</div>
            <div className="message-content">Thinking...</div>
          </div>
        )}

        {error && (
          <div className="message message-error">
            <div className="message-role">Error</div>
            <div className="message-content">{error}</div>
          </div>
        )}
      </div>

      <div className="input-container">
        <FloatingTextInput
          ref={inputRef}
          label="Ask the AI Assistant..."
          multiline={true}
          onEnter={handleSendMessage}
        />
        <Button onClick={handleSendMessage} disabled={loading}>
          Send
        </Button>
      </div>
    </div>
  );
};
```

### File: `consolidated-ui/frontend/src/components/AIAssistant/AIAssistant.module.scss`

```scss
.ai-assistant {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 900px;
  margin: 0 auto;

  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;

    .message {
      padding: 1rem;
      border-radius: 8px;

      &.message-user {
        background: #e3f2fd;
        margin-left: auto;
        max-width: 80%;
      }

      &.message-assistant {
        background: #f5f5f5;
        margin-right: auto;
        max-width: 80%;
      }

      &.message-error {
        background: #ffebee;
        color: #c62828;
      }

      &.loading {
        opacity: 0.7;
      }

      .message-role {
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
        color: #666;
      }

      .message-content {
        line-height: 1.6;

        // Markdown styling
        p { margin-bottom: 0.5rem; }
        code {
          background: rgba(0,0,0,0.05);
          padding: 0.2rem 0.4rem;
          border-radius: 3px;
        }
        pre {
          background: rgba(0,0,0,0.05);
          padding: 1rem;
          border-radius: 4px;
          overflow-x: auto;
        }
      }
    }
  }

  .input-container {
    border-top: 1px solid #e0e0e0;
    padding: 1rem;
    display: flex;
    gap: 1rem;
    align-items: flex-end;
  }
}
```

---

## Task 2: Create Backend API Endpoint (30-45 mins)

### File: `backend/app/api/v1/ai_chat.py`

**Objective**: Create FastAPI route for AI chat using Anthropic SDK

**Reference**: `C:/Users/17175/skilltree/src/app/api/sage/route.js`

**Implementation**:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from anthropic import Anthropic

router = APIRouter()

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class ConversationMessage(BaseModel):
    role: str
    content: str
    timestamp: int

class ChatRequest(BaseModel):
    user_input: str
    context: Optional[Dict] = {}

class ChatResponse(BaseModel):
    response: str
    model: str = "claude-3-5-sonnet-20240620"

SYSTEM_PROMPT = """You are an AI assistant helping developers with software development tasks.

You have expertise in:
- Software architecture and design patterns
- Code optimization and best practices
- Debugging and problem-solving
- API development and integration
- Database design and queries
- Testing strategies
- DevOps and CI/CD

Provide clear, concise, and practical advice. When relevant, include code examples.
You can use Markdown formatting and LaTeX math notation ($...$) in your responses.
"""

@router.post("/ai/chat", response_model=ChatResponse)
async def ai_chat(request: ChatRequest):
    """
    AI chat endpoint using Claude 3.5 Sonnet

    Supports:
    - Markdown formatting
    - LaTeX math notation ($...$)
    - Code blocks with syntax highlighting
    """
    try:
        # Build conversation context
        conversation_history = request.context.get("conversation_history", [])

        # Prepare messages for Anthropic
        messages = []
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        # Add current user input
        messages.append({
            "role": "user",
            "content": request.user_input
        })

        # Call Anthropic API
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        # Extract response text
        response_text = message.content[0].text

        return ChatResponse(
            response=response_text,
            model="claude-3-5-sonnet-20240620"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing AI request: {str(e)}"
        )
```

### Update: `backend/app/api/v1/__init__.py`

Add the new router:

```python
from fastapi import APIRouter
from .ai_chat import router as ai_chat_router
# ... other imports

api_router = APIRouter()

# Include AI chat router
api_router.include_router(
    ai_chat_router,
    prefix="/v1",
    tags=["ai"]
)
```

### Update: `backend/requirements.txt`

Add Anthropic SDK:

```
anthropic>=0.24.3
```

Then run:
```bash
pip install anthropic
```

### Environment Variable

Add to `.env` or set in environment:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

---

## Task 3: Create Page and Routing (15-30 mins)

### File: `consolidated-ui/frontend/src/pages/AIChatPage.tsx`

```typescript
import React from 'react';
import { AIAssistant } from '../components/AIAssistant/AIAssistant';

export const AIChatPage: React.FC = () => {
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>AI Assistant</h1>
        <p className="page-subtitle">
          Get help with development tasks, code reviews, and technical questions
        </p>
      </header>

      <main className="page-content" style={{ height: 'calc(100vh - 200px)' }}>
        <AIAssistant />
      </main>
    </div>
  );
};

export default AIChatPage;
```

### Update: `consolidated-ui/frontend/src/App.tsx`

Add AI chat route and navigation link:

```typescript
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { AgentMonitor } from './components/AgentMonitor';
import { WebSocketProvider } from './components/WebSocketProvider';
import { TerminalPage } from './pages/TerminalPage';
import { AIChatPage } from './pages/AIChatPage';  // NEW
import './App.css';

function App() {
  return (
    <WebSocketProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <nav className="bg-white shadow-sm border-b border-gray-200">
            <div className="container mx-auto px-4 py-3">
              <div className="flex items-center gap-6">
                <h1 className="text-xl font-bold text-gray-900">
                  rUv SPARC Dashboard
                </h1>

                <div className="flex gap-4">
                  <NavLink to="/" className={({ isActive }) => /* ... */}>
                    Agents
                  </NavLink>

                  <NavLink to="/terminals" className={({ isActive }) => /* ... */}>
                    Terminals
                  </NavLink>

                  {/* NEW: AI Assistant Link */}
                  <NavLink
                    to="/ai-chat"
                    className={({ isActive }) =>
                      isActive
                        ? 'px-4 py-2 rounded-md bg-blue-600 text-white transition-colors'
                        : 'px-4 py-2 rounded-md text-gray-700 hover:bg-gray-100 transition-colors'
                    }
                  >
                    AI Assistant
                  </NavLink>
                </div>
              </div>
            </div>
          </nav>

          <main className="container mx-auto px-4 py-6">
            <Routes>
              <Route path="/" element={<AgentMonitor />} />
              <Route path="/terminals" element={<TerminalPage />} />
              <Route path="/ai-chat" element={<AIChatPage />} />  {/* NEW */}
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </WebSocketProvider>
  );
}

export default App;
```

---

## Task 4: Test and Document (30-45 mins)

### Manual Testing Checklist

1. **Basic Functionality**
   ```bash
   # Start backend
   cd backend
   python -m uvicorn app.main:app --reload --port 8000

   # Start frontend (in another terminal)
   cd consolidated-ui/frontend
   npm run dev

   # Open browser: http://localhost:5173/ai-chat
   ```

2. **Test Cases**
   - [ ] Navigate to /ai-chat page
   - [ ] Page loads without errors
   - [ ] Input field is visible
   - [ ] Send button is enabled
   - [ ] Type message and click Send
   - [ ] Loading state appears
   - [ ] AI response displays
   - [ ] Response has proper formatting

3. **LaTeX Rendering**
   Test input: `What is the formula for energy? Please show it using LaTeX.`

   Expected: Should render $E = mc^2$ properly

4. **Markdown Rendering**
   Test input: `Show me a code example in Python for a simple function.`

   Expected: Code blocks should have syntax highlighting

5. **Error Handling**
   - [ ] Test with invalid API key (should show error)
   - [ ] Test with network disconnected (should show error)
   - [ ] Test with empty input (button should be disabled)

### Create Completion Document

**File**: `docs/PHASE-2-WEEK-3-AI-INTEGRATION-COMPLETE.md`

**Template**:

```markdown
# Phase 2, Week 3: AI Integration - COMPLETE

**Date**: 2025-11-17
**Status**: COMPLETE
**Time Spent**: ~3 hours
**Deliverables**: AI Assistant with LaTeX/Markdown support

---

## Executive Summary

Week 3 AI Integration is COMPLETE with Anthropic Claude 3.5 Sonnet, LaTeX math rendering via KaTeX, and Markdown support. Full chat interface with conversation history integrated into consolidated dashboard.

---

## Completed Tasks (8/8 - 100%)

1. ✅ Discovered Rose Tree AI architecture
2. ✅ Installed AI packages (4 packages)
3. ✅ Copied utilities and components
4. ✅ Created AI Assistant component
5. ✅ Created backend API endpoint
6. ✅ Created AI page and routing
7. ✅ Tested AI integration
8. ✅ Documented completion

---

## Features Implemented

### AI Chat
- Claude 3.5 Sonnet integration
- Conversation history (last 5 messages)
- Loading states and error handling
- Real-time responses

### LaTeX Rendering
- Inline formulas: `$E = mc^2$`
- Block formulas: `$$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$`
- KaTeX v0.16.11 rendering

### Markdown Support
- **Bold**, *italic*, ~~strikethrough~~
- Code blocks with syntax highlighting
- Lists (ordered and unordered)
- Links and images
- Custom spoiler blocks

---

## Files Created/Modified

### Created Files
1. `src/utils/marked.js` - LaTeX + Markdown renderer (58 lines)
2. `src/components/FloatingTextInput/` - Input component (157 lines + styles)
3. `src/components/Button/` - Button component
4. `src/components/AIAssistant/AIAssistant.tsx` - Main AI chat component
5. `src/components/AIAssistant/AIAssistant.module.scss` - Styles
6. `src/pages/AIChatPage.tsx` - AI chat page
7. `backend/app/api/v1/ai_chat.py` - FastAPI route

### Modified Files
8. `package.json` - Added 4 AI packages
9. `App.tsx` - Added /ai-chat route and navigation
10. `backend/requirements.txt` - Added anthropic SDK
11. `backend/app/api/v1/__init__.py` - Registered AI router

---

## Success Criteria

- [x] AI packages installed
- [x] Utilities copied
- [x] AI Assistant component created
- [x] Backend API endpoint created
- [x] AI page with routing
- [x] Navigation link added
- [x] LaTeX rendering works
- [x] Markdown rendering works
- [x] AI responses display correctly
- [x] Error handling works
- [x] Conversation history maintained

**Progress**: 11/11 complete (100%)

---

## Next Steps

### Week 4 (UI/UX Polish)
- Fix all 15 remaining TypeScript errors from Week 1
- Upgrade to Radix UI components
- Implement unified design system
- Add dark mode toggle
- Optimize performance

### Week 5 (Testing)
- Write E2E tests for AI chat
- Run accessibility audit
- Performance testing
- Cross-browser testing

### Week 6 (Deployment)
- Configure Docker deployment
- Set up auto-start on boot
- Create production build
- Final documentation

---

**Status**: Week 3 **COMPLETE** - Ready for Week 4 (UI/UX Polish)
```

---

## Quick Reference Commands

```bash
# Install backend dependency
cd backend
pip install anthropic

# Run backend
python -m uvicorn app.main:app --reload --port 8000

# Run frontend
cd consolidated-ui/frontend
npm run dev

# Test AI chat
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "What is React?"}'

# Build frontend
npm run build
```

---

## Troubleshooting

### Error: "ANTHROPIC_API_KEY not set"
**Solution**: Set environment variable
```bash
export ANTHROPIC_API_KEY=your_key_here  # Linux/Mac
set ANTHROPIC_API_KEY=your_key_here     # Windows
```

### Error: "Module 'anthropic' not found"
**Solution**: Install Python package
```bash
pip install anthropic
```

### Error: "marked is not defined"
**Solution**: Check import path in AIAssistant.tsx
```typescript
import marked from '../../utils/marked';
```

### LaTeX not rendering
**Solution**: Verify katex CSS is imported
```typescript
import 'katex/dist/katex.min.css';
```

---

## Estimated Time Breakdown

- **Task 1: AI Assistant Component** - 45-60 mins
  - Component structure: 15 mins
  - Message handling: 15 mins
  - Styling: 15-30 mins

- **Task 2: Backend API** - 30-45 mins
  - FastAPI route: 15 mins
  - Anthropic integration: 15 mins
  - Testing: 10-15 mins

- **Task 3: Page and Routing** - 15-30 mins
  - AIChatPage: 5 mins
  - App.tsx updates: 10 mins
  - Navigation styling: 5-10 mins

- **Task 4: Testing and Documentation** - 30-45 mins
  - Manual testing: 15-20 mins
  - Fix bugs: 10-15 mins
  - Documentation: 10-15 mins

**Total**: 2-3 hours

---

**Ready to implement!** Follow tasks 1-4 sequentially for best results.
