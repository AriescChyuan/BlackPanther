import cv2

tracker = cv2.TrackerKCF_create()
tracking = False
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Can't open camera")
    exit()

while True:
    ret, frame = cap.read()
    # cv2.imshow("test",frame)

    keyName = cv2.waitKey(1)

    if keyName == ord('q'):
        break
    if keyName == ord('a'):
        area = cv2.selectROI('get you', frame, showCrosshair=False, fromCenter=False)
        tracker.init(frame, area)
        tracking = True
    if tracking:
        success, point =tracker.update(frame)

        if success:
            print(point)
            p1 = [int(point[0]), int(point[1])]
            p2 = [int(point[0]+point[2]), int(point[1]+point[3])]
            cv2.rectangle(frame, p1, p2, (255,0,0),3)
    cv2.imshow('hi', frame)
cap.release()
cv2.destroyALLWindows()


