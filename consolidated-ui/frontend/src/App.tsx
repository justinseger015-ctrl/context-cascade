import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { AgentMonitor } from './components/AgentMonitor';
import { WebSocketProvider } from './components/WebSocketProvider';
import { TerminalPage } from './pages/TerminalPage';
import { AIChatPage } from './pages/AIChatPage';
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
                  <NavLink
                    to="/"
                    className={({ isActive }) =>
                      isActive
                        ? 'px-4 py-2 rounded-md bg-blue-600 text-white transition-colors'
                        : 'px-4 py-2 rounded-md text-gray-700 hover:bg-gray-100 transition-colors'
                    }
                  >
                    Agents
                  </NavLink>

                  <NavLink
                    to="/terminals"
                    className={({ isActive }) =>
                      isActive
                        ? 'px-4 py-2 rounded-md bg-blue-600 text-white transition-colors'
                        : 'px-4 py-2 rounded-md text-gray-700 hover:bg-gray-100 transition-colors'
                    }
                  >
                                        Terminals
                  </NavLink>

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
              <Route path="/ai-chat" element={<AIChatPage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </WebSocketProvider>
  );
}

export default App;
