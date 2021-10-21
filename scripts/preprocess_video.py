import argparse
import cv2
import glob
import os
import time


def calc_frame_range(skip, length, gap, idx, fps):
    start_frame = (skip + idx * (length + gap)) * fps
    end_frame = start_frame + length * fps
    return (start_frame, end_frame)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='', help='Input video')
    parser.add_argument('--output', type=str, default='', help='Output video')
    parser.add_argument('--sample_length', type=int, default=10, help='The length of sample')
    parser.add_argument('--sample_gap', type=int, default=300, help='The gap between samples')
    parser.add_argument('--sample_num', type=int, default=0, help='The number of samples')
    parser.add_argument('--begin_skip', type=int, default=0, help='Skip from begin')
    args = parser.parse_args()

    video_capture = cv2.VideoCapture(args.input)

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print("FPS:", fps)
    print("Width:", width)
    print("Height:", height)

    #fourcc意为四字符代码（Four-Character Codes），顾名思义，该编码由四个字符组成,下面是VideoWriter_fourcc对象一些常用的参数，注意：字符顺序不能弄混
    #cv2.VideoWriter_fourcc('I', '4', '2', '0'),该参数是YUV编码类型，文件名后缀为.avi
    #cv2.VideoWriter_fourcc('P', 'I', 'M', 'I'),该参数是MPEG-1编码类型，文件名后缀为.avi
    #cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'),该参数是MPEG-4编码类型，文件名后缀为.avi
    #cv2.VideoWriter_fourcc('T', 'H', 'E', 'O'),该参数是Ogg Vorbis,文件名后缀为.ogv
    #cv2.VideoWriter_fourcc('F', 'L', 'V', '1'),该参数是Flash视频，文件名后缀为.flv
    size = (int(width), int(height))
    video_writer = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*'MJPG'), fps, size)

    sample_idx = 0
    start_frame, end_frame = calc_frame_range(args.begin_skip,
        args.sample_length,
        args.sample_gap,
        sample_idx,
        fps)

    frame_idx = 0
    success, frame_src = video_capture.read()
    while success and sample_idx <= args.sample_num:
        if frame_idx >= start_frame and frame_idx <= end_frame:
            cv2.imshow('frame', frame_src)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            video_writer.write(frame_src)
        elif frame_idx > end_frame:
            sample_idx += 1
            start_frame, end_frame = calc_frame_range(args.begin_skip,
                args.sample_length,
                args.sample_gap,
                sample_idx,
                fps)
        # Read frame
        success, frame_src = video_capture.read()
        frame_idx += 1

    video_capture.release()
    video_writer.release()

if __name__ == '__main__':
    main()
