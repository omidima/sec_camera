from tkinter import *
import cv2
import os

class gui():

    def __init__(self):
        self.root=Tk()
        master=self.root
        self.root.title('چک کردن ویدیو دوربین مدار بسته')
        self.root.geometry("400x400+20+20")
        self.path=""
        self.noise=500
        self.save="c:/video"
        self.target=0
        self.contract1=0
        self.contract2=0
        self.contract3=0
        self.element

    def element(self):
        master=self.root
        Label(self.root, text="آدرس ویدیو را وارد کنید",bg="blue", fg="white").grid(row=0, column=1,sticky=W, pady=4)
        self.path = Entry(master)
        self.path.insert(10,"address")
        self.path.grid(row=0,column=0,sticky=W, pady=4) 

        Label(self.root, text="میزان نویز",bg="blue", fg="white").grid(row=2, column=1,sticky=W, pady=4)
        self.noise = Entry(master)
        self.noise.insert(10,"noise")
        self.noise.grid(row=2,column=0,sticky=W, pady=4) 

        Label(self.root, text="میزان دقت برنامه",bg="blue", fg="white").grid(row=3, column=1,sticky=W, pady=4)
        self.target = Entry(master)
        self.target.insert(10,"target")
        self.target.grid(row=3,column=0,sticky=W, pady=4) 

        Label(self.root, text=" :تنظیمات کنتراست",bg="#e1e2e3", fg="#454545").grid(row=4, column=1,sticky=W, pady=4)
        Label(self.root, text="میزان کنتراست آبی",bg="blue", fg="white").grid(row=5, column=1,sticky=W, pady=4)
        self.contract1 = Entry(master)
        self.contract1.insert(10,"contract")
        self.contract1.grid(row=5,column=0,sticky=W, pady=4) 
        Label(self.root, text="میزان کنتراست سبز",bg="blue", fg="white").grid(row=6, column=1,sticky=W, pady=4)
        self.contract2 = Entry(master)
        self.contract2.insert(10,"contract")
        self.contract2.grid(row=6,column=0,sticky=W, pady=4) 
        Label(self.root, text="میزان کنتراست قرمز",bg="blue", fg="white").grid(row=7, column=1,sticky=W, pady=4)
        self.contract3 = Entry(master)
        self.contract3.insert(10,"contract")
        self.contract3.grid(row=7,column=0,sticky=W, pady=4) 

        Button(self.root, text='نمایش', command=self.worker,bg='green', fg='white').grid(row=8, column=1, sticky=W, pady=4)
        Button(self.root, text='خروج', command=self.root.quit,bg='red', fg='white').grid(row=8, column=0, sticky=W, pady=4)

    def filecheck(self):
        try:
            os.chdir('photo')
        except:
            os.mkdir('photo')
            os.chdir('photo')

    def worker(self):
        first_frame = None
        pather=self.path.get()
        our_video = cv2.VideoCapture(pather)
        Counter=0
        a,b,c,d=0,0,0,0
        self.filecheck()
        while True:
            stroot=0
            if our_video.isOpened():
                check, frame = our_video.read()
                our_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                our_frame_gray = cv2.GaussianBlur(our_frame_gray,(int(self.contract1.get())
                                                                ,int(self.contract2.get()))
                                                                ,int(self.contract3.get()))

                if first_frame is None:
                        first_frame=our_frame_gray
                        continue

                delta_frame = cv2.absdiff(first_frame, our_frame_gray)
                first_frame=our_frame_gray
                threshold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
                threshold_frame = cv2.dilate(threshold_frame, None, iterations= int(self.target.get()))
                cnts, hierarchy = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in cnts:
                    if cv2.contourArea(contour) > int(self.noise.get()) :
                        x, y, w, h = cv2.boundingRect(contour)
                        if a==x and b==y and c==w and d==h:
                            continue
                        a,b,c,d = x,y,w,h
                        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 1)
                        stroot=1
                        
                    else:
                        continue
                        
                        
                if stroot ==1 :
                    cv2.imwrite('photo'+str(Counter) + ".jpg", frame)
                cv2.imshow('threshold_frame', threshold_frame)
                # cv2.imshow('Video2', frame)

                Counter+=1
                key = cv2.waitKey(1)
                if(key == ord('q')):
                    cv2.destroyAllWindows()
                    break
            else:
                our_video.open(pather)
        cv2.destroyAllWindows()


def main():
    guiForm = gui()
    guiForm.element()
    mainloop()
 
#.................................................  .......................
if __name__ == '__main__':
    main()


        
        
