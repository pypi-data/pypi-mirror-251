import torch
import os
import torch.nn as nn
from standup_face_recognition.facenet_pytorch import InceptionResnetV1


class Siamese:
    def __init__(self):
        Siamese_network = InceptionResnetV1(pretrained='vggface2')
        script_dir = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(script_dir, "20180402-114759-vggface2.pt")

        checkpoint = (torch.load(model_path))
        Siamese_network.load_state_dict(checkpoint)
        Siamese_network = Siamese_network.cuda()
        Siamese_network.eval()
        self.Siamese_network = Siamese_network
        self.cos = nn.CosineSimilarity(dim=1, eps=1e-6)
        team_embedding_path = os.path.join(script_dir, "team_embedding.pth")
        self.team_embedding = (torch.load(team_embedding_path))

    def face_recognition(self, detected_face, names):  # temp

        for det_face in detected_face[0]:
            similarity_list = []
            # embedding_list = []
            embedding1 = self.Siamese_network(det_face.permute(2, 0, 1).unsqueeze(0))
            for index, name in enumerate(names):
            #  for index, t in enumerate(temp.items()):
                # embedding2 = self.Siamese_network(t[1])
                # embedding_list.append(embedding2)
                cosine_similarity = self.cos(embedding1, self.team_embedding[index]).item()
                similarity_list.append({name: cosine_similarity})
            # torch.save(embedding_list, '/home/timo/pip_installable/standup-face-recognition/standup_face_recognition/team_embedding_webcam.pth')
            detected_face.append(similarity_list)
        return detected_face
