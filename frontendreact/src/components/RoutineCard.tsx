import { Routine } from '../types';

interface RoutineCardProps {
  routine: Routine;
  onClick: () => void;
}

export function RoutineCard({ routine, onClick }: RoutineCardProps) {
  const difficultyColors = {
    beginner: 'bg-emerald-500',
    intermediate: 'bg-amber-500',
    advanced: 'bg-rose-500'
  };

  return (
    <div
      onClick={onClick}
      className="group relative overflow-hidden rounded-3xl shadow-lg cursor-pointer transform transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900/60 via-slate-800/40 to-transparent z-10" />

      <img
        src={routine.asanas[0]?.image}
        alt={routine.name}
        className="w-full h-56 object-cover transition-transform duration-700 group-hover:scale-110"
      />

      <div className="absolute inset-0 z-20 p-6 flex flex-col justify-end">
        <div className="flex items-center gap-2 mb-2">
          <span className={`px-3 py-1 rounded-full text-xs font-semibold text-white ${difficultyColors[routine.difficulty]} backdrop-blur-sm`}>
            {routine.difficulty.toUpperCase()}
          </span>
          <span className="px-3 py-1 rounded-full text-xs font-semibold text-white bg-white/20 backdrop-blur-sm">
            {routine.asanas.length} poses
          </span>
        </div>

        <h3 className="text-2xl font-bold text-white mb-2 drop-shadow-lg">
          {routine.name}
        </h3>

        <p className="text-sm text-white/90 drop-shadow-md line-clamp-2">
          {routine.description}
        </p>
      </div>
    </div>
  );
}
