#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:Du Fei
import os
#生成学生类
class Student:
    def __init__(self,id,name,age,sex,height):
        self.id =id
        self.name=name
        self.age=age
        self.sex =sex
        self.height=height

    def printMe(self):
        print("学号：%d,姓名：%s,年龄：%d,性别：%s,身高：%f" % (self.id, self.name, self.age, self.sex, self.height))


#管理类
class StudentsManage:
    def __init__(self):
        self.allStudentsList =[]

    #显示所有学生的信息
    def allStudentsShow(self):
        for one in self.allStudentsList:
            one.printMe()
    #新增学生
    def addNewStudent(self,newStuList):
        # check学号是否重复复
        for one in self.allStudentsList:
            if one.id == newStuList.id:
                return -1 #学号重复
        self.allStudentsList.append(newStuList)
        return 1

    # 修改学生年龄
    def updateStudentsAge(self,id, newAge):
        for one in self.allStudentsList:
            if one.id == id:
                one.age = newAge
                break
        else:
            return -1  # 找不到此学号
        return 1

    #删除学生
    def deleteStudent(self,id):
        index =0
        for one in self.allStudentsList:
            if one.id ==id:
                del self.allStudentsList[index]
                break
            index +=1
        else:
            return -1#找不到要删除的学号
        return 1

    #按照姓名查找
    def searchStudents(self,name):
        flag =0
        for one in self.allStudentsList:
            if one.name==name:
                one.printMe()
                flag=1
        if flag==0:
            return -1#查无此人
        return 1

    # 按序号排序
    def orderById(self,flag):  # flag:1升序，2降序
        if flag == 1:  # 升序
            self.allStudentsList.sort(reverse=False, key=lambda x: x.id)
        else:
            self.allStudentsList.sort(reverse=True, key=lambda x: x.id)

    # 从文件中读取数据
    def readFromFile(self,fileName):
        if not os.path.exists(fileName):  # 如果文件不存在，则新增一个空文件
            f = open(fileName, "w")
            f.close()
        with open(fileName, "r", encoding="utf-8") as f:
            for onStr in f:
                oneList = onStr.strip("\n").split(",")
                oneList[0] = int(oneList[0])  # 学号
                oneList[1] = oneList[1]  # 姓名
                oneList[2] = int(oneList[2])  # 年龄
                oneList[3] = oneList[3]  # 性别
                oneList[4] = float(oneList[4])  # 身高
                stu = Student(int(oneList[0]),oneList[1],int(oneList[2]),oneList[3],float(oneList[4]))
                self.allStudentsList.append(stu)

    # 将数据写入文件
    def writeToFile(self,fileName):
        f = open(fileName, "w")
        f.close()

        with open(fileName, "a", encoding="utf-8") as f:
            for one in self.allStudentsList:
                oneStr = str(one.id) + "," + one.name + "," + str(one.age) + "," + one.sex + "," + str(one.height) + "\n"
                f.write(oneStr)

# 功能菜单
def menuShow():
    print("**********************************")
    print("*1.查看所有学生信息****************")
    print("*2.新增学生************************")
    print("*3.修改学生************************")
    print("*4.删除学生************************")
    print("*5.按姓名查找**********************")
    print("*6.按学号排序**********************")
    print("*7.保存***************************")
    print("*8.退出***************************")
    print("**********************************")


if __name__ == "__main__":
    stManage=StudentsManage()
    #从文件中读取数据
    stManage.readFromFile("student.txt")
    # print(allStudentsList)
    while True:
        # 显示主菜单
        menuShow()
        select =int(input("请选择功能选项："))
        if select == 1:
            stManage.allStudentsShow()
        elif select == 2:
            while True:
                try:
                    id = int(input("请输入学号："))
                    name = input("请输入姓名：")
                    age = int(input("请输入年龄："))
                    sex = input("请输入性别：")
                    height = float(input("请输入身高："))
                    stu = Student(id,name,age,sex,height)
                    if stManage.addNewStudent(stu) ==-1:
                        print("学号已存在,请重新输入")
                    else:
                        flag=input("新增用户成功,是否继续新增(y/n)?:")
                        if flag.lower() !="y":
                            break
                except:
                    print("输入有误请重新输入")

        elif select == 3:
            while True:
                id=int(input("请输入序号："))
                newAge=int(input("请输入新的年龄："))
                if stManage.updateStudentsAge(id,newAge) ==-1:
                    print("找不到此学号的学生，请重新输入")
                else:
                    flag = input("修改成功,是否继续修改(y/n)?:")
                    if flag.lower() != "y":
                        break

        elif select == 4:
            while True:
                id =int(input("请输入删除的学号："))
                if stManage.deleteStudent(id) == -1:
                    print("找不到此学号的学生，请重新输入")
                else:
                    flag = input("删除成功,是否继续删除(y/n)?:")
                    if flag.lower() != "y":
                        break
        elif select == 5:
            while True:
                name=input("请输入查找的姓名：")
                if stManage.searchStudents(name) ==-1:
                    print("查无此人")

                flag = input("是否继续查找(y/n)?:")
                if flag.lower() != "y":
                    break

        elif select == 6:
            flag=int(input("请选择排序方式（1：升序，2：降序）"))
            stManage.orderById(flag)
            stManage.allStudentsShow()
        elif select == 7:
            stManage.writeToFile("student.txt")
        else:
            exit()