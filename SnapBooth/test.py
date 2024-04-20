import cv2
import numpy as np   

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    
     # Flip the frame horizontally to remove mirroring
    frame = cv2.flip(frame, 1)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    kernel = np.array([[0.393, 0.769, 0.189],
                       [0.349, 0.686, 0.168],
                       [0.272, 0.534, 0.131]])
    sepia = cv2.transform(frame.astype(np.float32), kernel)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_frame[:, :, 1] = hsv_frame[:, :, 1] * 1.2
    hsv_frame[:, :, 2] = hsv_frame[:, :, 2] * 0.6
    noir = cv2.cvtColor(hsv_frame, cv2.COLOR_HSV2BGR)
    
    edges = cv2.Canny(frame, 100, 200)
    reduced_color = cv2.bilateralFilter(frame, 9, 75, 75)
    num_colors = 64  
    levels = num_colors - 1
    reduced_color = cv2.equalizeHist(gray)
    comic = cv2.bitwise_and(reduced_color, reduced_color, mask=edges)
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_frame[:, :, 1] = hsv_frame[:, :, 1] * 0.8  
    vintage = cv2.cvtColor(hsv_frame, cv2.COLOR_HSV2BGR)
    noise_strength = 0.02  
    vintage = vintage + np.random.uniform(-noise_strength, noise_strength, vintage.shape).astype('uint8')
    kernel_size = (3, 3) 
    vintage = cv2.blur(vintage, kernel_size)
    
    cv2.imshow('Normal Camera', frame)
    cv2.imshow('Sepia', sepia)
    cv2.imshow('Noir', noir)
    cv2.imshow('Comic', comic)
    cv2.imshow('Vintage', vintage)
    cv2.imshow('BMW', gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()































# import cv2

# cap = cv2.VideoCapture(1)

# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
    
# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
    
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break

#     # Display the resulting frame
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('Video Cam', gray_frame)

#     # Break the loop when 'q' is pressed
#     if cv2.waitKey(1) == ord('q'):
#         break

# # When everything is done, release the capture
# cap.release()
# cv2.destroyAllWindows()
