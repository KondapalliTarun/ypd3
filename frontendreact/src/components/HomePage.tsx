import { Dumbbell } from 'lucide-react';
import { routines } from '../data/routines';
import { RoutineCard } from './RoutineCard';
import { useApp } from '../contexts/AppContext';

interface HomePageProps {
  onSelectRoutine: () => void;
}

export function HomePage({ onSelectRoutine }: HomePageProps) {
  const { setSelectedRoutine } = useApp();

  const handleRoutineClick = (routine: typeof routines[0]) => {
    setSelectedRoutine(routine);
    onSelectRoutine();
  };

  const today = new Date();
  const dayOfWeek = today.toLocaleDateString('en-US', { weekday: 'long' });
  const dateFormatted = today.toLocaleDateString('en-US', {
    day: 'numeric',
    month: 'long'
  }).toUpperCase();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-orange-50 to-rose-50">
      <header className="bg-gradient-to-r from-orange-500 via-rose-500 to-pink-500 shadow-lg">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Dumbbell className="w-8 h-8 text-white" strokeWidth={2.5} />
              <h1 className="text-2xl font-bold text-white tracking-tight">
                Flexcellent
              </h1>
            </div>

            <div className="text-right">
              <p className="text-white/80 text-xs font-semibold tracking-wider">
                {dateFormatted}
              </p>
              <p className="text-white text-xl font-bold">
                {dayOfWeek}
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        <div className="text-center mb-10">
          <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-orange-600 via-rose-600 to-pink-600 bg-clip-text text-transparent mb-3">
            Asana, Suvasana!
          </h2>
          <p className="text-slate-600 text-lg">
            Choose your practice for today
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {routines.map((routine) => (
            <RoutineCard
              key={routine.id}
              routine={routine}
              onClick={() => handleRoutineClick(routine)}
            />
          ))}
        </div>
      </main>
    </div>
  );
}
