% code for make a video.

clc;
myObj = VideoWriter('newfile.mp4','MPEG-4');%��ʼ��һ��mp4�ļ�
myObj.FrameRate = 30;
open(myObj);

nFrames=66;
for i=0:nFrames
    fname=strcat('H:/matlab/matlabCode/3DHumanPose-master/result/image',num2str(i),'.jpg');
    frame = imread(fname);
    writeVideo(myObj,frame);
end 
close(myObj);