import gstgva  # pylint: disable=import-error
import numpy as np
import math
import copy
import json
from munkres import Munkres
import os

class PeopleCounting:

    def __init__(self):
        # Array of Gallery Objects - {embeddings(numpy array), timestamp}
        self.identities = []
        self.reid_threshold = 0.7
        self.matcher = Munkres()
        self.timestamp = 0

    def process_frame(self, frame):
        messages = list(frame.messages())
        if len(messages) > 0:
            json_msg = json.loads(messages[0])
            json_msg["count"] = {"people": len(self.identities)}
            self.timestamp = int(json_msg["timestamp"]) / 1000000000
            frame.remove_message(messages[0])
            frame.add_message(json.dumps(json_msg))

        self.get_ids_by_embeddings(frame)
        return True

    @staticmethod
    def compute_reid_distance(test_embedding, reference_embedding):
        xx = np.dot(test_embedding, test_embedding)
        yy = np.dot(reference_embedding, reference_embedding)
        xy = np.dot(test_embedding, reference_embedding)
        norm = math.sqrt(xx * yy) + 1e-6
        return np.float32(1.0) - xy / norm

    def get_ids_by_embeddings(self, frame):
        detected_tensors = []
        detection_ids = []
        detections = [x for x in frame.regions()]
        for i, detection in enumerate(detections):
            if detection.label() == "person":
                for j, tensor in enumerate(detection.tensors()):
                    if tensor.name() == "face_feature" and tensor.format() == "cosine_distance":
                        detected_tensors.append(tensor.data())
                        detection_ids.append(i)

        if len(detected_tensors) == 0:
            return
        if len(self.identities) == 0:
            for i in range(len(detected_tensors)):
                self.identities.append({"embedding": copy.deepcopy(
                    detected_tensors[i]), "timestamp": self.timestamp})
            return
        distances = np.empty(
            [len(detected_tensors), len(self.identities)], dtype=np.float32)

        for i in range(len(detected_tensors)):
            for j in range(len(self.identities)):
                distances[i][j] = PeopleCounting.compute_reid_distance(
                    detected_tensors[i], self.identities[j]["embedding"])

        matched_indexes = self.matcher.compute(distances.tolist())
        matched_detections = set()

        for match in matched_indexes:
            if distances[match[0]][match[1]] <= self.reid_threshold:
                self.identities[match[1]]["timestamp"] = self.timestamp
                matched_detections.add(match[0])

        for i in range(len(detected_tensors)):
            if i not in matched_detections:
                self.identities.append({"embedding": copy.deepcopy(
                    detected_tensors[i]), "timestamp": self.timestamp})

        n = len(self.identities)
        i = n - 1
        while i >= 0:
            # overdue if pass the last 5 seconds
            if int(self.timestamp - int(self.identities[i]["timestamp"])) > 5:
                self.identities[i] = self.identities[n - 1]
                self.identities.pop(n - 1)
                n -= 1
            i -= 1
