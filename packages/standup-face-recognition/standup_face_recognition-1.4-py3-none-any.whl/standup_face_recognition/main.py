import cv2
from standup_face_recognition.MTCNN_detector import MTCNN_detector
from face_recognition import Siamese
from utils import imread_templates, resize_images_tensor, show_face, standup_roulette


if __name__ == '__main__':
    # template_dict = imread_templates('/home/timo/face_recognition/team_images')
    names = ['Nitin', 'Timo', 'Hiep', 'Robert', 'Martin', 'Kai', 'Bharat', 'Markus', 'Karl', 'Matthias']
    order_person = ['Timo', 'Bharat', 'Martin', 'Matthias', 'Kai', 'Robert', 'Nitin', 'Hiep', 'Karl']
    person, direction = standup_roulette(names)
    person = 'Karl'
    # face recognition
    face_recognition = Siamese()
    # Open a connection to the webcam (0 represents the default camera)
    cap = cv2.VideoCapture(0)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('/home/timo/face_recognition/output.mp4', fourcc, 20.0, (640, 480))

    # Check if the webcam opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    counter = 0
    smooth_filter = 5
    # moving_avg_faces = []
    moving_avg_faces = 0.0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        counter += 1
        if counter % smooth_filter == 0:
            counter = 1
            moving_avg_faces = 0.0

        # Check if the frame was successfully captured
        if not ret:
            print("Error: Could not read frame.")
            break

        # MTCNN face detector
        MTCNN_face_detector = MTCNN_detector()
        detected_faces_mtcnn = MTCNN_face_detector.get_bbox_detection(frame)

        if detected_faces_mtcnn[0][0] is not None:
            # resize for face_recognition model
            resized_faces = resize_images_tensor(detected_faces_mtcnn, 128)

            moving_avg_faces = [0.0] * len(resized_faces[0])
            for ind, tensor_faces in enumerate((resized_faces[0])):
                moving_avg_faces[ind] = (moving_avg_faces[ind] + tensor_faces) / counter

            if counter % (smooth_filter-1) == 0:
                avg_faces = [moving_avg_faces]
                avg_faces.extend(resized_faces[1:])
                # MTCNN_face_detector.visualize_face_detection(frame, resized_faces)qn
                face_det_reg = face_recognition.face_recognition(avg_faces, names)

                show_face(frame, face_det_reg, person, direction)
        else:
            cv2.imshow('Webcam output', frame)

        # cv2.imwrite('/home/timo/face_recognition/webcam_images/frame.png', frame)
        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('n'):
            person_ind = order_person.index(person)
            if direction is 'clockwise':
                person = order_person[(person_ind + 1) % len(order_person)]
            else:
                person = order_person[(person_ind - 1) % len(order_person)]

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    # out.release()
    cv2.destroyAllWindows()
