#对象管理

*  1.1介绍

这篇文章将要讨论vlc的对象以及一般的面向对象的做法，参与发展和扩大libvlc

*  1.2对象创建

在vlc 中任何都是对象。每个主题都有一个根目录，或者多个子目录。下述功能是用于创建对象，以及联系这些目录。这些或许不够完全，作为参考看文件：include/vlc_objects.h§.    
lc_object_create() - 创建对象以及设置它的引用计数

vlc_object_destroy() -当引用计数为0时分配对象

vlc_object_attach() - bidirectionally link an object with its parent双向对象链接

vlc_object_detach() - remove all links between an object and its parent移除所有有的关系

*  1.3继承

对象可以有多个级别的继承。每个对象被表示类型vlc_object_t。每一个对象从这种类型的继承和可以转换为。在C语言中嵌入一个宏在每个继承的对象结构，常见的结构的元素（VLC_COMMON_MEMBERS）实现继承。例如，一个libvlc类型libvlc_int_t实例继承从vlc_object_t的嵌入VLC_COMMON_MEMBERS内部libvlc_int_t结构，如在下面的实施例1中看到。
struct libvlc_int_t {    VLC_COMMON_MEMBERS    /* Everything Else */}

*  1.4引用计数
 
为了简化垃圾收集，每个对象都有一个引用计数。当一个对象被创建（的malloc（）'D）它的引用计数设置为0。每当对象被调用时，调用者者必须增加其引用计数1。当调用者使用对象，它必须减少对象的引用计数1。幸运的是，这其中大部分是处理内部对象管理和清除功能。为了破坏（free（））对象的引用计数必须是0。下面的函数用于操作对象的引用计数。需要注意的是，这个列表可能是不完整的。仅供参考，请参阅文件/ vlc_objects.h。

vlc_object_release（）+1，增加一个对象的引用计数。此功能只能用于对象管理功能！粗心的使用会导致内存泄漏

vlc_object_release（）-1 一个对象的引用计数减少1。此功能只能用于对象管理功能！粗心的使用可能会导致坏早期的对象，而对象可能仍然在使用！