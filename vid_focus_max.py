import cv2


# Open Video
vid = cv2.VideoCapture('guvcview_video-65.mkv')

# Text Details
coor_var = (30, 90)
coor_frame = (30, 50)
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
colour = (0, 255, 0)
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

# Variable for finding max var frame
max = -1
fr_no = 0
max_fr = -1

# Close Video
out = cv2.VideoWriter('output.mp4',
                      cv2.VideoWriter_fourcc(*'MP4V'),
                      30, size)


# Video Processing
while (vid.isOpened()):
    rec, frame = vid.read()

    fr_no += 1

    if rec:
        crp = frame[y1:y2, x1:x2]
        gray = cv2.cvtColor(crp, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        var = round(lap.var(), 2)

        if (max < var):
            max = var
            max_fr = fr_no

        cv2.putText(frame, "Frame: " + str(fr_no), coor_frame, font,
                    font_scale, colour, thickness)
        cv2.putText(frame, "Variance: " + str(var), coor_var, font,
                    font_scale, colour, thickness)
        fm_rec = cv2.rectangle(frame, (x1, y1), (x2, y2),
                               colour_rec, thick_rec)

        out.write(fm_rec)
        cv2.imshow("Video", fm_rec)
    else:
        break

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Print Result and Exit
print(max_fr)
vid.release()
out.release()
cv2.destroyAllWindows()
