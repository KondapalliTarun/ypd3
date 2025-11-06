import { useEffect, useRef, useState } from 'react';
import { DetectionStatus, DetectionResult } from '../types';

export function useWebSocket(url: string) {
  const [result, setResult] = useState<DetectionResult>({
    status: DetectionStatus.INITIALIZING,
    message: 'Connecting to detection server...'
  });
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      setResult({
        status: DetectionStatus.INITIALIZING,
        message: 'Ready to detect poses'
      });
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.audio_data) {
          playAudio(data.audio_data);
        }

        if (data.type === 'init_response') {
          setResult({
            status: DetectionStatus.INITIALIZING,
            message: 'Ready to begin',
            pose_name: data.pose_name
          });
        } else if (data.data !== undefined) {
          let status: DetectionStatus;
          let message: string;

          switch (data.data) {
            case 0:
              status = DetectionStatus.NO_POSE;
              message = 'No pose detected - step into frame';
              break;
            case 1:
              status = DetectionStatus.INCORRECT;
              message = 'Incorrect pose - adjust your position';
              break;
            case 2:
              status = DetectionStatus.CORRECT;
              message = "Perfect! Hold it";
              break;
            case 3:
              status = DetectionStatus.PARTIAL;
              message = 'Almost there - adjust as instructed';
              break;
            case 4:
              status = DetectionStatus.NEXT_POSE;
              message = 'Moving to next pose';
              break;
            case 5:
              status = DetectionStatus.SEQUENCE_COMPLETE;
              message = 'Completed!';
              break;
            default:
              status = DetectionStatus.NO_POSE;
              message = 'No pose detected';
          }

          setResult({ status, message, confidence: data.confidence, pose_name: data.pose_name });
        }
      } catch (error) {
        console.error('WebSocket message error:', error);
      }
    };

    const playAudio = (base64Audio: string) => {
      try {
        if (!audioRef.current) {
          audioRef.current = new Audio();
        }
        audioRef.current.src = `data:audio/mp3;base64,${base64Audio}`;
        audioRef.current.play().catch(err => console.error('Audio playback error:', err));
      } catch (error) {
        console.error('Audio creation error:', error);
      }
    };

    ws.onerror = () => {
      setResult({
        status: DetectionStatus.INITIALIZING,
        message: 'Connection error - retrying...'
      });
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  const sendInit = (mode: 'single' | 'routine', asanaIds: number[], routineName?: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const message = JSON.stringify({
        type: 'init',
        mode,
        asanaIds,
        routineName
      });
      wsRef.current.send(message);
    }
  };

  const sendFrame = (imageData: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const message = JSON.stringify({
        imageData
      });
      wsRef.current.send(message);
    }
  };

  return { result, isConnected, sendFrame, sendInit };
}
