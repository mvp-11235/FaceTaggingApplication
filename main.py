import math
import os
import sys

import cv2
from PIL import Image
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QGridLayout, QLineEdit, QRadioButton, QMessageBox, QInputDialog


# QWidget 을 상속받아 애플리케이션의 틀 만들기

class MainWindow(QWidget):
# 창의 초기값 설정
   def getPhotoPath(self):
       # QFiledialog를 이용하여 파일 장보 불러오기(경로 추가)
       fname=QFileDialog.getOpenFileName(self, 'Open file')
       # 불러온 사진 파일의 위치를 변수에 저장
       self.imagepath = fname[0]
       # 원본 사진 파일의 위치를 저장
       self.originalpath = fname[0]
       # loadImage 메소드 호출하기
       self.loadImage()
   def loadImage(self):
       #사진을 pixmap객체화
       self.pixmap = QPixmap(self.imagepath)
       #사진 파일의 크기를 원하는 만큼의 크기로 조절하기
       pixmap_resized = self.pixmap.scaled(self.imgwidth, self.imgheight)
       #사진을 QLabel에 그리기
       self.label.setPixmap(pixmap_resized)
   #EditWindow 객체를 새로 만들기
   def createEditingWindow(self):
       self.editwin = EditWindow()
       self.editwin.setWidgets(self)
       self.editwin.show()

   def __init__(self):
       super().__init__()
       self.imgwidth = 600
       self.imgheight = 450
       #창의 초기값 설정
       # 창의 크기, 위치 및 제목과 관련된 코드

       #창의 위치와 크기 정하기 위한 변수
       self.top = 200
       self.left = 500
       self.width = 300
       self.height = 400

       #창의 제목 정해주기
       self.setWindowTitle("사진 속 얼굴 태깅 애플리케이션")
       #창의 위치 및 크기 정하기
       self.setGeometry(self.left, self.top, self.width, self.height)
       self.delclicked = False
   def setWidgets(self):
       #버튼 만들기
       self.btn1 = QPushButton("이미지 업로드", self)
       #버튼 1 클릭시 getPhotoPath가 실행
       self.btn1.clicked.connect(self.getPhotoPath)
       #버튼 2
       self.btn2 = QPushButton("이미지 편집", self)
       #버튼 2 클릭시 createEditingWindow 메소드가 실행
       self.btn2.clicked.connect(self.createEditingWindow)
       # 버튼 3
       self.btn3 = QPushButton("얼굴 찾기", self)
       # 버튼 3 클릭시 findFace 메소드 실행
       self.btn3.clicked.connect(self.findFace)
       # 버튼 4
       self.btn4 = QPushButton("얼굴 삭제", self)
       # 버튼 4 클릭시 deleteFace 매소드 실행
       self.btn4.clicked.connect(self.delFace)
       #버튼 5
       self.btn5 = QPushButton("얼굴 추가", self)
       # 버튼 5 클릭시 createAddFaceWindow 메소드 실행
       self.btn5.clicked.connect(self.createAddFaceWindow)
       #버튼 6
       self.btn6 = QPushButton("이름 태그", self)
       # 버튼 6 클릭시 createAddFaceWindow 매소드 실행
       self.btn6.clicked.connect(self.createTagNameWindow)

       #버튼의 위치 지정(수직 박스 레이아웃 이용)
       #QVBoxLayout 객체 만들기
       vbox = QVBoxLayout()
       #QVBoxLayout에 위젯 등록하기
       vbox.addWidget(self.btn1)
       vbox.addWidget(self.btn2)
       vbox.addWidget(self.btn3)
       vbox.addWidget(self.btn4)
       vbox.addWidget(self.btn5)
       vbox.addWidget(self.btn6)
       # QVBoxLayout을 위젯화 시키기
       buttons_widget = QWidget()
       buttons_widget.setLayout(vbox)
       #이미지가 업로드될 공간 만들기
       self.label = QLabel("여기에 이미지가 업로드됩니다", self)
       #QHBoxLayout 객체 만들기
       hbox = QHBoxLayout()
       #QLabel을 QHBoxLayout에 등록하기
       hbox.addWidget(self.label)
       #위젯화된 버튼 수직 박스 레이아웃을 QHBoxLayout에 등록하기
       hbox.addWidget(buttons_widget)
       #전체 창을 지정한 Layout을 기반으로 배치(hbox)
       self.setLayout(hbox)

   # openCV를 사용하여 얼굴 위치 찾기
   def findFace(self):
       self.fList = FaceList()
       # face_cascade 라는 변수에 아까 찾아온 XML 로드하기
       face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
       # img 변수에 얼굴을 찾고 싶은 이미지 imread 라는 메소드 사용해서 읽어오기
       img = cv2.imread(self.imagepath, cv2.IMREAD_COLOR)
       img = cv2.resize(img, (self.imgwidth, self.imgheight))
       # 얼굴을 찾기 위해서 원본 이미지를 c vtColor 변환 메소드를 활용하여 흑백으로 변환하기
       gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       faces = face_cascade.detectMultiScale(gray, 1.2, 1).tolist()  # 리스트로 변환
       # face변수에는 검출된 얼굴의 x 좌표, y 좌표 내포하고 있음. 그리고 넓이 w와 높이 h를 포함하고 있음.
       for (x, y, w, h) in faces:
           # 어디에 있는지 터미널에 출력하기
           print(x, y, w, h)
           # fList에 append_face 메소드를 활용해서 찾은 얼굴 좌표 (x, y, w, h) 추가하기
           self.fList.append_face(x, y, w, h)
           # 원본 이미지에 얼굴을 위치를 상자로 표시합니다.
           cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

       # 다시 이미지를 보이기
       self.showImage(img)

   def showImage(self, img):
       # 다시 QImage 형태로 변환해 봅시다
       # img의 넓이, 높이 그리고 색상을 추출하여 height, width, color에 담기
       height, width, colors = img.shape
       bytesPerLine = 3 * width
       # QuGUI에서 QImage 인스턴스 하나 생성
       image = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
       # 기존 RGB 형태를 BGR 형태로 바꿈
       self.image = image.rgbSwapped()
       # 원래 있던 자리에 얼굴 인식한 이미지 올리기
       self.label.setPixmap(QPixmap.fromImage(self.image))

   def delFace(self):
       # 1) 사진이 업로드 되었고
       if self.label.pixmap() == None: # 사진이 업로드 안됨.
           print("사진이 업로드 되지 않았음!")
       # 2) 얼굴이 detect된 상태어야지 지울 수가 있음
       elif self.fList is None or self.fList.count_face() == 0: # 변수 초기화 체크, 얼굴 개수 0개 이상
           print("탐색된 얼굴이 없음!")
       else:
           print("어느 위치를 지우시겠습니까? 원하는 위치에 좌클릭 해주세요.")
           # 얼굴을 지우기 위해서 마우스 클릭이 가능하도록 해주기 위한 boolean 변수 delclicked
           self.delclicked = True
   def mousePressEvent(self, event):
       diag = 10000.0
       # 마우스 클릭 이벤트가 밸생했고, 얼굴이 있는 경우에만 작동하는 매소드.
       if self.delclicked == True:
           print('(%d %d)' % (event.x(), event.y()))
           for i in self.fList.face_list: # 0: x좌표, 1: y좌표, 2: w넓이, 3: 높이
               # 박스의 중심점 좌표 계산.
               centx = i.x + (i.w/2)
               centy = i.y + (i.h/2)
               # 저장된 얼굴 좌표 중심점과 클릭한 위치의 거리를 비교
               if diag > abs(math.sqrt(((centx-event.x())**2)+((centy-event.y())**2))):
                   # 저장된 얼굴 좌표 중심점과 클릭한 위치의 거리를 비교해서 더 작은 경우 diag에 새롭게 저장
                   diag = abs(math.sqrt(((centx-event.x())**2)+((centy-event.y())**2)))
                   # 더 가까운 얼굴 id로 대체
                   faceid = i.id
                   # 마우스 클릭이 얼굴상자 안에서 발생했는지
               if event.x() >= i.x and event.x() <= (i.x + i.w):
                    if event.y() >= i.y and event.y() <= (i.y + i.h):
                        print("removing face id: ", faceid)
                        # 얼굴 id를 기준으로 얼굴 관리 리스트에서 얼굴 정보 제거
                        self.fList.remove_face(faceid)

           # 다시 사진에 그리기 위해 이미지 로딩
           img = cv2.imread(self.imagepath, cv2.IMREAD_COLOR)
           img = cv2.resize(img, (self.imgwidth, self.imgheight))
           # 얼굴 관리 리스트에서 얼굴 정보를 하나씩 가져와서 다시 박스 그리기
           for f in self.fList.face_list:
               # 어디에 있는지 찾아봅시다.
               print(f.x, f.y, f.h, f.name, f.id)
               # 원본 이미지에 얼굴의 위치를 표시합니다.
               cv2.rectangle(img, (f.x, f.y), (f.x + f.w, f.y + f.h), (255, 0, 0), 2)
           # 다시 이미지를 창에 띄우기
           self.showImage(img)
           # 얼굴 삭제 기능 비활성화
           self.delclicked = False

   # AddFaceWindow 창을 띄우기 위한 함수
   def createAddFaceWindow(self):
       self.addfacewin = AddFaceWindow()
       self.addfacewin.setWidgets(self)
       self.addfacewin.show()

   # createTagNameWindow 창을 띄우기 위한 함수
   def createTagNameWindow(self):
       self.tagnamewin = TagNameWindow()
       self.tagnamewin.setWidgets(self)
       self.tagnamewin.show()

