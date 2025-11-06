import { useEffect, useState } from 'react';
import { X, SwitchCamera, Check } from 'lucide-react';
import { useApp } from '../contexts/AppContext';
import { useCamera } from '../hooks/useCamera';
import { useWebSocket } from '../hooks/useWebSocket';
import { DetectionStatus } from '../types';

interface CameraViewProps {
  onExit: () => void;
}

export function CameraView({ onExit }: CameraViewProps) {
  const { selectedRoutine, selectedAsana, isFullRoutine } = useApp();
  const { videoRef, isReady, error, toggleCamera, captureFrame } = useCamera();
  const { result, sendFrame, sendInit, isConnected } = useWebSocket('ws://localhost:8765');

  const [currentPoseName, setCurrentPoseName] = useState('');
  const [sessionInitialized, setSessionInitialized] = useState(false);

  useEffect(() => {
    if (isConnected && !sessionInitialized && selectedRoutine) {
      const mode = isFullRoutine ? 'routine' : 'single';
      const asanaIds = isFullRoutine
        ? selectedRoutine.asanas.map(a => a.id)
        : selectedAsana ? [selectedAsana.id] : [selectedRoutine.asanas[0].id];
      const routineName = isFullRoutine ? selectedRoutine.name : undefined;

      sendInit(mode, asanaIds, routineName);
      setSessionInitialized(true);
    }
  }, [isConnected, sessionInitialized, selectedRoutine, selectedAsana, isFullRoutine, sendInit]);

  useEffect(() => {
    if (result.pose_name) {
      setCurrentPoseName(result.pose_name);
    }

    if (result.status === DetectionStatus.SEQUENCE_COMPLETE) {
      setTimeout(() => {
        alert('Congratulations! Practice completed!');
        onExit();
      }, 2000);
    }
  }, [result, onExit]);

  useEffect(() => {
    if (!isReady || !sessionInitialized) return;

    const interval = setInterval(() => {
      const frameData = captureFrame();
      if (frameData) {
        sendFrame(`data:image/jpeg;base64,${frameData}`);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [isReady, sessionInitialized, sendFrame, captureFrame]);

  const statusColors = {
    [DetectionStatus.INITIALIZING]: 'bg-slate-600',
    [DetectionStatus.NO_POSE]: 'bg-slate-600',
    [DetectionStatus.INCORRECT]: 'bg-rose-600',
    [DetectionStatus.CORRECT]: 'bg-emerald-600',
    [DetectionStatus.PARTIAL]: 'bg-amber-600',
    [DetectionStatus.NEXT_POSE]: 'bg-blue-600',
    [DetectionStatus.SEQUENCE_COMPLETE]: 'bg-green-600',
  };

  const statusIcons: Record<DetectionStatus, JSX.Element | null> = {
    [DetectionStatus.INITIALIZING]: null,
    [DetectionStatus.NO_POSE]: null,
    [DetectionStatus.INCORRECT]: null,
    [DetectionStatus.CORRECT]: <Check className="w-6 h-6" />,
    [DetectionStatus.PARTIAL]: <Check className="w-6 h-6 opacity-50" />,
    [DetectionStatus.NEXT_POSE]: null,
    [DetectionStatus.SEQUENCE_COMPLETE]: <Check className="w-6 h-6" />
  };

  return (
    <div className="fixed inset-0 bg-black z-50 flex flex-col">
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="absolute inset-0 w-full h-full object-cover"
      />

      <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/80" />

      <div className="relative z-10 flex flex-col h-full">
        <div className="flex items-center justify-between p-4">
          <button
            onClick={onExit}
            className="p-3 rounded-full bg-white/10 backdrop-blur-md hover:bg-white/20 transition-all"
          >
            <X className="w-6 h-6 text-white" />
          </button>

          <div className="flex-1 mx-4">
            <div className="bg-white/10 backdrop-blur-md rounded-full px-4 py-2">
              <h2 className="text-white font-bold text-center truncate">
                {currentPoseName || (selectedAsana?.name || selectedRoutine?.asanas[0]?.name || 'Loading...')}
              </h2>
            </div>
          </div>

          <button
            onClick={toggleCamera}
            className="p-3 rounded-full bg-white/10 backdrop-blur-md hover:bg-white/20 transition-all"
          >
            <SwitchCamera className="w-6 h-6 text-white" />
          </button>
        </div>

        <div className="flex-1" />

        <div className="p-4">
          <div
            className={`${statusColors[result.status]} backdrop-blur-md rounded-2xl p-6 transition-all duration-300`}
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <p className="text-white text-lg font-bold mb-1">
                  {result.message}
                </p>
                {result.confidence !== undefined && result.confidence > 0 && (
                  <p className="text-white/80 text-sm">
                    Accuracy: {Math.round(result.confidence * 100)}%
                  </p>
                )}
              </div>

              {statusIcons[result.status] && (
                <div className="text-white ml-4">
                  {statusIcons[result.status]}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-black z-20">
          <div className="text-center px-6">
            <p className="text-white text-lg mb-4">{error}</p>
            <button
              onClick={onExit}
              className="px-6 py-3 bg-white text-slate-900 font-bold rounded-xl hover:bg-white/90 transition-all"
            >
              Go Back
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
