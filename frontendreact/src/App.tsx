import { useState } from 'react';
import { AppProvider } from './contexts/AppContext';
import { HomePage } from './components/HomePage';
import { RoutineDetailPage } from './components/RoutineDetailPage';
import { CameraView } from './components/CameraView';

type View = 'home' | 'routine-detail' | 'camera';

function AppContent() {
  const [currentView, setCurrentView] = useState<View>('home');

  return (
    <div className="transition-opacity duration-300">
      {currentView === 'home' && (
        <HomePage onSelectRoutine={() => setCurrentView('routine-detail')} />
      )}

      {currentView === 'routine-detail' && (
        <RoutineDetailPage
          onBack={() => setCurrentView('home')}
          onStartPractice={() => setCurrentView('camera')}
        />
      )}

      {currentView === 'camera' && (
        <CameraView onExit={() => setCurrentView('routine-detail')} />
      )}
    </div>
  );
}

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;