#MinWindow를 상속받아 이미지 편집창 틀 만들기
class EditWindow(MainWindow):
 #창의 초기값 설정
    def __init__(self):
        super().__init__()
        #창의 위치와 크기 변화
        self.width = 300
        self.height = 400
        self.setGeometry(self.left, self.top, self.width, self.height)

    def setWidgets(self, mainwindow):
        #QLabel 배치
        self.labelwidth = QLabel("너비 바꾸기")
        #수정할 width 입력란
        self.textwidth = QLineEdit('width', self)
        #QLabel 배치
        self.labelheight = QLabel("높이 바꾸기")
        #수정할 height 입력란
        self.textheight = QLineEdit('height', self)
        #QLabel 배치
        self.labelcolor = QLabel("사진색 바꾸기")

        #RadioButton 배치
        self.radiobtn1 = QRadioButton("원본")
        #처음에 원본에 체크되어 있음
        self.radiobtn1.setChecked(True)
        self.radiochecked = "원본"
        self.radiobtn2 = QRadioButton("회색 계열")
        self.radiobtn3 = QRadioButton("빨간색 계열")
        self.radiobtn4 = QRadioButton("초록색 계열")
        self.radiobtn5 = QRadioButton("파란색 계열")

        # 현재 Radiobutton이 선택되면 btnstate 매소드 호출
        self.radiobtn1.toggled.connect(self.btnstate)
        self.radiobtn2.toggled.connect(self.btnstate)
        self.radiobtn3.toggled.connect(self.btnstate)
        self.radiobtn4.toggled.connect(self.btnstate)
        self.radiobtn5.toggled.connect(self.btnstate)

        #버튼 배치
        self.btnOK = QPushButton('확인', self)
        #확인 버튼 눌렀을 시 QLabel에 수정된 이미지 시각화(객체 전달)
        self.btnOK.clicked.connect(lambda: self.editImage(mainwindow))

        #QVBoxLayout 객체 만들기
        vbox = QVBoxLayout()
        #위젯들을 QVBoxLayout에 등록하기
        vbox.addWidget(self.labelwidth)
        vbox.addWidget(self.textwidth)
        vbox.addWidget(self.labelheight)
        vbox.addWidget(self.textheight)
        vbox.addWidget(self.labelcolor)
        vbox.addWidget(self.radiobtn1)
        vbox.addWidget(self.radiobtn2)
        vbox.addWidget(self.radiobtn3)
        vbox.addWidget(self.radiobtn4)
        vbox.addWidget(self.radiobtn5)
        vbox.addWidget(self.btnOK)

        # 이미지 편집창을 지정한 Layout을 기반으로 배치(vbox)
        self.setLayout(vbox)
    def editImage(self, mainwindow):
        # 수정할 width 입력란에 입력된 것을 변수화
        imgwidth_edited = self.textwidth.text()
        # 수정할 height 입력란에 입력된 것을 변수화
        imgheight_edited = self.textheight.text()

        #만약 width 라고 인풋이 그대로 있으면 원래 이미지 너비
        if imgwidth_edited == 'width':
            imgwidth_edited = mainwindow.imgwidth
        if imgheight_edited == 'height':
            imgheight_edited = mainwindow.imgheight

        # 입력한 수정할 너비와 높이가 숫자인지 아닌지 확인
        try:
            # 변수를 숫자화해서 전달받은 MainWindow 객체의 이미지 너비, 높이 변수에 저장
            mainwindow.imgwidth = int(imgwidth_edited)
            mainwindow.imgheight = int(imgheight_edited)

            # 전달받은 MainWindow 객체의 QLabel에 이미지 다시 로드
            mainwindow.loadImage()
             #현재 편집창 닫기
            self.close()
        except ValueError:
            QMessageBox.question(self, '너비 input에 문제', "너비나 높이의 인풋이 숫자가 아닙니다.", QMessageBox.Ok)

        # Pillow의 image 객체를 통해 원본 이미지 가져옴
        img = Image.open(mainwindow.originalpath)

        # RadioButton에서 다른 색으로 바꾸는 선택지를 택했을 때
        # RadioButton에서 우너본을 선택했을 때
        if self.radiochecked == "원본":
            img_edited = img
        # RadioButton에서 회색 계열을 선택했을 때
        if self.radiochecked == "회색 계열":
            img_edited = img.convert("L")

        # RadioButton에서 빨간색 계열을 선택했을 때
        if self.radiochecked == "빨간색 계열":
            red = (0.90, 0.36, 0.18, 0,
                    0.11, 0.72, 0.07, 0,
                    0.02, 0.12, 0.95, 0)
            img_edited = img.convert("RGB", red)

        # RadioButton에서 초록색 계열을 선택했을 때
        if self.radiochecked == "초록색 계열":
            green = (0.41, 0.36, 0.18, 0,
                    0.50, 0.72, 0.07, 0,
                    0.02, 0.12, 0.95, 0)
            img_edited = img.convert("RGB", green)

        # RadioButton에서 파란색 계열을 선택했을 때
        if self.radiochecked == "파란색 계열":
            blue = (0.31, 0.36, 0.18, 0,
                    0.40, 0.72, 0.07, 0,
                    0.60, 0.12, 0.95, 0)
            img_edited = img.convert("RGB", blue)

        # 수정된 이미지를 저장
        img_edited.save("image_edited.jpg", "JPEG")
        #QLabel에 업로드 시킬 이미지 파일의 위치로 imagePath 변환
        mainwindow.imagepath = os.getcwd() + "\image_edited.jpg"
        # 전달받은 MainWindow 객체의 Qlable에 이미지 다시 로드
        mainwindow.loadImage()

    # 선택된 Radiobutton 에 대한 텍스트 정보 얻어오기
    def btnstate(self):
        radiobtn = self.sender()
        self.radiochecked = radiobtn.text()


