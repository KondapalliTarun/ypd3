import { useEffect, useRef, useState } from 'react';
import { DetectionStatus, DetectionResult } from '../types';

export function useWebSocket(url: string) {
  const [result, setResult] = useState<DetectionResult>({
    status: DetectionStatus.INITIALIZING,
    message: 'Connecting to detection server...'
  });
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

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

        if (data.data !== undefined) {
          let status: DetectionStatus;
          let message: string;

          switch (data.data) {
            case 0:
              status = DetectionStatus.NO_POSE;
              message = 'No pose detected - step into frame';
              break;
            case 1:
              status = DetectionStatus.INCORRECT;
              message = data.message || 'Incorrect pose - adjust your position';
              break;
            case 2:
              status = DetectionStatus.CORRECT;
              message = data.message || "Perfect! You're doing great!";
              break;
            case 3:
              status = DetectionStatus.PARTIAL;
              message = data.message || 'Almost there - minor adjustments needed';
              break;
            case 4:
              status = DetectionStatus.NEXT_POSE;
              message = data.message || 'Moving to next pose';
              break;
            case 5:
              status = DetectionStatus.SEQUENCE_COMPLETE;
              message = 'Routine completed!';
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

  const sendFrame = (imageData: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const message = JSON.stringify({
        imageData
      });
      wsRef.current.send(message);
    }
  };

  return { result, isConnected, sendFrame };
}
