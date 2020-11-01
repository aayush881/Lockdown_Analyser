from tkinter import *

class App():
    def __init__(self, root):
        self.root = root


        # Set grid_propagate to False to allow 5-by-5 buttons resizing later



        self.root.geometry("900x500")
        self.root.title("Lockdown Analyser")
        self.BottomFrame = Frame(root,bg="green")
        self.v=8
        self.BottomFrame.grid(row=0,column=3,ipadx=20,ipady=100)
        self.arr = [[0 for i in range(4)] for j in range(4)]
        self.jk=1000000
        self.kk = 1000000
        self.infected=0
        self.a=-1
        self.b=-1
        self.grid = []
        self.arr=[]
        for i in range(4):
            res=[]
            for j in range(4):
                res.append(0)
            self.arr.append(res)
        buttonQ = Button(self.BottomFrame,bg="red",fg="white", padx=40,pady=10,text="Quit",font="10,bold", command=quit,relief=SUNKEN)
        buttonS = Button(self.BottomFrame,bg="magenta3",fg="white",font="8,bold", padx=40,pady=10,text="Save",command=self.saveToFile(),relief=SUNKEN)
        buttonS.grid(row=0, column=0, padx=40,pady=20)
        buttonQ.grid(row=1, column=0, padx=20,pady=20)

    def getClick1(self, i, j):
        orig_color = self.grid[i][j].cget("bg")
        self.arr[i][j]=1
        self.infected += 1
        print('$')
        if orig_color=="turquoise":
            self.grid[i][j]["bg"]="red"
            self.grid[i][j]["fg"] = "white"

    def containVirus(self):
        d = ((0, 1), (0, -1), (1, 0), (-1, 0))

        def in_grid(i, j):
            return not (i < 0 or j < 0 or i >= 4 or j >= 4)

        def dfs(i, j, res, visited):
            for di, dj in d:
                ci, cj = i + di, j + dj
                if not in_grid(ci, cj) or self.arr[ci][cj] != 1 or (ci, cj) in visited:
                    continue
                res.add((ci, cj))
                visited.add((ci, cj))
                dfs(ci, cj, res, visited)

        def get_groups():
            groups = []
            visited = set()
            for i in range(4):
                for j in range(4):
                    if self.arr[i][j] == 1 and (i, j) not in visited:
                        group = set()
                        group.add((i, j))
                        dfs(i, j, group, visited)
                        groups.append(group)
            return groups

        def affected_cells(group):
            res = set()
            for i, j in group:
                for di, dj in d:
                    ci, cj = i + di, j + dj
                    if not in_grid(ci, cj) or self.arr[ci][cj] > 0:
                        continue
                    res.add((ci, cj))
            return len(res)

        def build_walls(group, new_v):
            res = 0
            for i, j in group:
                for di, dj in d:
                    ci, cj = i + di, j + dj
                    if not in_grid(ci, cj) or self.arr[ci][cj] > 0:
                        continue
                    res += 1
                self.arr[i][j] = new_v
            return res

        group_index = 2
        walls_count = 0

        def expand_groups(groups):
            cur = []
            for g in groups:
                for i, j in g:
                    cur.append((i, j))
            for i, j in cur:
                for di, dj in d:
                    ci, cj = i + di, j + dj
                    if not in_grid(ci, cj) or self.arr[ci][cj] > 0:
                        continue

                    self.arr[ci][cj] = 1
                    #self.infected+=1;
                    self.getClick1(ci,cj)

        while True:
            cur_groups = get_groups()
            if not cur_groups:
                break
            max_group = max(cur_groups, key=affected_cells)

            walls_count += build_walls(max_group, group_index)
            cur_groups.remove(max_group)
            if not cur_groups:
                break
            expand_groups(cur_groups)

            group_index += 1

        print(walls_count)



    def findPaths(self,path, i, j, vis,ans):

        if vis[i][j] == 1:
            return
        (M, N) = (4,4)
        res = []
        # if we have reached the last cell, print the route
        if i == M - 1 and j == N - 1:
            # we need to perform some task out here
            res.extend(path)
            res.append((i,j))
            c=0
            #print(res)
            #print(res)
            for x,y in res:
                if self.arr[x][y]!=0:
                    c+=1
            #print(c)
            if c==self.infected and len(res)<self.jk:
                self.jk=len(res)
                ans.clear()
                ans.append(res)
            return

        # include current cell in path
        path.append((i,j))
        vis[i][j] = 1
        # move right
        if 0 <= i < M and 0 <= j + 1 < N:
            self.findPaths(path, i, j + 1, vis,ans)
        # move down
        if 0 <= i + 1 < M and 0 <= j < N:
            self.findPaths(path, i + 1, j, vis,ans)
        if 0 <= i - 1 < M and 0 <= j < N:
            self.findPaths(path, i - 1, j, vis,ans)
        if 0 <= i < M and 0 <= j - 1 < N:
            self.findPaths(path, i, j - 1, vis,ans)
        # remove current cell from path
        vis[i][j] = 0
        path.pop()

    def Function(self):
        for i in range(4):
            row = []
            #res = []
            for j in range(4):
                #res.append(0)
                row.append(Button(frame, fg="dark blue",width=5, height=2,font="10,bold",command=lambda i=i, j=j: self.getClick(i, j),
                                  bg='turquoise',
                                  text=f"{chr(i + ord('A'))}{j + 1}"))

                row[-1].grid(row=i+1, column=j,padx=10,pady=10)


            self.grid.append(row)

        #self.grid[3][3]["bg"] = "purple"
        #self.grid[3][3]["fg"] = "white"
            #self.arr.append(res)

        btn = Button(self.BottomFrame,padx=40,pady=10,font="10,bold",bg="yellow2",text="Analyse", command=lambda : self.containVirus(),relief=SUNKEN)
        btn.grid(row=2, column=0, padx=20,pady=20)
        btnp = Button(self.BottomFrame,padx=40,pady=10,font="10,bold",bg="spring green",text="PCR", command=lambda : self.pcr(),relief=SUNKEN)
        btnp.grid(row=3, column=0, padx=20,pady=20)
        btnp = Button(self.BottomFrame,padx=40,pady=10,font="10,bold",bg="spring green", text="TRANSPORT", command=lambda: self.call(),relief=SUNKEN)
        btnp.grid(row=4, column=0, padx=20,pady=20)


    def getClick(self,i, j):
        origcolor = self.grid[i][j].cget('bg')
        self.arr[i][j]=1
        self.infected += 1
        self.grid[i][j]["bg"]="red"
        self.grid[i][j]["fg"] = "white"
    def saveToFile(self):
        myFile=open("xyzn.txt", 'w')
        for i in range(4):
            for j in range(4):
                if self.arr[i][j]==0:
                    myFile.write("0")
                else:
                    myFile.write("1")
            myFile.write("\n")
        #myFile.flush()
        myFile.close()
        myFile = open("xyzn.txt",'r')
        print(myFile.read())
        myFile.close()

    def color(self,ans,tc):
        grid1 = []
        if (tc==1):
            gh="PCR"
            c="yellow"
            f="brown4"
        else:
            gh="T"
            c="brown4"
            f="white"
        print(self.v)
        l=Label(frame,text=gh,fg=f,bg=c,font="bold")
        l.grid(row=self.v-2,column=0,padx=10,ipady=10,pady=10)
        l1= Label(frame, text=gh, fg=f, bg=c,font="bold")
        l1.grid(row=self.v-2, column=1, padx=10,ipady=10,pady=10)
        l2 = Label(frame, text=gh, fg=f, bg=c,font="bold")
        l2.grid(row=self.v-2, column=2, padx=10,ipady=10,pady=10)
        l3= Label(frame, text=gh, fg=f, bg=c,font="bold")
        l3.grid(row=self.v-2, column=3, padx=10,ipady=10,pady=10)
        for i in range(4):
            row = []
            for j in range(4):
                if len(ans)==0:
                    xc="turquoise"
                elif tuple((i,j)) in ans[0]:
                    print(i,j)
                    xc="lawngreen"
                else:
                    xc="turquoise"
                row.append(Button(frame,width=6, height=3, background=xc,
                                  text=f"{chr(i + ord('A'))}{j + 1}"))

                row[-1].grid(row=i+self.v,column=j,padx=10,pady=10)
            grid1.append(row)
        if tc==1:
            grid1[3][3]["bg"] = "purple"
            grid1[3][3]["fg"] = "white"
            grid1[3][3]["border"] = "10"
        self.v+=8

    def findPaths1(self,path, i, j, y1,y2,vis, ans):

        if vis[i][j] == 1 or self.arr[i][j]!=0:
            return
        (M, N) = (4, 4)
        res = []
        # if we have reached the last cell, print the route
        if i == y1 and j ==y2:
            # we need to perform some task out here
            res.extend(path)
            res.append((i, j))
            c = 0
            # print(res)
            # print(res)
            if len(res) < self.kk:
                self.kk = len(res)
                ans.clear()
                ans.append(res)
            return

        # include current cell in path
        path.append((i, j))
        vis[i][j] = 1
        # move right
        if 0 <= i < M and 0 <= j + 1 < N:
            self.findPaths1(path, i, j + 1,y1,y2, vis, ans)
        # move down
        if 0 <= i + 1 < M and 0 <= j < N:
            self.findPaths1(path, i + 1, j,y1,y2, vis, ans)
        if 0 <= i - 1 < M and 0 <= j < N:
            self.findPaths1(path, i - 1, j,y1,y2, vis, ans)
        if 0 <= i < M and 0 <= j - 1 < N:
            self.findPaths1(path, i, j - 1, y1,y2,vis, ans)
        # remove current cell from path
        vis[i][j] = 0
        path.pop()

    def submit(self,srcentry,dstentry,srcval,dstval):
        s = srcentry.get()
        d = dstentry.get()
        x1=-1
        x2=-1
        y1=-1
        y2=-1
        for i in range(4):
            for j in range(4):
                my_text = self.grid[i][j].cget('text')
                if (my_text==s):
                    x1=i
                    x2=j
                if (my_text==d):
                    y1=i
                    y2=j
        print(f"The Source Region is :{x1,x2} ")
        print(f"The Destination Region is : {y1,y2}")
        vis = [[False for col in range(4)] for row in range(4)]
        path=[]
        ans=[]
        for i in range(4):
            for j in range(4):
                print(self.arr[i][j],end=' ')
            print()
        self.findPaths1(path,x1,x2,y1,y2,vis,ans)
        print(ans)
        if len(ans)==0 or x1==-1 or x2==-1 or y1==-1 or y2==-1:
            print("No path exists!!")
            l=Label(frame,text="No path exists",font="45")
            l.grid(row=9,column=0)

        else:
            tc=2
            self.color(ans,tc)
        self.kk = 1000000

    def resetFun(self,srcentry,dstentry,srcval,dstval):
        srcval.set("")
        dstval.set("")

    def call(self):


        src = Label(self.BottomFrame, text="Source",bg="brown",fg="white")
        dst = Label(self.BottomFrame,text="Destination",bg="brown",fg="white")
        src.grid(row=5, column=0,pady=3)
        dst.grid(row=6, column=0,pady=3)
        srcval = StringVar()
        dstval = StringVar()
        srcentry = Entry(self.BottomFrame,textvariable=srcval,bg="green yellow")
        dstentry = Entry(self.BottomFrame,textvariable=dstval,bg="green yellow")
        srcentry.grid(row=5, column=1)
        dstentry.grid(row=6, column=1)
        sub = Button(self.BottomFrame,text="Submit",bg="DarkGoldenrod1",command= lambda:self.submit(srcentry,dstentry,srcval,dstval))
        sub.grid(row=7, column=1,pady=3)
        reset = Button(self.BottomFrame,bg="DarkGoldenrod1",text="Reset Values!",command= lambda:self.resetFun(srcentry,dstentry,srcval,dstval))
        reset.grid(row=8, column=1,pady=3)




    def pcr(self):
        x = y = 0
        ans=[]
        path = []
        print(self.infected)
        vis = [[False for col in range(4)] for row in range(4)]
        self.findPaths(path, x, y, vis,ans)
        self.jk = 1000000
        print(ans)
        tc=1
        self.color(ans,tc)

            #if c == self.infected:
                #funPath(ans[i])

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=400,height=500)

root = Tk()
l=Label(root,fg="brown4",bg="yellow",font=("Calbri 10 bold"),text="INTRUCTIONS:\n\n1. Press 'ANALYSE' for border locks."
                                                                  "\n2.Press 'PCR' for find path for PCR van\n"
                                                                  "3. Press 'TRANSPORT' for knowing status of delivery of goods."
                                                                  "\n4.PRESS 'QUIT' for exit")
l.grid(row=0,column=0,ipady=80,padx=20)
sizex = 800
sizey = 600
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
myframe=Frame(root,relief=SUNKEN,width=1000,height=1000,bd=1,bg="pink")
myframe.grid(row=0,column=1)
canvas=Canvas(myframe,bg="ivory4")
frame=Frame(canvas,bg="ivory4",padx=20,pady=20,relief=GROOVE)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)



myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left",ipadx=20, ipady=20)
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)

app = App(root)
app.Function()

root.mainloop()