# 한 이미지 상 여러 얼굴을 관리하기 위한 얼굴 리스트 클래스
class FaceList:
   def __init__(self):
       # 얼굴 리스트 초기화
       self.face_list = []
       self.next_id = 0

   # 현재 저장되어 있는 얼굴 개수 확인
   def count_face(self):
       return len(self.face_list)

   # 알고리즘으로 찾은 얼굴들을 리스트에 추가하는 기능
   def append_face(self, x, y, w, h):
       self.face_list.append(Face(x, y, w, h, '', self.next_id))
       self.next_id += 1

   def remove_face(self, ind):
       cnt = 0
       for i in self.face_list:
           if i.id == ind:
               del self.face_list[cnt]
           cnt += 1

# 얼굴 정보를 담을 얼굴 클래스
class Face():
   def __init__(self, x, y, w, h, name, idx):
       self.x = x
       self.y = y
       self.w = w
       self.h = h
       self.name = name
       self.id = idx

# 얼굴 입력을 위한 새 창 틀 만들기
class AddFaceWindow(MainWindow):
    def __init__(self):
        super().__init__()

    def setWidgets(self, mainwindow):
        self.setGeometry(self.left, self.top, 200, 300)

        # 왼쪽의 이미지 라벨
        self.mlabel = SquareLabel(mainwindow.imagepath, mainwindow.imgwidth, mainwindow.imgheight, mainwindow.fList)

        # 오른쪽의 버튼들
        self.btnAddFace = QPushButton("얼굴 추가", self)
        self.btnAddFace.clicked.connect(lambda: self.mlabel.addFace())
        self.btnOK = QPushButton("확인", self)
        self.btnOK.clicked.connect(lambda: self.finishFace(mainwindow))

        # QVBoxLayout 객체 만들기
        vbox = QVBoxLayout()
        # 버튼을 QVBoxLayout 에 등록하기
        vbox.addWidget(self.btnAddFace)
        vbox.addWidget(self.btnOK)

        # vbox를 위젯으로 변환
        buttons_widget = QWidget()
        buttons_widget.setLayout(vbox)

        # QHBoxLayout 객체 만들기
        hbox = QHBoxLayout()
        # 이미지 라벨과 버튼 위젯 추가하기
        hbox.addWidget(self.mlabel)
        hbox.addWidget(buttons_widget)
        self.setLayout(hbox)

    def finishFace(self, mainwindow):
        mainwindow.label.setPixmap(self.mlabel.pixmap_resized)
        self.close()

