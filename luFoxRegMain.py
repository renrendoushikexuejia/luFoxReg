import sys
import winreg
import os
from eth_account import Account

from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QFileDialog,QMessageBox
from Ui_luFoxReg import Ui_Form #导入你写的界面类


###定义函数
def desktop_path():#通过注册表获得桌面路径
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key,"Desktop")[0]

###定义变量
luCount = 1    #生成的私钥数量
luProjectName = '小狐狸'    #默认项目名称
luCountList = ['5','1','2','3','4','10','15','20','25','30','40','50','70','100']   #定义一个列表，初始化ComboBox cb1
luDir = desktop_path()


class MyMainWindow(QMainWindow,Ui_Form): 

    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)

        #初始化ComboBox cb1
        self.cb1.addItems(luCountList)

        #绑定信号槽
        self.pb1.clicked.connect(self.fPb1Clicked)
        self.pb2.clicked.connect(self.fPb2Clicked)
    
    #选择文件保存的位置
    def fPb1Clicked(self):
        #引入全局变量
        global luProjectName, luDir
        luDir = QFileDialog.getExistingDirectory(self, '选择保存位置', desktop_path(), QFileDialog.ShowDirsOnly)

        #判断项目名称是否合适
        curProjectName = self.le1.text()

        if curProjectName == '':    #如果项目名称为空，则设置luProjectName为'小狐狸'
            luProjectName = '小狐狸'

        elif curProjectName.isspace():  #如果项目名称中有空格，则提示并清空lineText1
            self.le1.clear()
            QMessageBox.information(self, '提示', '项目名称可以不输入，但不能为空白字符')
            luProjectName = '小狐狸'
            return

        elif curProjectName.find('+') != -1 or curProjectName.find(' ') != -1 : #如果项目名称中有'+'或' '，则提示并清空lineText1
            self.le1.clear()
            QMessageBox.information(self, '提示', '项目名称可以不输入，但不能有+号和空格')
            luProjectName = '小狐狸'
            return
            
        else:
            luProjectName = curProjectName
            
        #生成包含文件名的路径，并判断路径是否可用
        luDir = luDir + '/' + luProjectName + '.txt'

        if os.path.exists(luDir):
            self.le2.setText('请选择文件保存位置')
            QMessageBox.information(self, '提示', '存在同名项目。请更改项目名或重新选择文件位置')
            luDir = desktop_path()
            return

        self.le2.setText(luDir)

        

    def fPb2Clicked(self):
        #引入全局变量
        global luProjectName, luDir
        luCount = int(self.cb1.currentText())
        
        if self.le2.text() == '请选择文件保存位置' or luDir == desktop_path():  #luDir == desktop_path()是否有必要？
            QMessageBox.information(self, '提示','请选择文件保存位置')
            return
        
        #判断文件是否成功打开
        #open()的返回值是什么
        #这里不判断文件是否成功打开
        f = open(luDir, mode = 'x',encoding='utf-8')    #'x'写模式，新建一个文件，如果该文件已存在则会报错。

        #写入内容
        for i in range(0, luCount):
            
            #生成eth账户
            Account.enable_unaudited_hdwallet_features()    #不知道这一句是什么意思，少了这一句会报错
            acct, mnemonic = Account.create_with_mnemonic() #返回本地账户和助记词
            ethPri = acct._key_obj                          #私钥
            ethPub = ethPri.public_key                      #公钥
            ethAddr = acct.address                          #地址
            
            
            #都转换为字符串，否则不能拼接mStr
            ethPri = str(ethPri)
            ethPub = str(ethPub)
            ethAddr = str(ethAddr)
            #写入到文件中，格式为    项目名称+序号+私钥+助记词+公钥+地址
            x = str( i+1)   #x是序号
            mStr= luProjectName+'+'+x+'+'+ethPri+'+'+mnemonic+'+'+ethPub+'+'+ethAddr+'\n'
            f.write(mStr)


        f.close()
        self.le2.setText('请选择文件保存位置')

        #生成文件之后，运行文件
        #os.system(luDir)   os.system() 运行时会出现cmd的黑框
        QMessageBox.information(self, '提示', '账户已生成，请到对应文件夹下查看')

       
        return


#以下主程序创建不适应高分屏，在高分屏电脑上 文本显示不完整
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
sys.exit(app.exec_()) 

