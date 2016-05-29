# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import strftime
import time,datetime
import sys
import string
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
class InputDlg(QDialog):
    def __init__(self,parent=None):
        super(InputDlg,self).__init__(parent)
        self.setMinimumSize(1000,660)
        self.setMaximumSize(1500,660)
        label1=QLabel(self.tr("省份"))
        label2=QLabel(self.tr("城市"))
        label3=QLabel(self.tr("开始时间"))
        label4=QLabel(self.tr("结束时间"))

        self.provinceLabel=QLabel(self.tr("江苏"))
        self.provinceLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.cityLabel=QLabel(self.tr("南京"))
        self.cityLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        
        provinceButton=QPushButton(self.tr("修改"))
        cityButton=QPushButton(self.tr("修改"))
        
        self.connect(provinceButton,SIGNAL("clicked()"),self.slotprovince)
        self.connect(cityButton,SIGNAL("clicked()"),self.slotcity)
        ####################################################################
        #global startyear,startmonth,startday,endyear,endmonth,endday
        self.time_startLabel=QDateEdit()
        self.time_startLabel2=QTimeEdit()
        self.time_startLabel.setCurrentSection(QDateTimeEdit.DaySection)
        self.time_startLabel.setDateTime(QDateTime(QDate(int(strftime("%Y")),int(strftime("%m")),int(strftime("%d"))),QTime(0,0,0)))
        self.time_startLabel.setCalendarPopup(True)
        self.time_startLabel2.setTime(QTime(0,0,0))
        self.time_endLabel=QDateEdit()
        self.time_endLabel2=QTimeEdit()
        self.time_endLabel.setDateTime(QDateTime(QDate(int(strftime("%Y")),int(strftime("%m")),int(strftime("%d"))),QTime(0,0,0)))
        self.time_endLabel2.setTime(QTime(23,59,59))
        self.time_endLabel.setCurrentSection(QDateTimeEdit.DaySection)
        self.time_endLabel.setCalendarPopup(True)
        #######################################################################
        global startcaptureFlag,endcaptureFlag
        startcaptureFlag=False
        endcaptureFlag=False
        startcaptureButton=QPushButton(self.tr("\n开始采集\n"))
        endcaptureButton=QPushButton(self.tr("\n停止采集\n"))
        anlysisButton=QPushButton(self.tr("\n\n舆情聚类分析\n\n"))
        #anlysisButton.setGeometry(370,20,101,25)
        self.connect(startcaptureButton,SIGNAL("clicked()"),self.slotstartcaptureButton)
        self.connect(endcaptureButton,SIGNAL("clicked()"),self.slotendcaptureButton)
        self.connect(anlysisButton,SIGNAL("clicked()"),self.slotanlysisButton)
        self.text_showcapture = QTableWidget(0,1)
        self.text_showcapture.setColumnWidth(0,580)
        self.text_showcapture.setHorizontalHeaderLabels([u'微博采集完成列表'])
        try:
            showcapture=open("D:\\09Limited_buffer\\earlywarningbyci\\cola\\data\\worker\\jobs\\sina_weibo_crawler\\job.log","r")
            lines=showcapture.readlines()
            j=0
            for i in lines:
                list=i.split("-")
                self.text_showcapture.insertRow(j)
            #newItem=QTableWidgetItem(list[5])
                newItem=QTableWidgetItem(i)
                self.text_showcapture.setItem(j,0,newItem)
                j=j+1
        except:
            next
        #######################################################################
        self.text_beforefilter = QTableWidget(0,3)
        self.text_beforefilter.setColumnWidth(0,130)
        self.text_beforefilter.setColumnWidth(1,50)
        self.text_beforefilter.setColumnWidth(2,350)
        self.text_beforefilter.setHorizontalHeaderLabels([u'创建时间',u'关注度',u'内容'])
        self.text_filtered = QTableWidget(0,3)
        self.text_filtered.setColumnWidth(0,130)
        self.text_filtered.setColumnWidth(1,50)
        self.text_filtered.setColumnWidth(2,350)
        self.text_filtered.setHorizontalHeaderLabels([u'创建时间',u'关注度',u'内容'])
        showbeforefilterButton=QPushButton(self.tr("显示已采集文本"))
        startfilterButton=QPushButton(self.tr("显示过滤后文本"))
        self.connect(showbeforefilterButton,SIGNAL("clicked()"),self.slotshowbeforefilterButton)
        self.connect(startfilterButton,SIGNAL("clicked()"),self.slotstartfilterButton)
        #######################################################################
        layout=QGridLayout()
        layout.addWidget(label1,0,0)
        layout.addWidget(self.provinceLabel,0,1)
        layout.addWidget(provinceButton,0,2)
        layout.addWidget(label2,1,0)
        layout.addWidget(self.cityLabel,1,1)
        layout.addWidget(cityButton,1,2)
        layout.addWidget(label3,2,0,1,1)
        layout.addWidget(self.time_startLabel,2,1,1,1)
        layout.addWidget(self.time_startLabel2,2,2,1,1)
        layout.addWidget(label4,3,0,1,1)
        layout.addWidget(self.time_endLabel,3,1,1,1)
        layout.addWidget(self.time_endLabel2,3,2,1,1)
        layout.addWidget(startcaptureButton,0,3,2,1)
        layout.addWidget(endcaptureButton,2,3,2,1)
        layout.addWidget(anlysisButton,0,4,4,1)
        layout.addWidget(showbeforefilterButton,7,14,1,1)
        layout.addWidget(startfilterButton,14,14,1,1)
        layout.addWidget(self.text_showcapture,4,0,10,5)
        layout.addWidget(self.text_beforefilter,0,6,7,9)
        layout.addWidget(self.text_filtered,8,6,6,9)

        
        self.setLayout(layout)
        self.setWindowTitle(self.tr("网络舆情预警系统"))

    def slotprovince(self):
        province,ok=QInputDialog.getText(self,self.tr("省份修改"),
                                     self.tr("请输入要采集的省份:"),
                                     QLineEdit.Normal,self.provinceLabel.text())
        #print province.toUtf8()
        if ok and (not province.isEmpty()):
            self.provinceLabel.setText(province)
        
    def slotcity(self):
        city,ok=QInputDialog.getText(self,self.tr("城市修改"),
                                     self.tr("请输入要采集的城市:"),
                                     QLineEdit.Normal,self.cityLabel.text())
        if ok and (not city.isEmpty()):
            self.cityLabel.setText(city)

    def slotstartcaptureButton(self):
        startdate=self.time_startLabel.date()
        enddate=self.time_endLabel.date()
        startyear=startdate.year()
        startmonth=startdate.month()
        startday=startdate.day()
        endyear=enddate.year()
        endmonth=enddate.month()
        endday=enddate.day()
        starttime=self.time_startLabel2.time()
        endtime=self.time_endLabel2.time()
        starthour=starttime.hour()
        startmin=starttime.minute()
        startsec=starttime.second()
        endhour=endtime.hour()
        endmin=endtime.minute()
        endsec=endtime.second()
        start=time.mktime(datetime.datetime(int(startyear),int(startmonth),int(startday),int(starthour),int(startmin),int(startsec)).timetuple())
        end=time.mktime(datetime.datetime(int(endyear),int(endmonth),int(endday),int(endhour),int(endmin),int(endsec)).timetuple())
        if start>end:
            QMessageBox.warning(self,u"错误提示",u"开始时间在结束时间之后！")
            return
        province=self.provinceLabel.text()
        provincestr=province.toUtf8().data()
        city=self.cityLabel.text()
        citystr=city.toUtf8().data()
        print provincestr,citystr
        #if provincestr == eval("u'\u6c5f\u82cf'"):
        #    print "haha"
        localvalue=open("..\\cola\\contrib\\weibo\\localvalue.txt","wt")
        if provincestr==citystr:
            print >>localvalue,provincestr
        else:
            print >>localvalue,provincestr,citystr
        localvalue.close()
        timevalue=open("..\\cola\\contrib\\weibo\\timevalue.txt","wt")
        print >>timevalue,start,end
        timevalue.close()
        global startcaptureFlag
        startcaptureFlag=True
        if startcaptureFlag:
            sys.path.insert(0,"D:\\09Limited_buffer\\earlywarningbyci\\cola\\contrib\\weibo")
            import __init__
            #print "import init?"
            if __name__ == "__main__":
                print "work!"
                from cola.worker.loader import load_job
                load_job(__init__.os.path.dirname(__init__.os.path.abspath(__init__.__file__)))
            
    def slotendcaptureButton(self):
        global endcaptureFlag,startcaptureFlag
        endcaptureFlag=True
        startcaptureFlag=False
        if endcaptureFlag:
            sys.path.insert(0,"D:\\09Limited_buffer\\earlywarningbyci\\cola\\contrib\\weibo")
            import stop
            print "import stop?"
            if __name__ == '__main__':
                ip, port = stop.get_ip(), getattr(stop.user_config.job, 'port')
                stop.logger.info('Trying to stop single running worker')
                try:
                     stop.client_call('%s:%s' % (ip, port), 'stop')
                except stop.socket.error:
                    stop.stop = raw_input("Force to stop? (y or n) ").strip()
                    if stop.stop == 'y' or stop.stop == 'yes':
                        stop.job_path = stop.os.path.split(stop.os.path.abspath(stop.__file__))[0]
                        stop.recover(stop.job_path)
                    else:
                        print 'ignore'
                stop.logger.info('Successfully stopped single running worker')
    def slotanlysisButton(self):
        sys.path.insert(0,"D:\\09Limited_buffer\\earlywarningbyci\\wordanalys\\")
        if __name__ == '__main__':
            import rpy2.robjects as robjects
            r = robjects.r
            r.source('D:\\09Limited_buffer\\earlywarningbyci\\wordanalys\\lucky.r')
    def slotshowbeforefilterButton(self):
        sys.path.insert(0,"D:\\09Limited_buffer\\earlywarningbyci\\classification")
        if __name__ == '__main__':
            import connectdb
        filterout=open("predicted.txt","r")
        lines=filterout.readlines()
        j=0
        for i in lines:
            list=i.split()
            label=list[0]
            mic_id=list[2]
            mic_focus=list[3]
            mic_created=list[4]+" "+list[5]
            list_length = len(list)
            mic_content=list[6]
            for k in range(7,list_length):
                mic_content=mic_content+list[k]
            mic_content=mic_content.decode("utf-8")
            if j>0:
                self.text_beforefilter.insertRow(j-1)
                newItem=QTableWidgetItem(mic_created)
                self.text_beforefilter.setItem(j-1,0,newItem)
                newItem=QTableWidgetItem(mic_focus)
                self.text_beforefilter.setItem(j-1,1,newItem)
                newItem=QTableWidgetItem(mic_content)
                self.text_beforefilter.setItem(j-1,2,newItem)
            j=j+1
    def slotstartfilterButton(self):
        filterout=open("predicted.txt","r")
        lines=filterout.readlines()
        j=0
        temp=0
        for i in lines:
            list=i.split()
            label=list[0]
            #print type(label)
            mic_id=list[2]
            mic_focus=list[3]
            mic_created=list[4]+" "+list[5]
            list_length = len(list)
            mic_content=list[6]
            for k in range(7,list_length):
                mic_content=mic_content+list[k]
            mic_content=mic_content.decode("utf-8")
            if (j>0) and (label=='-1.0'):
                self.text_filtered.insertRow(temp)
                newItem=QTableWidgetItem(mic_created)
                self.text_filtered.setItem(temp,0,newItem)
                newItem=QTableWidgetItem(mic_focus)
                self.text_filtered.setItem(temp,1,newItem)
                newItem=QTableWidgetItem(mic_content)
                self.text_filtered.setItem(temp,2,newItem)
                temp=temp+1
            j=j+1
if __name__ == "__main__":
    app=QApplication(sys.argv)
    widget=QWidget()
    widget.resize(1600,1600)
    form=InputDlg()
    form.show()
    app.exec_()