class SquareLabel(QLabel):
    def __init__(self, imgpath, w, h, faceList):
        super().__init__()
        self.pixmap = QPixmap(imgpath)
        self.pixmap_resized = self.pixmap.scaled(w, h)
        self.setPixmap(self.pixmap_resized)

        # QPainter 설정
        painter = QPainter(self.pixmap_resized)
        # 펜 색과 굵기 설정
        painter.setPen(QPen(QColor('blue'), 3))
        for f in faceList.face_list:
            print(f.x, f.y, f.w, f.h)
            painter.drawRect(f.x, f.y, f.w, f.h)

        # 글자색을 주황색으로 하기 위한 코드
        painter.setPen(QPen(QColor('orange'), 3))

        # 글자 그리기
        for f in faceList.face_list:
            painter.drawText(f.x, f.y-5, f.name)
        painter.end()

        # 사진을 SquareLabel 에 그리기
        self.setPixmap(self.pixmap_resized)
        self.left_clicking = False
        self.faceList = faceList

    def mousePressEvent(self, event):
        # print("mousePressEvent", event.x(), event.y(), event.button())
        if event.button() == 1:
            self.startX = event.x()
            self.startY = event.y()
            self.left_clicking = True

    def mouseReleaseEvent(self, event):
        # print("mouseReleaseEvent", event.x(), event.y(), event.button())
        if event.button() == 1:
            self.finishX = event.x()
            self.finishY = event.y()
            self.left_clicking = False

    def mouseMoveEvent(self, event):
        # print("mouseMoveEvent", event.x(), event.y())
        if self.left_clicking:
            # 임시 pixmap 생성
            self.pixmap_temp = self.pixmap_resized.copy()
            # QPainter 설정
            painter = QPainter(self.pixmap_temp)
            # 펜 색과 굵기 설정
            painter.setPen(QPen(QColor('green'), 3))
            painter.drawRect(self.startX, self.startY, event.x() - self.startX, event.y() - self.startY)

            # 수정된 pixmap으로 재설정
            self.setPixmap(self.pixmap_temp)

    def addFace(self):
        x, y, w, h = self.startX, self.startY, self.finishX - self.startX, self.finishY - self.startY
        self.faceList.append_face(x, y, w, h)
        painter = QPainter(self.pixmap_resized)
        painter.setPen(QPen(QColor('blue'), 3))
        painter.drawRect(x, y, w, h)
        self.setPixmap(self.pixmap_resized)

