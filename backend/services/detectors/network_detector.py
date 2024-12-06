from typing import List, Dict
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from ..models.network_pattern import NetworkPattern

class NetworkDetector:
    def __init__(self):
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.patterns: List[NetworkPattern] = []

    async def analyze_traffic(self, traffic_data: Dict) -> List[Dict]:
        """Analyze network traffic for suspicious patterns"""
        features = self._extract_features(traffic_data)
        predictions = self.classifier.predict_proba(features)
        return self._generate_alerts(predictions, traffic_data)

    def _extract_features(self, traffic_data: Dict) -> np.ndarray:
        """Extract relevant features from network traffic"""
        features = []
        for packet in traffic_data['packets']:
            features.append([
                packet['size'],
                packet['protocol'],
                packet['port'],
                packet['frequency']
            ])
        return np.array(features)

    def _generate_alerts(self, predictions: np.ndarray, traffic_data: Dict) -> List[Dict]:
        """Generate alerts based on predictions"""
        alerts = []
        for pred, packet in zip(predictions, traffic_data['packets']):
            if pred[1] > 0.8:  # High probability of malicious traffic
                alerts.append({
                    'type': 'NETWORK_ANOMALY',
                    'confidence': float(pred[1]),
                    'source': packet['source'],
                    'destination': packet['destination'],
                    'protocol': packet['protocol']
                })
        return alerts