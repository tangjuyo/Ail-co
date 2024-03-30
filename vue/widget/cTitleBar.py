#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月15日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CTitleBar
@description: 自定义标题栏
"""

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QWindowStateChangeEvent, QFont, QMouseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QLabel, QPushButton, QApplication


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class CTitleBar(QWidget):

    Radius = 24

    def __init__(self, *args, title='', **kwargs):
        super(CTitleBar, self).__init__(*args, **kwargs)
        self.setupUi()
        # 支持设置背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos = None
        # 找到父控件(或者自身)
        self._root = self.window()  # self.parent() or self

        self.labelTitle.setText(title)
        # 是否需要隐藏最小化或者最大化按钮
        self.showMinimizeButton(self.isMinimizeable())
        self.showNormalButton(False)
        self.showMaximizeButton(self.isMaximizeable())

        # 绑定信号
        self._root.windowTitleChanged.connect(self.setWindowTitle)
        self.buttonMinimum.clicked.connect(self.showMinimized)
        self.buttonMaximum.clicked.connect(self.showMaximized)
        self.buttonNormal.clicked.connect(self.showNormal)
        self.buttonClose.clicked.connect(self._root.close)
        # 对父控件(或者自身)安装事件过滤器
        self._root.installEventFilter(self)

    def showMinimized(self):
        self._root.showMinimized()
        # 强制取消hover状态
        QApplication.sendEvent(self.buttonMinimum, QMouseEvent(
            QMouseEvent.Leave, QPointF(), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def showNormal(self):
        self._root.showNormal()
        # 强制取消hover状态
        QApplication.sendEvent(self.buttonMaximum, QMouseEvent(
            QMouseEvent.Leave, QPointF(), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def showMaximized(self):
        self._root.showMaximized()
        # 强制取消hover状态
        QApplication.sendEvent(self.buttonNormal, QMouseEvent(
            QMouseEvent.Leave, QPointF(), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def isMinimizeable(self):
        return self.testWindowFlags(Qt.WindowMinimizeButtonHint)

    def isMaximizeable(self):
        return self.testWindowFlags(Qt.WindowMaximizeButtonHint)

    def isResizable(self):
        return self._root.minimumSize() != self._root.maximumSize()

    def showMinimizeButton(self, show=True):
        self.buttonMinimum.setVisible(show)
        self.widgetMinimum.setVisible(show)

    def showMaximizeButton(self, show=True):
        self.buttonMaximum.setVisible(show)
        self.widgetMaximum.setVisible(show)

    def showNormalButton(self, show=True):
        self.buttonNormal.setVisible(show)
        self.widgetNormal.setVisible(show)

    def showEvent(self, event):
        super(CTitleBar, self).showEvent(event)
        if not self.isResizable():
            self.showMaximizeButton(False)
            self.showNormalButton(False)
        else:
            self.showMaximizeButton(
                self.isMaximizeable() and not self._root.isMaximized())
            self.showNormalButton(self.isMaximizeable()
                                  and self._root.isMaximized())

    def eventFilter(self, target, event):
        if isinstance(event, QWindowStateChangeEvent):
            if self._root.isVisible() and not self._root.isMinimized() and \
                    self.testWindowFlags(Qt.WindowMinMaxButtonsHint):
                # 如果当前是最大化则隐藏最大化按钮
                maximized = self._root.isMaximized()
                self.showMaximizeButton(not maximized)
                self.showNormalButton(maximized)
                # 修复最大化边距空白问题
                if maximized:
                    self._oldMargins = self._root.layout().getContentsMargins()
                    self._root.layout().setContentsMargins(0, 0, 0, 0)
                else:
                    if hasattr(self, '_oldMargins'):
                        self._root.layout().setContentsMargins(*self._oldMargins)
        return super(CTitleBar, self).eventFilter(target, event)

    def mouseDoubleClickEvent(self, event):

        if not self.isMaximizeable() or not self.isResizable():
            return
        if self._root.isMaximized():
            self._root.showNormal()
        else:
            self._root.showMaximized()

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()

    def mouseReleaseEvent(self, event):

        self.mPos = None

    def mouseMoveEvent(self, event):
        if self._root.isMaximized():
            # 最大化时不可移动
            return
        if event.buttons() == Qt.LeftButton and self.mPos:
            pos = event.pos() - self.mPos
            self._root.move(self._root.pos() + pos)

    def testWindowFlags(self, windowFlags):
        return bool(self._root.windowFlags() & windowFlags)

    def setWindowTitle(self, title):
        self.labelTitle.setText(title)

    def setupUi(self):
        self.setMinimumSize(0, self.Radius)
        self.setMaximumSize(0xFFFFFF, self.Radius)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        for name in ('widgetMinimum', 'widgetMaximum', 'widgetNormal', 'widgetClose'):
            widget = QWidget(self)
            widget.setMinimumSize(self.Radius, self.Radius)
            widget.setMaximumSize(self.Radius, self.Radius)
            widget.setObjectName('CTitleBar_%s' % name)
            setattr(self, name, widget)
            layout.addWidget(widget)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 标题
        self.labelTitle = QLabel(self, alignment=Qt.AlignCenter)
        self.labelTitle.setObjectName('CTitleBar_labelTitle')
        layout.addWidget(self.labelTitle)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 最小化,最大化,还原,关闭按钮
        for name, text in (('buttonMinimum', '-'), ('buttonMaximum', '□'),
                           ('buttonNormal', '□'), ('buttonClose', 'X')):
            button = QPushButton(text, self, font=QFont('Webdings'))
            button.setMinimumSize(self.Radius, self.Radius)
            button.setMaximumSize(self.Radius, self.Radius)
            button.setObjectName('CTitleBar_%s' % name)
            setattr(self, name, button)
            layout.addWidget(button)
            
    