class TagNameWindow(MainWindow):
    def __init__(self):
        super().__init__()

    def setWidgets(self, mainwindow):
        self.setGeometry(self.left, self.top, 200, 300)

        # 왼쪽의 이미지 라벨
        self.mlabel = TaggingLabel(mainwindow.imagepath, mainwindow.imgwidth, mainwindow.imgheight, mainwindow.fList)

        # 오른쪽의 버튼들
        self.btnSave = QPushButton("저장", self)
        self.btnSave.clicked.connect(lambda: self.mlabel.saveFile())

        self.btnOK = QPushButton("확인", self)
        self.btnOK.clicked.connect(lambda: self.finishTag(mainwindow))

        # QVBoxLayout 객체 만들기
        vbox = QVBoxLayout()
        # 버튼을 QVBoxLayout 에 등록하기
        vbox.addWidget(self.btnSave)
        vbox.addWidget(self.btnOK)

        # vbox 를 위젯으로 변환
        buttons_widget = QWidget()
        buttons_widget.setLayout(vbox)

        # QHBoxLayout 객체 만들기
        hbox = QHBoxLayout()
        # 이미지 라벨과 버튼 위젯 추가하기
        hbox.addWidget(self.mlabel)
        hbox.addWidget(buttons_widget)
        self.setLayout(hbox)

    def finishTag(self, mainwindow):
        mainwindow.label.setPixmap(self.mlabel.pixmap_temp)
        self.close()

