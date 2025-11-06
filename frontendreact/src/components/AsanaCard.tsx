import { Asana } from '../types';

interface AsanaCardProps {
  asana: Asana;
  index: number;
  onClick: () => void;
}

export function AsanaCard({ asana, index, onClick }: AsanaCardProps) {
  return (
    <div
      onClick={onClick}
      className="group relative overflow-hidden rounded-2xl shadow-md cursor-pointer transform transition-all duration-300 hover:shadow-xl hover:scale-[1.02]"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-black/50 via-black/30 to-transparent z-10" />

      <img
        src={asana.image}
        alt={asana.name}
        className="w-full h-40 object-cover transition-transform duration-500 group-hover:scale-110"
      />

      <div className="absolute inset-0 z-20 p-4 flex flex-col justify-between">
        <div className="flex justify-between items-start">
          <span className="w-8 h-8 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center text-sm font-bold text-slate-700">
            {index + 1}
          </span>
        </div>

        <div>
          <h3 className="text-lg font-bold text-white drop-shadow-lg mb-1">
            {asana.name}
          </h3>
          {asana.sanskritName && (
            <p className="text-xs text-white/90 drop-shadow-md">
              {asana.sanskritName}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
