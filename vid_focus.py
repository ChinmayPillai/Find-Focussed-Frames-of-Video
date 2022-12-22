import cv2


# Open Video
vid = cv2.VideoCapture('guvcview_video-65.mkv')

# Text Details
coor_focus = (30, 50)
coor_var = (30, 90)
coor_diff = (30, 130)
coor_thresh = (30, 170)
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (0, 255, 0)
thickness = 2

frame_width = int(vid.get(3))
frame_height = int(vid.get(4))
size = (frame_width, frame_height)

# Focus Rectangle Details
x1 = 280
x2 = 480
y1 = 230
y2 = 330
colour_rec = (255, 0, 0)
thick_rec = 1

# Max and Min var initialisation
min = 9e9
max = -1


# Find max and min var
while (vid.isOpened()):
    rec, frame = vid.read()

    if rec:
        crp = frame[y1:y2, x1:x2]
        gray = cv2.cvtColor(crp, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        var = lap.var()

        if (max < var):
            max = var

        if (var < min):
            min = var

    else:
        break


# Set threshold, close and reopen video
threshold = round((max + min) / 2, 2)
vid.release()
vid = cv2.VideoCapture('guvcview_video-65.mkv')
out = cv2.VideoWriter('output.mp4',
                      cv2.VideoWriter_fourcc(*'MP4V'),
                      30, size)

# Video Processing
while (vid.isOpened()):
    rec, frame = vid.read()

    if rec:
        crp = frame[y1:y2, x1:x2]
        gray = cv2.cvtColor(crp, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        var = round(lap.var(), 2)
        diff = round(var - threshold, 2)

        if (diff > 0):
            text = "Focused"
        else:
            text = "Unfocused"

        cv2.putText(frame, text, coor_focus, font,
                    font_scale, color, thickness)
        cv2.putText(frame, "Variance: " + str(var), coor_var, font,
                    font_scale, color, thickness)
        cv2.putText(frame, "Diff: " + str(diff), coor_diff, font,
                    font_scale, color, thickness)
        # cv2.putText(frame, "Threshold: " + str(threshold), coor_thresh, font,
        #            font_scale, color, thickness)

        fm_rec = cv2.rectangle(frame, (x1, y1), (x2, y2),
                               colour_rec, thick_rec)

        out.write(fm_rec)
        cv2.imshow("Video", frame)
    else:
        break

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break


# Close everything
vid.release()
out.release()
cv2.destroyAllWindows()