class TaggingLabel(SquareLabel):
    def __init__(self, imgpath, w, h, faceList):
        super().__init__(imgpath, w, h, faceList)

    def mousePressEvent(self, event):
        for f in self.faceList.face_list:
            if f.x <= event.x() <= f.x + f.w and f.y <= event.y()<= f.y + f.h:
                print("얼굴 아이디: ", f.id, f.name)
                text, okPressed = QInputDialog.getText(self, "입력창", "이름:", QLineEdit.Normal)

                if okPressed and text != '':
                    f.name = text
                break
        self.drawNames()
        pass

    def mouseReleaseEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def drawNames(self):
        self.pixmap_temp = self.pixmap_resized.copy()
        painter = QPainter(self.pixmap_temp)
        painter.setPen(QPen(QColor('orange'), 3))
        for f in self.faceList.face_list:
            painter.drawText(f.x, f.y-5, f.name)
        painter.end()
        self.setPixmap(self.pixmap_temp)

    def saveFile(self):
        text, okPressed = QInputDialog.getText(self, "파일이름입력창", "파일명:", QLineEdit.Normal)
        if okPressed:
            self.pixmap_temp.save(text + '.jpg', 'JPG')

if __name__ == '__main__':
   app = QApplication(sys.argv)
   # MainWindow 객체 불러오기
   win = MainWindow()
   win.setWidgets()
   # 창 보여주기
   win.show()
   app.exec_()
