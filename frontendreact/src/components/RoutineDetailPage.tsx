import { ArrowLeft, Play } from 'lucide-react';
import { useApp } from '../contexts/AppContext';
import { AsanaCard } from './AsanaCard';

interface RoutineDetailPageProps {
  onBack: () => void;
  onStartPractice: () => void;
}

export function RoutineDetailPage({ onBack, onStartPractice }: RoutineDetailPageProps) {
  const { selectedRoutine, setSelectedAsana, setIsFullRoutine } = useApp();

  if (!selectedRoutine) return null;

  const handleAsanaClick = (asana: typeof selectedRoutine.asanas[0]) => {
    setSelectedAsana(asana);
    setIsFullRoutine(false);
    onStartPractice();
  };

  const handleFullRoutineClick = () => {
    setSelectedAsana(null);
    setIsFullRoutine(true);
    onStartPractice();
  };

  const difficultyColors = {
    beginner: 'from-emerald-500 to-emerald-600',
    intermediate: 'from-amber-500 to-amber-600',
    advanced: 'from-rose-500 to-rose-600'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-orange-50 to-rose-50">
      <header className="bg-gradient-to-r from-orange-500 via-rose-500 to-pink-500 shadow-lg sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-white hover:text-white/80 transition-colors"
          >
            <ArrowLeft className="w-6 h-6" />
            <span className="font-semibold">Back</span>
          </button>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center gap-3 mb-4">
              <span className={`px-4 py-2 rounded-full text-sm font-bold text-white bg-gradient-to-r ${difficultyColors[selectedRoutine.difficulty]} shadow-md`}>
                {selectedRoutine.difficulty.toUpperCase()}
              </span>
            </div>

            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-orange-600 via-rose-600 to-pink-600 bg-clip-text text-transparent mb-3">
              {selectedRoutine.name}
            </h1>

            <p className="text-slate-600 text-lg mb-6">
              {selectedRoutine.description}
            </p>

            <button
              onClick={handleFullRoutineClick}
              className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-orange-500 via-rose-500 to-pink-500 text-white font-bold rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
            >
              <Play className="w-5 h-5 fill-current" />
              Start Full Routine
            </button>
          </div>

          <div className="mb-6">
            <h2 className="text-2xl font-bold text-slate-800 mb-4">
              Or practice individual poses
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {selectedRoutine.asanas.map((asana, index) => (
              <AsanaCard
                key={asana.id}
                asana={asana}
                index={index}
                onClick={() => handleAsanaClick(asana)}
              />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
