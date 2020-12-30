
import os

class IOUTracker(object):
    def __init__(self,sigma_l=0,sigma_h=0.5,sigma_iou=0.5,t_min=2):
        super(IOUTracker, self).__init__()

        self.tracks_active = []
        self.tracks_finished = []
        self.track_id=0
        self.sigma_l=sigma_l
        self.sigma_h=sigma_h
        self.sigma_iou=sigma_iou
        self.t_min=t_min

    def iou(self, bbox1, bbox2):
        bbox1 = [float(x) for x in bbox1]
        bbox2 = [float(x) for x in bbox2]

        (x0_1, y0_1, x1_1, y1_1) = bbox1
        (x0_2, y0_2, x1_2, y1_2) = bbox2
        # get the overlap rectangle
        overlap_x0 = max(x0_1, x0_2)
        overlap_y0 = max(y0_1, y0_2)
        overlap_x1 = min(x1_1, x1_2)
        overlap_y1 = min(y1_1, y1_2)
        # check if there is an overlap
        if overlap_x1 - overlap_x0 <= 0 or overlap_y1 - overlap_y0 <= 0:
            return 0
        # if yes, calculate the ratio of the overlap to each ROI size and the unified size
        size_1 = (x1_1 - x0_1) * (y1_1 - y0_1)
        size_2 = (x1_2 - x0_2) * (y1_2 - y0_2)
        size_intersection = (overlap_x1 - overlap_x0) * (overlap_y1 - overlap_y0)
        size_union = size_1 + size_2 - size_intersection
        return size_intersection / size_union

    def track(self, detections, debug=False):
        dets = [det for det in detections if det['confidence'] >= self.sigma_l]
        updated_tracks = []
        new_tracks = []
        for track in self.tracks_active:
            if len(dets) > 0:
                # get det with highest iou
                best_match = max(dets, key=lambda x: self.iou(track['bboxes'][-1], x['bbox']))
                if self.iou(track['bboxes'][-1], best_match['bbox']) >= self.sigma_iou:
                    track['bboxes'].append(best_match['bbox'])
                    track['max_confidence'] = max(track['max_confidence'], best_match['confidence'])
                    track['object_type']=best_match['object_type']
                    track['idx']=best_match['idx']
                    updated_tracks.append(track)
                    if debug: print("keep track: ", track, flush=True)
                    # remove from best matching detection from detections
                    del dets[dets.index(best_match)]

            # if track was not updated
            if len(updated_tracks) == 0 or track is not updated_tracks[-1]:
                # finish track when the conditions are met
                if track['max_confidence'] >= self.sigma_h and len(track['bboxes']) >= self.t_min:
                    self.tracks_finished.append(track)

        # create new tracks
        for det in dets:
            new_tracks = [{'track_id': self.track_id,'bboxes': [det['bbox']], 'max_confidence': det['confidence'], 'object_type': det['object_type'], "idx": det["idx"]}]
            self.track_id=self.track_id+1
            if debug: print("add track: ", new_tracks, flush=True)

        self.tracks_active = updated_tracks + new_tracks
        # finish all remaining active tracks
        self.tracks_finished += [track for track in self.tracks_active
                        if track['max_confidence'] >= self.sigma_h and len(track['bboxes']) >= self.t_min]
        return self.tracks_active
